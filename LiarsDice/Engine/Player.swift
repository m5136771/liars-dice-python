import Foundation

/// One participant at the table — either the human or a bot.
public struct Player: Identifiable, Equatable, Sendable, Codable {
    public let id: UUID
    public var name: String
    public let isBot: Bool
    /// How many dice this player still owns. Lose a round, lose a die.
    public var diceCount: Int
    /// The dice rolled this round, hidden from everyone else.
    public var cup: [Int]

    public init(
        id: UUID = UUID(),
        name: String,
        isBot: Bool,
        diceCount: Int,
        cup: [Int] = []
    ) {
        self.id = id
        self.name = name
        self.isBot = isBot
        self.diceCount = diceCount
        self.cup = cup
    }

    public var isHuman: Bool { !isBot }
    public var isEliminated: Bool { diceCount <= 0 }
}
