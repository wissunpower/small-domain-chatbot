
from llama_index.core.indices.base import BaseIndex

from rag.index.accessor import (
    VectorStoreAccessor,
    ChromaDBAccessor,
)


def build_query_index(cfg: dict) -> BaseIndex:
    index_accessor_type: str = cfg['index_accessor']
    data_embedding_skip: bool = cfg['data_embedding_skip']

    if 'ChromaDB' == index_accessor_type:
        index_accessor = ChromaDBAccessor(cfg)
    else:
        index_accessor = VectorStoreAccessor(cfg)
    
    if not data_embedding_skip:
        # save index
        index_accessor.build_index()
    
    # load index
    index = index_accessor.get_index()

    return index
