import Foundation

/// A narratable thing that just happened. Transition methods on ``GameState``
/// return a list of these so the UI can animate and narrate the action
/// without re-deriving what changed.
public enum GameEvent: Equatable, Sendable {
    case roundStarted(round: Int, diceInPlay: Int)
    case openingBid(playerID: UUID, bid: Bid)
    case raised(playerID: UUID, bid: Bid)
    case challenged(challengerID: UUID, bidderID: UUID, bid: Bid)
    case revealed(Reveal)
    case lostDie(playerID: UUID, remaining: Int)
    case eliminated(playerID: UUID)
    case gameOver(humanWon: Bool)
}
