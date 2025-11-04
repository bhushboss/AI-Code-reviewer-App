# AI-Code-reviewer-App
 Analyze and improve code quality automatically. Tools: flake8, black, radon, Streamlit  1.Accept code input via UI or upload. 2.Analyze style using flake8 and black. 3.Measure complexity with radon. 4.Summarize improvements needed. 5.Display before/after suggestions. 6.Export a report. Deliverables: Streamlit app, sample code analysis report

Here is a complete README.md file for your Git repository, tailored to the "AI Code Reviewer" project we just built.
You can copy and paste this directly into a file named README.md in your project's root directory.

🤖 Python Code Reviewer
An automated AI-powered code reviewer built with Streamlit. This tool analyzes your Python code for style errors, formatting, and complexity, helping you improve code quality automatically.
✨ Features
 * Code Input: Paste your code directly or upload a .py file.
 * Style Analysis: Uses flake8 to find linting errors, style violations (like PEP 8), and logical errors.
 * Code Formatting: Uses black to show a "before and after" view of your code, formatted for consistency.
 * Complexity Metrics: Uses radon to measure Cyclomatic Complexity and provide raw metrics like LOC (Lines of Code).
 * Summary Dashboard: View key metrics (LOC, Avg. Complexity) at a glance.
 * Export Report: Download a complete analysis as a Markdown (.md) file.
🛠️ Technology Stack
 * Streamlit: For the interactive web UI.
 * flake8: For style and error linting.
 * black: For "uncompromising" code formatting.
 * radon: For code complexity (Cyclomatic Complexity, LOC, etc.) analysis.
🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.
Prerequisites
You need to have Python 3.7+ installed.
Installation
 * Clone the repository
 * Create a virtual environment:
   # On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate

 * Install the required libraries:
   You can install them directly from the command line:
   pip install streamlit flake8 black radon

   Or, create a requirements.txt file with the contents below and run pip install -r requirements.txt:
   # requirements.txt
streamlit
flake8
black
radon

🏃 How to Use
 * Run the Streamlit app from your terminal:
   streamlit run app.py

 * Your browser will automatically open to the app (usually at http://localhost:8501).
 * Upload your .py file or paste your code into the text area.
 * Click the "Analyze Code" button.
 * Review your results! You can see the formatted code, style issues, complexity report, and download the full analysis.
