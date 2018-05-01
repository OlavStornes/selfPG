SelfPG - a zero-player game set in a Turn based RPG-enviroment
======

# Vision

SelfPG is a growing project with a lot of promises and not that much depth as of yet. There are, however, some points that will be implemented soon&trade;

 * Parties deciding when to travel for a town, or build their own for other parties to use
 * Persistent quests that parties wish to complete.
 * Procedural generated loot
 * Varied towns where parties actually must wander through
 * Visualization of combat phases
 * Overworld with more complicated pathfinding (considering rivers, hurdles, mountains etc)
 * Generalized spell-system
    * Some sort of spell-book for users to explore
 * A log/dictionary over important stuff which has happened. 
 * Parties with a good-evil scale in regards to:
    - Assaulting other towns
    - Defending a given town under assault 
    - Attacking other parties
    - Aggressivity and loyalty towards 
 * Some kind of self-regulating system in regards to over- and underpopulation.
 * An ecosystem that have no need of user input
    * No input should be needed for the sim, but is not ruled out. God-like interaction is considered
 * Market value on items based on how much it has been selled/buyed in the near past.


# Startup

## New changes
SelfPG was originally built around a local enviroment in mind, using TKinter for the interface and presentation. 

Lately SelfPG has been converted from a complete package over to a pure backend, sending streams of data to a cloud database ([Firebase](https://self-pg.firebaseapp.com/)). Reasons for this are: 
- More users on one single enviroment
- Go a step into HTML/JS-development
- Play around with a cloud database that easily gives real time data without hassling with websockets and such
- Easier to share the work with others

If you really want to see how it was with tkinter, there is a branch called `LEGACY_tkinter` that you can explore. Be noted that this is already outdated, and may or may not be removed later on.


# Disclaimer
1. What SelfPG isn't
    * A playable game in a traditional sense
    * A high end simulation with fine tuned details
2. What SelfPG attempts to be:
    * A personal project to deepen the knowledge on python, HTML and JS
    * Something fun to watch as the computer does all the work



Note: A lot of the implementation is currently in early early access. Ironing out the edges in regards to balancing and aesthetics will be considered after more features are implemented properly.