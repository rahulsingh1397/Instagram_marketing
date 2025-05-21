#!/usr/bin/env python
import sys
import os
import warnings
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
import datetime

# Suppress all warnings
warnings.filterwarnings("ignore")

# --- .env file loading --- 
# Project root is considered e:\Projects\Python\Instagram_marketing
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
print(f"[MAIN_DEBUG] Attempting to load .env file from: {env_path}")

# Load .env file into a dictionary
dotenv_map = dotenv_values(env_path)
print(f"[MAIN_DEBUG] Content read from .env by dotenv_values: {dotenv_map}")

# Load environment variables
load_dotenv(env_path)

# Debug: Print all environment variables that start with OPENAI
print("\n[DEBUG] Current OPENAI environment variables:")
for key, value in os.environ.items():
    if key.startswith('OPENAI'):
        masked_value = value[:10] + '...' + value[-4:] if len(value) > 15 else '***REDACTED***'
        print(f"{key} = {masked_value}")

# Clear any existing environment variables that might interfere
for key in list(os.environ.keys()):
    if key.startswith(('OPENAI_', 'ANTHROPIC_', 'GEMINI_', 'SERPER_', 'MODEL')):
        os.environ.pop(key, None)
        print(f"[MAIN_DEBUG] Removed environment variable: {key}")

# Explicitly set only the environment variables we need
os.environ['GEMINI_API_KEY'] = dotenv_map.get('GEMINI_API_KEY', '')
os.environ['SERPER_API_KEY'] = dotenv_map.get('SERPER_API_KEY', '')
os.environ['MODEL'] = dotenv_map.get('MODEL', 'gemini-pro')

print(f"[MAIN_DEBUG] Using Gemini model: {os.getenv('MODEL')}")
print(f"[MAIN_DEBUG] GEMINI_API_KEY set: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
print(f"[MAIN_DEBUG] SERPER_API_KEY set: {'Yes' if os.getenv('SERPER_API_KEY') else 'No'}")

# Verify Gemini API key is loaded
if not os.getenv('GEMINI_API_KEY'):
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

# --- End .env file loading ---

# Import after environment is set up
from instagram.crew import InstagramCrew

def run():
    """
    Run the crew.
    """
    # Get user inputs
    inputs = {
        'current_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'instagram_description': input("Enter the Instagram description here: "),
        'topic_of_the_week': input("Enter the topic of the week here: ")
    }
    
    print("[MAIN_INFO] Starting crew kickoff...")
    try:
        # Create the crew, set inputs, and kickoff
        crew = InstagramCrew()
        crew.set_inputs(inputs)
        crew.crew().kickoff()
        print("[MAIN_INFO] Crew kickoff completed successfully.")
    except Exception as e:
        print(f"[MAIN_ERROR] An error occurred during crew kickoff: {e}")
        # Uncomment the line below to see the full traceback for debugging
        # raise


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        InstagramCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        InstagramCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        InstagramCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
