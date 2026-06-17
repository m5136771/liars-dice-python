import SwiftUI

/// Title screen and pre-game setup: your name, the crew size, difficulty, and
/// the optional "ones are wild" house rule. Hands a finished ``GameRules`` and
/// name back to the caller to start a game.
struct MainMenuView: View {
    var onStart: (String, GameRules) -> Void

    @AppStorage("playerName") private var name: String = ""
    @AppStorage("difficulty") private var difficultyRaw: String = Difficulty.normal.rawValue
    @AppStorage("soundEnabled") private var soundEnabled: Bool = true
    @AppStorage("hapticsEnabled") private var hapticsEnabled: Bool = true
    @State private var botCount: Int = 3
    @State private var onesWild: Bool = false
    @State private var showRules = false

    private var difficulty: Difficulty {
        Difficulty(rawValue: difficultyRaw) ?? .normal
    }

    var body: some View {
        ZStack {
            TableBackground()
            ScrollView {
                VStack(spacing: 22) {
                    header
                    settingsPanel
                    Button("SET SAIL ⚓︎") {
                        let rules = GameRules(
                            startingDice: 5,
                            botCount: botCount,
                            onesAreWild: onesWild,
                            difficulty: difficulty
                        )
                        onStart(name.trimmingCharacters(in: .whitespaces), rules)
                    }
                    .buttonStyle(RetroButtonStyle(fill: Palette.gold, fontSize: 22))

                    Button { showRules.toggle() } label: {
                        Text(showRules ? "Hide the rules" : "How d'ye play?")
                            .font(RetroFont.body(13))
                            .foregroundStyle(Palette.cream.opacity(0.85))
                    }
                    if showRules {
                        Text(Flavor.rules)
                            .font(RetroFont.body(13))
                            .foregroundStyle(Palette.ink)
                            .panel()
                            .transition(.opacity)
                    }
                }
                .padding(20)
            }
        }
        .animation(.easeInOut(duration: 0.2), value: showRules)
    }

    private var header: some View {
        VStack(spacing: 6) {
            Text("LIAR'S DICE")
                .font(RetroFont.title(44))
                .foregroundStyle(Palette.gold)
                .shadow(color: Palette.ink, radius: 0, x: 0, y: 3)
            Text("☠︎ A Pirate's Bluffing Game ☠︎")
                .font(RetroFont.body(14))
                .foregroundStyle(Palette.cream)
            Text(Flavor.tagline)
                .font(RetroFont.body(12))
                .foregroundStyle(Palette.cream.opacity(0.8))
                .multilineTextAlignment(.center)
                .padding(.top, 2)
        }
        .padding(.top, 10)
    }

    private var settingsPanel: some View {
        VStack(alignment: .leading, spacing: 16) {
            field(title: "YER NAME") {
                TextField("Captain No-Beard", text: $name)
                    .textInputAutocapitalization(.words)
                    .autocorrectionDisabled()
                    .font(RetroFont.body(16))
                    .foregroundStyle(Palette.ink)
                    .padding(10)
                    .background(RoundedRectangle(cornerRadius: 8).fill(Palette.bone))
                    .overlay(RoundedRectangle(cornerRadius: 8).stroke(Palette.ink, lineWidth: 2))
            }

            field(title: "DIFFICULTY") {
                HStack(spacing: 8) {
                    ForEach(Difficulty.allCases, id: \.self) { level in
                        chip(level.displayName, selected: difficulty == level) {
                            difficultyRaw = level.rawValue
                        }
                    }
                }
            }
            Text(difficulty.blurb)
                .font(RetroFont.body(11))
                .foregroundStyle(Palette.ink.opacity(0.7))

            field(title: "CREW SIZE") {
                HStack(spacing: 14) {
                    roundButton("–") { botCount = max(1, botCount - 1) }
                    Text("\(botCount) bots")
                        .font(RetroFont.heavy(18))
                        .foregroundStyle(Palette.ink)
                        .frame(minWidth: 90)
                    roundButton("+") { botCount = min(5, botCount + 1) }
                }
            }

            toggleRow("Ones are wild", isOn: $onesWild)
            toggleRow("Sound effects", isOn: $soundEnabled)
            toggleRow("Haptics", isOn: $hapticsEnabled)
        }
        .panel()
    }

    private func toggleRow(_ title: String, isOn: Binding<Bool>) -> some View {
        Toggle(isOn: isOn) {
            Text(title)
                .font(RetroFont.body(14))
                .foregroundStyle(Palette.ink)
        }
        .tint(Palette.danger)
    }

    // MARK: - Small building blocks

    @ViewBuilder
    private func field<Content: View>(title: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title)
                .font(RetroFont.body(12))
                .foregroundStyle(Palette.ink.opacity(0.7))
            content()
        }
    }

    private func chip(_ label: String, selected: Bool, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Text(label)
                .font(RetroFont.body(12))
                .foregroundStyle(selected ? Palette.ink : Palette.cream)
                .padding(.vertical, 8)
                .padding(.horizontal, 10)
                .frame(maxWidth: .infinity)
                .background(RoundedRectangle(cornerRadius: 8).fill(selected ? Palette.gold : Palette.wood))
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(Palette.ink, lineWidth: 2))
        }
        .buttonStyle(.plain)
    }

    private func roundButton(_ label: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Text(label)
                .font(RetroFont.title(22))
                .foregroundStyle(Palette.cream)
                .frame(width: 40, height: 40)
                .background(Circle().fill(Palette.wood))
                .overlay(Circle().stroke(Palette.ink, lineWidth: 2))
        }
        .buttonStyle(.plain)
    }
}
