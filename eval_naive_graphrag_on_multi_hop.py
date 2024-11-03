import os
# os.environ["OPENAI_API_KEY"] = "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"
import json
import sys
# sys.path.append("../..")

import nest_asyncio
nest_asyncio.apply()
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("nano-graphrag").setLevel(logging.INFO)
from nano_graphrag import GraphRAG, QueryParam
from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import (
    answer_correctness,
    answer_similarity,
)

# small evaluation dataset
multi_hop_rag_file = "./fixtures/MultiHopRAG_small.json"
multi_hop_corpus_file = "./fixtures/corpus_small.json"

with open(multi_hop_rag_file) as f:
    multi_hop_rag_dataset = json.load(f)
with open(multi_hop_corpus_file) as f:
    multi_hop_corpus = json.load(f)

corups_url_refernces = {}
for cor in multi_hop_corpus:
    corups_url_refernces[cor['url']] = cor

multi_hop_rag_dataset = multi_hop_rag_dataset[:100]
print("Queries have types:", set([q['question_type'] for q in multi_hop_rag_dataset]))
total_urls = set()
for q in multi_hop_rag_dataset:
    total_urls.update([up['url'] for up in q['evidence_list']])
corups_url_refernces = {k:v for k, v in corups_url_refernces.items() if k in total_urls}

total_corups = [f"## {cor['title']}\nAuthor: {cor['author']}, {cor['source']}\nCategory: {cor['category']}\nPublised: {cor['published_at']}\n{cor['body']}" for cor in corups_url_refernces.values()]

print(f"We will need {len(total_corups)} articles:")
print(total_corups[0][:200], "...")


# First time indexing will cost many time, roughly 15~20 minutes
graphrag_func = GraphRAG(working_dir="nano_graphrag_cache_multi_hop_rag_test", enable_naive_rag=True,
                         embedding_func_max_async=4)
graphrag_func.insert(total_corups)
# parameters setting
response_formate = "Single phrase or sentence, concise and no redundant explanation needed. If you don't have the answer in context, Just response 'Insufficient information'"
naive_rag_query_param = QueryParam(mode='naive', response_type=response_formate)
naive_rag_query_only_context_param = QueryParam(mode='naive', only_need_context=True)
local_graphrag_query_param = QueryParam(mode='local', response_type=response_formate)
local_graphrag_only_context__param = QueryParam(mode='local', only_need_context=True)
# a case (the first query in evaluation dataset)
query = multi_hop_rag_dataset[0]
print("Question:", query['query'])
print("GroundTruth Answer:", query['answer'])
print("NaiveRAG Answer:", graphrag_func.query(query['query'], param=naive_rag_query_param))
print("Local GraphRAG Answer:", graphrag_func.query(query['query'], param=local_graphrag_query_param))

# test for all queries
questions = [q['query'] for q in multi_hop_rag_dataset]
labels = [q['answer'] for q in multi_hop_rag_dataset]

from tqdm import tqdm
logging.getLogger("nano-graphrag").setLevel(logging.WARNING)
# query in naive rag & graph rag
naive_rag_answers = [
    graphrag_func.query(q, param=naive_rag_query_param) for q in tqdm(questions)
]
local_graphrag_answers = [
    graphrag_func.query(q, param=local_graphrag_query_param) for q in tqdm(questions)
]
# scores
naive_results = evaluate(
    Dataset.from_dict({
        "question": questions,
        "ground_truth": labels,
        "answer": naive_rag_answers,
    }),
    metrics=[
        # answer_relevancy,
        answer_correctness,
        answer_similarity,
    ],
)
local_graphrag_results = evaluate(
    Dataset.from_dict({
        "question": questions,
        "ground_truth": labels,
        "answer": local_graphrag_answers,
    }),
    metrics=[
        # answer_relevancy,
        answer_correctness,
        answer_similarity,
    ],
)
print("Naive RAG results", naive_results)
print("Local GraphRAG results", local_graphrag_results)