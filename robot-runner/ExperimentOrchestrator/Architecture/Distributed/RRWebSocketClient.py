import asyncio
import websockets
import json

class RRWebSocketClient:
    def __init__(self, server_address, client_id):
        self.server_address = server_address
        self.client_id = client_id
        self.kill_signal_received = False

    async def register(self):
        async with websockets.connect(self.server_address) as websocket:
            registration_data = {
                "type": "register",
                "client_id": self.client_id
            }
            await websocket.send(json.dumps(registration_data))
            while not self.kill_signal_received:
                message = await websocket.recv()
                data = json.loads(message)
                if data.get("type") == "kill":
                    self.kill_signal_received = True
                    print("Received kill signal. Terminating client.")
                else:
                    print(f"Received task: {data}")
                    ### RECEIVES THE TASK TO BE EXECUTED
                    ## Call the method received

    # Implement Method CALL
    
# Main code
async def main():
    server_address = "ws://localhost:8765"
    client_id = "c1"
    client = RRWebSocketClient(server_address, client_id)
    await client.register()

# Run the main coroutine
asyncio.run(main())
