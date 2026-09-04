import json
import logging

from fastapi import WebSocket, WebSocketDisconnect


logger = logging.getLogger(__name__)


async def handle_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    image_metadata: dict[str, str] | None = None
    logger.info("New client connected")

    try:
        while True:
            message = await websocket.receive()
            if message.get("type") == "websocket.disconnect":
                break

            data = message.get("text")
            if data is not None:
                try:
                    payload = json.loads(data)
                except json.JSONDecodeError:
                    logger.info("Received message: %s", data)
                    continue

                if payload.get("type") == "image-metadata":
                    image_metadata = {
                        "name": payload.get("name") or "image",
                        "mimeType": payload.get("mimeType") or "application/octet-stream",
                    }
                    logger.info("Receiving image: %s", image_metadata)
                elif payload.get("type") == "text":
                    text = payload.get("message", "")
                    logger.info("Received text: %s", text)
                    await websocket.send_json({
                        "type": "text-received",
                        "message": f"Text received: {text}",
                    })
                continue

            image = message.get("bytes")
            if image is not None:
                name = image_metadata["name"] if image_metadata else "image"
                logger.info("Received image: %s (%d bytes)", name, len(image))
                await websocket.send_json({
                    "type": "upload-complete",
                    "message": f'Image "{name}" uploaded successfully ({len(image)} bytes)',
                })
                image_metadata = None
    except WebSocketDisconnect:
        logger.info("Client disconnected")