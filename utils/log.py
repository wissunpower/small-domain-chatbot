
import datetime, logging
from config.chatbot_config import get_cfg


logger = logging.getLogger()
logger.setLevel(level=get_cfg['log_level'])
_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_formatter)
logger.addHandler(_stream_handler)

_file_handler = logging.FileHandler(get_cfg['log_dir'] + 'logfile_{:%Y-%m-%d_%H-%M}.log'.format(datetime.datetime.now()))
_file_handler.setFormatter(_formatter)
logger.addHandler(_file_handler)
