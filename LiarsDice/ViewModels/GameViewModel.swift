import Foundation
import SwiftUI
import Combine

/// Bridges the pure `GameState` engine to SwiftUI. It owns the game, runs bot
/// turns on a paced timer so the table feels alive, and turns engine events
/// into pirate narration. All mutation happens on the main actor so the
/// published state and the views stay in lockstep.
@MainActor
final class GameViewModel: ObservableObject {

    @Published private(set) var state: GameState
    /// Newest narration line, shown big in the center of the table.
    @Published private(set) var headline: String = ""
    /// Rolling log of recent events (oldest first), capped for memory.
    @Published private(set) var log: [String] = []
    /// True while bots are acting or a reveal is on screen — disables controls.
    @Published private(set) var isBusy: Bool = false
    /// Bumped at the start of each round to trigger the dice-roll animation.
    @Published private(set) var rollNonce: Int = 0

    let rules: GameRules
    let humanName: String
    private var rng = SystemRandomNumberGenerator()

    init(humanName: String, rules: GameRules) {
        self.rules = rules
        self.humanName = humanName
        var generator = SystemRandomNumberGenerator()
        self.state = GameState.newGame(playerName: humanName, rules: rules, using: &generator)
        self.rng = generator
        rollNonce = 1
        headline = "Round 1 — \(state.diceInPlay) dice in play. Shake yer cups!"
        log = [headline]
        start()
    }

    // MARK: - Convenience for the views

    var phase: GamePhase { state.phase }
    var currentBid: Bid? { state.currentBid }
    var human: Player? { state.humanPlayer }
    var opponents: [Player] { state.opponents }
    var reveal: Reveal? { state.currentReveal }
    var diceInPlay: Int { state.diceInPlay }

    var isHumanOpening: Bool {
        if case .opening(let starter) = state.phase {
            return state.player(starter)?.isHuman ?? false
        }
        return false
    }
    var isHumanBidding: Bool {
        if case .bidding(let current) = state.phase {
            return state.player(current)?.isHuman ?? false
        }
        return false
    }
    var awaitingHuman: Bool { (isHumanOpening || isHumanBidding) && !isBusy }
    var canChallenge: Bool { isHumanBidding && currentBid != nil && !isBusy }
    var canRaise: Bool { (isHumanBidding || isHumanOpening) && state.legalRaiseExists() && !isBusy }

    var gameOverHumanWon: Bool? {
        if case .gameOver(let won) = state.phase { return won }
        return nil
    }

    func name(_ id: UUID) -> String { state.player(id)?.name ?? "Someone" }

    func bidText(_ bid: Bid) -> String {
        let noun = bid.quantity == 1 ? "die" : "dice"
        return "\(bid.quantity) \(noun) showing \(bid.face)"
    }

    // MARK: - Human actions

    func submitOpeningBid(_ bid: Bid) {
        guard awaitingHuman, isHumanOpening else { return }
        narrate(state.submitOpeningBid(bid))
        runTurns()
    }

    func raise(_ bid: Bid) {
        guard awaitingHuman, isHumanBidding else { return }
        narrate(state.raise(bid))
        runTurns()
    }

    func challenge() {
        guard canChallenge else { return }
        narrate(state.challenge())
        runTurns()
    }

    func rematch() {
        var generator = SystemRandomNumberGenerator()
        state = GameState.newGame(playerName: humanName, rules: rules, using: &generator)
        rng = generator
        rollNonce += 1
        log = []
        headline = "Round 1 — \(state.diceInPlay) dice in play. Shake yer cups!"
        log = [headline]
        start()
    }

    // MARK: - Turn engine

    private func start() {
        Task { await runLoop() }
    }

    private func runTurns() {
        Task { await runLoop() }
    }

    /// Advance through bot turns and reveals until it's the human's move again,
    /// or the game ends.
    private func runLoop() async {
        isBusy = true
        loop: while true {
            switch state.phase {
            case .opening(let starter):
                guard let player = state.player(starter) else { break loop }
                if player.isBot {
                    await pause(.think)
                    let action = BotAI.action(for: state, using: &rng)
                    narrate(state.apply(action))
                } else {
                    break loop   // human's move
                }

            case .bidding(let current):
                guard let player = state.player(current) else { break loop }
                if player.isBot {
                    await pause(.think)
                    let action = BotAI.action(for: state, using: &rng)
                    narrate(state.apply(action))
                } else {
                    break loop   // human's move
                }

            case .reveal:
                await pause(.reveal)
                let events = state.resolveReveal(using: &rng)
                narrate(events)
                await pause(.round)

            case .gameOver:
                break loop
            }
        }
        isBusy = false
    }

    private enum Beat { case think, reveal, round }

    private func pause(_ beat: Beat) async {
        let seconds: Double
        switch beat {
        case .think:  seconds = 0.9
        case .reveal: seconds = 2.8
        case .round:  seconds = 1.2
        }
        try? await Task.sleep(for: .seconds(seconds))
    }

    // MARK: - Narration

    private func narrate(_ events: [GameEvent]) {
        for event in events {
            let line: String
            switch event {
            case .roundStarted(let round, let dice):
                rollNonce += 1
                line = "Round \(round) — \(dice) dice in play. Shake yer cups!"
            case .openingBid(let id, let bid):
                line = "\(name(id)) opens the biddin': \(bidText(bid))."
            case .raised(let id, let bid):
                line = "\(name(id)) raises to \(bidText(bid))."
            case .challenged(let challenger, let bidder, _):
                line = "\(name(challenger)) calls \(name(bidder)) a LIAR!"
            case .revealed(let reveal):
                let verdict = reveal.bidWasGood ? "The bid was GOOD!" : "It was a LIE!"
                line = "Count 'em up — \(reveal.total) showing \(reveal.bid.face). \(verdict)"
            case .lostDie(let id, let remaining):
                let noun = remaining == 1 ? "die" : "dice"
                line = "\(name(id)) loses a die — \(remaining) \(noun) left."
            case .eliminated(let id):
                line = "\(name(id)) is OUT of the game!"
            case .gameOver(let humanWon):
                line = humanWon ? "Last pirate standing — ye WIN!"
                                : "Ye've lost yer last die..."
            }
            headline = line
            log.append(line)
        }
        if log.count > 40 {
            log.removeFirst(log.count - 40)
        }
    }
}
