import os
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool
import streamlit as st

os.environ['OPENAI_MODEL_NAME'] = st.secrets["OPENAI_MODEL_NAME"]
os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]

def get_crew():
    # Create a new instance of the WebsiteSearchTool
    # Set the base URL of a website, e.g., "https://example.com/", so that the tool can search for sub-pages on that website
    tool_websearch = WebsiteSearchTool()

    # Creating Agents
    agent_planner = Agent(
        role="Content Planner",
        goal="Plan factually accurate content on software and infrastructure security on topic: {topic}",
        backstory="""You're working on guiding a junior developer on how to identify and avoid common software and infrastructure vulnerabilities caused by misconfigurations regarding topic: {topic}.
        You collect information that helps the junior developer learn something about the topic and make informed decisions.
        
        Your task is to plan for a guide that will ultimately have the following markdown format:
        
        1. <common misconfiguration 1>
            - Description of misconfiguration and the potential vulnerability.
            - How to identify if the misconfiguration is made.
            - How to rectify the misconfiguration
        """,
        # Your work is the basis for the Content Writer to write an article on this topic.""", <-- This line is removed.
        tools=[tool_websearch],
        allow_delegation=False, # <-- This is now set to False
        verbose=False,
    )

    agent_writer = writer = Agent(
        role="Content Writer",
        goal="Write insightful and factually accurate step by step guide on how a junior developer can avoid common software and infrastructure vulnerabilities due to misconfigurations regarding the topic: {topic}",

        backstory="""You're working on a writing step by step guide on the following topic: {topic}
        You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic.
        You follow the main objectives and direction of the outline as provide by the Content Planner.""",

        allow_delegation=False, 
        verbose=False, 
    )

    # Creating Tasks
    task_plan = Task(
        description="""\
        1. Prioritize the common software and infrastructure misconfigurations that can lead to serious vulnerabilities regarding topic: {topic}.
        2. Identify the what are the necessary steps to identify if such misconfigurations occured and how to fix them.
        3. Develop a detailed content outline, including introduction, key points.""",

        expected_output="""\
        A comprehensive content plan document with step by step guide to help a junior developer identify possible common misconfigurations and rectify them.""",
        agent=agent_planner,
    )

    task_write = Task(
        description="""\
        1. Use the content plan to craft an easy to understand step by step guide on {topic}, teaching a junior developer how to identify potential security vulnerabilities due to misconfigurations.
        2. Ensure that each potential misconfiguration is structured such that the reader can understand the seriousness of the issue, how to identify if he made the misconfiguration and how to rectify it.
        3. Go into more detail on specific steps to identify the issue and to rectify the misconfiguration.
        4. Proofread for grammatical errors and alignment the common style used in tech blogs.""",

        expected_output="""
        A well-written guide in markdown format with the following content structure:
        1. <common misconfiguration 1>
            - Description of misconfiguration and the potential vulnerability.
            - How to identify if the misconfiguration is made.
            - How to rectify the misconfiguration
        """,
        agent=agent_writer,
    )

    # Creating the Crew
    crew = Crew(
        agents=[agent_planner, agent_writer],
        tasks=[task_plan, task_write],
        verbose=False
    )

    return crew

def crewai_prompt(input: str):
    crew = get_crew()
    result = crew.kickoff(inputs={"topic": input})
    return result.raw