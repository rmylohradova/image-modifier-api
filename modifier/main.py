import fastapi
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from modifier.schemas import ModifyBy
from modifier.image_services import process, upload_image
import os

from PIL import Image

app = FastAPI()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f"URL '{request.url} doesn't exist'"
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the image modifier"


@app.post("/modifier")
def modify_image(image_name, data: ModifyBy):
    original_im = os.path.join("modifier/files/original", image_name)
    with Image.open(original_im) as image:
        image = process(data, image)
        mod_im_path = os.path.join("modifier/files/modified", image_name)
    image.save(mod_im_path)
    return FileResponse(mod_im_path)


@app.post("/image_upload/")
def upload_im(image: UploadFile = fastapi.File(...)):
    file_path = upload_image('modifier/files/original/', image)
    if file_path is None:
        raise_bad_request("not valid file")
    return {"name": file_path.split('/')[-1]}








