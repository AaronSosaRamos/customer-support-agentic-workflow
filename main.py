import streamlit as st
import json
from graph.graph import app
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Streamlit UI
def main():
    st.set_page_config(page_title="Customer Support Dashboard", layout="wide", initial_sidebar_state="expanded")
    st.title("🌟 Customer Support with Agentic Workflow 🌟")
    st.markdown("### Professional UI by: Wilfredo Aaron Sosa Ramos")

    # Initialize session state
    if "result" not in st.session_state:
        st.session_state.result = None

    # Sidebar inputs
    st.sidebar.header("📥 Input Settings")
    file_url = st.sidebar.text_input("🌐 File URL", "http://scielo.sld.cu/pdf/rus/v13n6/2218-3620-rus-13-06-123.pdf")
    customer_request = st.sidebar.text_area(
        "✍️ Customer Request", "How can I be a good customer in base of the given article?"
    )
    lang = st.sidebar.selectbox("🌍 Language", ["en", "es", "fr", "de", "zh"], index=0)

    if st.sidebar.button("🚀 Process Request"):
        with st.spinner("Processing your request..."):
            inputs = {
                "file_url": file_url,
                "customer_request": customer_request,
                "lang": lang,
            }

            try:
                result = app.invoke(inputs)
                logger.info(f"Generated Result: {result}")
                st.session_state.result = result  # Store result in session state
            except Exception as e:
                st.error(f"Error processing request: {e}")
                st.session_state.result = None

    # Display results if available
    if st.session_state.result:
        display_results(st.session_state.result)

# Display results
def display_results(result):
    if not result:
        st.error("❌ No result available. Please try again.")
        return

    # Create columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Summary Output")
        summary_output = result.get("summary_output", {})
        st.write(f"**Summary**: {summary_output.get('summary', 'No summary available.')}")
        
        st.markdown("#### 🔑 Key Points")
        key_points = summary_output.get("key_points", [])
        if key_points:
            for point in key_points:
                st.write(f"- {point.get('text', 'No text')} (Importance: {point.get('importance_score', 'N/A')})")
        else:
            st.write("No key points available.")

        st.write(f"**Confidence Score**: {summary_output.get('confidence_score', 'N/A')}")
        st.write(f"**Word Count**: {summary_output.get('word_count', 'N/A')}")
        st.write(f"**Language Used**: {summary_output.get('language_used', 'N/A')}")

    with col2:
        st.markdown("### 📊 Analysis Output")
        analysis_output = result.get("analysis_output", {})
        st.write(f"**Sentiment**: {analysis_output.get('sentiment', 'N/A')}")
        st.write(f"**Dominant Theme**: {analysis_output.get('dominant_theme', 'N/A')}")
        st.write(f"**Linguistic Complexity**: {analysis_output.get('linguistic_complexity', 'N/A')}")
        st.write(f"**Coverage Score**: {analysis_output.get('coverage_score', 'N/A')}")
        st.write(f"**Contradictions Found**: {analysis_output.get('contradictions_found', 'N/A')}")
        st.write(f"**Factual Accuracy Score**: {analysis_output.get('factual_accuracy_score', 'N/A')}")
        st.write(f"**Tone Consistency**: {analysis_output.get('tone_consistency', 'N/A')}")
        st.write(f"**Coherence Score**: {analysis_output.get('coherence_score', 'N/A')}")
        st.write(f"**Summary Structure**: {analysis_output.get('summary_structure', 'N/A')}")
        st.write(f"**Critical Points Covered**: {analysis_output.get('critical_points_covered', 'N/A')}")
        st.write(f"**Redundant Phrases**: {', '.join(analysis_output.get('redundant_phrases', [])) if analysis_output.get('redundant_phrases') else 'None'}")

    st.markdown("### ✅ Suggested Actions")
    suggest_actions_output = result.get("suggest_actions_output", {})
    actions = suggest_actions_output.get("actions", [])
    if actions:
        for action in actions:
            st.markdown(f"#### 🎯 {action.get('action', 'No action provided')}")
            st.write(f"- **Priority**: {action.get('priority', 'N/A')}")
            st.write(f"- **Rationale**: {action.get('rationale', 'N/A')}")
            st.write(f"- **Estimated Impact**: {action.get('estimated_impact', 'N/A')}")
            st.write(f"- **Feasibility Score**: {action.get('feasibility_score', 'N/A')}")
    else:
        st.write("No suggested actions available.")

    st.write(f"**Next Steps**: {suggest_actions_output.get('next_steps', 'N/A')}")

    # File download options
    st.markdown("### 💾 Download Options")
    download_format = st.radio("Choose download format", ["JSON", "Markdown"], key="download_format")

    if st.button("⬇️ Download File", key="download_file"):
        if download_format == "JSON":
            save_json(result)
        elif download_format == "Markdown":
            save_markdown(result)

# Save as JSON
def save_json(result):
    filtered_data = {key: value for key, value in result.items() if key != 'context'}
    json_result = json.dumps(filtered_data, indent=4)
    st.download_button(
        label="💾 Download JSON",
        data=json_result,
        file_name="result.json",
        mime="application/json",
        key="json_download_button"
    )

# Save as Markdown
def save_markdown(result):
    md_result = convert_to_markdown(result)
    st.download_button(
        label="📜 Download Markdown",
        data=md_result,
        file_name="result.md",
        mime="text/markdown",
        key="markdown_download_button"
    )

# Convert result to Markdown format
def convert_to_markdown(result):
    markdown_lines = []

    markdown_lines.append("# Summary Output")
    summary_output = result.get("summary_output", {})
    markdown_lines.append(f"**Summary**: {summary_output.get('summary', 'No summary available.')}")

    markdown_lines.append("## Key Points")
    for point in summary_output.get("key_points", []):
        markdown_lines.append(f"- {point.get('text', 'No text')} (Importance: {point.get('importance_score', 'N/A')})")

    markdown_lines.append(f"**Confidence Score**: {summary_output.get('confidence_score', 'N/A')}")
    markdown_lines.append(f"**Word Count**: {summary_output.get('word_count', 'N/A')}")
    markdown_lines.append(f"**Language Used**: {summary_output.get('language_used', 'N/A')}")

    markdown_lines.append("\n# Analysis Output")
    analysis_output = result.get("analysis_output", {})
    markdown_lines.append(f"**Sentiment**: {analysis_output.get('sentiment', 'N/A')}")
    markdown_lines.append(f"**Dominant Theme**: {analysis_output.get('dominant_theme', 'N/A')}")
    markdown_lines.append(f"**Linguistic Complexity**: {analysis_output.get('linguistic_complexity', 'N/A')}")
    markdown_lines.append(f"**Coverage Score**: {analysis_output.get('coverage_score', 'N/A')}")
    markdown_lines.append(f"**Contradictions Found**: {analysis_output.get('contradictions_found', 'N/A')}")
    markdown_lines.append(f"**Factual Accuracy Score**: {analysis_output.get('factual_accuracy_score', 'N/A')}")
    markdown_lines.append(f"**Tone Consistency**: {analysis_output.get('tone_consistency', 'N/A')}")
    markdown_lines.append(f"**Coherence Score**: {analysis_output.get('coherence_score', 'N/A')}")
    markdown_lines.append(f"**Summary Structure**: {analysis_output.get('summary_structure', 'N/A')}")
    markdown_lines.append(f"**Critical Points Covered**: {analysis_output.get('critical_points_covered', 'N/A')}")

    markdown_lines.append("\n# Suggested Actions")
    suggest_actions_output = result.get("suggest_actions_output", {})
    for action in suggest_actions_output.get("actions", []):
        markdown_lines.append(f"### {action.get('action', 'No action provided')}")
        markdown_lines.append(f"- **Priority**: {action.get('priority', 'N/A')}")
        markdown_lines.append(f"- **Rationale**: {action.get('rationale', 'N/A')}")
        markdown_lines.append(f"- **Estimated Impact**: {action.get('estimated_impact', 'N/A')}")
        markdown_lines.append(f"- **Feasibility Score**: {action.get('feasibility_score', 'N/A')}")

    markdown_lines.append(f"**Next Steps**: {suggest_actions_output.get('next_steps', 'N/A')}")

    return "\n".join(markdown_lines)

if __name__ == "__main__":
    main()
