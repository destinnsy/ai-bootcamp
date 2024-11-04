from datetime import time

from langchain_community.document_loaders import JSONLoader
import json
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv('.streamlit/secrets.toml')

original_file_path = './catalogs/im8-reform.json'

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# This is the "Updated" helper function for calling LLM
def get_completion(file_path: str):
    json_data = json.loads(Path(file_path).read_text())

    prompt = f"""
In the JSON object provided below, extract the value of the key "with-ids".
The expected value is an array of strings.
You are to respond ONLY with the value.
The respond must be JSON readable.
                        
{json_data}
"""

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create( #originally was openai.chat.completions
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
        top_p=1.0,
        max_tokens=2048,
        n=1,
        response_format={"type": "json_object"},
    )
    extracted_data = json.loads(response.choices[0].message.content)
    return extracted_data['with-ids']


must_have = get_completion('./profiles/low-risk-level-0.json')
should_have = get_completion('./profiles/low-risk-level-1.json')
good_to_have = get_completion('./profiles/low-risk-level-2.json')

def metadata_func(record: dict, metadata: dict) -> dict:
    id = record.get('id')
    metadata['id'] = id
    if id in must_have:
        metadata['security level'] = 'must have'
    elif id in should_have:
        metadata['security level'] = 'should have'
    elif id in good_to_have:
        metadata['security level'] = 'good to have'

    return metadata

document_list = JSONLoader(
    file_path=original_file_path,
    jq_schema='.catalog.groups[].controls[]',
    text_content=False,
    metadata_func=metadata_func
).load()

embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large')

#
# vectordb = Chroma.from_documents(
#     documents=document_list,
#     embedding=embeddings_model,
#     collection_name="IM8",
#     persist_directory='./vector_db'
# )

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index_name = "im8-index"

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=embeddings_model)

vector_store.add_documents(documents=document_list)