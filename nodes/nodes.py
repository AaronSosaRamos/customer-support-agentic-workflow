from document_loaders.pdf_loader import load_pdf_documents
from schemas.schemas import (
    AnalysisOutput,
    SuggestActionsOutput, 
    SummaryOutput
)
from utils.logger import setup_logger
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv, find_dotenv
from vector_store_db.vector_store_db import compile_and_return_retriever
from langchain.schema import (
       HumanMessage,
       SystemMessage
)
from model.model import llm

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

def generate_context(state):
    docs = load_pdf_documents(state['file_url'])

    retriever = compile_and_return_retriever(docs)
    context = retriever.invoke(state['customer_request'])

    logger.info(f"FIRST NODE - GENERATE CONTEXT: {context}")

    return {
        "context": context
    }

def generate_summary(state):
    json_parser = JsonOutputParser(pydantic_object=SummaryOutput)

    messages = [
        SystemMessage(content=f"You are an expert in customer support summarization. Your role is to analyze the provided context and generate a clear, concise summary tailored to the customer's request. The summary must meet the structure defined in the task."),
        HumanMessage(content=f"""Please generate a detailed summary based on the following information:

        Context:
        {state['context']}

        Customer Request:
        {state['customer_request']}

        Your summary must address the following:
        1. **Summary**: Provide a concise version of the context that aligns with the customer's request.
        2. **Key Points**: Identify and extract the most relevant points from the context that directly address the customer's needs.
        3. **Confidence Score**: Evaluate the confidence level of the summary based on the clarity and relevance of the context (0 to 1).
        4. **Word Count**: Indicate the total number of words in the summary.
        5. **Language Used**: Specify the language in which the summary is provided.

        Ensure your response is structured to comply with the following format:
        {json_parser.get_format_instructions()}

        You must respond in this language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"SECOND NODE - GENERATE SUMMARY: {parsed_result}")

    return {
        "summary_output": parsed_result
    }

def generate_analysis(state):
    json_parser = JsonOutputParser(pydantic_object=AnalysisOutput)

    messages = [
        SystemMessage(content=f"You are an expert in analyzing summaries for customer support. Your role is to provide a detailed analysis of the given summary, evaluating its quality, content, and alignment with the customer's request. Your analysis must follow the structure defined in the task."),
        HumanMessage(content=f"""Please analyze the following summary and provide a comprehensive evaluation based on the specified criteria:

        Summary:
        {state['summary_output']}

        Customer Request:
        {state['customer_request']}

        Your analysis must include the following components:
        1. **Sentiment**: Identify the overall sentiment of the summarized text (e.g., positive, neutral, negative).
        2. **Dominant Theme**: Highlight the main theme or topic identified in the summary.
        3. **Linguistic Complexity**: Assess the complexity of the language used in the summary (e.g., simple, moderate, complex).
        4. **Coverage Score**: Evaluate the extent to which the summary covers key aspects of the original request (0 to 1).
        5. **Contradictions Found**: Indicate whether any contradictory statements were identified in the summary.
        6. **Keyword Density**: Extract keywords and calculate their relative density in the summary.
        7. **Factual Accuracy Score**: Provide a score evaluating the factual accuracy of the summary (0 to 1).
        8. **Tone Consistency**: Assess whether the tone matches the requested tone (e.g., formal, casual).
        9. **Coherence Score**: Evaluate the logical flow and coherence of the summary (0 to 1).
        10. **Summary Structure**: Identify the type of structure used in the summary (e.g., chronological, thematic).
        11. **Critical Points Covered**: Determine whether all critical points were addressed in the summary.
        12. **Redundant Phrases**: List any redundant or repetitive phrases detected in the summary.

        Ensure your response adheres to the following format:
        {json_parser.get_format_instructions()}

        You must respond in this language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"THIRD NODE - GENERATE ANALYSIS: {parsed_result}")

    return {
        "analysis_output": parsed_result
    }

def suggest_actions(state):
    json_parser = JsonOutputParser(pydantic_object=SuggestActionsOutput)

    messages = [
        SystemMessage(content=f"You are an expert in customer support strategy. Your role is to suggest actionable recommendations based on the analysis of the summary and the customer's request. Your suggestions must align with the specified structure."),
        HumanMessage(content=f"""Based on the provided analysis, generate actionable recommendations that directly address the customer's needs:

        Analysis Output:
        {state['analysis_output']}

        Customer Request:
        {state['customer_request']}

        Your suggested actions must include the following components:
        1. **Action List**: Provide a list of specific actions that the customer support team can take to address the identified needs and themes.
        2. **Priority Ranking**: Rank the actions based on their importance and urgency, starting with the most critical.
        3. **Rationale**: Explain why each action is important and how it addresses the customer’s request.
        4. **Estimated Impact**: Indicate the potential impact of each action (e.g., high, medium, low).
        5. **Feasibility Score**: Provide a feasibility score (0 to 1) for each action, considering the effort required versus expected outcomes.
        6. **Next Steps**: Summarize the immediate next steps that should be taken based on the suggested actions.

        Ensure your response adheres to the following format:
        {json_parser.get_format_instructions()}

        You must respond in this language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"FOURTH NODE - SUGGEST ACTIONS: {parsed_result}")

    return {
        "suggest_actions_output": parsed_result
    }
