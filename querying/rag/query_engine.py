# Create query engine with reranking
def create_query_engine(index, reranker):
    query_engine = index.as_query_engine(similarity_top_k=40, node_postprocessors=[reranker])
    return query_engine
