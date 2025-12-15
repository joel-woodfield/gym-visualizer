import asyncio
import json
from typing import Any

from websockets.asyncio.server import serve, ServerConnection

from gymnasium_env import GymnasiumEnv, EnvironmentError, PolicyError


class GymController:
    def __init__(self, send: callable) -> None:
        self._env = GymnasiumEnv()

        self._send = send
        self._playing = False
        self._play_task: asyncio.Task[None] | None = None

    async def _emit_state(self, type: str, data: dict[str, Any]) -> None:
        message = {"type": type, "data": data}
        await self._send(message)

    async def step(self) -> None:
        data = self._step_once()
        await self._emit_state("step", data)

    async def reset(self) -> None:
        data = self._reset_once()
        await self._emit_state("reset", data)

    def start_play(self) -> None:
        if not self._playing:
            self._playing = True
            self._play_task = asyncio.create_task(
                self.play_loop(dt=0.1)
            )

    def stop_play(self) -> None:
        if self._playing:
            self._playing = False
            if self._play_task:
                self._play_task.cancel()
                self._play_task = None

    def _step_once(self) -> dict[str, Any]:
        if not self._env.has_reset:
            return self._reset_once()

        observation, reward, terminated, truncated, info = self._env.step()
        frame = self._env.render()

        return {
            "stepIdx": info["current_step"],
            "frame": frame,
            "observation": observation,
            "reward": reward,
            "done": terminated or truncated,
            "episodeReturn": info["episode_return"],
            "action": info["action"],
        }
        
    def _reset_once(self) -> dict[str, Any]:
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

    async def play_loop(self, dt: float = 0.) -> None:
        try:
            while self._playing:
                data = self._step_once()
                await self._emit_state("step", data)

                if dt > 0:
                    await asyncio.sleep(dt)

        except asyncio.CancelledError:
            pass

    def set_policy(self, code: str) -> None:
        if self._playing:
            self.stop_play()

        self._env.set_policy(code)

    def set_env_id(self, env_id: str) -> None:
        if self._playing:
            self.stop_play()

        self._env.init_env(env_id)

    async def handle_message(
        self, 
        message: dict[str, Any],
    ) -> dict[str, Any]:
        msg_type = message.get("type")

        if msg_type == "step":
            await self.step()
        elif msg_type == "reset":
            await self.reset()
        elif msg_type == "play":
            self.start_play()
        elif msg_type == "pause":
            self.stop_play()
        elif msg_type == "submitPolicy":
            data = message.get("data")
            self.set_policy(data)
        elif msg_type == "submitEnv":
            data = message.get("data")
            self.set_env_id(data)
            await self.reset()
        else:
            print(f"Unknown message type: {msg_type}")


async def handler(websocket: ServerConnection) -> None:
    async def send(message: dict[str, Any]) -> None:
        await websocket.send(json.dumps(message))

    controller = GymController(send)

    try:
        # Reset env on new connection and send initial data to client
        await controller.reset()

        async for message in websocket:
            try:
                await controller.handle_message(json.loads(message))
            except PolicyError as e:
                await send({
                    "type": "error",
                    "data": str(e),
                })
            except EnvironmentError as e:
                await send({
                    "type": "error",
                    "data": str(e),
                })

    except PolicyError as e:
        await send({
            "type": "error",
            "data": str(e),
        })
    except EnvironmentError as e:
        await send({
            "type": "error",
            "data": str(e),
        })
    


async def main() -> None:
    async with serve(handler, "", 8765) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
