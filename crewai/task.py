from crewai import Task
import agent  # Import agents from agent.py
from dotenv import load_dotenv  # Import load_dotenv for environment variables
import yaml
import os
from pydantic import BaseModel, Field
from typing import List
from output_schema import ContentOutput, SocialMediaPost


# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables
open_ai_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not open_ai_key or not groq_api_key:
    raise EnvironmentError("Missing API keys in the .env file. Please check your configuration.")

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

# Debug: In nội dung task_config
print("Debugging task_config:", task_config)

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
        config=task_config.get('research_task', None),
        agent=agent.agents.get("research_specialist_agent", None)
    )

    writing_task = Task(
        config=task_config.get('writing_task', None),
        agent=agent.agents.get("blog_writer_agent", None)
    )

    editing_task = Task(
        config=task_config.get('editing_task', None),
        agent=agent.agents.get("content_editor_agent", None)
    )

    quality_review_task = Task(
        config=task_config.get('quality_review_task', None),
        agent=agent.agents.get("quality_reviewer_agent", None),
        # output_pydantic=ContentOutput
    )
    # Debugging output_pydantic assignment
    print("Debugging quality_review_task output_pydantic:", quality_review_task.output_pydantic)

    return [research_specialist_task, writing_task, editing_task, quality_review_task]

if __name__ == "__main__":
    # Debugging: Kiểm tra task_config đã load đúng chưa
    print("\nDebugging: Loaded task configuration (raw):")
    print(task_config)

    # Tạo danh sách task và debug từng task
    tasks = create_tasks(task_config)
    print("\nDebugging: Created tasks with output_pydantic:")
    for task in tasks:
        task_name = task.config.get('name', 'Unnamed Task') if task.config else "Config is None"
        output_type = task.output_pydantic if hasattr(task, 'output_pydantic') else "No output_pydantic"
        print(f"Task: {task_name}, Output Type: {output_type}")
