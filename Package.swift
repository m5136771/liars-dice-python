// swift-tools-version: 5.9
import PackageDescription

// This package exists so the pure game logic in `LiarsDice/Engine` can be built
// and unit-tested straight from the command line (`swift test`) on any Mac,
// independently of the iOS app. The same source files are also compiled into
// the iOS app target by the Xcode project.
let package = Package(
    name: "LiarsDiceEngine",
    platforms: [
        .iOS(.v17),
        .macOS(.v13)
    ],
    products: [
        .library(name: "LiarsDiceEngine", targets: ["LiarsDiceEngine"])
    ],
    targets: [
        .target(
            name: "LiarsDiceEngine",
            path: "LiarsDice/Engine"
        ),
        .testTarget(
            name: "LiarsDiceEngineTests",
            dependencies: ["LiarsDiceEngine"],
            path: "Tests/LiarsDiceEngineTests"
        )
    ]
)
