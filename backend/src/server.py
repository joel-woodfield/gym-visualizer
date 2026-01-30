import asyncio
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from gymnasium_env import GymnasiumEnv, EnvironmentError, PolicyError
import uvicorn

app = FastAPI()
PORT = 8765


class GymController:
    def __init__(self, websocket: WebSocket) -> None:
        self._env = GymnasiumEnv()
        self._websocket = websocket
        self._playing = False
        self._play_task: asyncio.Task[None] | None = None

    async def _emit_state(self, type: str, data: dict[str, Any]) -> None:
        """Sends a JSON message to the client."""
        await self._websocket.send_json({"type": type, "data": data})

    async def step(self) -> None:
        data = self._step_once()
        await self._emit_state("step", data)

    async def reset(self) -> None:
        self.stop_play()
        data = self._reset_once()
        await self._emit_state("reset", data)

    def start_play(self, fps: int) -> None:
        dt = 1.0 / fps

        if not self._playing:
            self._playing = True
            self._play_task = asyncio.create_task(
                self.play_loop(dt=dt)
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
        except Exception as e:
            # Handle potential connection issues during background loop
            print(f"Error in play_loop: {e}")
            self.stop_play()

    def set_policy(self, code: str) -> None:
        if self._playing:
            self.stop_play()
        self._env.set_policy(code)

    def set_env_id(self, env_id: str) -> None:
        if self._playing:
            self.stop_play()
        self._env.init_env(env_id)

    async def handle_message(self, message: dict[str, Any]) -> None:
        msg_type = message.get("type")

        if msg_type == "step":
            await self.step()
        elif msg_type == "reset":
            await self.reset()
        elif msg_type == "play":
            fps = int(message.get("fps", 60))
            self.start_play(fps)
        elif msg_type == "pause":
            self.stop_play()
        elif msg_type == "submitPolicy":
            self.set_policy(message.get("data"))
        elif msg_type == "submitEnv":
            self.set_env_id(message.get("data"))
            await self.reset()
        else:
            print(f"Unknown message type: {msg_type}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    controller = GymController(websocket)

    try:
        await controller.reset()

        while True:
            data = await websocket.receive_json()
            try:
                await controller.handle_message(data)
            except (PolicyError, EnvironmentError) as e:
                print(e)
                await websocket.send_json({"type": "error", "data": str(e)})

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        controller.stop_play()

# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")


if __name__ == "__main__":
    print(f"Visit http://localhost:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)

