from asyncio import sleep
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from video_processor import VideoProcessor

app = FastAPI()
FRAMES_DELAY = 0.04

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <img id="videoElement" src=""></video>
        <script>
        const videoElement = document.getElementById('videoElement');

        const socket = new WebSocket('ws://192.168.1.3/video');

        socket.onmessage = function(event) {
            videoElement.src = 'data:image/jpeg;base64,' + event.data;
        };
        </script>
    </body>
</html>
"""


@app.websocket("/video")
async def video_stream(websocket: WebSocket):
    video = VideoProcessor()

    await websocket.accept()

    for status, frame in video.get_frame():
        frame_base64 = video.process_frame(frame)
        if not status:
            await websocket.send_text("No video")
        await websocket.send_text(frame_base64)

        await sleep(
            FRAMES_DELAY
        )  # Optimize streaming and needed for accepting new clients


@app.get("/")
def index():
    return HTMLResponse(html)
