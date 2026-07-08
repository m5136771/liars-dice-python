import Foundation

/// Whose move it is and what the game is currently waiting on. The view layer
/// reads this to decide what to draw and which controls to enable.
public enum GamePhase: Equatable, Sendable {
    /// The round just started; `starter` must make the opening bid (no
    /// challenge is possible because there's nothing to challenge yet).
    case opening(starter: UUID)

    /// Bidding is underway; it is `current`'s turn to raise or challenge.
    case bidding(current: UUID)

    /// A challenge was made and the dice are on the table.
    case reveal(Reveal)

    /// The game is finished.
    case gameOver(humanWon: Bool)
}
