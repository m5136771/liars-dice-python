import SwiftUI

@main
struct LiarsDiceApp: App {
    var body: some Scene {
        WindowGroup {
            RootView()
                .preferredColorScheme(.dark)
        }
    }
}

/// Switches between the main menu and an in-progress game. A new
/// ``GameViewModel`` is created each time a game starts, and torn down when the
/// player returns to shore.
struct RootView: View {
    @State private var game: GameViewModel?

    var body: some View {
        ZStack {
            if let game {
                GameTableView(vm: game) {
                    withAnimation(.easeInOut) { self.game = nil }
                }
                .transition(.move(edge: .trailing).combined(with: .opacity))
            } else {
                MainMenuView { name, rules in
                    withAnimation(.easeInOut) {
                        game = GameViewModel(humanName: name, rules: rules)
                    }
                }
                .transition(.move(edge: .leading).combined(with: .opacity))
            }
        }
    }
}
