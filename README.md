# EvoPawness Game

<p>Based on the article that I write https://github.com/haryoaw/evo-pawness</p>

<p>The game will be used to experiment AI Algorithm. Currently, No AI Algorithm that has been implemented. For the rules of the game, you can read the article.</p>

<b>NEW </b> : GUI is added
## Requirement
1. Python 3.6 (Anaconda Python is preferred)
2. Pandas

If you use GUI:
1. PyQt5

## How to use
1. Clone the git repository
2. Activate your CLI or terminal and do command `python main.py` in the main directory.

## Format output CLI
I will make it easier to use later on. Just hang on with this UX.Here is the output format:

#### Possible Action
List of Action :
<div>
`{'ACTION_KEY': {'action': 'ACTION_TYPE',
          'PARAMS' : 'VALUE PARAMS'},
{'p1a0': {'action': 'activate',
          'pawn_atk': 1,
          'pawn_hp': 3,
          'pawn_index': 0,
          'pawn_step': 1,
          'pawn_x': 0,
          'pawn_y': 1,
          'player_index': 1},
 'p1a1': {'action': 'activate',
          'pawn_atk': 1,
          'pawn_hp': 3,
          'pawn_index': 1,
          'pawn_step': 1,
          'pawn_x': 2,
          'pawn_y': 1,
          'player_index': 1},
 'p1a2': {'action': 'activate',
          'pawn_atk': 1,
          'pawn_hp': 3,
          'pawn_index': 2,
          'pawn_step': 1,
          'pawn_x': 4,
          'pawn_y': 1,
          'player_index': 1},
 'p1a3': {'action': 'activate',
          'pawn_atk': 1,
          'pawn_hp': 3,
          'pawn_index': 3,
          'pawn_step': 1,
          'pawn_x': 6,
          'pawn_y': 1,
          'player_index': 1},
 'p1a4': {'action': 'activate',
          'pawn_atk': 1,
          'pawn_hp': 3,
          'pawn_index': 4,
          'pawn_step': 1,
          'pawn_x': 8,
          'pawn_y': 1,
          'player_index': 1}}``</div>
          <br>
#### Board
<div>
`Noo+onee Noo+onee Noo+onee Noo+onee K1k3+15 Noo+onee Noo+onee Noo+onee Noo+onee
S1i0k1+3 Noo+onee S1i1k1+3 Noo+onee S1i2k1+3 Noo+onee S1i3k1+3 Noo+onee S1i4k1+3
Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee
Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee
Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee
Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee
Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee Noo+onee
S0i0k1+3 Noo+onee S0i1k1+3 Noo+onee S0i2k1+3 Noo+onee S0i3k1+3 Noo+onee S0i4k1+3
Noo+onee Noo+onee Noo+onee Noo+onee K0k3+15 Noo+onee Noo+onee Noo+onee Noo+onee
`</div>
To read:<br>
S1i0k1+3
S = Soldier the type of pawn
1 = player index
i0 = pawn index is 0
k1 = attack point of pawn is 1
+3 = health point of pawn is 3
<br>
#### Mana Status of Each Players

`Mana (White, Black) = (5, 5)`<br>
#### Rune
`Rune List:
{}`

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
- [x] Documenting (almost all of them)
- [ ] Fix the mess of the code (need more class and remove unnecessary code)
- [ ] Create the GUI
- [ ] Use classic AI Algorithm
- [ ] Use Reinforcement Learning
## FAQ
Q : Can I Contribute? <br>
A : Of course, just tell me what you want to contribute. <br>

Q : Can I Contact you? <br>
A : email me in haryomaenan@gmail.com if you want to contact me. Especially about this project.
