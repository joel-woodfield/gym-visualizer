import asyncio
import json
from typing import Any

from websockets.asyncio.server import serve, ServerConnection

from gymnasium_env import GymnasiumEnv


class GymController:
    def __init__(self) -> None:
        self._env = GymnasiumEnv()

    def step(self) -> dict[str, Any]:
        if not self._env.has_reset:
            return self.reset()

        observation, reward, terminated, truncated, info = self._env.step()
        frame = self._env.render()

        return {
            "stepIdx": info["current_step"],
            "frame": frame,
            "observation": observation,
            "reward": reward,
            "done": terminated or truncated,
            "episodeReturn": info["episode_return"],
        }
        
    def reset(self) -> dict[str, Any]:
        obs, info = self._env.reset()
        frame = self._env.render()
        return {
            "stepIdx": info["current_step"],
            "frame": frame,
            "observation": obs,
            "reward": 0,
            "done": False,
            "episodeReturn": info["episode_return"],
        }

    def handle_message(self, message: dict[str, Any]) -> dict[str, Any]:
        msg_type = message.get("type")
        if msg_type == "step":
            data = self.step()
            return {"type": "step", "data": data}
        elif msg_type == "reset":
            data = self.reset()
            return {"type": "reset", "data": data}
        else:
            return {"error": "Unknown message type"}


async def handler(websocket: ServerConnection) -> None:
    controller = GymController()

    while True:
        message = await websocket.recv()
        data = json.loads(message)

        response_data = controller.handle_message(data)
        response = json.dumps(response_data)

        await websocket.send(response)


async def main() -> None:
    async with serve(handler, "", 8765) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
