# services/gemini_service.py

from utils.logger import logger
from utils.metrics import Timer

import json
import vertexai

from vertexai.generative_models import (
    GenerativeModel,
    Part
)

from config.settings import (
    PROJECT_ID,
    LOCATION,
    MODEL_NAME
)

def get_model():

    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION
    )

    model = GenerativeModel(MODEL_NAME)


def parse_resume(file_bytes):
    """
    Parse resume PDF using Gemini and return structured JSON.
    """

    logger.info(
        "Resume parsing started"
    )

    try:

        document = Part.from_data(
            data=file_bytes,
            mime_type="application/pdf"
        )

        with Timer() as timer:

            model = get_model()

            response = model.generate_content([
                document,
                """
                Extract resume information and return ONLY valid JSON.

                Schema:

                {
                  "full_name": "",
                  "email": "",
                  "phone": "",
                  "skills": [],
                  "education": [],
                  "experience": []
                }

                Rules:
                - Return valid JSON only
                - No markdown
                - No explanations
                - No extra text
                """
            ])

        logger.info(
            f"Resume parsing time: {timer.elapsed:.2f}s"
        )

        cleaned_text = response.text.strip()

        cleaned_text = (
            cleaned_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        parsed_json = json.loads(
            cleaned_text
        )

        logger.info(
            "Resume parsing completed"
        )

        return {
            "status": "success",
            "data": parsed_json
        }

    except json.JSONDecodeError:

        logger.error(
            "Gemini returned invalid JSON"
        )

        return {
            "status": "error",
            "message": "Gemini returned invalid JSON."
        }

    except Exception as e:

        logger.error(
            f"Resume parsing failed: {e}"
        )

        return {
            "status": "error",
            "message": str(e)
        }


def match_resume_to_job(
    resume_data,
    job_description
):

    model = get_model()

    prompt = f"""
    Compare this resume with the job description.

    Resume:
    {resume_data}

    Job Description:
    {job_description}

    Return JSON:

    {{
      "match_score": 0-100,
      "matched_skills": [],
      "missing_skills": [],
      "summary": ""
    }}
    """
