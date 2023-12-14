import random
from map_constructor import *
from food import *
import util
from search import *


class SnakeGameState:
    def __init__(self, width=60, height=60, custom_map=None, food_algorithm=None,food_speed=1):
        self.food_algorithm = food_algorithm
        self.food_speed = food_speed
        if custom_map is not None:
            self._initialize_from_map(custom_map)
        else:
            self.width = width
            self.height = height
            self.snake = [(width // 2, height // 2)]
            self.walls = set()
            self.food_items = []  
            self.add_food_item() 
        self.direction = None
        self.score = 0
        self.game_over = False
        self.counter = 0
        

    def add_food_item(self,position=None):
        
        new_food = Food(self, algorithm=self.food_algorithm, initial_position = position, speed = self.food_speed)
        self.food_items.append(new_food)

    def _initialize_from_map(self, custom_map):
        self.height = len(custom_map)
        self.width = len(custom_map[0])
        self.snake = []
        self.food_items = []
        self.walls = set()

        food_position = None

        for y, row in enumerate(custom_map):
            for x, cell in enumerate(row):
                if cell == 'X':
                    self.snake.append((x, y))
                elif cell == 'Y':
                    food_position = (x, y)
                elif cell == 'H':
                    self.walls.add((x, y))

        if not self.snake:
            raise ValueError("Must have a starting point for the snake marked with 'X'")
        self.add_food_item(position=food_position)

    def update(self):
        if self.game_over or self.direction is None:
            return
        head_x, head_y = self.snake[0]
        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1

        new_head = (head_x, head_y)
        self.game_over = self._check_collision(new_head)
        self.snake.insert(0, new_head)  
        food_eaten = False
        for food in self.food_items:
            if new_head == food.get_position():
                self.score += 100
                self.food_items.pop()
                self.add_food_item()  
                food_eaten = True
                break 

        if not food_eaten:
            self.snake.pop()
        for food in self.food_items:
            food.move()
        self.score -= 1


    def _check_collision(self, head):
        x, y = head
        if head in self.walls:
            return True
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        if head in self.snake[1:]:
            return True
        return False


    def change_direction(self, direction):
        if (direction == 'UP' and not self.direction == 'DOWN') or \
           (direction == 'DOWN' and not self.direction == 'UP') or \
           (direction == 'LEFT' and not self.direction == 'RIGHT') or \
           (direction == 'RIGHT' and not self.direction == 'LEFT'):
            self.direction = direction

    def is_game_over(self):
        return self.game_over


    def generateSuccessor(self, agent, action):
        new_state = self.deepcopy()
        if agent == "Snake":
            head_x, head_y = new_state.snake[0]
            direction_moves = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

            dx, dy = direction_moves[action]
            new_head = (head_x + dx, head_y + dy)
            x,y = new_head
            if new_head not in [food.get_position() for food in new_state.food_items]:
                new_state.snake.pop() 
            else:
                new_state.score+=100
                new_state.food_items.pop()
            if new_head in new_state.walls or new_head in new_state.snake[1:]:
                new_state.game_over=True
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                new_state.game_over = True
            new_state.snake.insert(0, new_head)  
            new_state.direction = action
            new_state.score -=5
        

        elif agent == "Food":
            for food in new_state.food_items:
                food.update_position_based_on_action(action)

        return new_state

    

    def evaluationFunction(self, currentGameState):
        score = currentGameState.score
        head = currentGameState.snake[0]
        tail = currentGameState.snake[-1]
        if currentGameState.is_game_over():
            return score + float("-inf")
        if currentGameState.food_items:
            currentGameState.counter=0
        if not currentGameState.food_items:
            currentGameState.counter+=1
            survival_reward = 5 
            score += survival_reward * currentGameState.counter
        return score 


    
    
    def deepcopy(self):
        new_state = SnakeGameState(self.width, self.height)
        new_state.snake = [segment for segment in self.snake]
        new_state.food_items = [food.deepcopy() for food in self.food_items] 
        new_state.direction = self.direction
        new_state.score = self.score
        new_state.game_over = self.game_over
        new_state.walls = set(self.walls)
        new_state.counter = self.counter
        return new_state


    def getLegalActions(self, agent):
        if agent == "Snake":
            directions = ["UP", "DOWN", "LEFT", "RIGHT"]
            opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
            if self.direction:
                directions.remove(opposite[self.direction])
            
            return directions

        elif agent == "Food":
            if not self.food_items:
                return []
            if self.food_items[0].counter < int(self.food_items[0].speed):
                return ["STAY"]
            directions = ["UP", "DOWN", "LEFT", "RIGHT"]
            legal_directions = ["STAY"]
            for direction in directions:
                new_position = self.get_new_position(self.food_items[0].get_position(), direction)
                if self.is_valid_position(new_position):
                    legal_directions.append(direction)
            return legal_directions

    def is_valid_position(self, position):
        x, y = position
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if position in self.walls:
            return False
        if position in self.snake:
            return False
        return True

    def get_new_position(self, current_position, action):
        direction_moves = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0), "STAY": (0, 0)}
        dx, dy = direction_moves[action]
        new_x, new_y = current_position[0] + dx, current_position[1] + dy
        return new_x, new_y


    def find_valid_food_position(self):
        while True:
            potential_location = (random.randint(0, self.width - 1),
                                  random.randint(0, self.height - 1))
            if self.is_valid_position(potential_location):
                return potential_location
            

def space_access(currentGameState):
    width, height = currentGameState.width, currentGameState.height
    snake = currentGameState.snake
    snake_body = set(snake[1:]) 
    grid = [[0 for _ in range(width)] for _ in range(height)]
    for x, y in snake_body:
        grid[y][x] = 1 
    accessible_area = flood_fill(grid, snake[0][0], snake[0][1])
    accessibility_score = accessible_area - len(snake)  

    return accessibility_score

def flood_fill(grid, x, y):
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid) or grid[y][x] != 0:
        return 0
    grid[y][x] = -1  
    return 1 + flood_fill(grid, x + 1, y) + flood_fill(grid, x - 1, y) + flood_fill(grid, x, y + 1) + flood_fill(grid, x, y - 1)



