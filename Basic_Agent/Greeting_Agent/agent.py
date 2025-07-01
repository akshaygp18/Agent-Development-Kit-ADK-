from google.adk.agents import Agent 

root_agent = Agent(
    name = "Greeting_agent",
    model = "gemini-2.0-flash",
    description = "Greeting agent",
    instruction = """
    you are helpful assistant that greets the users.
    Ask for the users name and greet them by name.
    """

)