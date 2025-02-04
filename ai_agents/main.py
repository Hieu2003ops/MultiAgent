from dotenv import load_dotenv
import os
from agent import agents
from task import create_tasks, task_config
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from IPython.display import display, Markdown

# Load environment variables
load_dotenv()

# Fetch API keys
open_ai_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not open_ai_key or not groq_api_key:
    raise EnvironmentError("Missing API keys in the .env file. Please check your configuration.")

# Initialize language models
llm = ChatOpenAI(model="gpt-4o-mini", api_key=open_ai_key)
groq_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api_key, temperature=0.7)

# Function to run CrewAI pipeline
def run_crewai_pipeline(topic):
    tasks = create_tasks(task_config)  # Ensure tasks are initialized

    content_creation_crew = Crew(
        agents=[
            agents["research_specialist_agent"],
            agents["blog_writer_agent"],
            agents["content_editor_agent"],
            agents["quality_reviewer_agent"]
        ],
        tasks=tasks,
        manager_llm=llm,
        process=Process.hierarchical,
        verbose=True,
    )

    # Run the pipeline
    result = content_creation_crew.kickoff(inputs={'topic': topic})

    # Process result
    markdown_result = f"# CrewAI Output\n\n{str(result)}"

    # Save output to Markdown file
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline_result.md")
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_result)

    return markdown_result, output_path

# Test if running directly
if __name__ == "__main__":
    test_topic = "The Role of AI in Modern Education"
    output, file_path = run_crewai_pipeline(test_topic)
    print("Generated Content:", output)
    print("Markdown File Saved at:", file_path)
