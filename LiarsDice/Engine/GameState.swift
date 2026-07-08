import Foundation

/// The complete, self-contained state of a Liar's Dice game.
///
/// This type owns all the rules. State only changes through the `mutating`
/// transition methods, each of which returns the list of ``GameEvent``s it
/// produced so the view layer can animate and narrate. It is pure value-type
/// logic with no UI and no global state, which makes it trivial to unit test
/// and (later) to serialize for save games.
public struct GameState: Equatable, Sendable {
    public private(set) var players: [Player]
    public private(set) var rules: GameRules
    public private(set) var phase: GamePhase
    public private(set) var currentBid: Bid?
    public private(set) var currentBidderID: UUID?
    public private(set) var round: Int

    /// Full initializer, used by tests and (eventually) save-game loading.
    /// Normal play should start a game with ``newGame(playerName:rules:using:)``.
    public init(
        players: [Player],
        rules: GameRules,
        phase: GamePhase,
        currentBid: Bid?,
        currentBidderID: UUID?,
        round: Int
    ) {
        self.players = players
        self.rules = rules
        self.phase = phase
        self.currentBid = currentBid
        self.currentBidderID = currentBidderID
        self.round = round
    }

    // MARK: - Setup

    /// Default pirate crew names, handed out in order.
    public static let defaultBotNames = [
        "One-Eyed Jack", "Salty Sue", "Blackbeard", "Peg-Leg Pete",
        "Mad Morgan", "Calico Kate", "Cutthroat Cal", "Barnacle Bill"
    ]

    /// Start a fresh game: one human plus `rules.botCount` bots, everyone with
    /// `rules.startingDice` dice, a random starting player, and the first round
    /// already rolled and waiting on the opening bid.
    public static func newGame<R: RandomNumberGenerator>(
        playerName: String,
        rules: GameRules = GameRules(),
        using rng: inout R
    ) -> GameState {
        var players: [Player] = [
            Player(name: playerName.isEmpty ? "You" : playerName,
                   isBot: false,
                   diceCount: rules.startingDice)
        ]
        for i in 0..<rules.botCount {
            let name = i < defaultBotNames.count ? defaultBotNames[i] : "Bot \(i + 1)"
            players.append(Player(name: name, isBot: true, diceCount: rules.startingDice))
        }

        let starterIndex = Int.random(in: 0..<players.count, using: &rng)
        let starterID = players[starterIndex].id

        var state = GameState(
            players: players,
            rules: rules,
            phase: .opening(starter: starterID),
            currentBid: nil,
            currentBidderID: nil,
            round: 0
        )
        _ = state.beginRound(starter: starterID, using: &rng)
        return state
    }

    // MARK: - Derived information

    public var humanPlayer: Player? { players.first { $0.isHuman } }
    public var opponents: [Player] { players.filter { $0.isBot } }
    public var activePlayers: [Player] { players.filter { !$0.isEliminated } }

    /// Total dice currently in cups across the whole table.
    public var diceInPlay: Int { players.reduce(0) { $0 + $1.cup.count } }

    public func player(_ id: UUID) -> Player? { players.first { $0.id == id } }

    /// Whoever must act right now (the opener, or the current bidder), if any.
    public var currentPlayerID: UUID? {
        switch phase {
        case .opening(let starter): return starter
        case .bidding(let current): return current
        case .reveal, .gameOver:    return nil
        }
    }

    public var currentPlayer: Player? {
        currentPlayerID.flatMap(player)
    }

    public var isHumanTurn: Bool {
        currentPlayer?.isHuman ?? false
    }

    public var currentReveal: Reveal? {
        if case .reveal(let r) = phase { return r }
        return nil
    }

    public var isGameOver: Bool {
        if case .gameOver = phase { return true }
        return false
    }

    /// Count of dice across the table showing `face` (counting wild ones when
    /// that rule is enabled and `face` isn't 1 itself).
    public func tableCount(of face: Int) -> Int {
        players.reduce(0) { acc, p in
            var matches = p.cup.filter { $0 == face }.count
            if rules.onesAreWild && face != 1 {
                matches += p.cup.filter { $0 == 1 }.count
            }
            return acc + matches
        }
    }

    /// Is there any legal raise above the current bid? (You can't bid past
    /// "every die in play is a 6".)
    public func legalRaiseExists() -> Bool {
        guard let bid = currentBid else { return true }
        return bid.quantity < diceInPlay || bid.face < 6
    }

    /// The smallest bid that is strictly higher than the current bid, if one
    /// exists. Handy as the default starting point for the human's raise UI.
    public func minimumRaise() -> Bid? {
        guard let bid = currentBid else { return Bid(quantity: 1, face: 1) }
        if bid.face < 6 {
            return Bid(quantity: bid.quantity, face: bid.face + 1)
        }
        if bid.quantity < diceInPlay {
            return Bid(quantity: bid.quantity + 1, face: 1)
        }
        return nil
    }

    // MARK: - Transitions

    /// Apply a turn action (from a human tap or a bot decision) during bidding
    /// or opening. Returns the events produced.
    public mutating func apply(_ action: TurnAction) -> [GameEvent] {
        switch action {
        case .openingBid(let bid): return submitOpeningBid(bid)
        case .raise(let bid):      return raise(bid)
        case .challenge:           return challenge()
        }
    }

    /// The starting player commits the round's first bid.
    public mutating func submitOpeningBid(_ bid: Bid) -> [GameEvent] {
        guard case .opening(let starter) = phase else { return [] }
        currentBid = bid
        currentBidderID = starter
        phase = .bidding(current: nextActivePlayerID(after: starter))
        return [.openingBid(playerID: starter, bid: bid)]
    }

    /// The current player raises the bid. The caller is responsible for only
    /// passing a strictly-higher bid; an illegal bid is ignored.
    public mutating func raise(_ bid: Bid) -> [GameEvent] {
        guard case .bidding(let current) = phase, let old = currentBid else { return [] }
        guard bid.isHigher(than: old) else { return [] }
        currentBid = bid
        currentBidderID = current
        phase = .bidding(current: nextActivePlayerID(after: current))
        return [.raised(playerID: current, bid: bid)]
    }

    /// The current player calls the previous bidder a liar. Dice are tallied
    /// immediately and the loser is determined; the state moves to `.reveal`.
    public mutating func challenge() -> [GameEvent] {
        guard case .bidding(let challenger) = phase,
              let bid = currentBid,
              let bidder = currentBidderID else { return [] }

        let total = tableCount(of: bid.face)
        let bidWasGood = total >= bid.quantity
        let loser = bidWasGood ? challenger : bidder

        let reveal = Reveal(
            bid: bid,
            challengerID: challenger,
            bidderID: bidder,
            total: total,
            bidWasGood: bidWasGood,
            loserID: loser
        )
        phase = .reveal(reveal)
        return [
            .challenged(challengerID: challenger, bidderID: bidder, bid: bid),
            .revealed(reveal)
        ]
    }

    /// After the reveal has been shown, settle up: the loser drops a die, the
    /// game checks for a winner, and (if play continues) the next round is
    /// rolled with the loser starting.
    public mutating func resolveReveal<R: RandomNumberGenerator>(
        using rng: inout R
    ) -> [GameEvent] {
        guard case .reveal(let reveal) = phase,
              let loserIndex = players.firstIndex(where: { $0.id == reveal.loserID })
        else { return [] }

        players[loserIndex].diceCount -= 1
        var events: [GameEvent] = [
            .lostDie(playerID: reveal.loserID, remaining: players[loserIndex].diceCount)
        ]

        let loserEliminated = players[loserIndex].isEliminated
        if loserEliminated {
            players[loserIndex].cup = []
            events.append(.eliminated(playerID: reveal.loserID))
        }

        // End conditions: the human is out, or only one player remains.
        if let human = humanPlayer, human.isEliminated {
            phase = .gameOver(humanWon: false)
            events.append(.gameOver(humanWon: false))
            return events
        }
        let remaining = activePlayers
        if remaining.count <= 1 {
            let humanWon = remaining.first?.isHuman ?? false
            phase = .gameOver(humanWon: humanWon)
            events.append(.gameOver(humanWon: humanWon))
            return events
        }

        // Otherwise, roll a new round. The loser starts (or, if they were just
        // knocked out, the next player still in the game).
        let nextStarter = loserEliminated
            ? nextActivePlayerID(after: reveal.loserID)
            : reveal.loserID
        events.append(contentsOf: beginRound(starter: nextStarter, using: &rng))
        return events
    }

    // MARK: - Round setup

    private mutating func beginRound<R: RandomNumberGenerator>(
        starter: UUID,
        using rng: inout R
    ) -> [GameEvent] {
        round += 1
        for index in players.indices {
            if players[index].isEliminated {
                players[index].cup = []
            } else {
                players[index].cup = GameState.roll(players[index].diceCount, using: &rng)
            }
        }
        currentBid = nil
        currentBidderID = nil
        phase = .opening(starter: starter)
        return [.roundStarted(round: round, diceInPlay: diceInPlay)]
    }

    // MARK: - Helpers

    private static func roll<R: RandomNumberGenerator>(
        _ count: Int,
        using rng: inout R
    ) -> [Int] {
        (0..<count).map { _ in Int.random(in: 1...6, using: &rng) }
    }

    /// Walk forward around the table from `id` and return the next player who
    /// still has dice. Assumes at least one other active player exists.
    public func nextActivePlayerID(after id: UUID) -> UUID {
        guard let start = players.firstIndex(where: { $0.id == id }) else {
            return id
        }
        let count = players.count
        for step in 1...count {
            let candidate = players[(start + step) % count]
            if !candidate.isEliminated {
                return candidate.id
            }
        }
        return id
    }
}
