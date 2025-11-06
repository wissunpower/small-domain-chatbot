
import abc
import datetime

import chromadb
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    )
from llama_index.core.indices.base import BaseIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

from utils.log import logger


class IVectorIndexAccessible(abc.ABC):
    @abc.abstractmethod
    def build_index(self):
        pass
    
    @abc.abstractmethod
    def get_index(self) -> BaseIndex:
        pass


class VectorStoreAccessor(IVectorIndexAccessible):
    def __init__(self, cfg: dict):
        self.input_dir: str = cfg['data_dir']
        self.persist_dir: str = cfg['index_dir']

    def build_index(self):
        documents = SimpleDirectoryReader(self.input_dir, recursive=False).load_data()
        storage_context = StorageContext.from_defaults()
        
        start_time = datetime.datetime.now()
        index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True,
            storage_context=storage_context,
            )
        
        end_time = datetime.datetime.now()
        logger.debug(f'docs embedding finish. {end_time}(elapsed {end_time - start_time})')
        
        # save index
        storage_context.persist(self.persist_dir)
    
    def get_index(self) -> BaseIndex:
        start_time = datetime.datetime.now()
        storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
        end_time = datetime.datetime.now()
        logger.debug(f'StorageContext from_defaults finish. {end_time}(elapsed {end_time - start_time})')
        
        start_time = datetime.datetime.now()
        index = load_index_from_storage(storage_context)
        end_time = datetime.datetime.now()
        logger.debug(f'load_index_from_storage finish. {end_time}(elapsed {end_time - start_time})')
        
        return index


class ChromaDBAccessor(IVectorIndexAccessible):
    def __init__(self, cfg: dict):
        self.input_dir: str = cfg['data_dir']
        self.persist_dir: str = cfg['index_dir']
        self.collection_name = cfg['collection_name']

    def build_index(self):
        documents = SimpleDirectoryReader(self.input_dir, recursive=False).load_data()
        db = chromadb.PersistentClient(path=self.persist_dir)
        chroma_collection = db.get_or_create_collection(self.collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        start_time = datetime.datetime.now()
        index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True,
            storage_context=storage_context,
            )
        
        end_time = datetime.datetime.now()
        logger.debug(f'docs embedding finish. {end_time}(elapsed {end_time - start_time})')
    
    def get_index(self) -> BaseIndex:
        start_time = datetime.datetime.now()
        db = chromadb.PersistentClient(path=self.persist_dir)
        chroma_collection = db.get_or_create_collection(self.collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        end_time = datetime.datetime.now()
        logger.debug(f'ChromaVectorStore create finish. {end_time}(elapsed {end_time - start_time})')
        
        start_time = datetime.datetime.now()
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            )
        end_time = datetime.datetime.now()
        logger.debug(f'VectorStoreIndex from_vector_store finish. {end_time}(elapsed {end_time - start_time})')
        
        return index
