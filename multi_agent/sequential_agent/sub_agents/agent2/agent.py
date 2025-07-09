import pandas as pd
import re
from tqdm import tqdm
from dotenv import load_dotenv
import os
from google.adk.agents import LlmAgent


load_dotenv()  # Loads environment variables from a .env file into the environment

# Example: Accessing a variable
api_key = os.getenv("GOOGLE_API_KEY")

# import vertexai
# from vertexai.generative_models import (
#     GenerationConfig,
#     GenerativeModel,
#     HarmBlockThreshold,
#     HarmCategory,
#     Part,
# )



# generative_multimodal_model = GenerativeModel("gemini-2.0-flash")


import pandas as pd
from tqdm import tqdm
import os
from google.generativeai import GenerativeModel, GenerationConfig

def extract_and_save_technical_skills():
    """
    Loads a hardcoded CSV file, extracts valid technical/software-related skills from each row using a generative AI model,
    and saves a new CSV with an 'extracted_technical_skills' column.

    - Reads: '../output_with_technical_skills.csv' (must have a column 'technical_skills')
    - Saves: '../output_with_technical_skills_from_paragraph.csv'
    - Uses a Google Generative AI model to extract only valid skills like programming languages, tools, platforms, and methodologies.
    - Removes vague, soft, or business-related terms.
    - Keeps phrases like 'API Integration', 'Azure', 'Cloud Infrastructure Management' intact.

    No parameters required. This function is fully self-contained.
    """
    input_path = "sequential_agent/sub_agents/output_with_technical_skills.csv"
    output_filename = "output_with_technical_skills_from_paragraph.csv"
    output_path = os.path.join(os.path.dirname(input_path), "..", output_filename)

    # Initialize model and config
    generation_config = GenerationConfig(
        temperature=0.2,
        top_p=1,
        top_k=1,
        max_output_tokens=512
    )
    generative_model = GenerativeModel("gemini-2.0-flash")

    df = pd.read_csv(input_path)

    all_skills = []
    for text in tqdm(df['technical_skills'], desc="Extracting technical skills"):
        prompt = (
    "You're an AI assistant. From the paragraph below, extract only **precise and valid technical, software-related, and programming skills**.\n"
    "- Include: tools (e.g., Oracle CPQ, Microsoft Power Platform), cloud platforms (e.g., Azure, AWS), methodologies (e.g., Agile delivery methodology), and technologies (e.g., SQL, Python, software development lifecycle, web development).\n"
    "- For anything cloud-related, extract only concrete skill phrases like **'Cloud Infrastructure Management', 'Cloud Deployment', 'Cloud Troubleshooting', 'Azure'**, not vague terms like just 'Cloud' or long sentences.\n"
    "- Do not rewrite or map cloud-related descriptions into predefined terms like 'Cloud Deployment' or 'Cloud Troubleshooting'; only extract phrases as written if they clearly represent a skill.\n"
    "- Discard generic or broad phrases like 'Scalable Applications Design and Implementation','security best practices for cloud environments', 'problem-solving skills'.\n"
    "- Do not split commonly paired technical actions like 'Application Testing and Debugging' — keep them as one combined skill if written together in the text.\n"
    "- If a skill has context (e.g., 'API integration', 'Agile delivery methodology'), retain the complete phrase.\n"
    "- If multiple related methodologies like 'Agile' and 'Waterfall' are mentioned with similar context, combine them into a single phrase such as 'Agile and Waterfall Delivery Methodology'.\n"
    "- Always include clearly stated cloud-related skills such as 'Cloud Technologies and Deployment' or 'Cloud Infrastructure Management' even if they appear alongside other skills.\n"
    "- Do not include soft skills or responsibilities (e.g., communication, leadership).\n"
    "- Include concrete technical concepts like 'Cloud Technologies', 'application development methodologies', 'application design' even if preceded by vague terms like 'strong understanding of'. Also, include well-known methodologies or skills such as 'Project Management' if explicitly mentioned.\n"
    "- Exclude business analysis or functional skills such as 'Business Process Modeling', 'troubleshooting', 'integration techniques',  unless specifically required as a technical skill.\n"
    "- Simplify phrases like 'SQL queries' to core technologies (e.g., 'SQL') and remove generic suffixes like 'strategies', 'issues', or 'queries' from known skill terms.\n"
    "- Preserve combined skill phrases such as 'Application Design and Development' if they appear together in the text.\n"
    "- Remove trailing words like 'practices', 'principles', or 'techniques' if the base phrase is a standard methodology or skill (e.g., 'Agile Project Management Practices' → 'Agile Project Management').\n"
    "- Return only a **clean, comma-separated list** of technical skills. No extra text or explanation.\n\n"
    f"{text}\n\n"
    "Answer format: Skill1, Skill2, Skill3, ..."
)

        try:
            response = generative_model.generate_content(prompt, generation_config=generation_config)
            if response and hasattr(response, "text"):
                all_skills.append(response.text.strip())
            else:
                all_skills.append("No skills extracted")
        except Exception as e:
            all_skills.append(f"Error: {e}")


    df['extracted_technical_skills'] = all_skills
    df.to_csv(output_path, index=False)


# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"


technical_skill_extraction_agent = LlmAgent(
    name="Technical_skill_extraction_Agent",
    model=GEMINI_MODEL,
    instruction="You are a Technical Skill Extraction AI agent.",
    description="Extracts technical skills.",
    tools=[extract_and_save_technical_skills],
    output_key="extracted_technical_skills",
    
)