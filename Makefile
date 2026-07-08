# Convenience tasks. Run `make help` for the list.

.PHONY: help test project open build

help:
	@echo "Liar's Dice — developer tasks"
	@echo ""
	@echo "  make test      Run the game-engine unit tests (swift test)"
	@echo "  make project   Regenerate LiarsDice.xcodeproj from project.yml (needs xcodegen)"
	@echo "  make open      Open the app in Xcode"
	@echo "  make build     Build the app for the iOS Simulator (needs Xcode)"
	@echo ""

# Runs the pure-logic engine tests from the command line. No Xcode required.
test:
	swift test

# Only needed if the committed Xcode project ever drifts. Requires:
#   brew install xcodegen
project:
	xcodegen generate

open:
	open LiarsDice.xcodeproj

# Builds without launching Xcode's UI. Adjust the simulator name as needed.
build:
	xcodebuild -project LiarsDice.xcodeproj -scheme LiarsDice \
		-destination 'platform=iOS Simulator,name=iPhone 15' build
