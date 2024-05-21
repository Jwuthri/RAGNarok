from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI


from langchain.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()


class CustomAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.01)

    def agent_1_name(self):
        return Agent(
            role="Research Analyst",
            backstory=dedent(f"""Define agent 1 backstory here"""),
            goal=dedent(
                f"""Analyze the company website and provided description to extract insights on culture, values, and specific needs."""
            ),
            tools=[search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def agent_2_name(self):
        return Agent(
            role="Answer writer",
            backstory=dedent(f"""Skilled in crafting compelling answer to question"""),
            goal=dedent(f"""Use insights from the Research Analyst to answer any given question."""),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )
