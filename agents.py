from langgraph.prebuilt import create_react_agent   # ← fixed import
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def build_search_agent():
    return create_react_agent(
        model=llm,
        tools=[web_search]
    )

def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[scrape_url]
    )

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer."
    ),
    (
        "human",
        """
Topic: {topic}

Research:
{research}

Write a detailed report with:

1. Introduction
2. Key Findings
3. Conclusion
4. Sources

Be professional and factual.
"""
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a research quality evaluator."
    ),
    (
        "human",
        """
Report:
{report}

Respond in this format:

Score: x/10

Strengths:
- ...

Areas to Improve:
- ...

Verdict:
...
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()