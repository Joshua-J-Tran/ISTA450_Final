import tkinter as tk
from GameState import *
from map_constructor import *
from SearchAgent import *
from ReflexAgent import *
from Alpha_beta_agent import *
from food import *
import sys 
import argparse


class SnakeGameGUI:
    def __init__(self, game_state,speed=1, food_agent_type=None):
        self.game_state = game_state
        self.cell_size = 20
        self.speed = speed 
        self.food_agent_type = food_agent_type
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.canvas = tk.Canvas(self.window, width=self.game_state.width * self.cell_size,
                                height=self.game_state.height * self.cell_size)
    
        self.canvas.pack()
        self.window.bind("<Key>", self.on_key_press)
        self.window.bind("<Escape>", self.close_window)
        self.nodes_explored_label = tk.Label(self.window, text="Nodes Explored: 0", font=("Arial", 14))
        self.nodes_explored_label.pack(side="left")
        self.score_label = tk.Label(self.window, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(side="right")
        self._draw_grid()

    def close_window(self, event=None):
        self.window.destroy()

    def _draw_grid(self):
        for x in range(self.game_state.width):
            self.canvas.create_line(x * self.cell_size, 0, x * self.cell_size, self.game_state.height * self.cell_size, fill="gray")
        for y in range(self.game_state.height):
            self.canvas.create_line(0, y * self.cell_size, self.game_state.width * self.cell_size, y * self.cell_size, fill="gray")


    def update_score(self):
        self.score_label.config(text=f"Score: {self.game_state.score}")
        self.window.update_idletasks()


    def draw(self):
        self.canvas.delete(tk.ALL)  
        self._draw_grid()

        for x, y in self.game_state.walls:
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                        fill="black")
        
        for x, y in self.game_state.snake:
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                        fill="green", outline="")

        for food in self.game_state.food_items:
            fx, fy = food.get_position()
            self.canvas.create_oval(fx * self.cell_size, fy * self.cell_size,
                                    (fx + 1) * self.cell_size, (fy + 1) * self.cell_size,
                                    fill="red", outline="")
        self.window.update()


    def on_key_press(self, event):
        key = event.keysym
        if key == "Up":
            self.game_state.change_direction('UP')
        elif key == "Down":
            self.game_state.change_direction('DOWN')
        elif key == "Left":
            self.game_state.change_direction('LEFT')
        elif key == "Right":
            self.game_state.change_direction('RIGHT')

    def run(self):
        update_interval = int(100 / self.speed) 
        
        while not self.game_state.is_game_over():
            self.game_state.update()
            self.draw()
            self.window.after(update_interval) 


    def run_with_path(self, agent):
        path = []  
        update_interval = int(100 / self.speed)
        while not self.game_state.is_game_over():
            if not path:
                path = agent.getPath(self.game_state)
                print("Generated Path:", path)
            if path:
                action = path.pop(0)
                self.game_state.change_direction(action)

            self.game_state.update()
            self.draw()
            self.displayNodesExplored(agent.getNodesExplored())
            self.update_score()
            self.window.after(update_interval)


    
    def run_with_step(self, agent):
        update_interval = int(100 / self.speed)
        while not self.game_state.is_game_over():
            action = agent.getAction(self.game_state)
            #print("Agent Action:", action)
            if action:
                self.game_state.change_direction(action)
            self.game_state.update()
            self.draw()
            self.displayNodesExplored(agent.getNodesExplored())
            self.update_score()
            self.window.after(update_interval)

    def run_no_graphic(self, agent):
        while not self.game_state.is_game_over():
            action = agent.getAction(self.game_state)
            if action:
                self.game_state.change_direction(action)
            self.game_state.update()
        print("Final Score:", self.game_state.score)

    def displayNodesExplored(self, nodes_explored):
        self.nodes_explored_label.config(text=f"Nodes Explored: {nodes_explored}")
        self.window.update_idletasks()




def main():
    parser = argparse.ArgumentParser(description="Snake Game")
    parser.add_argument('-m', '--map', help='Custom map file', required=False)
    parser.add_argument('-ht', '--height', type=int, help='Height of the grid', default=60)
    parser.add_argument('-wd', '--width', type=int, help='Width of the grid', default=60)
    parser.add_argument('-s', '--speed', type=float, default=1.0, help='Speed of the snake')
    parser.add_argument('-p', '--agent', help='Specify the agent type', required=False)
    parser.add_argument('-a', '--algorithm', help='Algorithm used by the agent', required=False)
    parser.add_argument('-f', '--food_agent', help='Specify the food agent type', required=False)
    parser.add_argument('-fs', '--food_speed',type=float, default=3.0, help='Speed cost of food, larger mean slower', required=False)
    parser.add_argument('-g', '--graphic', help='Graphic', required=False)

    args = parser.parse_args()

    print(f"Map: {args.map}, Height: {args.height}, Width: {args.width}, Speed: {args.speed}, Agent: {args.agent}, Algorithm: {args.algorithm}")
    custom_map = read_map_from_file(args.map) if args.map else None
    game_state = SnakeGameState(custom_map=custom_map, width=args.width, height=args.height,food_algorithm=args.food_agent,food_speed = args.food_speed)
    gui = SnakeGameGUI(game_state, speed=args.speed)


    if args.agent:
        if args.agent == 'search':
            if args.algorithm == 'dfs':
                agent = SearchAgent(searchFunction=depthFirstSearch)
            elif args.algorithm == 'bfs':
                agent = SearchAgent(searchFunction=breadthFirstSearch)
            elif args.algorithm == 'A*':
                agent = SearchAgent(searchFunction=aStarSearch)
            elif args.algorithm == 'H':
                agent = SearchAgent(searchFunction=heuristicSearch)
            else:
                raise ValueError("Unknown algorithm")
            if not args.graphic:
                gui.run_with_path(agent)

        
        elif args.agent == 'reflex':
            if args.algorithm == 'dfs':
                agent = ReflexAgent(searchFunction=depthFirstSearch)
            elif args.algorithm == 'bfs':
                agent = ReflexAgent(searchFunction=breadthFirstSearch)
            elif args.algorithm == 'A*':
                agent = ReflexAgent(searchFunction=aStarSearch)
            elif args.algorithm == 'H':
                agent = ReflexAgent(searchFunction=heuristicSearch)
            else:
                raise ValueError("Unknown algorithm")
            gui.run_with_step(agent)
        
        elif args.agent == 'AB':
            agent = AlphaBetaAgent(depth = 9,evaluationFunction= game_state.evaluationFunction)
            if not args.graphic:
                gui.run_with_step(agent)
            gui.run_no_graphic( agent)

        else:
            raise ValueError("must be 'search' or 'reflex'")



    else:
        gui.run()
    gui.window.mainloop()



if __name__ == "__main__":
    main()