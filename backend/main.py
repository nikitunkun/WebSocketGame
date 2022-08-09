"""Multiplayer websocket game. Allows players to move around the map in real time"""

from typing import Dict, List, Union

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    """Game Connection Manager"""

    def __init__(self):
        """
        Initializing Connection Manager.

        :param
        :return:
        """
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, user: str):
        """
        Connecting to the game and getting all active players.

        :param websocket
        :param user:
        :return:
        """

        await websocket.accept()

        websocket.cookies["user"] = str(user)
        for connection in self.active_connections:
            await websocket.send_json({"event": "create", "user": connection.cookies["user"]})

        self.active_connections.append(websocket)

        for connection in self.active_connections:
            await connection.send_json({"event": "create", "user": user})

    def disconnect(self, websocket: WebSocket):
        """
        Disconnecting from the game.

        :param websocket:
        :return:
        """

        self.active_connections.remove(websocket)

    async def broadcast(self, message: Union[str, Dict]):
        """
        Sending a message to the client side.

        :param message:
        :return:
        """

        if isinstance(message, dict):
            for connection in self.active_connections:
                await connection.send_json(message)

        elif isinstance(message, str):
            for connection in self.active_connections:
                await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{user}")
async def websocket_game(websocket: WebSocket, user: str):
    """
    Game Handler.

    :param websocket:
    :param user:
    :return:
    """

    await manager.connect(websocket, user)
    try:
        while True:
            request = await websocket.receive_text()
            await manager.broadcast(request)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"event": "delete", "user": user})
