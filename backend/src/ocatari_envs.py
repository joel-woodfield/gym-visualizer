import collections

import gymnasium as gym
from gymnasium.envs.registration import register
import numpy as np
from ocatari.core import OCAtari


def get_position_obs(objects: list) -> np.ndarray:
    pos = []
    for obj in objects:
        pos.append(obj.x)
        pos.append(obj.y)
    return np.array(pos)


def get_relative_obs(objects: list, entity_name: str) -> np.ndarray:
    for obj in objects:
        if obj.category == entity_name:
            x1 = obj.x
            y1 = obj.y
            break

    rel_pos = [x1, y1]
    for obj in objects:
        if obj.category != entity_name:
            x2 = obj.x
            y2 = obj.y
            rel_pos.append(x2 - x1)
            rel_pos.append(y2 - y1)

    return np.array(rel_pos)


def get_relative_obs_indicator(objects: list, entity_name: str) -> np.ndarray:
    for obj in objects:
        if obj.category == entity_name:
            x1 = obj.x
            y1 = obj.y
            break

    rel_pos = [x1, y1, 255]
    for obj in objects:
        if obj.category != entity_name:
            x2 = obj.x
            y2 = obj.y
            rel_pos.append(x2 - x1)
            rel_pos.append(y2 - y1)

            indicator = int(obj.__class__.__name__ != "NoObject") * 255
            rel_pos.append(indicator)

    return np.array(rel_pos)


def get_relative_obs_indicator_sign(objects: list, entity_name: str) -> np.ndarray:
    rel_pos = get_relative_obs_indicator(objects, entity_name)
    return np.sign(rel_pos) * 255


class RelationalEnv(OCAtari):
    metadata = {
        "render_modes": ["rgb_array"],
        "render_fps": 30,
    }

    def __init__(
        self, 
        env_id: str, 
        type: str, 
        frame_stack: int = 1, 
        velocity: bool = False, 
        render_mode: str | None = None,
        **kwargs,
    ):
        print(f"Render mode: {render_mode}")
        print(kwargs)
        super().__init__(env_id, render_mode=render_mode, **kwargs)

        self.type = type
        self.velocity = velocity
        if self.velocity and frame_stack == 1:
            raise ValueError("frame_stack must be > 1 if velocity is True")

        buffer_size = 2 if velocity else frame_stack
        self._obs_buffer = collections.deque(maxlen=buffer_size)

        assert self.observation_space.shape[1] % 2 == 0, "Observation space must be even"
        num_objects = self.observation_space.shape[1] // 2
        if self.type == "position" or self.type == "relative":
            obs_dim = num_objects * 2
        elif self.type == "relative_indicator" or self.type == "relative_indicator_sign":
            obs_dim = num_objects * 3

        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(buffer_size * obs_dim,),
        )
    
    def update_obs_buffer(self):
        obs = self._get_current_obs()
        self._obs_buffer.append(obs)
        
    def _get_current_obs(self):
        if self.type == "position":
            return get_position_obs(self.objects)
        elif self.type == "relative":
            return get_relative_obs(self.objects, "Player")
        elif self.type == "relative_indicator":
            return get_relative_obs_indicator(self.objects, "Player")
        elif self.type == "relative_indicator_sign":
            return get_relative_obs_indicator_sign(self.objects, "Player")
        else:
            raise ValueError(f"Unknown observation type: {self.type}")

    def _get_obs(self):
        if self.velocity:
            if len(self._obs_buffer) < 2:
                raise ValueError("Not enough frames in buffer to compute velocity")
            vel = self._obs_buffer[-1] - self._obs_buffer[-2]
            return np.concatenate((self._obs_buffer[-1], vel), axis=0).ravel()
        else:
            return np.array(self._obs_buffer).ravel()

    def reset(self, **kwargs):
        _, info = super().reset(seed=np.random.randint(0, 1e6))
        self._obs_buffer.clear()
        for _ in range(self._obs_buffer.maxlen):
            self.update_obs_buffer()
        return self._get_obs(), info

    def step(self, action):
        _, reward, terminated, truncated, info = super().step(action)
        self.update_obs_buffer()
        obs = self._get_obs()
        return obs, reward, terminated, truncated, info

    @property
    def ale(self):
        return self._ale


register(
    id="ocatari/AirRaid",
    entry_point="ocatari_envs:RelationalEnv",
    kwargs={"env_id": "AirRaidNoFrameskip-v4", "type": "relative_indicator"},
)


register(
    id="ocatari/Amidar",
    entry_point="ocatari_envs:RelationalEnv",
    kwargs={"env_id": "AmidarNoFrameskip-v4", "type": "relative_indicator"},
)


register(
    id="ocatari/Asterix",
    entry_point="ocatari_envs:RelationalEnv",
    kwargs={"env_id": "AsterixNoFrameskip-v4", "type": "relative_indicator"},
)


register(
    id="ocatari/Bowling",
    entry_point="ocatari_envs:RelationalEnv",
    kwargs={"env_id": "BowlingNoFrameskip-v4", "type": "relative_indicator"},
)


register(
    id="ocatari/Boxing",
    entry_point="ocatari_envs:RelationalEnv",
    kwargs={"env_id": "BoxingNoFrameskip-v4", "type": "relative_indicator"},
)


def test():
    env = RelationalEnv("AssaultNoFrameskip-v4", "relative_indicator", frame_stack=1)
    obs, info = env.reset()
    for i in range(1000):
        obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
        if i % 100 == 0:
            print(obs)
        if terminated or truncated:
            obs, info = env.reset()


if __name__ == "__main__":
    test()