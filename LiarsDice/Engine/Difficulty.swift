import Foundation

/// How sharp the bots play. Higher difficulty bots are better at sniffing out
/// a bluff (they challenge closer to the true odds) and bluff a touch less.
public enum Difficulty: String, CaseIterable, Sendable, Codable {
    case easy
    case normal
    case hard

    public var displayName: String {
        switch self {
        case .easy:   return "Cabin Boy"
        case .normal: return "Buccaneer"
        case .hard:   return "Sea Devil"
        }
    }

    public var blurb: String {
        switch self {
        case .easy:   return "Forgiving foes who call your bluff only when it's blatant."
        case .normal: return "A fair fight. The crew plays the odds."
        case .hard:   return "Sharp-eyed devils who count every die and rarely miss."
        }
    }

    /// Scales how readily a bot challenges a suspicious bid.
    /// Higher means more skeptical (and more accurate).
    var skepticism: Double {
        switch self {
        case .easy:   return 0.6
        case .normal: return 1.0
        case .hard:   return 1.4
        }
    }
}
