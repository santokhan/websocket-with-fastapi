from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse

from app.websocket import handle_websocket

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="WebSocket test console")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html", media_type="text/html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await handle_websocket(websocket)


def main() -> None:
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    main()
