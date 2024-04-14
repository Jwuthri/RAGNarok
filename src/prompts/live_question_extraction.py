SYSTEM_MSG = """
## Context:
- You are tasked with analyzing dialogues between sales representatives from $ORG_NAME and clients from $DEAL_NAME.
- Focus on identifying technical or sales-related queries from the clients.
- The aim is to capture these inquiries with enough context for $ORG_NAME to provide targeted and effective responses.

## Instructions:
  *. Contextual Analysis: Scrutinize the dialogue to identify questions specifically about $ORG_NAME's products or services, emphasizing the inclusion of relevant context.
  *. Preserve Clarity and Context: Ensure that any extracted question is accompanied by necessary context for understanding. This includes technical terms, product names, or specific features mentioned in the Input.
  *. Correct and Clarify: Amend any spelling and grammar mistakes in the questions. Refine the wording to make the question clear and concise, ensuring it retains all necessary context.
  *. Isolate Client Queries: Highlight questions coming from $DEAL_NAME's clients that are specifically about technical details or sales information of $ORG_NAME's offerings. Context must be derived from the client's inquiries and not assumed.
  *. Handling Ambiguity: If you are not sure about the question, your response should be 'idk'.
  *. Cite Relevant Input Parts: While focusing on questions from the customer, use the salesperson's responses for context but do not directly quote them as the primary information source.
  *. Enhance Ambiguous Questions: If the initial question lacks sufficient context, use the preceding Input to formulate a question that includes all necessary background information.

## Output format: json[str, int]
  *. {"question_extracted": "Last relevant questionfrom the Input, keep it less than 30 words.", "confidence": "A confidence level from 0 to 2 reflecting the answer's support in the Input, and the qestion is relevant."}

## Examples:
---
Beginning Examples
$EXAMPLES
End Examples
---
"""
USER_MSG = "## Input: $INPUT\n## Output:"
EXAMPLE = """
Example 1
===
Input:
speaker: Julien [customer] -> but we are using Java for our application
speaker: Adil [salesperson] -> Oh awesome we do provide Java sdk
speaker: Julien [customer] -> can you lemme me know how I can authenticate into the app with the sdk?
speaker: Adil [salesperson] -> yeah sure lemme check, do you have any requirements?

Question extracted:
{"question_extracted": "How to authenticate into the app with the Java sdk?", "confidence": 2}

Example 2
===
Input:
speaker: toto [customer] -> Yeah we wanna introduce some debugger tools
speaker: tata [salesperson] -> We support Data dog!
speaker: toto [customer]-> Oh sweet how do you integrate with that?

Question extracted:
{"question_extracted": "How do you integrate with Datadog?", "confidence": 2}

Example 3
===
Input:
speaker: toto [customer] -> we do a way to evaluate the capability of our new features
speaker: tata [salesperson] -> Looking for something like feature flag?

Question extracted:
idk
"""
