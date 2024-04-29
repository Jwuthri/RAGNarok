SYSTEM_MSG = """
## Context:
- You are programmed to act as an advanced note-taker, skilled at analyzing and extracting key information from Inputs.
- Your role involves processing conversations between sales representatives from $ORG_NAME and their customers from $DEAL_NAME.
- Your specific Task is to extract insights provided by the customer during the Input, especially in response to a specific questions posed by $ORG_NAME's salesperson.

## Instructions:
  * Answer Extraction: Utilize only the information provided in the Input to formulate an answer.
  * No Information Present: If the required information to answer the question is absent from the Input, respond with idk.
  * Accuracy and Specificity: Refrain from inferring or assuming details not explicitly stated in the Input.
  * Error Correction: Correct any spelling and grammatical errors when quoting directly from the Input.
  * Customer-centric Responses: Ensure the answer reflects information from the customer. You may use the salesperson's messages to contextualize or interpret the customer's responses but not as direct sources of information for the answer.
  * Clarity in Presentation: Deliver the answer in third person, ensuring it is straightforward and within a 150-word limit for easy understanding. Structure the answer clearly, using bold subheadings and bullet points for multiple aspects.

## Expected Output Format:
The response should be in JSON format with the following structure:
{
  "answer": "Crafted answer based on the customer's statements in the Input.",
  "confidence": "A confidence level from 0 to 2 reflecting the answer's support in the Input."
}
If you cannot determine an answer from the provided Input, respond with: idk

The confidence level should reflect the certainty about the answer:
    0: The answer is not present in the Input.
    1: The answer is partially supported by the Input.
    2: The answer is fully supported by the Input.

## Examples:
---
Beginning Example
$EXAMPLES
End Example
---

## Question:
$DISCOVERY_QUESTION
"""
USER_MSG = "## Input: $INPUT\n## Output:"
EXAMPLE = """
Example 1
===
## Question:
Do you use any progamming language?
## Input:
speaker: customer -> but we are using Java for our application
speaker: salesperson -> Oh awesome we do provide Java sdk
speaker: customer -> can you lemme me know how I can authenticate into the app with the sdk?
speaker: salesperson -> yeah sure lemme check, do you have any requirements?
speaker: salesperson -> We are curently working with a team of 10 people on the sales side
## Output:
{"answer": "They use Java", "confidence": 2}

Example 2
===
## Question:
Do you use any progamming language?
## Input:
speaker: customer -> we have 1000 customer and 100 employees
speaker: salesperson -> when are you going public?
speaker: customer -> hmmm maybe by the end of the year
## Output:
idk

Example 3
===
## Question:
Do you use any progamming language?
## Input:
speaker: customer -> we also use Python
speaker: salesperson -> Oh awesome we do provide python sdk

## Output:
{"answer": "They use Java and Python", "confidence": 2}
"""
INPUT = """
### Speaker: Mike Parker [customer]: Good. I'm doing well. Thanks for being so patient with this, this meeting. I'm glad we've finally reconnected.
### Speaker: Adil Aijaz [salesperson]: No worries at all. This is just like, uh, I totally understand you are, uh, at a public company, a lot of stuff happens. It's uh, I totally understand. How's the quarter going so far?
### Speaker: Mike Parker [customer]: Yeah, it's been good. Um, yeah, we, I think we IPOed in September and so. We had that, uh, we had, uh, I guess that was partially Q3. We just finished up Q4, you know? And so. Um, yeah, it's been good. It's like, um, going public means that forecastability is, you know, pretty critical and. There's you know, a little bit more deal inspection and so forth, but it's been fun.
### Speaker: Adil Aijaz [salesperson]: It's uh, your C F O becomes a lot more. I mean, it becomes seriously important at that stage. Because you really need that, you know, this is the number and then exceed the expectations, things like that. And I'm sure the pressure on the sales org is, is unreal.
### Speaker: Mike Parker [customer]: Yeah. I mean, you know, there is pressure. Fortunately, we have like a pretty good. Engine overall. So, um, you know, but yeah, you're right. Like. You wanna, when you, when you have to read out to the street, there's a little bit of a different dynamic than just, you know, kind of, uh, uh, moving along and, and, you know, focus on. In internal stakeholders. So how are things going with you?
### Speaker: Adil Aijaz [salesperson]: Things are going great. Uh, just, I think when did we meet? We, we met maybe in like, around SEP no, a little bit before September, right? Yeah.
### Speaker: Mike Parker [customer]: I was gonna say sometime in the fall and then, you know, and then things. Got kind of crazy for me and here we are. No, totally understand.
### Speaker: Adil Aijaz [salesperson]: Yeah. Yeah. So yeah, a lot hasn't been happening, right. I mean, you know, like startup speed is very different. The just been crazy building. Bringing on customers. Interesting use cases, developing. You know, like the, uh, the, uh, good sign of, of. Of of, uh, uh, a sign of a good market is simply that. You end up having more use cases than you imagined. Right. And so I think that is, that has happened. We've had some, uh, one set of customers come in. Who are like, um, but a multi-product use case that I never thought about it, which was. Um, you know, they had, uh, uh, they had, they started with a core product. Um, and that over time they acquired three to four additional companies. Small companies, startups. And then what happened was that the SES of those organizations left. And so the SES of the parent organization are now responsible for selling. Five different products.
### Speaker: Mike Parker [customer]: Hmm.
### Speaker: Adil Aijaz [salesperson]: And. They're like, how do we do this? Right. So this was a use case. I never really considered that. Oh, you could be in a multi-product scenario where even an se is not an expert in everything. And so that showed up, so that that's pretty cool overall, you know? Uh, stop speed. Life is good. How is, or how are holidays for you? Yeah, uh, pretty good.
### Speaker: Mike Parker [customer]: We. We have two young kids. And so there was a little bit of. Is everyone. This is in at least in the Northeast, there's a lot of like just illness going around. So we had a little bit of that, but, um, nothing too crazy. Traveled back to my childhood home in Western. The Western part of the state, Massachusetts. Um, and yeah, otherwise things have been, uh, have been pretty good.
### Speaker: Adil Aijaz [salesperson]: Do you still have family out there west Massachusetts? Yeah.
### Speaker: Mike Parker [customer]: So I have three siblings that live out in the. Boston ish area. Um, but my dad lives out, you know, two hours west. Um, more rural part of the state. So go back there periodically. It's nice. You know, nice little getaway. Um, pretty cool. So yeah. Yeah. Things were good.
### Speaker: Adil Aijaz [salesperson]: Well, thank you so much for the time today. I wanted to reconnect and, uh, my agenda was pretty simple. Just, uh, a C, if, if now is a good time for us to. Think about a little bit more of, of, uh, you know, taking a more serious look, see if there's an opportunity to collaborate. That number two. I also wanted to show you the product simply because yeah, from a feedback perspective, you know, Hey, because a lot has happened since we last talked. And so want to bring you up to speed and not only that, but also get your perspective on where to take it from here, type of a thing. Does that make sense?
### Speaker: Mike Parker [customer]: Yeah, that that'd be great. I think like, um, I was gonna suggest a demo as well, just cause I was trying to kinda catch up and you know, that's a great way to kind of. Uh, learn things in a high bandwidth way. Um, and then, yeah, like I think when we last talked, I was discussing. If there's a slack version of this that, you know, might, might help. And we, we can, we can talk through that maybe after, after seeing the, the product. Yeah.
### Speaker: Adil Aijaz [salesperson]: Yeah. Makes sense. Makes sense. So, yes, let's invert that let's first give you a quick demo, just so you can. Situate yourself again, into where, what the product does. And then, um, uh, and then we can talk about. Potential applicability, things like that. Okay. So.
### Speaker: Mike Parker [customer]: Um, let me just give you double.
### Speaker: Adil Aijaz [salesperson]: I'll uh, okay. Of course. Let me just assume you remember nothing and just pitch it again. Okay. And the basic pitch was that, uh, look the, uh, when you were selling a product. Uh, product expertise matters. And the problem is that even for, uh, for remotely technical products, complicated products. That expertise comes from SES. Now the problem is that the SES are a constrained and expensive resource. You can't afford to give them to every rep. Um, I think you mentioned you guys have something like a pooling model going on, uh, the SMB level, I'm sure at the mid-market level. There's some sort of like still pooling, but better. And the problem simply ends up being that your se calendar becomes the busiest calendar. The most difficult to get time on, uh, in, in the GTM organization. Which then has implications on deal velocity because anytime a rep needs help. Um, on a call, wanna bring an S in a call. It just is like, oh, the next available slot is four days down the road, five days down the road. Right. And so that just slows down deals. And then on the flip side for the SES, it becomes very hard to. Do mind share and timeshare between top of funnel deals. That may or may not qualify and actual like real POCs. That that will make or break the quantum. Right. Um, and so they're splitting time between like fake deals and real deals to use, like more. Uh, <laugh>, uh, uh, uh, uh, stronger words and not just does not end up well for, uh, the business in general. So what we are, what I'm imagining is a world that I can, I can enable every rep, every S T R, and EV, even around ramping S SC. Those are my three personas. Um, with a, uh, with a AI sales engineer called Sam. Uh, that is an expert at ATLA used products. Um, and the key thing is that if there are five levels of difficulty to a question, right? Uh, we are not trying to address all five for now. Right? Eventually we'll answer all five, uh, uh, all five levels. First level is even a good SDR. Who's ramped up should be able to answer level five. Is. Even an se has difficulty answering it. They have to go do some research, go figure out, talk to five different people and then give an answer. Right? So in that spectrum, Sam specializes in first three levels. Level one, two level three level four. It'll still be able to help you, but not our predictably level five will almost always fit. Right? That's the basic idea. Um, and, uh, the last thing is, is imagine as two different experiences, there's an in-call experience. Where Sam joins a call in this case, it has joined a call. Uh, this particular call and then there's pre-call and post-call help as well, where you can talk to it, uh, uh, to prepare for a call, uh, uh, as well as to do follow ups. Does that make sense? Any questions about that before I jump into the product?
### Speaker: Mike Parker [customer]: Yep. No, that makes sense. Okay. Awesome.
### Speaker: Adil Aijaz [salesperson]: Uh, so let me just show you the product. Um, I think we had the old shitty UI, but I gave you the first time. I'll. Uh, uh, this one might be a bit on the newer side, but any case, so. Again, I'll assume that you don't remember anything. I'll walk you through five to six different points. Number one how Sam, uh, impersonates in a seat. It's not just a search on top of your knowledge base. It tries to impersonate an se in value selling and objection, handling and competitive threat detection. Number two, it helps you solve roadmap. Number three, it helps you retrieve and or generate assets. That might be valuable for follow-up number four. It helps you with technical discovery and number five. It customizes answers based on what you've been talking about. Right. Um, so I'll walk through each one of those things. The first thing is, and I'll again, how do you ask a question for now? You ask a question this way, chat U PT style. Uh, we are working on a solution where Sam can automatically detect questions, yada, yada, yada, but in the next month I will, that month, month and a half, that should be here. Um, so for now you just type a question. Let me just go through these, some of these questions. Uh, the first one is a level one level, two question. Does your product do X. Right. And what it enables me to do is to show you something interesting. First, Sam gives you two levels of answers. The first answer is a quick and dirty answer, uh, which is valuable if you're using Sam in a call. You don't have time to look at a lot of stuff. So how can I get a quick answer right now? Once I get that answer, if I have more time or I'm using Sam pre or post call? Then I get a little bit more detail. Uh, where we begin to see how some imperson is in us. Right. So Sam gives you the no. No, we don't do something. But then from there, Sam moves on to doing what a good ASEE would do. Nobody else. What do we do in stock? Right. And then Sam takes the one step further, like any good se says nobody. Yes. And here's why we do it. Right. Here's why we chose the approach we chose. Not only that, but also some recognizes that it's dealing with a potential objection. A customer asked for something. We don't have it. Uh, instead of brushing this under the rug and vices in the Astro calls down the road. Let's talk about it. So Sam surfaces, this prompt. Uh, which is very valuable for a younger rep, right? Not for like somebody with 15 years of experience where let's ask the question, why is this important? What is a use case? Can you gimme an example? Things like that, right? So you be, do the, you understand the why maybe the customer says this is, I was just curious, maybe the customer says this is my top tire priority. Either way let's find out this is the first thing I wanted to show you. Any feedback, thoughts on this before I move to my second and third things.
### Speaker: Mike Parker [customer]: Yeah, this is good. Um, I oh, I'll hold my questions. Um, or my thoughts cause so I can, so I can see the rest, but, um, yeah, it seems cool. Okay. Great.
### Speaker: Adil Aijaz [salesperson]: So then a related idea to this is that, um, uh, and SCL on a call, one of their jobs is to provide extra vision on a dealer, right? Uh, one of those things is, well, who else is on this deal? And the way you figure that out is how the customer's ever gonna tell you, I'm talking to these three other customers. Well, I mean, sometimes they do, but most of the times they don't. You need to understand who else is in the deal by listening closely to what the customer is saying. So in this case, if you ask the question, what is the size? It's a very surface on the surface. Very, a very innocent question. What is the size of your SDK? Now Sam gives you the answer. Here's the quick and dirty answer. Here's the more detailed answer, right? Um, it's useful, but what's more useful is Sam raises this alert, right? I'll show it to you in a collapse state. So it's more summarized. Sam is raises an alert that, Hey, this question means more. Than what, what appears at the surface? And what it means is that your competitor lost shortly could be planting FUD. Against you, what is a FUD? Your S STKs are larger than, uh, they're they're SDKs. What does that matter? Because size impact performance. Right now, if you're live in a call, this really helps you to do better discovery, but if you're preop post call, you cannot actually read. The official answer. Which is wiser, why RST is bigger. Because, uh, because of these, these design considerations, and now you end up improving as a seller, right? Because now you are like, okay, great. Now I understand why we do things the way we do them. And I can be better prepared for this sort of stuff. Next time. I, any feedback on the, any need thoughts prefer move on. Yeah, no, I like that.
### Speaker: Mike Parker [customer]: I like that too. Um, my observation so far is that you have like, it's a bit opinionated in terms of like detecting. Um, yeah, like bud and follow up. It's it. It's opinionated in what SES should do.
### Speaker: Adil Aijaz [salesperson]: Correct.
### Speaker: Mike Parker [customer]: In addition to just like providing knowledge, which I, I do like that. Correct.
### Speaker: Adil Aijaz [salesperson]: And again, it can never replace an se, right. Because an se is strategic to a deal. Does a lot more than answering questions. Right. But what, what we are asking ourselves is what are all the. All the little things that an se does. Especially near the top of the funnel. Where we can replicate those effectively in Sam so that the se pressure is relieved. Right. So that we can. Uh, up the quality of our reps and our SDRs if they're involved as well. So another thing in SC does on a call is, um, uh, they help the seller, not just sell what's on the truck, but the promise of future innovation, right? Because in a very competitive market, you often need to be like, no, no, we. Sure we don't have that capability. Are we building it right? That sort of stuff. And if you don't put any controls on it, your reps can start hallucinating and start making things up. Right. You don't want that to, instead of shutting that down, you can just give your product roadmap. To Sam and what Sam can do. Is based on the question, pull in the right item from your roadmap. So that the seller can confidently sell the futures. Right. Which is, Hey, I understand. So here's a question. What events does your. Split rum agent track. Sam gives you a surface level answer. Which is, these are the events we track, yada, yada, yada, but then it recognizes. That there is a roadmap item that we recently launched. That the rep might not be aware because you know, roadmaps move quickly. Or there's something coming in the next three to six months. Right? Let me, let me surface that to the reps. The rep can say something along the lines of. This is an area of active innovation. Here's something we just launched. If you're interested, I can connect you with RSC, right? I can get you more information. That sort of stuff. Right. And then of course you can get more detail if you're using it outside of a column. Thoughts feedback.
### Speaker: Mike Parker [customer]: Uh, uh, yeah, I mean, I, similarly just like the idea that. It's not just informational. It's a little bit prescriptive. Um, so yeah. Um, I like that. Okay.
### Speaker: Adil Aijaz [salesperson]: And then the last two, three things is that of, uh, uh, oftentimes a good answer is not just a tell answer. It's also a show answer, right? Um, so in this case, how do you connect X to Y. The tell answer is useless. Right? Who's gonna sit there and, and read this. Sure. You can include this in an email. But the show answer is far more interesting. What Sam can do is it can look through your YouTube. If you have any demos that are being given on webinars and, or I, I don't think clay view does that. But, you know, loom demos, anything that where you can share with us. Videos of SES demoing things. We can find the right video. We can find the right spot in that video. That then the rep can use. In their follow up. Right. And send that video to the customer. Not only that, but also Sam can. Generate for you a slide. Right. So oftentimes say 15 minutes before a call, you realize, oh shit, I'm missing a, a key slide. Technical slide in my deck. Right. Instead of being blocked on the se. Uh, I can just ask them to build a slide for me. Right? So in this case, I ask Sam. Um, you know, what are the steps involved? Give me a slide. Sam generates a slide in the future. It will also retrieve slides for you, but the key points are it's in splits own brand. So it's, it can be enclave view's own brand. It's not a Mickey mouse template. And the second point is that you can open it up in Google slides. And, and clean it up for five minutes. The goal is not that this is a pic picture, perfect slide, right. Which you can show to the customer. The goal is let's slap on the content in roughly the right template. Uh, or sorry, in the right template, roughly the right format. And then you spend five minutes cleaning it up. Uh, the human spends five minutes, cleaning it up and now you're ready to ready for your next meal. That's the basic idea. Um, any feedback, thoughts on this before I, yeah.
### Speaker: Mike Parker [customer]: That's I like that. Yeah. Okay.
### Speaker: Adil Aijaz [salesperson]: Uh, last couple of things of course are wrap. Uh, an se does a lot more than just answer questions. You're also responsible along with the rep to do discovery an a deal. Um, and, uh, discovery, if the rapid is responsible for banned medic, whatever. Uh, the se is responsible for ICP evaluation or whatever, like technical questions. And so Sam reminds you of those questions over here. Group stem right here are my. Three to, uh, nine questions that I should be asking every customer. But more importantly, what Sam does is it also takes notes. So for instance, in this case, since I'm live on a call with you. It's actively listening. And if I were to ask you one of these questions, um, you, it would, uh, it would take down the note, right? So for instance, if I ask you the question, do you use Google analytics? Oh, yeah. Could you say that again? Do you use Google analytics?
### Speaker: Mike Parker [customer]: Do we, uh, I'm not sure if we do, um, but I'm, but I'm familiar with it for sure. Okay, great.
### Speaker: Adil Aijaz [salesperson]: So let's see sound, uh, take the snow in just a sec and like it wakes up every now and then, but let me show you this, working on a different, uh, uh, a different call, just so you can get a sense of how it works. So, let me show you on main LJ. Okay. So here's a, a call that I had earlier in this scenario. You'll notice how Sam took down notes. Now, every time Dick and Harry is doing note-taking right. What's different about Sam is it's taking notes. Uh, very opinionated, no notes to use your work, right. It's saying what is important? My discovery is important. I'm gonna take notes along that. So it says, you know, the customer said Datadog is we're using Datadog for monitoring. Um, I asked the question, you know, what, what are you using for feature flags? It, it, it sort of like took down this note and this can now be, uh, saved back in Salesforce. So that's one, but not only that. What's really interesting is Sam now pulls this information into its special answering. So if you're not asked the question. In this may no J thing. How do you integrate with APMs? Right. That's the question. Uh, I'm asking it about split in the context of main OJ. Now notice what Sam does. It ans it customizes its answer. It doesn't give you cookie cutter one. It says split integrates with a APM tools like Datadog, which is currently used by your organization. Right? How did it get that? It got that from here because it took down this note now, why is this valuable? It's valuable because. SES can often be, uh, uh, you know, uh, swapping in and out by an se falls. Sick. Working on a critical deal from other se has to step in. They have to start all over again. It's like, okay, what is the, what is what's their tech stack? What are they using? Right. Now Sam can help out because Sam is listening has been on every call. It's now able to use this information to give you a more tailored answer. Does that make sense? Yeah.
### Speaker: Mike Parker [customer]: Yeah, that's nice.
### Speaker: Adil Aijaz [salesperson]: Okay. Awesome. Uh, okay. Just to show you enclave your side. It took down this note. Yep. Mike, Parker's not sure if they used the right. So it took the live note. And then the last thing of course is now to come full circle. We also provide you with a poor man's version of. Gong where you can look at a call, but I mean, again, uh, I'm sure clay has already using something else, but this is just to. In case you guys don't use it or you want to go. For, you know, like we, we provide the full, full service as well. Now to your question, is it available in slack? Of course, it's available in slack where you can do so this is a test org where you can similarly ask a question over here. Hey, Sam. And then I can ask, uh, a question over here. What is flick again? I know it's a very dumb question. But it's a very, uh, simple one where it comes up with the answer. Gives you, the summary gives you the detailed answer. And doesn't look pretty. That's fine. But it at least is available. Where your reps were ASEs live. So, uh, hopefully that, that gives you perspective.
### Speaker: Mike Parker [customer]: Neat. Yeah, that's cool. That's it?
### Speaker: Adil Aijaz [salesperson]: That's it from my demo. Nice.
### Speaker: Mike Parker [customer]: Yeah, I think like, um, I, I guess I'll just react sort of react if, if that's helpful. Yeah. So, absolutely. Um, I think where my mind goes is. Uh, yeah, I think there's value for AEs who are. Um, you know, either new to role or just, like you said, just there's se sort of capacity. Limitations. Like we, we have a ratio of. Roughly 25 or 30 to one for our like commercial, our SMB commercial business. Um, in terms of AEs and essays. Or, you know, essays. So, um, so, yeah, we have AEs flying solo a lot of the time. Like, I, I would think of this as maybe like a co a co-pilot for them, like a technical co-pilot. Um, that's one use case. I think the slack one is interesting for a big company like ours, because. You know, product mastery and domain knowledge is like something that constantly. Um, it, it's hard to keep up with and slack is the center of gravity for those kinds of questions. Um, and so like, I think I've, I mentioned this the last time we spoke, we have a channel. That we call public SA team. And it's just, yeah, you basically, everyone asks question probably, you know, 20 questions a day or something like that. And so it becomes this like living knowledge base, but you know, we get the same question probably like at least. One question is like, does X integrate with Clavio? And we have like, you know, pretty vanilla answer to that. And we've debated having. A bot sort of auto respond. Correct. Um, but you know, the question was, could we. Or what I was contemplating the last time we spoke. Was, you know, could we treat the existing. Um, slack channel as like a body of knowledge to train. Correct Sam on. And then we have, you know, a Wiki we've got other stuff as well. Um, so that's another use case is just like, uh, you know, sort of. Automated sort of communications around product knowledge and. Maybe ref referring people to the right help documentation, et cetera. Um, the other use case that I wonder if you've heard is. And this is what I was getting at. When I said it was opinionated. Is like as a training tool almost. So I wonder if I could like, sort of have it process. You know, I, I choose like five, I don't know, gold standard sort of. Calls have it. Replay those almost like Sam. Uh, goes through those. And then like the thing that I like is, um, the stuff that you casually mentioned, cuz you've got lots of experience in the industry and you know, like what the top tier SES do. Like people need to learn that. So like, oh, this is FUD. How should I respond to FUD? You know? So you're like, you're your productizing it, but also I want the humans to know it as well. Um, and so it's the thud, it's the, you know, questions. Like I thought of this thing that I, I trained the team on. Um, called the XY problem where someone asks about. The, the perceived solution rather than the actual problem. And so I'm like, okay, you, you gotta unpack that a little bit and ask questions. Um, so that I'd say what, what I. What I, um, the two use cases that come most to mind. Mine, maybe there's the, maybe there's a cell on the AE side. Um, but also there's the. You know, could it, could it, could it sort of automate. Se like communications in, in our slack channel, for example, that's one thing. And then the other one is, you know, uh, you know, taking the opinionated sort of responses and then using it as a training, sort of co-pilot for. For folks as well. Um, so buil building like a library. Of calls that have been monitored by Sam and, and using it as a, a training tool, essentially. I don't know. Have you heard that one at all or not?
### Speaker: Adil Aijaz [salesperson]: Yeah, absolutely. I think that has, I I've heard, I've heard of it. Uh, but I think I've heard of it in two different contexts. Sorry, let me just connect to my chart. I'm gonna go off. Camera while I'm moving.
### Speaker: Mike Parker [customer]: Yeah, no worries. No worries.
### Speaker: Adil Aijaz [salesperson]: I'm not at my home. I'm at my parents' home. So, uh, let me just quickly turn off camera and then. Um, uh, and I'll, I'll respond to you while we are talking. So I've heard of it being, uh, mentioned in two different two different ways. One is the more explicit training tool where it's actually a training training tool. As you sort of like a alluded to. The other one is a little bit more looser than that. And it's the, it's the idea that if you. Solve the first use case where it's like an ask and se uh, uh, bot available on slack, then the SES themselves naturally get trained. Right because they are following along and, uh, in the act of following along. They learn right. And so, um, so I think in a way those two, two, uh, uh, use cases are related.
### Speaker: Mike Parker [customer]: Um, but yeah, that's a fair point, actually. Yeah. Yeah. That makes sense.
### Speaker: Adil Aijaz [salesperson]: But having said that, uh, I have heard the, the feedback that there should be a more explicit tool. I'm currently not going in that direction just yet, but I can imagine that that would become. Um, because, uh, <laugh> so I I'll be, I'll be honest with you why I'm not going in that direction. The reason why I'm not going in that direction just yet is because, um, overwhelmingly, what I've found is that. People managers love the idea of coaching. ICS hate the idea of coaching. <laugh> and I do not wanna be in a position where my primary user hates what I'm doing.
### Speaker: Mike Parker [customer]: Yes. Yes. That makes sense.
### Speaker: Adil Aijaz [salesperson]: <laugh> yeah. So I'm trying to be like, well, let me build a tool that you will love using because it helps you do your job better and helps you not like total your thumbs waiting for an answer a while you are like, um, man, like I need to follow up with this customer quickly. So can I, I do that. So. <laugh> so that's my perspective of that. Um, so let me, let me, um, let me ask you this then. Uh, what is the possibility, uh, do, uh, of, um, you know, like doing a two week POC type of a thing, right. It literally the what's involved here, just so just so you know, what's involved here, right? What's involved is, um, one hour worth of effort on your part. So we, you just we'll figure out the public data sets for you. Um, one hour worth of effort where you can give us your gong, you know, you can figure out 10 gong calls, 10 RFPs. If you guys fill out any RFPs. RPS, um, and effectively like, uh, if you can give us access to the slack, ask slack channel, we have a tool that can scrape that on a regular basis. You just need to get us approval for that. Um, but basically like give us the data and then we take two weeks to train it and then we come back and give you a slack channel. That's it. <laugh> and then you take two weeks to, to just ask it questions and get comfortable that can you trust it or not, but you, I don't mean you in individually. It just means, you know, you assign. Three to five people on your team to be like, Hey, give it a shot. Like ask it as many questions as you can. And then you build trust. Is there a possibility in. And regardless, what's a good timing for it for you.
### Speaker: Mike Parker [customer]: Yeah. Um, honestly, my biggest concern is the, now that we're public company, like, are they gonna, you know, am I gonna get tons of scrutiny for bringing in any new software? If I give you access to certain information? Unfortunately we've become, you know? Yeah, of course you could imagine. Um, what I am wondering is. You know, RFPs are usually like, not that sensitive, might I be able to gather a few of those? The gong calls. Sometimes those are public links. I might be able to sort of get away with it. I think hooking up the slack I'll have to run through it. So that'll like trigger, you know?
### Speaker: Adil Aijaz [salesperson]: Yeah. Yeah.
"""