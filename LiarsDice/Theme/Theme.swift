import SwiftUI

/// Central place for the game's retro "pirate tavern" look: a tight, high
/// contrast palette, chunky monospaced type, and a couple of reusable
/// components so every screen feels like one game.
///
/// The aesthetic is deliberately a step up from plain text — bold flat colors,
/// thick ink borders, carved-bone dice — while staying lightweight (everything
/// is drawn by SwiftUI, no image assets required). Swapping in a true pixel
/// font like "Press Start 2P" later is a one-line change in `RetroFont`.

extension Color {
    init(hex: UInt) {
        let r = Double((hex >> 16) & 0xFF) / 255.0
        let g = Double((hex >> 8) & 0xFF) / 255.0
        let b = Double(hex & 0xFF) / 255.0
        self.init(.sRGB, red: r, green: g, blue: b, opacity: 1.0)
    }
}

enum Palette {
    static let night     = Color(hex: 0x14151F)
    static let table     = Color(hex: 0x2A6F5A)
    static let tableDark = Color(hex: 0x1E5142)
    static let wood      = Color(hex: 0x4A3526)
    static let woodDark  = Color(hex: 0x2A1C12)
    static let parchment = Color(hex: 0xE9D8A6)
    static let gold      = Color(hex: 0xF2C14E)
    static let bone      = Color(hex: 0xF6F0E2)
    static let pip       = Color(hex: 0x23201A)
    static let danger    = Color(hex: 0xD1495B)
    static let raise     = Color(hex: 0x3D8BFF)
    static let ink       = Color(hex: 0x241B12)
    static let cream     = Color(hex: 0xF7F3E8)
}

enum RetroFont {
    // To use a real pixel font, drop the .ttf into the app, register it in
    // Info.plist (Fonts provided by application), and return Font.custom here.
    static func title(_ size: CGFloat) -> Font { .system(size: size, weight: .black, design: .monospaced) }
    static func heavy(_ size: CGFloat) -> Font { .system(size: size, weight: .heavy, design: .monospaced) }
    static func body(_ size: CGFloat) -> Font  { .system(size: size, weight: .semibold, design: .monospaced) }
}

/// The felt-and-wood table backdrop shared by the menu and the game.
struct TableBackground: View {
    var body: some View {
        ZStack {
            Palette.night
            RadialGradient(
                colors: [Palette.table, Palette.tableDark],
                center: .center,
                startRadius: 40,
                endRadius: 520
            )
            .ignoresSafeArea()
            // A subtle wooden frame around the felt.
            RoundedRectangle(cornerRadius: 0)
                .stroke(Palette.woodDark, lineWidth: 18)
                .ignoresSafeArea()
        }
        .ignoresSafeArea()
    }
}

/// A chunky, ink-bordered button that drops down a few points when pressed.
struct RetroButtonStyle: ButtonStyle {
    var fill: Color = Palette.gold
    var textColor: Color = Palette.ink
    var fontSize: CGFloat = 18

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(RetroFont.heavy(fontSize))
            .foregroundStyle(textColor)
            .padding(.vertical, 12)
            .padding(.horizontal, 18)
            .frame(maxWidth: .infinity)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(fill)
                    .shadow(color: Palette.ink.opacity(0.5),
                            radius: 0, x: 0, y: configuration.isPressed ? 1 : 4)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Palette.ink, lineWidth: 3)
            )
            .offset(y: configuration.isPressed ? 3 : 0)
            .animation(.easeOut(duration: 0.08), value: configuration.isPressed)
    }
}

/// A parchment panel with a thick ink border.
private struct PanelModifier: ViewModifier {
    var fill: Color
    func body(content: Content) -> some View {
        content
            .padding(14)
            .background(RoundedRectangle(cornerRadius: 12).fill(fill))
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(Palette.ink, lineWidth: 3))
    }
}

extension View {
    func panel(_ fill: Color = Palette.parchment) -> some View {
        modifier(PanelModifier(fill: fill))
    }
}
