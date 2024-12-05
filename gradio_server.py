import gradio as gr
import os
from nano_graphrag import GraphRAG, QueryParam
os.environ["OPENAI_API_KEY"] = "***"
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
 
 
def random_response(message, history):
    import random
    return random.choice(["Yes", "No"])

def grapgrag_response(mesage, history):
    graph_func = GraphRAG(working_dir="./web3_test")

    with open("./web3/txtWhitePapers/ark.pdf.txt") as f:
        graph_func.insert(f.read())

    # Perform local graphrag search (I think is better and more scalable one)
    response = graph_func.query(mesage, param=QueryParam(mode="local"))
    return response
 
gr.ChatInterface(grapgrag_response).launch()
