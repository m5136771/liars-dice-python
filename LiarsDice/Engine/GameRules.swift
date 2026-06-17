import Foundation

/// The knobs that define a single game's setup. Defaults match the classic
/// pirate game: one human, three bots, five dice each.
public struct GameRules: Equatable, Sendable, Codable {
    public var startingDice: Int
    public var botCount: Int
    /// When enabled, dice showing `1` count toward *any* bid face (the common
    /// "ones are wild" house rule). Off by default to match the original game.
    public var onesAreWild: Bool
    public var difficulty: Difficulty

    public init(
        startingDice: Int = 5,
        botCount: Int = 3,
        onesAreWild: Bool = false,
        difficulty: Difficulty = .normal
    ) {
        self.startingDice = max(1, startingDice)
        self.botCount = max(1, botCount)
        self.onesAreWild = onesAreWild
        self.difficulty = difficulty
    }
}
