import base64
from io import BytesIO
from typing import Any, SupportsFloat, cast

import gymnasium as gym
import numpy as np
from PIL import Image

import ocatari_envs  # register the OCatari environments
from observation_formatting import format_obs


DEFAULT_POLICY = """import numpy as np
def policy(obs: np.ndarray, num_actions: int) -> int:
    action = np.random.randint(0, num_actions)
    return action"""


class PolicyError(Exception):
    pass


class EnvironmentError(Exception):
    pass


class UserPolicy:
    def __init__(self, code: str) -> None:
        self.set_code(code)
    
    def act(self, obs: np.ndarray, num_actions: int) -> int:
        return self._name_space["policy"](obs, num_actions)

    def set_code(self, code: str) -> None:
        self._name_space = {}
        exec(code, self._name_space)


class GymnasiumEnv:
    def __init__(self, env_id: str = "CartPole-v1") -> None:
        self.init_env(env_id)
        self.policy = UserPolicy(DEFAULT_POLICY)

    def set_policy(self, policy: str) -> None:
        self.policy.set_code(policy)

    def init_env(self, env_id: str) -> None:
        try:
            self._env = gym.make(env_id, render_mode="rgb_array")
        except Exception as e:
            raise EnvironmentError(f"Error initializing environment with id '{env_id}': {e}")

        self._current_step = 0
        self._episode_return = 0.
        self.has_reset = False
        self._prev_obs = None

    def reset(self) -> tuple[list[float], dict[str, Any]]:
        try:
            observation, info = self._env.reset()
            self._prev_obs = observation
            observation = format_obs(self._env.spec.id, observation)

        except Exception as e:
            raise EnvironmentError(f"Error resetting environment: {e}")

        self._current_step = 0
        self._episode_return = 0.
        info["episode_return"] = self._episode_return
        info["current_step"] = self._current_step
        self.has_reset = True
        return observation, info

    def step(self) -> tuple[list[float], SupportsFloat, bool, bool, dict[str, Any]]:
        if self._prev_obs is None:
            try:
                action = self._env.action_space.sample()
            except Exception as e:
                raise EnvironmentError(f"Error sampling action from environment: {e}")
        else:
            try:
                action = self.policy.act(self._prev_obs, self._env.action_space.n)
            except Exception as e:
                raise PolicyError(f"Error in user-defined policy: {e}")

        try:
            observation, reward, terminated, truncated, info = self._env.step(action)
            self._prev_obs = observation
            observation = format_obs(self._env.spec.id, observation)

        except Exception as e:
            raise EnvironmentError(f"Error stepping environment: {e}")

        self._current_step += 1
        self._episode_return += cast(float, reward)
        info["episode_return"] = self._episode_return
        info["current_step"] = self._current_step
        info["action"] = int(action)

        return observation, reward, terminated, truncated, info

    def render(self) -> str:
        try:
            frame = cast(np.ndarray, self._env.render())
        except Exception as e:
            raise EnvironmentError(f"Error rendering environment: {e}")

        frame = Image.fromarray(frame)
        buf = BytesIO()
        frame.save(buf, format="PNG")
        frame = base64.b64encode(buf.getvalue()).decode("utf-8")
        return frame