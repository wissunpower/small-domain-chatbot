
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.llms.custom import CustomLLM
from llama_index.llms.ollama import Ollama
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from models.prompt_helper import QwenPromptHelper


def build_llm_model(cfg: dict) -> FunctionCallingLLM | CustomLLM:
    llm_platform: str = cfg['llm_platform']
    model_name: str = cfg['llm_model_name']
    
    if Ollama.__name__.lower() == llm_platform.lower():
        host: str = cfg['ollama_host']
        port: str = str(cfg['ollama_port'])
        base_url: str = "http://" + host + ":" + port
        llm = Ollama(
            model=model_name,
            base_url= base_url,
            request_timeout=360.0,
            # Manually set the context window to limit memory usage
            context_window=12000,
            )
    else:
        # Current version default setting is Qwen
        prompt_helper = QwenPromptHelper
        
        # Set Qwen as the language model and set generation config
        llm = HuggingFaceLLM(
            model_name=model_name,
            tokenizer_name=model_name,
            context_window=30000,
            max_new_tokens=2000,
            generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
            messages_to_prompt=prompt_helper.messages_to_prompt,
            completion_to_prompt=prompt_helper.completion_to_prompt,
            device_map="auto",
            )
    
    return llm

def build_model(cfg: dict):
    Settings.llm = build_llm_model(cfg)
    
    # Set embedding model
    embed_model_name: str = cfg['embed_model_name']
    Settings.embed_model = HuggingFaceEmbedding(
        model_name = embed_model_name
    )
    
    # Settings.chunk_size = 512
    # Settings.chunk_overlap = 64
    
    # Set the size of the text chunk for retrieval
    Settings.transformations = [SentenceSplitter(chunk_size=1024)]
