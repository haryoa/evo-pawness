# EvoPawness Game

Based on the article that I write https://towardsdatascience.com/create-your-own-board-game-with-powerful-ai-from-scratch-part-1-5dcb028002b8  

<p>The game will be used to experiment AI Algorithm. Currently, No AI Algorithm that has been implemented. For the rules of the game, you can read the article.</p>

GUI has been added
## Requirement
1. Python 3.6 (Anaconda Python is preferred)
2. Pandas

If you use GUI:
1. PyQt5

## How to use
1. Clone the git repository
2. Activate your CLI or terminal and do command `python main.py` or `python main_gui.py` in the main directory.

## Format output CLI

#### Possible Action
List of Action :  
`{'ACTION_KEY': {'action': 'ACTION_TYPE',
          'PARAMS' : 'VALUE PARAMS'}
#### Board
To read:  
S1i0k1+3  
S = Soldier the type of pawn  
1 = player index  
i0 = pawn index is 0  
k1 = attack point of pawn is 1  
+3 = health point of pawn is 3  

#### Mana Status of Each Players

`Mana (White, Black) = (5, 5)`<br>
#### Rune
`Rune List:
{}`

## How to use the GUI:
![alt text](GUI.PNG "Logo Title Text 1")

Use this command on your terminal
`python main_gui.py`

## Command list on CLI:
|Command| Description|
|-------|------------|
|exit|exit the game|
|ACTION_KEY|input the action. The ACTION_KEY is stated in the list of action provided in the command line.|
## Progress
- [x] Add basic elements to be input of AI Algorithm
- [ ] Documenting (almost all of them)
- [ ] Fix the mess of the code (need more class and remove unnecessary code)
- [x] Create the GUI
- [x] Use classic AI Algorithm
- [ ] Experimenting Value-based Reinforcement Learning
- [ ] Experimenting Policy-based Reinforcement Learning
- [ ] Experimenting Value and Policy based Reinforcement Learning

## FAQ
Q : Can I Contribute? <br>
A : Of course, just tell me what you want to contribute. <br>

Q : Can I Contact you? <br>
A : email me in haryomaenan@gmail.com if you want to contact me. Especially about this project.
