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


# Dependencies



```
jsonpickle
dash==0.21.0                    # The core dash backend
dash-renderer==0.11.3           # The dash front-end
dash-html-components==0.9.0     # HTML components
dash-core-components==0.21.0rc1 # Supercharged components
plotly --upgrade                # Plotly graphing library used in examples
```

# Startup
SelfPG has two parts: One is the server who generates data, and the other is the Dash GUI which reads input.
First, run __main.py__ to generate data. Then run the front-end server with __dash_gui.py__. 

# Disclaimer
1. What SelfPG isn't
    * A playable game in a traditional sense
    * A high end simulation with fine tuned details
2. What SelfPG attempts to be:
    * A personal project to deepens the knowledge on python and self-taught introduction of GUI-development
    * Something fun to watch as the computer does all the work
    * 



Note: A lot of the implementation is currently in early early access. Ironing out the edges in regards to balancing and aesthetics will be considered after more features are implemented properly.