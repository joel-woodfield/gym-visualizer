import base64
from io import BytesIO
from typing import Any, SupportsFloat, cast

import gymnasium as gym
import minigrid
import minigrid.wrappers
import numpy as np
from PIL import Image

import ocatari_envs  # register the OCatari environments
from observation_formatting import format_obs


DEFAULT_POLICY = """import numpy as np
def policy(obs: np.ndarray, num_actions: int) -> int:
    action = np.random.randint(0, num_actions)
    return action"""


class FlatCurrentReducedWrapper(gym.ObservationWrapper):
    """
    Encode mission strings using a one-hot scheme,
    and combine these with observed images into one flat array.

    This wrapper is not applicable to BabyAI environments, given that these have their own language component.

    Example:
        >>> import gymnasium as gym
        >>> import matplotlib.pyplot as plt
        >>> from minigrid.wrappers import FlatObsWrapper
        >>> env = gym.make("MiniGrid-LavaCrossingS11N5-v0")
        >>> env_obs = FlatObsWrapper(env)
        >>> obs, _ = env_obs.reset()
        >>> obs.shape
        (2835,)
    """

    def __init__(self, env, maxStrLen=96):
        super().__init__(env)

        imgSpace = env.observation_space.spaces["image"]
        
        self.select_indices = [0,1,2,8,9]
        # Define a mapping from environment names to select indices
        env_select_indices = {
            "DistShift": [0, 1, 2, 8, 9], # left, right, forward
            "LavaGap": [0, 1, 2, 8, 9], # left, right, forward
            "LavaCrossing": [0, 1, 2, 8, 9], # left, right, forward
            
            "SimpleCrossing": [0, 1, 2, 8], # left, right, forward
            "FourRooms": [0, 1, 2, 8], # left, right, forward
            "Empty": [0, 1, 2, 8], # left, right, forward
            
            "MultiRoom": [0, 1, 2, 4, 8, 17, 18], # left, right, forward, toggle

            "Dynamic-Obstacles": [0, 1, 2, 4, 6, 8], # left, right, forward

            "Unlock": [0, 1, 2, 4, 5, 8, 17, 18, 19], # left, right, forward, toggle #No pickup key
            "UnlockPickup": [0, 1, 2, 4, 5, 7, 8, 17, 18, 19], # left, right, forward, pickup, toggle #No pickup key

            "DoorKey": [0, 1, 2, 4, 5, 8, 17, 18, 19], # left, right, forward, pickup, toggle #Pickup key

            "GoToDoor": [0, 1, 2, 4, 8, 11, 12, 13, 14, 15, 16], # left, right, forward, done

            "RedBlueDoors": [0, 1, 2, 4, 8, 11, 13, 17, 18], # left, right, forward, toggle
            "PutNear": [0, 1, 2, 4, 8, 17, 18], # left, right, forward, pickup, drop 
        }

        # Get the environment name
        env_name = env.spec.id
        
        env_identifier = env_name
        for key in env_select_indices.keys():
            if key in env_name:
                env_identifier = key     

        # Set select_indices based on the environment name
        if env_identifier in env_select_indices:
            self.select_indices = env_select_indices[env_identifier]
            print(f"Environment {env_identifier} with Observations {self.select_indices}")
        else:
            raise ValueError(f"Environment {env_identifier} is not supported by this wrapper.")

        
        imgSize = imgSpace.shape[0] * imgSpace.shape[1] * len(self.select_indices) #reduce(operator.mul, imgSpace.shape, 1)

        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(imgSize,),
            dtype="float32",
        )

        self.cachedStr: str = None

    def observation(self, obs):
        image = obs["image"]
        mission = obs["mission"]
        #print('image.shape', image.shape)
        #print('image.flatten().shape', image.flatten().shape)
        obs = image[:,:,self.select_indices].flatten().astype(np.float32)
        obs = obs * 2 - 1 # convert to range -1,1 instead of 0,1

        #obs =
        # print('obs.shape', obs.shape)
        return obs


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

        if env_id.startswith("MiniGrid"):
            self._env = minigrid.wrappers.ViewSizeWrapper(self._env, agent_view_size=3)
            self._env = minigrid.wrappers.OneHotPartialObsWrapper(self._env)
            self._env = FlatCurrentReducedWrapper(self._env)

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