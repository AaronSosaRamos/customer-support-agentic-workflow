from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)