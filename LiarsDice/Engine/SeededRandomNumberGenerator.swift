import Foundation

/// A small, fast, fully deterministic generator (SplitMix64).
///
/// Used by the unit tests for reproducible games, and available to the app for
/// future "daily challenge" style seeded rounds. Given the same seed it always
/// produces the same sequence.
public struct SeededRandomNumberGenerator: RandomNumberGenerator, Sendable {
    private var state: UInt64

    public init(seed: UInt64) {
        self.state = seed
    }

    public mutating func next() -> UInt64 {
        state = state &+ 0x9E3779B97F4A7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58476D1CE4E5B9
        z = (z ^ (z >> 27)) &* 0x94D049BB133111EB
        return z ^ (z >> 31)
    }
}
