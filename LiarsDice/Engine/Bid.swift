import Foundation

/// A claim that *at least* `quantity` dice across the whole table are showing `face`.
///
/// Raising the stakes means either claiming a larger quantity, or the same
/// quantity at a higher face value. This is the single rule that makes the
/// bidding ladder work.
public struct Bid: Equatable, Hashable, Sendable, Codable {
    public let quantity: Int
    public let face: Int

    public init(quantity: Int, face: Int) {
        self.quantity = quantity
        self.face = face
    }

    /// A legal raise must increase the quantity, or keep the quantity while
    /// increasing the face value.
    public func isHigher(than other: Bid) -> Bool {
        if quantity > other.quantity { return true }
        if quantity == other.quantity && face > other.face { return true }
        return false
    }
}
