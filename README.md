# COMP472_A2

https://github.com/domhart98/COMP472_A2

This program initializes a board or state. I did not have time to create the random state generator, so the initial state must be entered manually.

Firstly, the user selects which algorithm and which heuristic will be used to solve the puzzle.

The script will generate child nodes from the initial node, then add them to a PriorityQueue. The priority value depends on the algorithm.

The next node to be searched will be gotten from the front of the Priority Queue and the process repeats.

Eventually, a solution must be reached. The results are written to corresponding output files.
