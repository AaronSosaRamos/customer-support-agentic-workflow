from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import uuid
import requests
import tempfile
from utils.logger import setup_logger

logger = setup_logger(__name__)

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 100
)

class FileHandler:
    def __init__(self, file_loader, file_extension):
        self.file_loader = file_loader
        self.file_extension = file_extension

    def load(self, url):
        # Generate a unique filename with a UUID prefix
        unique_filename = f"{uuid.uuid4()}.{self.file_extension}"

        try:
            # Download the file from the URL and save it to a temporary file
            response = requests.get(url, timeout=10)  
            response.raise_for_status()  # Raise an HTTPError for bad responses

            with tempfile.NamedTemporaryFile(delete=False, prefix=unique_filename) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

        except requests.exceptions.RequestException as req_err:
            logger.error(f"HTTP request error: {req_err}")
            raise req_err
        except Exception as e:
            logger.error(f"An error occurred while downloading or saving the file: {e}")
            raise e

        # Use the file_loader to load the documents
        try:
            loader = self.file_loader(file_path=temp_file_path)
        except Exception as e:
            logger.error(f"No such file found at {temp_file_path}")
            raise e
        try:
            documents = loader.load()
        except Exception as e:
            logger.error(f"File content might be private or unavailable or the URL is incorrect.")
            raise e

        # Remove the temporary file
        os.remove(temp_file_path)

        return documents