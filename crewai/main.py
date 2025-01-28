# from dotenv import load_dotenv
# import os
# from agent import agents  # Importing the agents from agent.py
# from task import create_tasks, task_config  # Importing the task creation function from task.py
# from crewai import Crew, Process
# from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq

# # Load environment variables from .env file
# load_dotenv()

# # Fetch API keys from environment variables
# open_ai_key = os.getenv("OPENAI_API_KEY")
# groq_api_key = os.getenv("GROQ_API_KEY")

# llm = ChatOpenAI(model="gpt-4o-mini", api_key=open_ai_key)
# groq_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api_key, temperature=0.7)

# if not open_ai_key or not groq_api_key:
#     raise EnvironmentError("Missing API keys in the .env file. Please check your configuration.")

# # Define the topic for the content pipeline
# topic = "How to apply Generative AI Into Personalized Study With Some Science Subjects in Universities"

# # Create tasks
# tasks = create_tasks(task_config)  # Ensure tasks are initialized

# # Creating Crew
# content_creation_crew = Crew(
#     agents=[
#         agents["research_specialist_agent"],
#         agents["blog_writer_agent"],
#         agents["content_editor_agent"],
#         agents["quality_reviewer_agent"]
#     ],
#     tasks=tasks,
#     manager_llm=llm,
#     process=Process.hierarchical,
#     verbose=True
# )

# # Run Crew AI pipeline
# print("Starting the Crew AI pipeline...")
# result = content_creation_crew.kickoff(inputs={
#     'topic': topic
# })

# # Write the result to a markdown file in the crewai folder
# output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crewai")
# os.makedirs(output_dir, exist_ok=True)
# output_file_path = os.path.join(output_dir, "pipeline_result.md")

# with open(output_file_path, "w") as md_file:
#     md_file.write(f"# Pipeline Execution Result\n\n{result}")

# print("Pipeline execution result written to:", output_file_path)












from dotenv import load_dotenv
import os
from agent import agents  # Importing the agents from agent.py
from task import create_tasks, task_config  # Importing the task creation function from task.py
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from IPython.display import display, Markdown

# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables
open_ai_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", api_key=open_ai_key)
groq_llm = ChatGroq(model="groq/llama-3.1-70b-versatile", api_key=groq_api_key, temperature=0.7)

if not open_ai_key or not groq_api_key:
    raise EnvironmentError("Missing API keys in the .env file. Please check your configuration.")

# Define the topic for the content pipeline
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
    process=Process.sequential,
    verbose=True
)

# Run Crew AI pipeline
result = content_creation_crew.kickoff(inputs={
    'topic': topic
})

# Display the final article output
display(Markdown(result.dict()['article']))

# Write the article content to a markdown file in the crewai folder
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crewai")
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, "pipeline_result.md")

with open(output_file_path, "w") as md_file:
    md_file.write(f"# Pipeline Execution Result\n\n{result.dict()['article']}")