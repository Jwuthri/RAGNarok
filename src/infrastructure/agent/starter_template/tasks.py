from crewai import Task
from textwrap import dedent


class CustomTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $1,000 commission!"

    def task_1_name(self, agent, question, company_name):
        return Task(
            description=dedent(
                f"""
## Context:
Based on the given question {question} you need to find relevant information to answer this quuestion. Remember the question are suppose to be about {company_name}
{self.__tip_section()}
                """
            ),
            expected_output="interesting information about {company_name}",
            agent=agent,
        )

    def task_2_name(self, agent):
        return Task(
            description=dedent(
                f"""
## Instructions:
  * You respond to queries in the language in which they are asked.
  * Retain technical jargon or specific terms (e.g., "feature flag") in English to maintain clarity and precision.
  * Answer Extraction: Utilize only the information provided in the Input to formulate an answer.
  * No Information Present: If the required information to answer the question is absent from the Input, respond with idk.
  * Accuracy and Specificity: Refrain from inferring or assuming details not explicitly stated in the Input.
  * Error Correction: Correct any spelling and grammatical errors when quoting directly from the Input.
  * Elastic Answer: If the question hints at a desired length, follow that hint, Otherwise, use under 250 words
  * Answer formatting: You MUST ALWAYS format 'text' with bullet points. If there are several points, incorporate bold subheadings for each point
{self.__tip_section()}
                """
            ),
            expected_output=dedent(
                """
## Expected Output Format: json[str, str]
The response should be in JSON format with the following structure:
{
    "confidence": int "A confidence level from 0 to 2 reflecting the answer's support in the Input.",
    "answer": str "is a markdown string.",
    "summary": str "is a summary of 'text' in under 20 words."
}
The confidence level should reflect the certainty about the answer:
    This can be 0, 1, or 2:
    0: Low confidence; the question cannot be fully addressed with the provided Input
    1: Partial confidence; the question can be partially answered with the provided Input
    2: Full confidence; the question can be directly answered using information with the provided Input
            """
            ),
            agent=agent,
        )
