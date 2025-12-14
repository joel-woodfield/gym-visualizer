import asyncio
import json

from websockets.asyncio.server import serve

async def handler(websocket):
    while True:
        message = await websocket.recv()
        data = json.loads(message).get("data", None)

        if data is None:
            data = {}

        step = data.get("stepIdx", -1) + 1
        message = json.dumps(
            {
                "type": "step",
                "data": {"stepIdx": step},
            }
        )
        await websocket.send(message)

async def main():
    async with serve(handler, "", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
