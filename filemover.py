from typing import Optional
from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
import aiofiles
from typing import List
import os
app = FastAPI()

################################ Data model for the file structure #################################

@app.get("/")
async def r():
    return {"100": "Ha Ha it's working" }

class Folder(BaseModel):
    path : str  
###################### API for creating folders ##########################
@app.post("/folder")
async def filedata(data: Folder):
    try: 
        os.makedirs(data.path)
    except FileExistsError:
        return {'Error': "Folder already exists"}
    else:
        return {"100": "folder created sucessfully"}


###################### data model for file upload ###################################
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    for file in files:
        async with aiofiles.open(file.filename, 'wb') as f:
            while content := await file.read(1024): # async read chunk
                await f.write(content)
            
    return {"Uploaded Filenames": [file.filename for file in files]}

