import logging
import os


base_cfg = {
    'log_dir': './_log',
    'log_level': logging.INFO,

    # example : 'VectorStore', 'ChromaDB'
    'index_accessor': 'ChromaDB',
    'data_dir': './_data',
    'index_dir': './_storage',
    'collection_name': 'small_domain_chatbot',

    'data_embedding_skip': False,

    # example : 'Ollama', 'HuggingFaceLLM'
    'llm_platform': 'Ollama',
    # example : 'llama3.1', 'Qwen/Qwen3-0.6B'
    'llm_model_name': 'llama3.1',
    # example : 'BAAI/bge-base-en-v1.5', 'BAAI/bge-m3'
    'embed_model_name': 'BAAI/bge-m3',
}


# develop environment configuration override
dev_cfg = base_cfg
dev_cfg['log_level'] = logging.DEBUG
dev_cfg['data_embedding_skip'] = True


#get_cfg = base_cfg
get_cfg = dev_cfg


def post_process_dir_cfg(cfg_dict: dict, key_name: str):
    if not cfg_dict[key_name].endswith(os.path.sep) \
        and not cfg_dict[key_name].endswith('/'):
        # Ensure output dir is valid for later use
        cfg_dict[key_name] += os.path.sep

post_process_dir_cfg(get_cfg, 'log_dir')
post_process_dir_cfg(get_cfg, 'data_dir')
post_process_dir_cfg(get_cfg, 'index_dir')