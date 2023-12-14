from GameState import *
import random
from util import *
class Food:
    def __init__(self, game_state, algorithm=None, initial_position=None, speed=1):
        self.game_state = game_state
        self.speed = speed
        self.counter = 0
        if algorithm == "random":
            self.algorithm = random_movement
        elif algorithm == "away":
            self.algorithm = self.away_movement
        else:
            self.algorithm = algorithm

        if initial_position is not None:
            self.position = initial_position
        else:
            self.position = self.game_state.find_valid_food_position()

    def get_position(self):
        return self.position

    def move(self):
        self.counter += 1
        if self.counter >= int(self.speed):
            valid_positions = self.game_state.getLegalActions("Food")
            if self.algorithm:

                action = self.algorithm(self.game_state, self.position, valid_positions)
                self.update_position_based_on_action(action)
            self.counter = 0
    
    def deepcopy(self):
        copied_food = Food(self.game_state, self.algorithm, self.position, self.speed)
        copied_food.counter = self.counter  
        return copied_food

    def away_movement(self, game_state, current_position, valid_directions):
        snake_head = game_state.snake[0]
        farthest_direction = None
        max_distance = -1

        for direction in valid_directions:
            new_position = game_state.get_new_position(current_position, direction)
            distance = manhattanDistance(new_position, snake_head)
            if distance > max_distance:
                max_distance = distance
                farthest_direction = direction

        return farthest_direction

    def update_position_based_on_action(self, action):
        if action == "STAY":
            pass
        elif action in ["UP", "DOWN", "LEFT", "RIGHT"]:
            new_position = self.game_state.get_new_position(self.position, action)
            if self.game_state.is_valid_position(new_position):
                self.position = new_position

def random_movement(game_state, current_position, valid_positions):
    return random.choice(valid_positions) if valid_positions else current_position