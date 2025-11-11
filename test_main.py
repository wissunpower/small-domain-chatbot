
import datetime

from config.chatbot_config import get_cfg
from utils.log import logger
from models import build_model
from rag.index import build_query_index


build_model(get_cfg)

index = build_query_index(get_cfg)
query_engine = index.as_query_engine(similarity_top_k=5)


while True:
    text_input = input("User: ")
    if text_input == "exit":
        break

    start_time = datetime.datetime.now()
    response = query_engine.query(text_input)
    end_time = datetime.datetime.now()
    print(f"Agent: {response}")
    logger.debug(f'{end_time} elapsed for query is {end_time - start_time}')
