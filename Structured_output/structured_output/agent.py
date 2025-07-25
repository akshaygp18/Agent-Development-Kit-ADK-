from google.adk.agents import Agent
from pydantic import BaseModel, Field


class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email.Should be concise and descriptive.")
    body: str = Field(
        description="The main content of the email. Should be well-formatted with proper greeting, paragrahs and signature."
        )


root_agent = Agent(
    name='structured_output',
    model="gemini-2.0-flash",
    instruction="""
    You are an Email Generation Assistant.
    Your task is to generate a professional email based on the user's request.

    GUIDELINES:
    - Create an appropriate subject line (concise and relevant)
    - Write a well-structured email body with:
        * Professional greeting
        * Clear and concise main content
        * Appropriate closing
        * Your name as signature
    - Suggest relevant attachments if applicable (empty list if none is needed)
    - Email tone shoud match the purpose (formal for business, friendly for colleagues)
    - Keep emails concise but complete 

    IMPORTANT:Your response MUST be a valid JSON matching this structure:
    {
       "subject":"subject line here",
       "body","Email body here with proper paragraphs and formatting", 
    }

    DO NOT include any explanations or additional text outside the JSON response.
    """,
    description="Generates professional emails with structured subject and body",
    output_schema=EmailContent,
    output_key="email",
)