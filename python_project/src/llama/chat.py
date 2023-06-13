import os
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from llama_index import (
    GPTVectorStoreIndex,
    LLMPredictor,
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from src.llama import utils


def index_init():
  return None

def llama_chat(question):
  model_name = "text-davinci-003"
  model_temperature = 0
  api_key = os.getenv("OPENAI_API_KEY")  # Replace with your actual OpenAI API k
  DATA_PATH = os.getenv("DATA_PATH")
  INDEX_PATH = os.getenv("INDEX_PATH")
  llm = utils.get_llm(model_name, model_temperature, api_key)
  index = None
  service_context = ServiceContext.from_defaults(llm_predictor=LLMPredictor(llm=llm))
  # indexが存在する場合
  if os.path.isfile( INDEX_PATH+ "/vector_store.json"):
    print("index exists")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
    index = load_index_from_storage(storage_context)
  else:
    print("index not found")
    documents = SimpleDirectoryReader(DATA_PATH).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=INDEX_PATH)

  query_engine = index.as_query_engine(
    streaming=True,
    similarity_top_k=3,
    service_context=service_context
  )
  response = query_engine.query(question)
  for text in response.response_gen:
    yield text
  
  # return response



