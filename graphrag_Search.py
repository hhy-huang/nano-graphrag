import os
from nano_graphrag import GraphRAG, QueryParam
# os.environ["OPENAI_API_KEY"] = "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"


graph_func = GraphRAG(working_dir="./web3")

with open("./web3/txtWhitePapers/ark.pdf.txt") as f:
    graph_func.insert(f.read())

# Perform global graphrag search
print("Perform global graphrag search:")
print(graph_func.query("What are the top themes in this story?"))
print("#"*100)
# Perform local graphrag search (I think is better and more scalable one)
print("Perform local graphrag search:")
print(graph_func.query("What are the top themes in this story?", param=QueryParam(mode="local")))
