# EvoPawness Game

<p>Based on the article that I write https://github.com/haryoaw/evo-pawness</p>

<p>The game will be used to experiment AI Algorithm. Currently, No AI Algorithm that has been implemented. For the rules of the game, you can read the article.</p>

<b>NEW </b> : GUI is added
## Requirement
1. Python 3.6 (Anaconda Python is preferred)
2. Pandas
`pip -U install pandas`

If you use GUI:
1. PyQt5
Install
`pip -U install pyqt5`
## How to use
1. Clone the git repository
2. Activate your CLI or terminal and do command `python main.py` (if you want to use CLI) or `python game_view_gui.py` (if you want to use the GUI) in the main directory.

## Format output CLI
I will make it easier to use later on. Just hang on with this UX.Here is the output format:

#### Possible Action
How To Read: 
List of Action :
{'ACTION_KEY': {'action': 'ACTION_TYPE',
          'PARAMS' : 'VALUE PARAMS'},
{'p1a0': {'action': 'activate',
          'pawn_atk': 1,
          'pawn_hp': 3,
          'pawn_index': 0,
          'pawn_step': 1,
          'pawn_x': 0,
          'pawn_y': 1,
          'player_index': 1},

#### Pawn
How To Read:
Soi2a1h3sFa : SoldierPawn, Index-pawn 2, Attack Point 1 , Health 3, Status Active : False

## How to use the GUI:
Use this command on your terminal
`python game_view_gui.py`

## Command list on CLI:
|Command| Description|
|-------|------------|
|exit|exit the game|
|ACTION_KEY|input the action. The ACTION_KEY is stated in the list of action provided in the command line.|
## Progress
- [x] Add basic elements to be input of AI Algorithm
- [ ] Documenting 
- [ ] Fix the mess of the code (need more class and remove unnecessary code)
- [X] Create the GUI
- [ ] Use classic AI Algorithm
- [ ] Use Reinforcement Learning
## FAQ
Q : Can I Contribute? <br>
A : Of course, just tell me what you want to contribute. <br>

Q : Can I Contact you? <br>
A : email me in haryomaenan@gmail.com if you want to contact me. Especially about this project.
