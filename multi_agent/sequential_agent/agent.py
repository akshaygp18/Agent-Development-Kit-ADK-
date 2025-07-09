from google.adk.agents import SequentialAgent

from .sub_agents.agent1 import rawskill_extraction_agent
from .sub_agents.agent2 import technical_skill_extraction_agent



# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="SkillExtractionPipeline",
    sub_agents=[rawskill_extraction_agent, technical_skill_extraction_agent],
    description="A pipeline that extracts raw and technical skills from input text using a sequence of specialized agents.",
)