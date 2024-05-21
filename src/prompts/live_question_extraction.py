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
{"answer": "Last relevant questionfrom the Input, keep it less than 30 words.", "confidence": "A confidence level from 0 to 2 reflecting the answer's support in the Input, and the qestion is relevant."}
If you cannot determine an answer from the provided Input, respond with: idk

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
## Input:
speaker: customer -> but we are using Java for our application
speaker: salesperson -> Oh awesome we do provide Java sdk
speaker: customer -> can you lemme me know how I can authenticate into the app with the sdk?
speaker: salesperson -> yeah sure lemme check, do you have any requirements?
## Output:
{"answer": "How to authenticate into the app with the Java sdk?", "confidence": 2}

Example 2
===
## Input:
speaker: customer -> Yeah we wanna introduce some debugger tools
speaker: salesperson -> We support Data dog!
speaker: customer-> Oh sweet how do you integrate with that?
## Output:
{"answer": "How do you integrate with Datadog?", "confidence": 2}

Example 3
===
## Input:
speaker: customer -> we do a way to evaluate the capability of our new features
speaker: salesperson -> Looking for something like feature flag?
## Output:
idk
"""
INPUT = """
### Speaker: Mike Parker [customer]: Good. I'm doing well. Thanks for being so patient with this, this meeting. I'm glad we've finally reconnected.
### Speaker: Adil Aijaz [salesperson]: No worries at all. This is just like, uh, I totally understand you are, uh, at a public company, a lot of stuff happens. It's uh, I totally understand. How's the quarter going so far?
### Speaker: Mike Parker [customer]: Yeah, it's been good. Um, yeah, we, I think we IPOed in September and so. We had that, uh, we had, uh, I guess that was partially Q3. We just finished up Q4, you know? And so. Um, yeah, it's been good. It's like, um, going public means that forecastability is, you know, pretty critical and. There's you know, a little bit more deal inspection and so forth, but it's been fun.
### Speaker: Adil Aijaz [salesperson]: It's uh, your C F O becomes a lot more. I mean, it becomes seriously important at that stage. Because you really need that, you know, this is the number and then exceed the expectations, things like that. And I'm sure the pressure on the sales org is, is unreal.
### Speaker: Mike Parker [customer]: Yeah. I mean, you know, there is pressure. Fortunately, we have like a pretty good. Engine overall. So, um, you know, but yeah, you're right. Like. You wanna, when you, when you have to read out to the street, there's a little bit of a different dynamic than just, you know, kind of, uh, uh, moving along and, and, you know, focus on. In internal stakeholders. So how are things going with you?
### Speaker: Adil Aijaz [salesperson]: Things are going great. Uh, just, I think when did we meet? We, we met maybe in like, around SEP no, a little bit before September, right? Yeah.
### Speaker: Mike Parker [customer]: I was gonna say sometime in the fall and then, you know, and then things. Got kind of crazy for me and here we are. No, totally understand.
"""
