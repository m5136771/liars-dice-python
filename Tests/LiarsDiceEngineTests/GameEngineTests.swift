import XCTest
import LiarsDiceEngine

final class GameEngineTests: XCTestCase {

    // MARK: - Bid ordering

    func testBidIsHigher() {
        let base = Bid(quantity: 3, face: 4)
        XCTAssertTrue(Bid(quantity: 4, face: 1).isHigher(than: base))   // more dice wins
        XCTAssertTrue(Bid(quantity: 3, face: 5).isHigher(than: base))   // same qty, higher face
        XCTAssertFalse(Bid(quantity: 3, face: 4).isHigher(than: base))  // equal is not higher
        XCTAssertFalse(Bid(quantity: 3, face: 3).isHigher(than: base))  // lower face
        XCTAssertFalse(Bid(quantity: 2, face: 6).isHigher(than: base))  // fewer dice
    }

    // MARK: - New game setup

    func testNewGameSetup() {
        var rng = SeededRandomNumberGenerator(seed: 1)
        let state = GameState.newGame(
            playerName: "Tester",
            rules: GameRules(startingDice: 5, botCount: 3),
            using: &rng
        )
        XCTAssertEqual(state.players.count, 4)
        XCTAssertEqual(state.opponents.count, 3)
        XCTAssertEqual(state.humanPlayer?.name, "Tester")
        XCTAssertEqual(state.diceInPlay, 20)
        XCTAssertEqual(state.round, 1)
        XCTAssertTrue(state.players.allSatisfy { $0.cup.count == 5 })
        if case .opening = state.phase {} else {
            XCTFail("A fresh game should be waiting on an opening bid")
        }
    }

    func testEmptyNameFallsBack() {
        var rng = SeededRandomNumberGenerator(seed: 7)
        let state = GameState.newGame(playerName: "", using: &rng)
        XCTAssertEqual(state.humanPlayer?.name, "You")
    }

    // MARK: - Challenge resolution

    /// Builds a 2-player bidding state with fixed cups so outcomes are exact.
    private func biddingState(
        humanCup: [Int],
        botCup: [Int],
        bid: Bid,
        bidderIsBot: Bool,
        onesWild: Bool = false
    ) -> (state: GameState, humanID: UUID, botID: UUID) {
        let human = Player(name: "You", isBot: false, diceCount: humanCup.count, cup: humanCup)
        let bot = Player(name: "Bot", isBot: true, diceCount: botCup.count, cup: botCup)
        // The current player (challenger) is whoever is NOT the bidder.
        let bidderID = bidderIsBot ? bot.id : human.id
        let challengerID = bidderIsBot ? human.id : bot.id
        let state = GameState(
            players: [human, bot],
            rules: GameRules(startingDice: max(humanCup.count, botCup.count),
                             botCount: 1, onesAreWild: onesWild),
            phase: .bidding(current: challengerID),
            currentBid: bid,
            currentBidderID: bidderID,
            round: 1
        )
        return (state, human.id, bot.id)
    }

    func testChallengeWhenBidIsGood() {
        // Three 3s on the table (2 + 1); bid of three 3s is exactly met.
        var (state, humanID, botID) = biddingState(
            humanCup: [3, 3],
            botCup: [3, 5],
            bid: Bid(quantity: 3, face: 3),
            bidderIsBot: true
        )
        let events = state.challenge()
        let reveal = state.currentReveal
        XCTAssertEqual(reveal?.total, 3)
        XCTAssertEqual(reveal?.bidWasGood, true)
        // Bid was good, so the challenger (the human) loses.
        XCTAssertEqual(reveal?.loserID, humanID)
        XCTAssertNotEqual(reveal?.loserID, botID)
        XCTAssertTrue(events.contains(.revealed(reveal!)))
    }

    func testChallengeWhenBidIsALie() {
        // Only two 5s exist, but the bot bid three 5s. The bluff is caught.
        var (state, _, botID) = biddingState(
            humanCup: [5, 2],
            botCup: [5, 1],
            bid: Bid(quantity: 3, face: 5),
            bidderIsBot: true
        )
        _ = state.challenge()
        XCTAssertEqual(state.currentReveal?.total, 2)
        XCTAssertEqual(state.currentReveal?.bidWasGood, false)
        XCTAssertEqual(state.currentReveal?.loserID, botID)  // bidder caught lying
    }

    func testOnesAreWildCounting() {
        // Two natural 4s plus two wild 1s = four 4s when the rule is on.
        var (state, _, _) = biddingState(
            humanCup: [4, 1],
            botCup: [4, 1],
            bid: Bid(quantity: 4, face: 4),
            bidderIsBot: true,
            onesWild: true
        )
        _ = state.challenge()
        XCTAssertEqual(state.currentReveal?.total, 4)
        XCTAssertEqual(state.currentReveal?.bidWasGood, true)
    }

    // MARK: - Resolving a reveal

    func testResolveRevealLosesADieAndStartsNextRound() {
        var (state, humanID, _) = biddingState(
            humanCup: [3, 3],
            botCup: [3, 5],
            bid: Bid(quantity: 3, face: 3),
            bidderIsBot: true
        )
        _ = state.challenge()             // human (challenger) will lose
        var rng = SeededRandomNumberGenerator(seed: 99)
        _ = state.resolveReveal(using: &rng)

        XCTAssertEqual(state.player(humanID)?.diceCount, 1)  // 2 -> 1
        XCTAssertEqual(state.round, 2)
        // Loser starts the next round.
        if case .opening(let starter) = state.phase {
            XCTAssertEqual(starter, humanID)
        } else {
            XCTFail("Expected the next round to be waiting on an opening bid")
        }
    }

    func testHumanEliminationEndsGame() {
        // Human has a single die and will lose the challenge.
        let human = Player(name: "You", isBot: false, diceCount: 1, cup: [2])
        let bot = Player(name: "Bot", isBot: true, diceCount: 2, cup: [6, 6])
        var state = GameState(
            players: [human, bot],
            rules: GameRules(startingDice: 2, botCount: 1),
            phase: .bidding(current: human.id),   // human challenges
            currentBid: Bid(quantity: 2, face: 6),
            currentBidderID: bot.id,
            round: 1
        )
        _ = state.challenge()  // two 6s exist, bid good -> human loses
        var rng = SeededRandomNumberGenerator(seed: 3)
        _ = state.resolveReveal(using: &rng)
        XCTAssertEqual(state.phase, .gameOver(humanWon: false))
    }

    func testLastPlayerStandingWins() {
        // Bot has one die and will lose; only the human remains afterward.
        let human = Player(name: "You", isBot: false, diceCount: 2, cup: [1, 1])
        let bot = Player(name: "Bot", isBot: true, diceCount: 1, cup: [2])
        var state = GameState(
            players: [human, bot],
            rules: GameRules(startingDice: 2, botCount: 1),
            phase: .bidding(current: human.id),   // human challenges a lie
            currentBid: Bid(quantity: 3, face: 6),
            currentBidderID: bot.id,
            round: 1
        )
        _ = state.challenge()  // zero 6s -> bid was a lie -> bot loses its last die
        var rng = SeededRandomNumberGenerator(seed: 5)
        _ = state.resolveReveal(using: &rng)
        XCTAssertEqual(state.phase, .gameOver(humanWon: true))
    }

    // MARK: - Bid helpers

    func testMinimumRaiseAndLegalRaise() {
        let human = Player(name: "You", isBot: false, diceCount: 3, cup: [1, 2, 3])
        let bot = Player(name: "Bot", isBot: true, diceCount: 3, cup: [4, 5, 6])
        var state = GameState(
            players: [human, bot],
            rules: GameRules(startingDice: 3, botCount: 1),
            phase: .bidding(current: human.id),
            currentBid: Bid(quantity: 2, face: 4),
            currentBidderID: bot.id,
            round: 1
        )
        XCTAssertTrue(state.legalRaiseExists())
        XCTAssertEqual(state.minimumRaise(), Bid(quantity: 2, face: 5))

        // Bump to the ceiling: every one of the 6 dice showing a 6.
        _ = state.raise(Bid(quantity: 6, face: 6))
        XCTAssertFalse(state.legalRaiseExists())
        XCTAssertNil(state.minimumRaise())
    }

    func testNextActivePlayerSkipsEliminated() {
        let a = Player(name: "A", isBot: false, diceCount: 2)
        let b = Player(name: "B", isBot: true, diceCount: 0)  // out
        let c = Player(name: "C", isBot: true, diceCount: 2)
        let state = GameState(
            players: [a, b, c],
            rules: GameRules(startingDice: 2, botCount: 2),
            phase: .bidding(current: a.id),
            currentBid: Bid(quantity: 1, face: 1),
            currentBidderID: a.id,
            round: 1
        )
        XCTAssertEqual(state.nextActivePlayerID(after: a.id), c.id)  // skips eliminated B
    }

    // MARK: - Full game integration

    func testFullGameTerminates() {
        // Drive every seat with the bot AI and make sure a seeded game always
        // reaches a winner without stalling.
        var rng = SeededRandomNumberGenerator(seed: 20260617)
        var state = GameState.newGame(
            playerName: "Sim",
            rules: GameRules(startingDice: 5, botCount: 3),
            using: &rng
        )
        var safety = 0
        while !state.isGameOver && safety < 100_000 {
            safety += 1
            switch state.phase {
            case .opening, .bidding:
                let action = BotAI.action(for: state, using: &rng)
                _ = state.apply(action)
            case .reveal:
                _ = state.resolveReveal(using: &rng)
            case .gameOver:
                break
            }
        }
        XCTAssertTrue(state.isGameOver)
        XCTAssertLessThan(safety, 100_000)
        XCTAssertEqual(state.activePlayers.count, 1)
    }
}
