def read_map_from_file(file_path):
    with open(file_path, 'r') as file:
        custom_map = [line.rstrip('\n') for line in file.readlines()]
    
    max_width, height = find_bounds(custom_map)
    return pad_map(custom_map, max_width, height)


def find_bounds(custom_map):
    max_width = max(len(row) for row in custom_map)
    height = len(custom_map)
    return max_width, height


def pad_map(custom_map, max_width, height):
    padded_map = []
    max_width += 2
    height += 2
    padded_map.append('H' * max_width)

    for row in custom_map:
        row_padded = 'H' + row + 'H'
        row_padded = row_padded[:max_width].replace(' ', 'H')
        padded_map.append(row_padded)

    padded_map.append('H' * max_width)

    return padded_map


def run(self, speed=1.0):
        while not self.game_state.is_game_over():
            self.game_state.update()
            self.draw()
            self.window.after(int(100 / speed)) 
        self.window.mainloop()