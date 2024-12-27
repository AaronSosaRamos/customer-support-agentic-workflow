from graph.graph import app
from utils.logger import setup_logger
from utils.save_dict_to_json import save_dict_to_json

logger = setup_logger(__name__)

if __name__ == '__main__':
    inputs = {
        "file_url": "http://scielo.sld.cu/pdf/rus/v13n6/2218-3620-rus-13-06-123.pdf",
        "customer_request": "How can I be a good customer in base of the given article?",
        "lang": "en",
    }

    result = app.invoke(inputs)

    logger.info(f"Generated Result: {result}")

    save_dict_to_json(result, "output/output.json")