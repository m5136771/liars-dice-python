import Foundation

/// A single decision a player can make on their turn. Both the human UI and
/// the bot AI produce one of these, and ``GameState`` applies it.
public enum TurnAction: Equatable, Sendable {
    case openingBid(Bid)
    case raise(Bid)
    case challenge
}
