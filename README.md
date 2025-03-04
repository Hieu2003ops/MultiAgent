# Multi-Agent Article Research Assistant

An intelligent multi-agent system designed to streamline the research and writing process for articles on **Generative AI in Medicine and Education**. This project harnesses the power of CrewAI and Python to bring together four specialized agents that work collaboratively to generate high-quality, research-oriented content.

## Overview

This project leverages a multi-agent architecture where each of the four agents is assigned a distinct role in crafting comprehensive articles. By integrating advanced language models such as **Groq** and **OpenAI 40 mini**, the system ensures that every generated piece is not only relevant but also insightful. Designed with content creators, university students, and marketing professionals in mind, this tool is a game-changer for anyone looking to ideate, draft, or refine research articles.

## Key Features

- **Multi-Agent System:**  
  Four dedicated agents, each with its own specialty, collaborate to produce a complete research article.
  
- **CrewAI Framework:**  
  Robust design and orchestration of multi-agent workflows to ensure efficient and accurate task completion.
  
- **Advanced Language Models:**  
  Utilizes Groq and OpenAI 40 mini to generate and refine content with state-of-the-art AI capabilities.
  
- **Backend Integration:**  
  A FastAPI-powered backend paired with Ngrok for secure and public access.
  
- **Interactive Frontend:**  
  Streamlit-based user interface enhanced with CSS for an intuitive and visually appealing experience.

## System Architecture

The application is divided into three main components:

1. **Backend:**  
   Powered by FastAPI, this component launches a server that utilizes Ngrok to provide a public endpoint.
   
2. **Multi-Agent System:**  
   Built on the CrewAI framework, four specialized agents handle different aspects of article generation—from idea ideation and research aggregation to drafting and editing.
   
3. **Frontend:**  
   An interactive interface built using Streamlit and custom CSS that connects to the backend via the Ngrok port, providing real-time access and interaction.

## Installation and Setup

### Prerequisites

- **Python 3.x** installed on your system.
- **Ngrok Account:** Sign up for Ngrok to secure a public tunnel.
- Required Python packages (listed in `requirements.txt`).

### Installation Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/multi-agent-article-research-assistant.git
   cd multi-agent-article-research-assistant
