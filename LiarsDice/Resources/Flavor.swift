import Foundation

/// All the pirate-flavored writing lives here, kept apart from the rules engine
/// and the views. This is where the original game's personality is preserved.
enum Flavor {

    static let tagline = "Lie well. Call the liars. Don't be the last scallywag holding nothing."

    static let rules = """
    Everyone hides their dice. On yer turn ye either RAISE the bid — claim there \
    be MORE dice of a value, or the SAME number of a HIGHER value across every \
    cup — or ye CHALLENGE the last bid if ye smell a lie.

    On a challenge, all dice be counted. Guess wrong and ye lose a die. Lose \
    all yer dice and ye be OUT. Last pirate standing wins the gold!
    """

    static let victoryLines = [
        "Well, blow me down! Ye actually WON?!",
        "Ye stared the sea devils in the eye and out-lied every last one of 'em!",
        "Take yer gold and get off me ship before I change me mind! HAHAHA!"
    ]

    /// The legendary defeat sequence from the original game, lovingly preserved.
    /// Shown when you lose your last die and are sentenced to the Flying Dutchman.
    static let crazyPeteIntro = """
    Bosun: Well... ye really made a mistake. Now you're stuck here with us for \
    the rest of forever. I hope ye like Crazy Pete... because you'll be listening \
    to him for a loooooong time! Hahahaha!

    You're escorted to the lower deck and handed a toothbrush. As you near the \
    bilge, you start to hear someone talking...
    """

    static let crazyPeteMonologue = """
    Crazy Pete: I go to the store. A car is parked. Many cars are parked or \
    moving. Some are blue. Some are tan. They have windows. In the store, there \
    are items for sale. These include such things as soap, detergent, magazines, \
    and lettuce. You can enhance your life with these products. Soap can be used \
    for bathing, be it in a bathtub or in a shower. Lettuce is a vegetable. It is \
    usually green and leafy, and is the main ingredient of salads...

    Crazy Pete: If I drive around, I sometimes notice the houses and buildings \
    all around. Houses can be built from different kinds of materials. The most \
    common types are brick, wood, and vinyl siding. Houses have lawns that need \
    to be mowed regularly. Most people use riding lawnmowers to do this. Many \
    families designate the lawnmowing responsibility to a teenager in the \
    household...

    Crazy Pete: Now I will talk about farm land. Farm land can be identified by \
    some common features. They almost always consist of a very large patch of \
    dirt with small green plants lined up in very long rows. Some different types \
    of crops are soybeans, cotton, corn, tomatoes, and lettuce (which I mentioned \
    earlier). A very versatile vegetable is the potato. It can be baked, mashed, \
    or cut into thin strips and fried...

    Crazy Pete: I will end my writing here. I have tried to make it very boring, \
    and I hope I have succeeded. There are plenty of boring documents available \
    for you to read. Check your public library for more information. You can also \
    find boring materials at a bookstore or in magazines (which I mentioned \
    earlier)...
    """

    static let crazyPeteOutro = "Welcome to the Flying Dutchman. I guess this is just life now... Arrr."
}
