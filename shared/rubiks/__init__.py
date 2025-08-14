

from gymnasium.envs.registration import register

register(
    id="RubiksCube-v0",
    entry_point="rubiks.env:RubiksCubeEnv",
    max_episode_steps=500,
)
