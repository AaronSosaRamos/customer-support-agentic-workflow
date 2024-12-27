from pydantic import (
    BaseModel, 
    Field
)
from typing import (
    TypedDict, 
    List
)
from langchain_core.documents import Document

# Subschemas for modularity
class KeyPoint(BaseModel):
    text: str = Field(..., description="A key point extracted from the summary")
    importance_score: float = Field(..., description="Relevance or importance of this key point (0 to 1)")

class KeywordDensity(BaseModel):
    keyword: str = Field(..., description="The keyword identified in the summary")
    density: float = Field(..., description="Relative frequency of the keyword in the summary (0 to 1)")

# Main schemas
class SummaryOutput(BaseModel):
    summary: str = Field(..., description="The summarized version of the user request")
    key_points: List[KeyPoint] = Field(..., description="A list of key points extracted from the request")
    confidence_score: float = Field(..., description="Confidence level of the summary (0 to 1)")
    word_count: int = Field(..., description="Word count of the generated summary")
    language_used: str = Field(..., description="Language used for the summary")

class AnalysisOutput(BaseModel):
    sentiment: str = Field(..., description="Overall sentiment of the summarized text (e.g., positive, neutral, negative)")
    dominant_theme: str = Field(..., description="The main theme or topic identified in the summary")
    linguistic_complexity: str = Field(..., description="Complexity of language used in the summary (e.g., simple, moderate, complex)")
    coverage_score: float = Field(..., description="Extent to which the summary covers key aspects of the original request (0 to 1)")
    contradictions_found: bool = Field(..., description="Whether any contradictory statements were found in the summary")
    keyword_density: List[KeywordDensity] = Field(..., description="Keywords and their relative density in the summary")
    factual_accuracy_score: float = Field(..., description="Score evaluating the factual accuracy of the summary (0 to 1)")
    tone_consistency: bool = Field(..., description="Whether the tone matches the requested tone (e.g., formal, casual)")
    coherence_score: float = Field(..., description="Score evaluating the logical flow and coherence of the summary (0 to 1)")
    summary_structure: str = Field(..., description="Type of structure used in the summary (e.g., chronological, thematic)")
    critical_points_covered: bool = Field(..., description="Whether all critical points were addressed in the summary")
    redundant_phrases: List[str] = Field(..., description="Any redundant or repetitive phrases detected in the summary")

class SuggestedAction(BaseModel):
    action: str = Field(..., description="The suggested action based on the analysis")
    priority: int = Field(..., description="Priority ranking of this action")
    rationale: str = Field(..., description="Rationale for suggesting this action")
    estimated_impact: str = Field(..., description="Estimated impact of the action (e.g., high, medium, low)")
    feasibility_score: float = Field(..., description="Feasibility score for the action (0 to 1)")

class SuggestActionsOutput(BaseModel):
    actions: List[SuggestedAction] = Field(..., description="A list of suggested actions based on the analysis")
    next_steps: str = Field(..., description="General next steps recommended based on the actions")

class GraphState(TypedDict):
    file_url: str
    customer_request: str
    lang: str

    context: List[Document]
    summary_output: SummaryOutput
    analysis_output: AnalysisOutput
    suggest_actions_output: SuggestActionsOutput