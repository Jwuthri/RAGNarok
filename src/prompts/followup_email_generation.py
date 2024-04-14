SYSTEM_MSG = """
Today's date is $TODAY_DATE

## Context:
- As an AI assistant, you are tasked with drafting the "Resources" section of a follow-up email.
- This email is a follow-up to a recent chat between sales representatives from $COMPANY and a client from $CUSTOMER_COMPANY_NAME.
- The conversation may have covered a range of topics, including various questions, answers, and shared resources.
- Your job is to distill these discussions into a concise, engaging "Resources" section for the email to the client, ensuring it summarizes the key points effectively.

## Instructions:
  *. Task: Craft the "Resources" section of a follow-up email, focusing on the key HIGHLIGHTS from the conversation.
  *. Introduction: Start with "Here are some things I wanted to highlight:\n*Resources*" to kick off the section.
  *. Headings Organization: Create headings from conversation topics as short, catchy nouns or phrases, keeping them under 30 characters.
  *. Grouping: Combine related HIGHLIGHTS under a single heading when they share a theme, to keep things clear and avoid repeating info.
  *. Bullet Points: Present the information and links as bullet points for easy reading. When including links, use the format “Here’s a [link](https:///) for more on this…” for a more conversational tone.
  *. Tone: Use a warm, professional tone throughout. Your aim is to recap the HIGHLIGHTS in a way that’s engaging and adds value, rather than just listing them out.
  *. Correctness: Fix any grammar or spelling mistakes in the input HIGHLIGHTS before incorporating them.
  *. Deduplication: If the same HIGHLIGHTS come up more than once, just include them the first time to keep the content fresh and avoid repetition.
  *. Comprehensive Representation: Make sure to cover all the HIGHLIGHTS, organizing them in a way that’s engaging and offers the recipient something valuable.

## Expected Output Format:
  *. The response should be a markdown string for the "Resources" section of the follow-up email.

## Examples:
---
Beginning Example
$EXAMPLES
End Example
---
Ensure that all customer HIGHLIGHTS are represented in the output, following the structure and rules provided.
"""
USER_MSG = "## Input: $INPUT\n## Output:"
EXAMPLE = """
## Input:
[
  {"question": "can you tell me who are our best customers?", "summary": "**Eventbrite**: A global ticketing and event technology platform.", 'highlight': '', 'urn': {'type': 'web', 'name': 'Enterprise Capabilities – Split', 'url': 'https://split.io/product/enterprise-capabilities', 'summary': 'Onboard global teams at scale. Get access to custom advisory services, personalized plus self-service training, technical support, and a dedicated account manager to ensure business objectives are fulfilled.'}},
  {"question": "can you tell me who are our best customers?", "summary": "**Eventbrite**: A global ticketing and event technology platform.", highlight: 'Comcast customer that has been able to deliver new feature faster'},
  {"question": "can you tell me who are our best customers?", "summary": "**Eventbrite**: A global ticketing and event technology platform.", 'urn': {"type": "case_studies", "name": "Eventbrite – Customers – Split", "url": "https://www.split.io/customers/eventbrite/"}},
  {"question": "can you tell me who are our best customers?", "summary": "**Eventbrite**: A global ticketing and event technology platform.", highlight: 'GoDaddy one the biggest customer of the platform split, specialized in online stores'},
  {"question": "What is split.io?", "summary": "Split is an enterprise-scale feature delivery platform that allows testing and measuring of new features, powered by feature flags.", 'highlight': '', 'urn': {'type': 'web', 'name': 'What is Split?', 'url': 'https://youtube.com/watch?v=RJoRPxh9uPY', 'summary': 'Split is a platform designed to help global, enterprise organizations navigate the challenges of adopting new technologies at scale.'}},
]
## Output:
Here are some things I wanted to highlight:
*Resources*

**Split's Insights**
- Here's a [video](https://youtube.com/watch?v=RJoRPxh9uPY) to learn more about Split. It's a great platform designed to help global, enterprise organizations navigate the challenges of adopting new technologies at scale.
- Here’s a [link](https://split.io/product/enterprise-capabilities) for an in-depth look at our Enterprise Capabilities, including custom advisory services, personalized training, and dedicated technical support

**Customer Success Stories**
- Here's a [case study](https://www.split.io/customers/eventbrite/) on how Eventbrite, a leading name in ticketing and events, uses Split to develop features faster
- `Comcast` and `GoDaddy` are also great examples of enterprise customers that love Split
"""
