import SwiftUI

/// The playing table: opponents up top, the running narration and current bid
/// in the middle, your dice and controls at the bottom. A game-over panel
/// slides over everything when the last die is lost.
struct GameTableView: View {
    @ObservedObject var vm: GameViewModel
    var onExit: () -> Void

    private var revealing: Bool { vm.reveal != nil }
    private var highlightFace: Int? { vm.reveal?.bid.face }

    var body: some View {
        ZStack {
            TableBackground()

            VStack(spacing: 8) {
                topBar
                opponentsRow
                Spacer(minLength: 4)
                centerArea
                Spacer(minLength: 4)
                playerArea
            }
            .padding(.horizontal, 10)
            .padding(.top, 4)

            if let humanWon = vm.gameOverHumanWon {
                GameOverView(humanWon: humanWon, vm: vm, onExit: onExit)
                    .transition(.opacity.combined(with: .scale))
            }
        }
        .animation(.easeInOut(duration: 0.35), value: vm.gameOverHumanWon)
    }

    // MARK: - Top bar

    private var topBar: some View {
        HStack {
            Button(action: onExit) {
                Text("‹ Menu").font(RetroFont.body(13)).foregroundStyle(Palette.cream)
            }
            Spacer()
            Text("\(vm.diceInPlay) dice in play")
                .font(RetroFont.body(13))
                .foregroundStyle(Palette.gold)
        }
        .padding(.horizontal, 4)
    }

    // MARK: - Opponents

    private var opponentsRow: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(vm.opponents) { opp in
                    OpponentView(
                        player: opp,
                        isCurrent: vm.state.currentPlayerID == opp.id,
                        bid: opp.id == vm.state.currentBidderID ? vm.currentBid : nil,
                        revealed: revealing,
                        highlightFace: highlightFace,
                        rollTrigger: vm.rollNonce
                    )
                }
            }
            .frame(maxWidth: .infinity)
            .padding(.horizontal, 4)
        }
    }

    // MARK: - Center (narration + bid / reveal)

    private var centerArea: some View {
        VStack(spacing: 12) {
            if revealing, let reveal = vm.reveal {
                revealVisual(reveal)
            } else if let bid = vm.currentBid {
                currentBidVisual(bid)
            }

            Text(vm.headline)
                .font(RetroFont.body(15))
                .foregroundStyle(Palette.ink)
                .multilineTextAlignment(.center)
                .frame(maxWidth: .infinity)
                .panel(Palette.parchment.opacity(0.95))
        }
        .padding(.horizontal, 4)
    }

    private func currentBidVisual(_ bid: Bid) -> some View {
        VStack(spacing: 4) {
            Text("CURRENT BID")
                .font(RetroFont.body(12))
                .foregroundStyle(Palette.cream.opacity(0.8))
            HStack(spacing: 8) {
                Text("\(bid.quantity)")
                    .font(RetroFont.title(40))
                    .foregroundStyle(Palette.gold)
                Text("×").font(RetroFont.title(28)).foregroundStyle(Palette.cream)
                DieView(value: bid.face, size: 44)
            }
        }
    }

    private func revealVisual(_ reveal: Reveal) -> some View {
        VStack(spacing: 6) {
            Text(reveal.bidWasGood ? "THE BID HELD!" : "CAUGHT IN A LIE!")
                .font(RetroFont.title(20))
                .foregroundStyle(reveal.bidWasGood ? Palette.gold : Palette.danger)
            HStack(spacing: 8) {
                DieView(value: reveal.bid.face, size: 40)
                Text("× \(reveal.total)")
                    .font(RetroFont.title(30))
                    .foregroundStyle(Palette.cream)
                Text("(bid \(reveal.bid.quantity))")
                    .font(RetroFont.body(14))
                    .foregroundStyle(Palette.cream.opacity(0.8))
            }
        }
    }

    // MARK: - Player area

    private var playerArea: some View {
        VStack(spacing: 10) {
            yourDice
            controls
        }
    }

    private var yourDice: some View {
        VStack(spacing: 4) {
            Text("YER DICE")
                .font(RetroFont.body(12))
                .foregroundStyle(Palette.gold)
            HStack(spacing: 6) {
                if let human = vm.human {
                    ForEach(Array(human.cup.enumerated()), id: \.offset) { _, value in
                        DieView(value: value, size: 40, rollTrigger: vm.rollNonce)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Palette.gold, lineWidth: 3)
                                    .opacity(revealing && highlightFace == value ? 1 : 0)
                            )
                    }
                    if human.isEliminated {
                        Text("Out of dice!").font(RetroFont.body(14)).foregroundStyle(Palette.cream)
                    }
                }
            }
        }
    }

    @ViewBuilder private var controls: some View {
        if vm.gameOverHumanWon != nil {
            EmptyView()
        } else if vm.isHumanOpening && !vm.isBusy {
            BidControlView(mode: .opening, diceInPlay: vm.diceInPlay) { bid in
                vm.submitOpeningBid(bid)
            }
        } else if vm.isHumanBidding && !vm.isBusy {
            VStack(spacing: 10) {
                if vm.canRaise, let current = vm.currentBid {
                    BidControlView(mode: .raise(current), diceInPlay: vm.diceInPlay) { bid in
                        vm.raise(bid)
                    }
                } else {
                    Text("No higher bid be possible — ye must CHALLENGE!")
                        .font(RetroFont.body(13))
                        .foregroundStyle(Palette.cream)
                        .multilineTextAlignment(.center)
                }
                Button("CHALLENGE!") { vm.challenge() }
                    .buttonStyle(RetroButtonStyle(fill: Palette.danger, textColor: Palette.cream))
            }
        } else {
            Text(revealing ? "Countin' the dice..." : "Watch the table, matey...")
                .font(RetroFont.body(14))
                .foregroundStyle(Palette.cream.opacity(0.85))
                .frame(maxWidth: .infinity)
                .frame(height: 54)
        }
    }
}
