# .get_memory()

A game made with [Pygame](https://www.pygame.org) and [Qiskit](https://qiskit.org/).

## How to run

You'll need Python3 to run this game.

First download the source and then cd into the folder using a terminal. To install the dependencies, use the command

```python3 -m pip install -r requirements.txt ```

To play the game, use the command

```python3 rungame.py```

The game is played using two windows: the terminal window for text and the pygame window for visuals.

## How to play

You move by pressing *q*, *w*, *a* and *d*. You can also teleport with the space bar. The rest is for you to figure out.

## Why does this game exist?

There are three reasons that this game exists, and which led to it being what it is.

1. It was built during the [Ludum Dare 44 game jam](https://ldjam.com/events/ludum-dare/44), which had the theme "Your life is currency".

2. It was made as an example of using terrain generated by a quantum programs, by the method described in [this blog post](https://medium.com/qiskit/creating-infinite-worlds-with-quantum-computing-5e998e6d21c2).

3. It was made to explore the kinds of labyrinths generated by the classic one-line Commodore 64 program

   ```10 PRINT CHR$(205.5+RND(1)); : GOTO 10```
   
   This was ported into the following quantum program, which is the basis for the labyrinths in the game
   
   ```from qiskit import *; ''.join( [ '╱'*(b=='0') + '╲'*(b=='1') for b in execute(QuantumCircuit().from_qasm_str('include "qelib1.inc";qreg q[1];creg c[1];h q[0];measure q -> c;'),Aer.get_backend('qasm_simulator'),shots=1024,memory=True).result().get_memory()])```
   
   The original program is referred to simply as ```10 PRINT``` in [this book](https://10print.org/) about it, after the first part of the program. I instead name my program, and this game based upon it, using the part near the end: ```.get_memory()```.
   
## Things you might also like

* Scientifically accurate animations of teleportation (for bitmaps), made using Qiskit. See [here](https://github.com/quantumjim/quantograph/blob/master/example.md). These didn't quite make it into the game.
* [The history of games for quantum computers](https://medium.com/@decodoku/the-history-of-games-for-quantum-computers-a1de98859b5a)
