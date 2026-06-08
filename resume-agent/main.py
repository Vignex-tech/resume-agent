import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def tailor_bullet(original_bullet, job_requirement):
    prompt = f"""You are helping rewrite a single resume bullet point to better align with a specific job requirement.

ORIGINAL BULLET:
{original_bullet}

JOB REQUIREMENT IT SHOULD SPEAK TO:
{job_requirement}

Your task:
- Rewrite the bullet so it clearly connects to the job requirement.
- Start with a strong action verb and, where the original supports it, include a concrete result or scope.
- Use language and keywords from the requirement ONLY if the original genuinely supports them.

Critical rule:
- Do NOT invent skills, tools, technologies, metrics, or achievements that are not present or clearly implied in the original bullet. You may reframe and sharpen what is there, but you may not add experience the person did not have.
- If the original bullet has little or no real connection to the requirement, do not force one. Instead, rewrite it as the strongest honest version of itself and do not pretend it matches.

Output:
- Return ONLY the rewritten bullet text. No preamble, no quotation marks, no explanation."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()
print(response.text)