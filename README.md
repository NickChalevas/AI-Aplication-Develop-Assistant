✨ GPT-4 Code GeneratorDescriptionThis application is a desktop tool built with PyQt5 that interfaces with the OpenAI GPT-4 API to generate Python code and accompanying README documentation based on user prompts. It features a modern, dark-themed user interface, allowing users to quickly generate, view, and save code and markdown files.FeaturesIntuitive UI: A clean and responsive user interface built with PyQt5.GPT-4 Integration: Utilizes the OpenAI GPT-4 model for powerful code and documentation generation.Dual Editors: Dedicated editor panels for displaying generated Python code and Markdown READMEs.Dark Theme: A visually appealing dark mode for comfortable coding.Code & README Generation: Generate both functional Python code and comprehensive README.md files from a single prompt.File Saving: Easily save generated code as .py files and documentation as README.md files.Real-time Status Updates: Provides feedback on generation progress and any errors encountered.InstallationTo run this application, you'll need Python installed on your system, along with a few libraries.Clone the repository (or download the file):git clone https://your-repo-link-here.git
cd gpt4-code-generator
(Replace https://your-repo-link-here.git with the actual repository URL if this project is hosted.)Install dependencies:pip install PyQt5 requests
Set up your OpenAI API Key:Obtain an API key from the OpenAI website.Important: The current code has a hardcoded API key (self.api_key). For production use, it's highly recommended to store your API key securely, preferably as an environment variable, rather than directly in the code.For example, you could modify the __init__ method to retrieve it like this:import os
# ...
class ModernGPT4Bot(QMainWindow):
    def __init__(self):
        # ...
        self.api_key = os.getenv("OPENAI_API_KEY", "YOUR_DEFAULT_OR_PLACEHOLDER_KEY")
        # ...
Then, set the environment variable before running:export OPENAI_API_KEY="sk-your-openai-api-key"
# On Windows (Command Prompt):
set OPENAI_API_KEY="sk-your-openai-api-key"
# On Windows (PowerShell):
$env:OPENAI_API_KEY="sk-your-openai-api-key"
UsageRun the application:python your_app_file_name.py
(Replace your_app_file_name.py with the actual name of the Python script containing the ModernGPT4Bot class.)Enter your prompt: In the input field at the top, type a clear and concise description of the code you want GPT-4 to generate (e.g., "create a simple to-do list application with a GUI using tkinter").Generate: Click the "🚀 Generate" button or press Enter.View Results: The generated Python code will appear in the "Generated Code" editor, and the corresponding README.md will appear in the "Generated README.md" editor.Save Files: Use the "💾 Save Code" and "📄 Save README.md" buttons to save the content to your local machine.DependenciesPython 3.xPyQt5: For the graphical user interface.requests: For making HTTP requests to the OpenAI API.LicenseThis project is licensed under the MIT License - see the LICENSE.md file for details.