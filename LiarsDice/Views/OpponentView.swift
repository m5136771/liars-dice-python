import SwiftUI

/// One bot's seat at the top of the table: a speech bubble for their bid, their
/// dice (face-down, or revealed during a challenge), and their name.
struct OpponentView: View {
    let player: Player
    var isCurrent: Bool          // it's this bot's turn
    var bid: Bid?                // their current bid, if they hold the lead
    var revealed: Bool           // show real dice values (during a reveal)
    var highlightFace: Int?      // ring the dice that matched the challenged bid
    var rollTrigger: Int

    private var dieSize: CGFloat { player.diceCount > 4 ? 18 : 22 }

    var body: some View {
        VStack(spacing: 5) {
            bubble
                .frame(height: 26)

            diceRow

            Text(player.name)
                .font(RetroFont.body(11))
                .foregroundStyle(Palette.cream)
                .lineLimit(1)
                .minimumScaleFactor(0.7)
        }
        .padding(8)
        .frame(width: 96)
        .background(
            RoundedRectangle(cornerRadius: 10)
                .fill(isCurrent ? Palette.gold.opacity(0.22) : Color.clear)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 10)
                .stroke(isCurrent ? Palette.gold : Color.clear, lineWidth: 2)
        )
        .opacity(player.isEliminated ? 0.4 : 1)
        .overlay(alignment: .center) {
            if player.isEliminated {
                Text("OUT")
                    .font(RetroFont.heavy(14))
                    .foregroundStyle(Palette.cream)
                    .padding(.horizontal, 8).padding(.vertical, 3)
                    .background(Capsule().fill(Palette.danger))
                    .rotationEffect(.degrees(-12))
            }
        }
        .animation(.easeInOut(duration: 0.2), value: isCurrent)
    }

    @ViewBuilder private var bubble: some View {
        if player.isEliminated {
            EmptyView()
        } else if let bid, !revealed {
            HStack(spacing: 3) {
                Text("\(bid.quantity)×").font(RetroFont.heavy(12))
                DieView(value: bid.face, size: 16)
            }
            .padding(.horizontal, 8).padding(.vertical, 3)
            .background(Capsule().fill(Palette.parchment))
            .overlay(Capsule().stroke(Palette.ink, lineWidth: 2))
            .foregroundStyle(Palette.ink)
        } else if isCurrent && !revealed {
            Text("…thinkin'")
                .font(RetroFont.body(11))
                .foregroundStyle(Palette.ink)
                .padding(.horizontal, 8).padding(.vertical, 3)
                .background(Capsule().fill(Palette.parchment.opacity(0.85)))
        } else {
            EmptyView()
        }
    }

    @ViewBuilder private var diceRow: some View {
        HStack(spacing: 3) {
            if revealed {
                ForEach(Array(player.cup.enumerated()), id: \.offset) { _, value in
                    DieView(value: value, size: dieSize, rollTrigger: rollTrigger)
                        .overlay(
                            RoundedRectangle(cornerRadius: dieSize * 0.2)
                                .stroke(Palette.gold, lineWidth: 3)
                                .opacity(highlightFace == value ? 1 : 0)
                        )
                }
            } else {
                ForEach(Array(0..<max(0, player.diceCount)), id: \.self) { _ in
                    FaceDownDie(size: dieSize)
                }
            }
        }
        .frame(height: 24)
    }
}
