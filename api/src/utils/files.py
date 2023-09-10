import shutil
from uuid import uuid4
from src.data.config import BASE_DIR
from fastapi import UploadFile


def create(file: UploadFile, upath: str) -> str:
    extension = file.filename.split('.')[-1]
    path = f'media/{upath}/{uuid4()}.{extension}'
    with open(BASE_DIR / path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

def stream(video_path: str):
    with open(video_path, "rb") as video_file:
        while True:
            video_chunk = video_file.read(8192)
            if not video_chunk:
                break
            yield video_chunk