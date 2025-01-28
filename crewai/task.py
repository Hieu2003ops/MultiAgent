from crewai import Task
import agent  # Import agents from agent.py
from dotenv import load_dotenv  # Import load_dotenv for environment variables
import yaml
import os
from pydantic import BaseModel, Field
from typing import List

# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables
open_ai_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not open_ai_key or not groq_api_key:
    raise EnvironmentError("Missing API keys in the .env file. Please check your configuration.")

# Define structured output for the quality review task
class SocialMediaPost(BaseModel):
    platform: str = Field(..., description="The social media platform where the post will be published (e.g., Twitter, LinkedIn).")
    content: str = Field(..., description="The content of the social media post, including any hashtags or mentions.")

class ContentOutput(BaseModel):
    article: str = Field(..., description="The article, formatted in markdown.")
    social_media_posts: List[SocialMediaPost] = Field(..., description="A list of social media posts related to the article.")

# Function to load YAML configuration
def load_yaml_config(config_dir, file_name):
    """Load a YAML configuration file."""
    try:
        with open(os.path.join(config_dir, file_name), "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except yaml.YAMLError as e:
        print(f"YAML Error: {e}")
        raise

# Define configuration directory
base_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(base_dir, "../config")

# Load task configuration
task_config = load_yaml_config(config_dir, "tasks.yaml")

if not task_config:
    raise ValueError("Error: task_config is empty. Check tasks.yaml!")

# Create tasks
def create_tasks(task_config):
    """
    Create Crew AI tasks and connect them with agents.

    Args:
        task_config (dict): Configuration for tasks loaded from YAML.

    Returns:
        list: List of Crew AI tasks.
    """
    research_specialist_task = Task(
        config=task_config['research_task'],
        agent=agent.agents["research_specialist_agent"]  # Updated key name
    )

    writing_task = Task(
        config=task_config['writing_task'],
        agent=agent.agents["blog_writer_agent"]  # Updated key name
    )

    editing_task = Task(
        config=task_config['editing_task'],
        agent=agent.agents["content_editor_agent"]  # Updated key name
    )

    quality_review_task = Task(
        config=task_config['quality_review_task'],
        agent=agent.agents["quality_reviewer_agent"],  # Updated key name
        output_pydantic=ContentOutput
    )

    return [research_specialist_task, writing_task, editing_task, quality_review_task]

if __name__ == "__main__":
    # Debugging: Print raw task configuration loaded from YAML
    print("\nDebugging: Loaded task configuration (raw):")
    print(task_config)