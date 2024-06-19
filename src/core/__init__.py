from enum import Enum


class Applications(Enum):
    live_question_extraction = "live_question_extraction"
    followup_email_generation = "followup_email_generation"
    deal_knowledge_extraction = "deal_knowledge_extraction"
    deal_discovery_question = "deal_discovery_question"
    ask_about_deal = "ask_about_deal"


# @classmethod
# def output_type_router(cls, query: str, query_type: str) -> tuple[str, str]:
#     """
#     determine which type of query it is along the query to perform. Should it return a 'slide', 'image', 'text'.

#     :param query: The `query` parameter is a string that represents the query being passed to the
#     router function. In this case, the function is designed to handle queries related to images
#     :type query: str
#     :param query_type: query_type is a parameter that specifies the type of query being passed to
#     the router function. In this case, it is a string indicating whether the query is 'slide', 'image', 'text'
#     :type query_type: str
#     """
#     return query, query_type

# def determing_output_type(self, query: str) -> tuple[str, str]:
#     tool_transformer = FunctionToOpenAITool(self.output_type_router).generate_tool_json()
#     messages = [
#         ChatMessageSchema(
#             role="system",
#             message="You are an ai assistant that reroute the query to the correct output format, please use the provided tool",
#         ),
#         ChatMessageSchema(role="user", message=query),
#     ]
#     prediction = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
#     func_result = run_tool(prediction.tools_call, {"output_type_router": self.output_type_router})
#     if not func_result:
#         return query, "text"
#     else:
#         return func_result[0], func_result[1]
