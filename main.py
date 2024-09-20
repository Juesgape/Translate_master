from src.batch_translation import process_translation
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    input_file = "data/test-file.csv"
    output_file = "data/translated_output.xlsx"
    
    process_translation(input_file, output_file, False)
