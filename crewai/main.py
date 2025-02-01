from dotenv import load_dotenv
import os
from agent import agents  # Import agents from agent.py
from task import create_tasks, task_config  # Import task functions and output structure
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from IPython.display import display, Markdown
from output_schema import ContentOutput  # Import ContentOutput từ output_schema.py

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

# Define topic for the content pipeline
topic = "How to apply Generative AI Into Personalized Study With Some Science Subjects in Universities"

# Create tasks
tasks = create_tasks(task_config)  # Ensure tasks are initialized

# Creating Crew
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
    # output_pydantic=ContentOutput,
    verbose=True,
)

# Run Crew AI pipeline
result = content_creation_crew.kickoff(inputs={'topic': topic})

# Debugging result type and content
print("Debugging result type:", type(result))
print("Debugging result content:", result)

markdown_result = f"# CrewAI Output\n\n{str(result)}"

# Hiển thị Markdown trên giao diện
display(Markdown(markdown_result))

# Lưu kết quả vào file Markdown
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline_result.md")
with open(output_path, "w", encoding="utf-8") as md_file:
    md_file.write(markdown_result)

print("✅ Pipeline execution result saved to:", output_path)
