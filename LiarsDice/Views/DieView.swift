import SwiftUI

/// Pip positions in a unit square (0...1) for each die face.
enum PipLayout {
    static func positions(for value: Int) -> [(x: CGFloat, y: CGFloat)] {
        let lo: CGFloat = 0.28, mid: CGFloat = 0.5, hi: CGFloat = 0.72
        switch max(1, min(6, value)) {
        case 1: return [(mid, mid)]
        case 2: return [(lo, lo), (hi, hi)]
        case 3: return [(lo, lo), (mid, mid), (hi, hi)]
        case 4: return [(lo, lo), (hi, lo), (lo, hi), (hi, hi)]
        case 5: return [(lo, lo), (hi, lo), (mid, mid), (lo, hi), (hi, hi)]
        default: return [(lo, lo), (hi, lo), (lo, mid), (hi, mid), (lo, hi), (hi, hi)]
        }
    }
}

/// A single carved-bone die showing `value`, drawn with SwiftUI shapes.
/// Bumping `rollTrigger` makes it tumble — used at the start of each round.
struct DieView: View {
    let value: Int
    var size: CGFloat = 44
    var fill: Color = Palette.bone
    var pipColor: Color = Palette.pip
    var rollTrigger: Int = 0

    @State private var spin: Double = 0

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: size * 0.2)
                .fill(fill)
            ForEach(Array(PipLayout.positions(for: value).enumerated()), id: \.offset) { _, pip in
                Circle()
                    .fill(pipColor)
                    .frame(width: size * 0.17, height: size * 0.17)
                    .position(x: pip.x * size, y: pip.y * size)
            }
        }
        .frame(width: size, height: size)
        .overlay(
            RoundedRectangle(cornerRadius: size * 0.2)
                .stroke(Palette.ink, lineWidth: max(2, size * 0.07))
        )
        .rotation3DEffect(.degrees(spin), axis: (x: 1, y: 1, z: 0.2))
        .shadow(color: Palette.ink.opacity(0.35), radius: 0, x: 0, y: 2)
        .onChange(of: rollTrigger) { _, _ in
            withAnimation(.spring(response: 0.55, dampingFraction: 0.55)) {
                spin += 360
            }
        }
    }
}

/// A face-down die (an opponent's hidden cup), with a little bone marker.
struct FaceDownDie: View {
    var size: CGFloat = 26

    var body: some View {
        RoundedRectangle(cornerRadius: size * 0.2)
            .fill(Palette.wood)
            .overlay(
                Circle()
                    .fill(Palette.parchment.opacity(0.55))
                    .frame(width: size * 0.24, height: size * 0.24)
            )
            .overlay(
                RoundedRectangle(cornerRadius: size * 0.2)
                    .stroke(Palette.ink, lineWidth: max(2, size * 0.07))
            )
            .frame(width: size, height: size)
            .shadow(color: Palette.ink.opacity(0.35), radius: 0, x: 0, y: 2)
    }
}

#Preview {
    HStack(spacing: 8) {
        ForEach(1...6, id: \.self) { DieView(value: $0, size: 40) }
        FaceDownDie(size: 40)
    }
    .padding()
    .background(Palette.table)
}
