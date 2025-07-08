import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

# Create a new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "User_name":"Akshay",
    "User_prefernces":"""
        I like to play cricket, Badminton and Table Tennis.
        My favorite hobby is doing dance.
        My favorite TV show is Money Heist.
        """
}

# Create a new session
APP_NAME = "Q&A Bot"
USER_ID = "akshay18"
SESSION_ID = str(uuid.uuid4())

stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

print("CREATED NEW SESSION:")
print(f"session ID: {SESSION_ID}")

runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

new_message = types.content(
    role="user" parts=[types.Part(text="What is Akshay's favorite TV show?")]

)

