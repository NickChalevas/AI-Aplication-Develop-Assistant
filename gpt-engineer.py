import sys
import requests
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, 
                             QSplitter, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor

class GeneratorSignals(QObject):
    code_generated = pyqtSignal(str)
    readme_generated = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    status_update = pyqtSignal(str)

class ModernGPT4Bot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ GPT-4 Code Generator")
        self.setGeometry(100, 100, 1200, 900)
        
        # API configuration
        # self.api_key = ""
        # self.api_url = "https://api.openai.com/v1/chat/completions"
        self.timeout = 150
        
        # Signals
        self.signals = GeneratorSignals()
        self.signals.code_generated.connect(self.update_code_editor)
        self.signals.readme_generated.connect(self.update_markdown_editor)
        self.signals.error_occurred.connect(self.show_error)
        self.signals.status_update.connect(self.update_status)
        
        self.monaco_font = self.load_monaco_font()
        self.init_ui()
        self.apply_dark_theme()
    
    def load_monaco_font(self):
        font_db = QFontDatabase()
        if 'Monaco' in font_db.families():
            return QFont('Monaco', 12)
        elif 'Consolas' in font_db.families():
            return QFont('Consolas', 12)
        else:
            font = QFont('Monospace', 12)
            font.setStyleHint(QFont.TypeWriter)
            return font
    
    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.Text, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Button, QColor(60, 60, 60))
        dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(dark_palette)
        
        self.setStyleSheet("""
            QSplitter::handle {
                background-color: #3d3d3d;
                height: 5px;
            }
            QStatusBar {
                background-color: #2d2d2d;
            }
        """)
    
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header
        header = QLabel("✨ GPT-4 Code Generator")
        header_font = QFont(self.monaco_font)
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #4fc3f7;")
        header.setAlignment(Qt.AlignCenter)
        
        # Prompt section
        prompt_frame = QFrame()
        prompt_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 5px;")
        prompt_layout = QVBoxLayout(prompt_frame)
        prompt_layout.setContentsMargins(10, 10, 10, 10)
        
        self.prompt_input = QLineEdit()
        self.prompt_input.setFont(QFont(self.monaco_font.family(), 12))
        self.prompt_input.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #4fc3f7;
            }
        """)
        self.prompt_input.setPlaceholderText("e.g., 'create a calculator with pyqt5'")
        self.prompt_input.returnPressed.connect(self.generate_code)
        
        generate_btn = QPushButton("🚀 Generate")
        generate_btn.setFont(QFont(self.monaco_font.family(), 11))
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4fc3f7;
                color: #000000;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #5fd3ff;
            }
            QPushButton:pressed {
                background-color: #3fb3e7;
            }
        """)
        generate_btn.clicked.connect(self.generate_code)
        
        prompt_layout.addWidget(self.prompt_input)
        prompt_layout.addWidget(generate_btn, 0, Qt.AlignRight)
        
        # Splitter for editors
        splitter = QSplitter(Qt.Vertical)
        
        # Code editor
        code_frame = QFrame()
        code_frame.setFrameShape(QFrame.StyledPanel)
        code_layout = QVBoxLayout(code_frame)
        code_layout.setContentsMargins(0, 0, 0, 0)
        
        code_label = QLabel("Generated Code")
        code_label.setFont(QFont(self.monaco_font.family(), 11))
        code_label.setStyleSheet("color: #aab2c0; padding: 5px 10px;")
        
        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont(self.monaco_font.family(), 13))
        self.code_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3a3a3a;
                border-radius: 0;
                padding: 10px;
                selection-background-color: #264f78;
            }
        """)
        self.code_editor.setPlaceholderText("Your generated code will appear here...")
        
        code_layout.addWidget(code_label)
        code_layout.addWidget(self.code_editor)
        
        # Markdown editor
        markdown_frame = QFrame()
        markdown_frame.setFrameShape(QFrame.StyledPanel)
        markdown_layout = QVBoxLayout(markdown_frame)
        markdown_layout.setContentsMargins(0, 0, 0, 0)
        
        markdown_label = QLabel("Generated README.md")
        markdown_label.setFont(QFont(self.monaco_font.family(), 11))
        markdown_label.setStyleSheet("color: #aab2c0; padding: 5px 10px;")
        
        self.markdown_editor = QTextEdit()
        self.markdown_editor.setFont(QFont(self.monaco_font.family(), 13))
        self.markdown_editor.setStyleSheet(self.code_editor.styleSheet())
        self.markdown_editor.setPlaceholderText("Your generated documentation will appear here...")
        
        markdown_layout.addWidget(markdown_label)
        markdown_layout.addWidget(self.markdown_editor)
        
        splitter.addWidget(code_frame)
        splitter.addWidget(markdown_frame)
        splitter.setSizes([500, 400])
        
        # Save buttons
        save_buttons = QFrame()
        save_buttons.setStyleSheet("background-color: transparent;")
        save_layout = QHBoxLayout(save_buttons)
        save_layout.setContentsMargins(0, 0, 0, 0)
        
        save_code_btn = QPushButton("💾 Save Code")
        save_code_btn.setFont(QFont(self.monaco_font.family(), 11))
        save_code_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border: 1px solid #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #1d1d1d;
            }
        """)
        save_code_btn.clicked.connect(self.save_code)
        
        save_md_btn = QPushButton("📄 Save README.md")
        save_md_btn.setFont(QFont(self.monaco_font.family(), 11))
        save_md_btn.setStyleSheet(save_code_btn.styleSheet())
        save_md_btn.clicked.connect(self.save_markdown)
        
        save_layout.addWidget(save_code_btn)
        save_layout.addStretch()
        save_layout.addWidget(save_md_btn)
        
        # Status bar
        self.status_bar = QLabel("Ready")
        self.status_bar.setFont(QFont(self.monaco_font.family(), 10))
        self.status_bar.setStyleSheet("color: #7a7a7a; padding: 5px;")
        self.status_bar.setAlignment(Qt.AlignRight)
        
        # Assemble main layout
        main_layout.addWidget(header)
        main_layout.addWidget(prompt_frame)
        main_layout.addWidget(splitter, 1)
        main_layout.addWidget(save_buttons)
        main_layout.addWidget(self.status_bar)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def generate_code(self):
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.signals.status_update.emit("⚠️ Please enter a prompt")
            return
            
        self.signals.status_update.emit("⌛ Generating with GPT-4...")
        self.code_editor.setPlainText("")
        self.markdown_editor.setPlainText("")
        QApplication.processEvents()
        
        # Start generation in separate threads
        threading.Thread(target=self.generate_code_thread, args=(prompt,), daemon=True).start()
        threading.Thread(target=self.generate_readme_thread, args=(prompt,), daemon=True).start()
    
    def generate_code_thread(self, prompt):
        try:
            code_prompt = f"""Please generate complete, functional Python code based on:
{prompt}

Requirements:
1. Provide ONLY the complete Python code
2. No explanations or comments outside the code
3. Include all necessary imports
4. Add # -*- coding: utf-8 -*- at the top
5. Ensure PEP 8 compliance"""
            
            response = self.call_api(code_prompt)
            self.signals.code_generated.emit(response)
            self.signals.status_update.emit("✨ Code generation complete!")
        except Exception as e:
            self.signals.error_occurred.emit(f"Code generation failed: {str(e)}")
    
    def generate_readme_thread(self, prompt):
        try:
            readme_prompt = f"""Create a professional README.md for a Python project that:
{prompt}

Include these sections:
# Project Title
## Description
## Features
## Installation
## Usage
## Dependencies
## License (MIT)

Format with proper Markdown syntax and make it comprehensive."""
            
            response = self.call_api(readme_prompt)
            self.signals.readme_generated.emit(response)
        except Exception as e:
            self.signals.error_occurred.emit(f"README generation failed: {str(e)}")
    
    def call_api(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,  # Lower for more deterministic code
            "max_tokens": 2500
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        if "error" in response.json():
            error_msg = response.json()["error"].get("message", "Unknown API error")
            raise Exception(f"API Error: {error_msg}")
            
        return response.json()["choices"][0]["message"]["content"]
    
    def update_code_editor(self, text):
        self.code_editor.setPlainText(text)
    
    def update_markdown_editor(self, text):
        self.markdown_editor.setPlainText(text)
    
    def show_error(self, message):
        self.signals.status_update.emit(f"❌ {message}")
    
    def update_status(self, message):
        self.status_bar.setText(message)
    
    def save_code(self):
        content = self.code_editor.toPlainText()
        if not content:
            self.signals.status_update.emit("⚠️ No code to save")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Python File",
            "",
            "Python Files (*.py);;All Files (*)",
            options=QFileDialog.Options()
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.signals.status_update.emit(f"💾 Code saved to {file_path}")
            except Exception as e:
                self.signals.status_update.emit(f"❌ Error saving file: {str(e)}")
    
    def save_markdown(self):
        content = self.markdown_editor.toPlainText()
        if not content:
            self.signals.status_update.emit("⚠️ No markdown to save")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            "README.md",
            "Markdown Files (*.md);;All Files (*)",
            options=QFileDialog.Options()
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.signals.status_update.emit(f"📄 Markdown saved to {file_path}")
            except Exception as e:
                self.signals.status_update.emit(f"❌ Error saving file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setStyle('Fusion')
    
    window = ModernGPT4Bot()
    window.show()
    sys.exit(app.exec_())