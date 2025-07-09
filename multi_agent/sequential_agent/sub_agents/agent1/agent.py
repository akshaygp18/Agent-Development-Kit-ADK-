from google.adk.agents import LlmAgent

from google.adk.agents import Agent


import pandas as pd
import re
import os
import csv

def extract_raw_technical_skills():
    """
    Extracts the technical skills section from job descriptions in a CSV file and saves the output.

    This function:
    - Loads the dataset from '../demand1.csv'
    - Uses a regular expression to extract text from predefined section headers such as 
      "Technical Skills", "Skills", "Qualifications", etc., from the 'jdkeyword_Desc' column
    - Stores the extracted content in a new column called 'technical_skills'
    - Escapes values that start with '=' to prevent Excel from misinterpreting them as formulas
    - Saves the updated DataFrame to '../output_with_technical_skills.csv' with all text fields quoted

    Returns:
        str: The full path to the saved CSV file containing the extracted technical skills.
    """
    df = pd.read_csv("sequential_agent/sub_agents/demand1.csv")

    df['technical_skills'] = df['jdkeyword_Desc'].apply(
        lambda text: (
            "" if pd.isna(text) else (
                lambda t: (
                    re.search(
                        rf'^(?:{"|".join(["Professional\\s*&\\s*Technical\\s*Skills", "Technical\\s+Experience", "Qualifications", "Technical\\s+Skills", "Skills"])}):?\s*(.*?)'
                        r'(?=\n[A-Z][^\n]{1,80}:\s*$|\Z)',
                        t.replace('\r', '').strip(),
                        re.DOTALL | re.IGNORECASE | re.MULTILINE
                    )
                )
            )(text).group(1).strip() if (
                (lambda m: m is not None)(
                    re.search(
                        rf'^(?:{"|".join(["Professional\\s*&\\s*Technical\\s*Skills", "Technical\\s+Experience", "Qualifications", "Technical\\s+Skills", "Skills"])}):?\s*(.*?)'
                        r'(?=\n[A-Z][^\n]{1,80}:\s*$|\Z)',
                        text.replace('\r', '').strip(),
                        re.DOTALL | re.IGNORECASE | re.MULTILINE
                    )
                )
            ) else ""
        )
    )

    # Escape values that could be misread by Excel
    df['technical_skills'] = df['technical_skills'].apply(
        lambda x: f"'{x}" if isinstance(x, str) and x.startswith('=') else x
    )

    save_path = os.path.join(os.path.dirname(__file__), "..", "output_with_technical_skills.csv")
    df.to_csv(save_path, index=False, quoting=csv.QUOTE_ALL)  # Quote everything
    return save_path









# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the recommender agent
rawskill_extraction_agent = LlmAgent(
    name="Rawskill_extraction_Agent",
    model=GEMINI_MODEL,
    instruction="You are a Raw Skill Extraction AI agent.",
    description="Extracts technical skills.",
    tools=[extract_raw_technical_skills],
    output_key="technical_skills",
    
)

