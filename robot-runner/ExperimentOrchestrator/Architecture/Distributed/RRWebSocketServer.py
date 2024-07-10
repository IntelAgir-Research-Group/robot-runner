import asyncio
import websockets
import json

class RRWebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.connected_clients = {}

    async def handle_client_message(self, websocket, message):
        data = json.loads(message)
        if data.get("type") == "register":
            client_id = data.get("client_id")
            if client_id:
                self.connected_clients[client_id] = websocket
                print(f"Client {client_id} registered.")
        elif data.get("type") == "kill":
            await self.send_kill_signal()

    async def broadcast(self, message):
        await asyncio.gather(*[client.send(message) for client in self.connected_clients.values()])

    async def send_to_clients(self, message, client_ids):
        selected_clients = [client for client_id, client in self.connected_clients.items() if client_id in client_ids]
        await asyncio.gather(*[client.send(message) for client in selected_clients])
    
    async def send_kill_signal(self):
        await self.broadcast(json.dumps({"type": "kill"}))

    async def on_connect(self, websocket, path):
        try:
            async for message in websocket:
                await self.handle_client_message(websocket, message)
                pass
        finally:
            # Ensure the client is removed after disconnect
            to_remove = []  # Keep track of disconnected clients
            clients_copy = list(self.connected_clients.items())  # Copy the dictionary items to prevent runtime error
            for client_id, client_ws in clients_copy:
                if client_ws == websocket:
                    to_remove.append(client_id)
            for client_id in to_remove:
                self.connected_clients.pop(client_id, None)
    
    async def count_connected_clients(self):
        return len(self.connected_clients)
    
    async def start_server(self):
        server = await websockets.serve(self.on_connect, self.host, self.port)
        print('RR Server started!')
        return server

# Main code
# async def main():
#     server = RRWebSocketServer("localhost", 8765)
#     websocket_server = await server.start_server()
#     count = 0
#     while True:
#         # Perform other tasks while the server is running
#         await asyncio.sleep(1)
#         if count > 30:
#             print("Killing clients...")
#             await server.send_kill_signal()
#         count += 1

# Run the main coroutine
# asyncio.run(main())