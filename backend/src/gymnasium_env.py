import base64
from io import BytesIO
from typing import Any, SupportsFloat, cast

import gymnasium as gym
import numpy as np
from PIL import Image

class GymnasiumEnv:
    def __init__(self):
        self._env = gym.make("CartPole-v1", render_mode="rgb_array")
        self._current_step = 0
        self._episode_return = 0.

        self.has_reset = False

    def reset(self) -> tuple[list[float], dict[str, Any]]:
        observation, info = self._env.reset()
        observation = observation.tolist()

        self._current_step = 0
        self._episode_return = 0.
        info["episode_return"] = self._episode_return
        info["current_step"] = self._current_step
        self.has_reset = True
        return observation, info

    def step(self) -> tuple[list[float], SupportsFloat, bool, bool, dict[str, Any]]:
        action = self._env.action_space.sample()

        observation, reward, terminated, truncated, info = self._env.step(action)
        observation = observation.tolist()

        self._current_step += 1
        self._episode_return += cast(float, reward)
        info["episode_return"] = self._episode_return
        info["current_step"] = self._current_step
        return observation, reward, terminated, truncated, info

    def render(self) -> str:
        frame = cast(np.ndarray, self._env.render())
        frame = Image.fromarray(frame)
        buf = BytesIO()
        frame.save(buf, format="PNG")
        frame = base64.b64encode(buf.getvalue()).decode("utf-8")
        return frame