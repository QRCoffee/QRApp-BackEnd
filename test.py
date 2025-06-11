import asyncio
import websockets

async def listen_ws():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("🔌 WebSocket connected. Listening for messages...")
        try:
            while True:
                msg = await websocket.recv()
                print("📩 Received:", msg)
        except websockets.ConnectionClosed:
            print("❌ WebSocket closed")

if __name__ == "__main__":
    asyncio.run(listen_ws())
