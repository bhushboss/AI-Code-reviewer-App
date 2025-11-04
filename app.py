import streamlit as st
import subprocess
import tempfile
import os
from radon.raw import analyze as radon_raw
from radon.metrics import cc_visit

# Helper function to run flake8
def run_flake8(code_string):
    """Runs flake8 on a code string and returns the output."""
    # Use a temporary file to run flake8, as it works on files
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.py') as temp_file:
        temp_file.write(code_string)
        file_path = temp_file.name
    
    # Run flake8 using subprocess
    try:
        process = subprocess.run(
            ['flake8', file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Clean up the temp file
        os.unlink(file_path)
        
        if process.stdout:
            # Re-format output to remove the temp file's random name
            return process.stdout.replace(file_path, 'your_code.py')
        else:
            return "✅ All clear! No style issues found."
    except Exception as e:
        os.unlink(file_path) # Ensure cleanup on error
        return f"Error running flake8: {e}"

# Helper function to run black
def run_black(code_string):
    """Runs black on a code string and returns the formatted code."""
    try:
        process = subprocess.run(
            ['black', '-'],
            input=code_string,
            capture_output=True,
            text=True,
            timeout=10
        )
        if process.stderr:
            return f"Error running black: {process.stderr}"
        return process.stdout
    except Exception as e:
        return f"Error running black: {e}"

# Helper function to run radon
def run_radon(code_string):
    """Runs radon on a code string and returns complexity metrics."""
    try:
        # 1. Raw Metrics (LOC, LLOC, etc.)
        raw_analysis = radon_raw(code_string)
        report = f"**Raw Metrics:**\n"
        report += f"- Lines of Code (LOC): {raw_analysis.loc}\n"
        report += f"- Logical Lines of Code (LLOC): {raw_analysis.lloc}\n"
        report += f"- Source Lines of Code (SLOC): {raw_analysis.sloc}\n"
        report += f"- Comment Lines: {raw_analysis.comments}\n"
        report += f"- Single-line Comments: {raw_analysis.single_comments}\n"
        report += f"- Blank Lines: {raw_analysis.blank}\n\n"
        
        # 2. Cyclomatic Complexity
        report += "**Cyclomatic Complexity:**\n"
        complexity_results = cc_visit(code_string)
        
        total_complexity = 0
        func_count = 0
        
        if not complexity_results:
            report += "- No functions/methods found.\n"
        
        for item in complexity_results:
            item_type = item.type.capitalize()
            rank = item.rank() # A-F grade
            report += f"- **{item_type} `{item.name}`**: Complexity: **{item.complexity}** (Rank: **{rank}**)\n"
            if item.type == 'function' or item.type == 'method':
                total_complexity += item.complexity
                func_count += 1
                
        avg_complexity = (total_complexity / func_count) if func_count > 0 else 0
        
        # Return both the formatted report and the summary stats
        summary = {
            "loc": raw_analysis.loc,
            "lloc": raw_analysis.lloc,
            "avg_complexity": f"{avg_complexity:.2f}",
            "func_count": func_count
        }
        
        return report, summary
        
    except Exception as e:
        return f"Error running radon: {e}", {}

# --- Streamlit App UI ---

st.set_page_config(page_title="Python Code Reviewer", layout="wide")
st.title("🤖 Python Code Reviewer")
st.write("Analyze your Python code for style, formatting, and complexity.")

# 1. Accept code input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload or Paste Code")
    uploaded_file = st.file_uploader("Upload a Python file (.py)", type="py")
    
    st.write("Or paste your code below:")
    code_input = st.text_area("Code", height=400, placeholder="def hello():\n  print('Hello World')")

    analyze_button = st.button("Analyze Code")

# Initialize session state to hold results
if 'report' not in st.session_state:
    st.session_state.report = ""

# --- Analysis Logic ---
if analyze_button:
    # Determine which code source to use
    if uploaded_file is not None:
        original_code = uploaded_file.getvalue().decode("utf-8")
    else:
        original_code = code_input

    if not original_code.strip():
        st.error("Please upload a file or paste some code to analyze.")
    else:
        with st.spinner("Analyzing code... This may take a moment."):
            # 2. Analyze style (flake8)
            flake8_report = run_flake8(original_code)
            
            # 5. Get "after" suggestions (black)
            formatted_code = run_black(original_code)
            
            # 3. Measure complexity (radon)
            radon_report, radon_summary = run_radon(original_code)
            
            # --- Build the final downloadable report ---
            report_lines = []
            report_lines.append("# Code Analysis Report\n")
            
            # 4. Summarize improvements
            report_lines.append("## 📊 Summary\n")
            report_lines.append(f"* **Total Lines of Code (LOC):** {radon_summary.get('loc', 'N/A')}")
            report_lines.append(f"* **Logical Lines of Code (LLOC):** {radon_summary.get('lloc', 'N/A')}")
            report_lines.append(f"* **Functions/Methods Found:** {radon_summary.get('func_count', 'N/A')}")
            report_lines.append(f"* **Average Complexity:** {radon_summary.get('avg_complexity', 'N/A')}\n")

            report_lines.append("## 🎨 Style Report (flake8)\n")
            report_lines.append("```")
            report_lines.append(flake8_report)
            report_lines.append("```\n")
            
            report_lines.append("## 🔬 Complexity Report (radon)\n")
            report_lines.append(radon_report)
            
            report_lines.append("## ✨ Recommended Formatting (black)\n")
            report_lines.append("```python")
            report_lines.append(formatted_code)
            report_lines.append("```")
            
            # Store report in session state
            st.session_state.report = "\n".join(report_lines)
            st.session_state.original_code = original_code
            st.session_state.formatted_code = formatted_code
            st.session_state.flake8_report = flake8_report
            st.session_state.radon_report = radon_report
            st.session_state.radon_summary = radon_summary

# --- Display Results ---
with col2:
    st.subheader("Analysis Results")
    if not st.session_state.report:
        st.info("Results will be displayed here after analysis.")
    else:
        # 4. Summarize improvements
        st.markdown("**Summary Metrics**")
        summary = st.session_state.radon_summary
        metric_cols = st.columns(4)
        metric_cols[0].metric("Total LOC", summary.get('loc', 'N/A'))
        metric_cols[1].metric("Logical LOC", summary.get('lloc', 'N/A'))
        metric_cols[2].metric("Functions", summary.get('func_count', 'N/A'))
        metric_cols[3].metric("Avg. Complexity", summary.get('avg_complexity', 'N/A'))

        # 5. Display before/after suggestions
        st.markdown("**Code Formatting (Before vs. After)**")
        
        b_col, a_col = st.columns(2)
        with b_col:
            st.text("Before (Original)")
            st.code(st.session_state.original_code, language="python")
        with a_col:
            st.text("After (Formatted by Black)")
            st.code(st.session_state.formatted_code, language="python")
            
        # Display detailed reports
        with st.expander("Show Style Report (flake8)"):
            st.code(st.session_state.flake8_report, language="bash")

        with st.expander("Show Complexity Report (radon)"):
            st.markdown(st.session_state.radon_report)

        # 6. Export a report
        st.download_button(
            label="Export Full Report (.md)",
            data=st.session_state.report,
            file_name="code_analysis_report.md",
            mime="text/markdown",
      )
      
