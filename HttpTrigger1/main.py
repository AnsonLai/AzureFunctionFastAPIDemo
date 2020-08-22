from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"test": "root"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# REDIRECT
from fastapi.responses import RedirectResponse
@app.get("/redirect/")
async def redirect():
    response = RedirectResponse(url='http://google.com/')
    return response

# DOWNLOAD BLOB
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# Option 1: as a StreamingResponse
from fastapi.responses import StreamingResponse
import tempfile
@app.get("/streamdownload/")
async def streamdownload():
    connect_str = "************"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = "************"
    container_client = blob_service_client.get_container_client(container_name)

    local_file_name = '************.csv'

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    tempFilePath = tempfile.gettempdir()
    tempFile = tempfile.NamedTemporaryFile(delete=False)
    tempFileName = tempFile.name
    
    with open(tempFileName, "wb") as blob:
        data = blob_client.download_blob()
        data.readinto(blob)

    temp_file = open(tempFileName, "rb")

    response = StreamingResponse(temp_file, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=" + local_file_name

    return response

# Option 2: as a FileResponse
from fastapi.responses import FileResponse
@app.get("/filedownload/{filename}")
async def filedownload(filename: str):
    connect_str = "************"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = "************"
    container_client = blob_service_client.get_container_client(container_name)

    local_file_name = filename

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    tempFilePath = tempfile.gettempdir()
    tempFile = tempfile.NamedTemporaryFile(delete=False)
    tempFileName = tempFile.name

    with open(tempFileName, "wb") as blob:
        data = blob_client.download_blob()
        data.readinto(blob)

    temp_file = open(tempFileName, "rb")

    response = StreamingResponse(temp_file, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=" + local_file_name

    return response

# Option 3: as a FileResponse (Async) UNCOMMENT IMPORT
from fastapi.responses import FileResponse
# from azure.storage.blob.aio import BlobServiceClient, BlobClient, ContainerClient
@app.get("/filedownload/async/{filename}")
async def filedownload_aio(filename: str):
    connect_str = "************"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = "************"
    container_client = blob_service_client.get_container_client(container_name)

    local_file_name = filename

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    tempFilePath = tempfile.gettempdir()
    tempFile = tempfile.NamedTemporaryFile(delete=False)
    tempFileName = tempFile.name

    with open(tempFileName, "wb") as blob:
        stream = await blob_client.download_blob()
        data = await stream.readall()
        blob.write(data)

    temp_file = open(tempFileName, "rb")

    response = StreamingResponse(temp_file, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=" + local_file_name

    return response