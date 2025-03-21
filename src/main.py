import os
import warnings
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import DuckDuckGoSearchRun
from transformers import pipeline
from fpdf import FPDF
from datetime import datetime

# Suppress unnecessary warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class BlogGeneratorSystem:
    def __init__(self, api_key):
        # Using text generation pipeline with PyTorch backend
        self.generator = pipeline(
            "text-generation",
            model="EleutherAI/gpt-neo-125M",
            device=-1,
            framework="pt"  # Explicitly use PyTorch
        )
        self.search_tool = DuckDuckGoSearchRun()
        self.initialize_agents()
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(self.output_dir, exist_ok=True)

    def save_to_files(self, content, topic):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{topic.replace(' ', '_')}_{timestamp}"
        
        # Save as TXT
        txt_path = os.path.join(self.output_dir, f"{base_filename}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Save as PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split content into lines and add to PDF
        for line in content.split('\n'):
            pdf.multi_cell(0, 10, txt=line)
            
        pdf_path = os.path.join(self.output_dir, f"{base_filename}.pdf")
        pdf.output(pdf_path)
        
        return txt_path, pdf_path

    def generate_blog(self, topic):
        try:
            prompt = f"Write a blog post about {topic}:\n\n"
            
            # Generate text directly using the pipeline
            result = self.generator(
                prompt,
                max_length=512,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            
            # Extract generated text
            generated_text = result[0]['generated_text']
            cleaned_text = generated_text.replace(prompt, '')  # Remove the prompt from output
            
            # Save the generated content
            txt_path, pdf_path = self.save_to_files(cleaned_text, topic)
            return f"Blog post saved as:\nTXT: {txt_path}\nPDF: {pdf_path}"
            
        except Exception as e:
            return f"Error generating content: {str(e)}"

    def initialize_agents(self):
        """Initialize all agents"""
        pass  # We'll implement this after confirming basic functionality