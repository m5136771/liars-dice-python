import Foundation

/// Decides what a bot does on its turn. The logic is a tightened-up version of
/// the original Python bots: estimate how many matching dice are probably out
/// there, challenge when a bid clearly outruns that estimate, otherwise nudge
/// the bid up. Difficulty scales how skeptical (and accurate) the bots are.
public enum BotAI {

    /// Choose an action for whichever player must act in `state` (assumed to be
    /// a bot). Randomness flows through the injected generator so games are
    /// reproducible in tests.
    public static func action<R: RandomNumberGenerator>(
        for state: GameState,
        using rng: inout R
    ) -> TurnAction {
        guard let me = state.currentPlayer else {
            return .challenge
        }
        let diceInPlay = state.diceInPlay

        // Opening bid: lean on what we actually rolled, plus a little padding.
        guard let bid = state.currentBid else {
            let face = Int.random(in: 1...6, using: &rng)
            let own = me.cup.filter { $0 == face }.count
            var quantity = own + Int.random(in: 0...1, using: &rng)
            quantity = max(1, min(quantity, diceInPlay))
            return .openingBid(Bid(quantity: quantity, face: face))
        }

        // How many of the bid face do we expect across the table?
        let wildBonus = (state.rules.onesAreWild && bid.face != 1)
            ? me.cup.filter { $0 == 1 }.count : 0
        let own = me.cup.filter { $0 == bid.face }.count + wildBonus
        let unknownDice = diceInPlay - me.cup.count
        let perDie = (state.rules.onesAreWild && bid.face != 1) ? 2.0 / 6.0 : 1.0 / 6.0
        let expected = Double(own) + Double(unknownDice) * perDie

        let canRaiseQuantity = bid.quantity < diceInPlay
        let canRaiseFace = bid.face < 6
        let skepticism = state.rules.difficulty.skepticism
        let overage = Double(bid.quantity) - expected

        let challengeChance: Double
        if !canRaiseQuantity && !canRaiseFace {
            challengeChance = 1.0                      // no higher bid possible
        } else if overage > 1.0 {
            challengeChance = min(1.0, 0.78 * skepticism)  // bid looks greedy
        } else if overage > 0.0 {
            challengeChance = min(1.0, 0.30 * skepticism)  // a little high
        } else {
            challengeChance = min(1.0, 0.06 * skepticism)  // looks safe; rarely call
        }

        if Double.random(in: 0..<1, using: &rng) < challengeChance {
            return .challenge
        }

        // Raise. Prefer bumping the face we already hold the most of when we're
        // forced to pick, otherwise take the cheapest legal step up.
        if canRaiseFace && canRaiseQuantity {
            if Bool.random(using: &rng) {
                return .raise(Bid(quantity: bid.quantity, face: bid.face + 1))
            } else {
                return .raise(Bid(quantity: bid.quantity + 1, face: bestFace(for: me, default: bid.face)))
            }
        } else if canRaiseFace {
            return .raise(Bid(quantity: bid.quantity, face: bid.face + 1))
        } else {
            // face is maxed, so we must add quantity
            return .raise(Bid(quantity: bid.quantity + 1, face: bid.face))
        }
    }

    /// The face value this bot holds the most of (ties fall back to `default`).
    /// Used to steer a quantity-raise toward a face the bot can actually back up.
    private static func bestFace(for player: Player, default fallback: Int) -> Int {
        var counts = [Int: Int]()
        for die in player.cup { counts[die, default: 0] += 1 }
        guard let best = counts.max(by: { $0.value < $1.value }), best.value > 0 else {
            return fallback
        }
        return best.key
    }
}
