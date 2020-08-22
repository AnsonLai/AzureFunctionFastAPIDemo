import azure.functions as func
from bonnette import Bonnette

from .main import app

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# Option 1: as a StreamingResponse
from fastapi.responses import StreamingResponse

def main(req: func.HttpRequest) -> func.HttpResponse:
    handler = Bonnette(app)
    return handler(req)