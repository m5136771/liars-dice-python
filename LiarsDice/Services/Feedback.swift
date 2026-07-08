import Foundation
import AVFoundation
import UIKit

/// The eight chiptune effects bundled in LiarsDice/Resources/Audio.
enum GameSound: String, CaseIterable {
    case roll, bid, challenge
    case revealGood = "reveal_good"
    case revealLie = "reveal_lie"
    case loseDie = "lose_die"
    case win, lose
}

/// Reads the sound/haptics toggles from the same UserDefaults keys the menu
/// writes via `@AppStorage`. Both default to on.
enum FeedbackSettings {
    static var soundEnabled: Bool {
        UserDefaults.standard.object(forKey: "soundEnabled") as? Bool ?? true
    }
    static var hapticsEnabled: Bool {
        UserDefaults.standard.object(forKey: "hapticsEnabled") as? Bool ?? true
    }
}

/// Loads and plays the bundled sound effects. Players are cached so repeated
/// plays are instant, and the audio session is `.ambient` + `.mixWithOthers`
/// so the game never interrupts the player's own music and respects the
/// silent switch.
@MainActor
final class AudioManager {
    static let shared = AudioManager()

    private var players: [GameSound: AVAudioPlayer] = [:]
    private var sessionConfigured = false

    private func configureSession() {
        guard !sessionConfigured else { return }
        sessionConfigured = true
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.ambient, options: [.mixWithOthers])
        try? session.setActive(true)
    }

    private func url(for sound: GameSound) -> URL? {
        let name = sound.rawValue
        return Bundle.main.url(forResource: name, withExtension: "wav")
            ?? Bundle.main.url(forResource: name, withExtension: "wav", subdirectory: "Audio")
    }

    private func player(for sound: GameSound) -> AVAudioPlayer? {
        if let cached = players[sound] { return cached }
        guard let url = url(for: sound), let player = try? AVAudioPlayer(contentsOf: url) else {
            return nil
        }
        player.prepareToPlay()
        players[sound] = player
        return player
    }

    func play(_ sound: GameSound) {
        guard FeedbackSettings.soundEnabled else { return }
        configureSession()
        guard let player = player(for: sound) else { return }
        player.currentTime = 0
        player.play()
    }

    /// Preload every effect so the first in-game play has no hitch.
    func warmUp() {
        for sound in GameSound.allCases { _ = player(for: sound) }
    }
}

/// Thin wrapper over UIKit's haptic generators, gated by the user setting.
@MainActor
enum Haptics {
    static func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle) {
        guard FeedbackSettings.hapticsEnabled else { return }
        UIImpactFeedbackGenerator(style: style).impactOccurred()
    }

    static func notify(_ type: UINotificationFeedbackGenerator.FeedbackType) {
        guard FeedbackSettings.hapticsEnabled else { return }
        UINotificationFeedbackGenerator().notificationOccurred(type)
    }

    static func selection() {
        guard FeedbackSettings.hapticsEnabled else { return }
        UISelectionFeedbackGenerator().selectionChanged()
    }
}

/// Semantic game moments. The view model fires these; this layer maps each to a
/// matching sound + haptic so callers don't worry about either.
enum GameFeedback {
    case roll, bid, challenge, revealGood, revealLie, loseDie, eliminated, win, lose
}

@MainActor
enum Feedback {
    static func play(_ feedback: GameFeedback) {
        switch feedback {
        case .roll:       Haptics.impact(.light);   AudioManager.shared.play(.roll)
        case .bid:        Haptics.selection();       AudioManager.shared.play(.bid)
        case .challenge:  Haptics.impact(.heavy);    AudioManager.shared.play(.challenge)
        case .revealGood: Haptics.notify(.success);  AudioManager.shared.play(.revealGood)
        case .revealLie:  Haptics.notify(.warning);  AudioManager.shared.play(.revealLie)
        case .loseDie:    Haptics.impact(.medium);   AudioManager.shared.play(.loseDie)
        case .eliminated: Haptics.notify(.error)
        case .win:        Haptics.notify(.success);  AudioManager.shared.play(.win)
        case .lose:       Haptics.notify(.error);    AudioManager.shared.play(.lose)
        }
    }
}
