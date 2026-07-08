import SwiftUI

/// The human's bidding panel: pick a quantity and a face, then confirm. Works
/// for both the opening bid and a raise; in raise mode it refuses anything that
/// isn't strictly higher than the standing bid.
struct BidControlView: View {
    enum Mode: Equatable {
        case opening
        case raise(Bid)
    }

    let mode: Mode
    let diceInPlay: Int
    let onBid: (Bid) -> Void

    @State private var quantity: Int
    @State private var face: Int

    init(mode: Mode, diceInPlay: Int, onBid: @escaping (Bid) -> Void) {
        self.mode = mode
        self.diceInPlay = diceInPlay
        self.onBid = onBid
        switch mode {
        case .opening:
            _quantity = State(initialValue: min(2, max(1, diceInPlay)))
            _face = State(initialValue: 5)
        case .raise(let current):
            if current.face < 6 {
                _quantity = State(initialValue: current.quantity)
                _face = State(initialValue: current.face + 1)
            } else {
                _quantity = State(initialValue: min(current.quantity + 1, diceInPlay))
                _face = State(initialValue: 1)
            }
        }
    }

    private var bid: Bid { Bid(quantity: quantity, face: face) }

    private var isValid: Bool {
        guard quantity >= 1, quantity <= diceInPlay, (1...6).contains(face) else { return false }
        switch mode {
        case .opening:           return true
        case .raise(let current): return bid.isHigher(than: current)
        }
    }

    private var confirmTitle: String {
        if case .opening = mode { return "Make Bid" }
        return "Raise"
    }

    var body: some View {
        VStack(spacing: 12) {
            HStack(spacing: 18) {
                stepper(title: "HOW MANY") {
                    Text("\(quantity)")
                        .font(RetroFont.title(30))
                        .foregroundStyle(Palette.ink)
                        .frame(minWidth: 40)
                } onMinus: {
                    quantity = max(1, quantity - 1)
                } onPlus: {
                    quantity = min(diceInPlay, quantity + 1)
                }

                stepper(title: "SHOWING") {
                    DieView(value: face, size: 34)
                } onMinus: {
                    face = max(1, face - 1)
                } onPlus: {
                    face = min(6, face + 1)
                }
            }

            Button(confirmTitle) { onBid(bid) }
                .buttonStyle(RetroButtonStyle(fill: isValid ? Palette.gold : Palette.parchment))
                .disabled(!isValid)
                .opacity(isValid ? 1 : 0.5)
        }
        .panel()
    }

    @ViewBuilder
    private func stepper<Content: View>(
        title: String,
        @ViewBuilder value: () -> Content,
        onMinus: @escaping () -> Void,
        onPlus: @escaping () -> Void
    ) -> some View {
        VStack(spacing: 6) {
            Text(title)
                .font(RetroFont.body(11))
                .foregroundStyle(Palette.ink.opacity(0.7))
            HStack(spacing: 8) {
                roundButton("–", action: onMinus)
                value()
                roundButton("+", action: onPlus)
            }
        }
    }

    private func roundButton(_ label: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Text(label)
                .font(RetroFont.title(22))
                .foregroundStyle(Palette.cream)
                .frame(width: 38, height: 38)
                .background(Circle().fill(Palette.wood))
                .overlay(Circle().stroke(Palette.ink, lineWidth: 2))
        }
        .buttonStyle(.plain)
    }
}
