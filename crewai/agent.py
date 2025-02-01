from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import Agent
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv
import os
import yaml


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


# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables
open_ai_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# print(open_ai_key)

if not open_ai_key or not groq_api_key:
    raise EnvironmentError("Missing API keys in the .env file. Please check your configuration.")

# Define configuration directory
base_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(base_dir, "../config")

# Load agent configuration
agent_config = load_yaml_config(config_dir, "agents.yaml")

# Initialize LLMs
llm = ChatOpenAI(model="gpt-4o-mini", api_key=open_ai_key)
groq_llm = ChatGroq(model="groq/llama-3.1-70b-versatile", api_key=groq_api_key, temperature=0.7)

# Create Agents
agents = {
    "research_specialist_agent": Agent(
        config=agent_config.get('research_specialist_agent', {}),
        tools=[ScrapeWebsiteTool()],
        llm=llm
    ),
    "blog_writer_agent": Agent(
        config=agent_config.get('blog_writer_agent', {}),
        llm=llm
    ),
    "content_editor_agent": Agent(
        config=agent_config.get('content_editor_agent', {}),
        llm=llm
    ),
    "quality_reviewer_agent": Agent(
        config=agent_config.get('quality_reviewer_agent', {}),
        llm=llm
    )
}

if __name__ == "__main__":
    print("Agents initialized successfully:", agents)
