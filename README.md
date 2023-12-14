# ISTA450_Final


1. Map Selection (-m or --map):
Specifies a custom map file to be used for the game.
Map can be created with 0 as empty area, X as agent, Y as Foof, H as Walls

Example: -m mapfile.txt

2. Grid Height (-ht or --height):
Sets the height of the grid for the game.

Example: -ht 30

3. Grid Width (-wd or --width):
Sets the width of the grid for the game.

Example: -wd 30

4. Game Speed (-s or --speed):
Adjusts the speed of the game.

Example: -s 1.5 (1.5 times the normal speed)

5. Agent Selection (-p or --agent):
Chooses the type of AI agent for the snake.
+Search Agent (search): generate a path and follow it until the next piece of food
+Reflex Agent (reflex): Generate a path every step
+AB agent (AB): Utilize Alpha Beta Pruning and look ahead to make the best choice

Example: -p search

6. Algorithm Choice (-a or --algorithm):
Selects the algorithm used by the AI agent.
Options include: dfs (Depth-First Search), bfs (Breadth-First Search), A* (A-Star Search), H (Heuristic Search), rightTurn (Agent that turns right every few moves)

Example: -a dfs

7. Food Agent (-f or --food_agent):
Specifies the AI agent for the food .
away: Move a distance farthest away from the snake
random: Move randomly

Example: -f away

8. Food Speed (-fs or --food_speed):
Specified the cost of action for the food to move
with 2 the agent move once every 2 step

Example: -fs 2

9. Graphic (-g or --graphic):
If included will disable graphic
The game will output score on the terminal.

Example: -g anything

