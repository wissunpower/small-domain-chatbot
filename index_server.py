
import datetime

from multiprocessing import Lock, Process
from multiprocessing.managers import BaseManager

from config.chatbot_config import get_cfg
from utils.log import logger
from models import build_model
from rag.index import build_query_index

from flask_handler import run_handler


index = None
lock = Lock()

def query_index(query_text):
    """Query the global index."""
    global index

    start_time = datetime.datetime.now()

    response = index.as_query_engine(
        similarity_top_k=5
        ).query(query_text)

    end_time = datetime.datetime.now()
    logger.info(f'{end_time} elapsed for query is {end_time - start_time}')

    return response

if __name__ == "__main__":
    build_model(get_cfg)
    
    with lock:
        index = build_query_index(get_cfg)
    
    # initialize manager connection
    # NOTE: you might want to handle the password in a less hardcoded way
    manager = BaseManager(("", 5602), b"password")
    manager.register('query_index', query_index)
    server = manager.get_server()

    handler_process = Process(target=run_handler)
    handler_process.start()

    logger.info("server started...")
    server.serve_forever()
