import base64
import cv2
import cv2.typing as cv_types
import imutils
from typing import Any, Generator, Tuple
from singleton import SingletonMeta

VIDEO_W: int = 1280
VIDEO_H: int = 720
VIDEO_QUALITY: int = 50


class VideoProcessor(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.video_in: cv2.VideoCapture = cv2.VideoCapture(0)  # Camera on

        # Possible to add video_out for logging
        # self.video_out = cv2.VideoWriter()

        self._video_size: Tuple[int, int] = int(self.video_in.get(3)), int(
            self.video_in.get(4)
        )

    def get_frame(self) -> Generator[Tuple[bool, cv_types.MatLike], Any, Any]:
        while self.video_in.isOpened():
            img, frame = self.video_in.read()
            yield (img, frame)

    def process_frame(self, frame: cv_types.MatLike) -> str:
        frame = imutils.resize(frame, VIDEO_W, VIDEO_H)
        success, buffer = cv2.imencode(
            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), VIDEO_QUALITY]
        )
        if not success:
            raise cv2.error("Frame encoding failed")
        encoded = base64.b64encode(buffer.tobytes()).decode("utf-8")
        return encoded

    def release(self) -> None:
        self.video_in.release()
