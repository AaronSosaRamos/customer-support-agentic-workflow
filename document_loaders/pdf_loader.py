from document_loaders.file_handler import (
    FileHandler,
    splitter
)
from langchain_community.document_loaders import PyPDFLoader
from utils.logger import setup_logger

logger = setup_logger(__name__)

def load_pdf_documents(pdf_url: str, verbose=False):
    pdf_loader = FileHandler(PyPDFLoader, "pdf")
    docs = pdf_loader.load(pdf_url)

    if docs:
        split_docs = splitter.split_documents(docs)

        if verbose:
            logger.info(f"Found PDF file")
            logger.info(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs