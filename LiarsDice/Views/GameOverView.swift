import SwiftUI

/// Shown when the game ends. Winning gets the bosun's grudging congratulations;
/// losing your last die sends you to the Flying Dutchman to endure Crazy Pete.
struct GameOverView: View {
    let humanWon: Bool
    @ObservedObject var vm: GameViewModel
    var onExit: () -> Void

    var body: some View {
        ZStack {
            Color.black.opacity(0.78).ignoresSafeArea()
            if humanWon { victory } else { defeat }
        }
    }

    private var victory: some View {
        VStack(spacing: 18) {
            Text("⚓︎").font(.system(size: 56))
            Text("YE WIN!")
                .font(RetroFont.title(40))
                .foregroundStyle(Palette.gold)
            VStack(spacing: 8) {
                ForEach(Flavor.victoryLines, id: \.self) { line in
                    Text(line)
                        .font(RetroFont.body(14))
                        .foregroundStyle(Palette.ink)
                        .multilineTextAlignment(.center)
                }
            }
            .panel()
            buttons
        }
        .padding(24)
    }

    private var defeat: some View {
        VStack(spacing: 14) {
            Text("GAME OVER")
                .font(RetroFont.title(34))
                .foregroundStyle(Palette.danger)
            ScrollView {
                VStack(alignment: .leading, spacing: 14) {
                    Text(Flavor.crazyPeteIntro)
                    Text(Flavor.crazyPeteMonologue)
                    Text(Flavor.crazyPeteOutro)
                        .foregroundStyle(Palette.danger)
                }
                .font(RetroFont.body(13))
                .foregroundStyle(Palette.ink)
                .padding(4)
            }
            .frame(maxHeight: 320)
            .panel()
            buttons
        }
        .padding(20)
    }

    private var buttons: some View {
        HStack(spacing: 12) {
            Button("Play Again") { vm.rematch() }
                .buttonStyle(RetroButtonStyle(fill: Palette.gold))
            Button("Back to Shore") { onExit() }
                .buttonStyle(RetroButtonStyle(fill: Palette.parchment))
        }
    }
}
