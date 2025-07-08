from google.adk.agents import Agent 

question_answering_agent = Agent(
    name="question_answering_agent",
    model="gemini-2.0-flash",
    description="Question answering agent",
    instructions="""
    You are a helpful assistant that answers questions about the user's preferences.

    Here is the some information about the user:
    Name:
    {User_name}
    Preferences:
    {User_preferences}
    """,
   
)