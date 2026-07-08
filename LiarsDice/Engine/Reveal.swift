import Foundation

/// The outcome of a challenge: every cup is shown, the matching dice are
/// counted, and someone is proven wrong.
public struct Reveal: Equatable, Sendable, Codable {
    public let bid: Bid
    public let challengerID: UUID
    public let bidderID: UUID
    /// Total dice across the whole table that matched the bid's face
    /// (including wild ones, if that rule is on).
    public let total: Int
    /// `true` if there really were at least `bid.quantity` matching dice.
    public let bidWasGood: Bool
    /// Whoever was proven wrong and loses a die.
    public let loserID: UUID

    public init(
        bid: Bid,
        challengerID: UUID,
        bidderID: UUID,
        total: Int,
        bidWasGood: Bool,
        loserID: UUID
    ) {
        self.bid = bid
        self.challengerID = challengerID
        self.bidderID = bidderID
        self.total = total
        self.bidWasGood = bidWasGood
        self.loserID = loserID
    }
}
