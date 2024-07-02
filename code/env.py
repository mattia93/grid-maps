import numpy as np
import itertools

class navigation_env():
    def __init__(self, grid_size):
        # Initialize layout with grid size and default positions
        layout_dict = {
            'block': np.zeros([grid_size, grid_size]),
            'start_pos': [0, 0],
            'goal_pos': [0, 0], 
        }
        self.grid_size = grid_size

    # Load a layout from the sequence
    def load_layout(self, seq):
        block_binary, start_pos, goal_pos = seq
        self.start_pos = tuple([int(i) for i in start_pos])
        self.cur_pos = tuple([int(i) for i in start_pos])
        self.goal_pos = tuple([int(i) for i in goal_pos])
        self.blocks = np.array(block_binary, dtype=int)
        self.grid_size = self.blocks.shape[0]

    # Reset the game to the starting position
    def reset_game(self):
        self.cur_pos = tuple([int(i) for i in self.start_pos])

    # # Navigate the environment based on a series of actions
    # def navigate(self, action: [int]):
    #     done = False
    #     if self.cur_pos == self.goal_pos:
    #         done = True
    #         return done
    #     for a in action:
    #         valids = filter_pos(self.cur_pos, self.blocks, self.grid_size)
    #         if valids[a]:
    #             self.cur_pos = move_action(self.cur_pos, human_actions[a])
    #             if self.cur_pos == self.goal_pos:
    #                 done = True
    #                 break
    #     return done