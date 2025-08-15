import gymnasium as gym
from gymnasium import spaces
import numpy as np
from .cube import RubiksCube

class RubiksCubeEnv(gym.Env):
    def __init__(self, size=3, scramble_moves=10):
        super().__init__()
        self.size = size
        self.cube = RubiksCube(size=self.size)
        self.scramble_moves = scramble_moves
        self.faces = self.cube.faces  # ['U', 'D', 'L', 'R', 'F', 'B']
        self.n_actions = len(self.faces) * 2  # each face: clockwise + counterclockwise

        # Action space: 0–11 (0=U CW, 1=U CCW, 2=D CW, ..., 11=B CCW)
        self.action_space = spaces.Discrete(self.n_actions)

        # Observation: 6 × size² array, each entry is an int from 0–5
        self.observation_space = spaces.Box(
            low=0,
            high=5,
            shape=(6 * self.size * self.size,),
            dtype=np.int32
        )

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.cube = RubiksCube(self.size)
        
        # Use scramble_moves from options if provided, otherwise use default
        scramble_moves = self.scramble_moves
        if options and 'scramble_moves' in options:
            scramble_moves = options['scramble_moves']

        self.cube.scramble(moves=scramble_moves, rng=self.np_random)
        return self._get_obs(), {}  # second return is the info dict

    def step(self, action):
        face_idx = action // 2
        clockwise = action % 2 == 0
        face = self.faces[face_idx]
        self.cube.rotate_face(face, clockwise)

        obs = self._get_obs()
        terminated = self._is_solved()
        truncated = False  # or define a max_step limit and use it
        reward = 1.0 if terminated else 0.0
        info = {}

        return obs, reward, terminated, truncated, info

    def render(self):
        print(self.cube.state)

    def _get_obs(self):
        return self.cube.state

    def _is_solved(self):
        return self.cube.is_solved()
    
    def close(self):
        pass
