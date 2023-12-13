import os
from typing import Any

import aiofiles
import starlette.status as status
from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.schemas import File

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui"), name="static")
MEDIA_FOLDER = 'storage'


@app.get("/api/get_files", response_model=list[File])
def get_files_list() -> Any:
    files_list = [{'name': f.name, 'date': f.stat().st_mtime} for f in list(os.scandir(MEDIA_FOLDER))]
    return files_list


@app.post("/api/uploadfiles")
async def create_upload_files(files: list[UploadFile]):
    for file in files:
        # TODO: remove file path
        async with aiofiles.open(f"media/{file.filename}", 'wb') as out_file:
            while content := await file.read(1024 * 1024 * 5):  # async read chunk in byte
                await out_file.write(content)  # async write chunk
    return RedirectResponse(url="/ui/index.html", status_code=status.HTTP_302_FOUND)
