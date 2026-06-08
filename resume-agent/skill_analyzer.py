import json
from google import genai
from pypdf import PdfReader
from document_ingester import doc_reader
from dotenv import load_dotenv
import os 
load_dotenv()
read_pdf = doc_reader.read_pdf

client = genai.Client(api_key= os.environ['API_KEY'])
def analyze_gaps(resume_text, job_description):
    prompt = f"""You are comparing a candidate's resume against a job description to find skill gaps.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Produce two lists:
1. missing_skills: skills/technologies the JOB explicitly asks for that do NOT appear anywhere in the resume (check the whole resume, including project descriptions, not just the skills line).
2. irrelevant_skills: skills on the RESUME that are CLEARLY unrelated to this job and add no value.

Critical rules:
- For irrelevant_skills, be VERY conservative. Only list something if it is obviously unrelated (e.g. a graphic design tool for an AI engineering role). If a skill could plausibly support the role in any way (software development, integration, cloud, databases, APIs), do NOT list it. When in doubt, leave it out.
- Only list skills actually present in the respective source. Do not invent.
IMPORTANT:
- Focus on the "Skills in demand" and "Responsibilities/Desired profile" sections, which are the real requirements. Go through the listed skills one by one and decide present-or-missing for each.
- Do NOT include items from an "Advantages", "Nice to have", or "Bonus" section — those are optional, not gaps.
- Only include actual skills or technologies, not general experiences or circumstances (e.g. "experience in a regulated environment" is not a skill).

Return ONLY valid JSON in exactly this form, nothing else:
{{"missing_skills": ["..."], "irrelevant_skills": ["..."]}}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw = response.text.strip()
    # models sometimes wrap JSON in ```json ... ``` fences — strip them
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[raw.find("{"):raw.rfind("}") + 1]

    return json.loads(raw)


# test it
resume_text = read_pdf("VigneshMSurie.pdf")
job_description = """An international consulting group founded in 2019, Ekkiden leads an ecosystem of passionate and committed consultants who lead organizational, operational and technological transformation projects in IT/Digital, Industry/R&D and sustainability, for key accounts and SMEs, in France, Switzerland, Spain and Germany.

Agentic AI Engineer (H/F/X)
Your mission:
We are looking for an Agentic AI Engineer with a passion for artificial intelligence applied to business process automation.

You will participate in the design, development and deployment of solutions based on autonomous AI agents, capable of interacting with different information systems, analyzing data and performing complex tasks in a secure and controlled manner.

As part of a growing team, you will help transform processes that are currently done manually into intelligent and automated workflows, while ensuring a high level of governance, traceability and compliance.

Responsibilities:
Design and develop robust and scalable Agentic AI architectures.
Translate business needs into AI-based automation solutions.
Implement mechanisms for orchestration and collaboration between agents.
Integrate agents with existing systems via MCPs, APIs, and other connectivity mechanisms.
Define the levels of autonomy of agents and implement the necessary safeguards.
Ensure security, governance and control of the actions carried out by the agents.
Develop monitoring, logging and auditability solutions to track and analyze agent behavior.
Collaborate closely with technical and business teams to identify the most relevant use cases.
Desired profile
Minimum 3 to 5 years of experience in software development, automation or artificial intelligence.
Real-world experience on projects using LLMs, generative AI, or Agentic AI architectures.
Good understanding of integration, architecture and security issues.
Ability to analyze business processes and propose pragmatic solutions with high added value.
Experience on Cloud, On-Premise or hybrid environments.
Excellent communication skills and collaborative spirit.
Skills in demand
Agentic AI
AI Agent Architecture
AI Governance & Controls
AI Agent Security
AI Agent Auditability
MCP (Model Context Protocol)
APIs & Systems Integration
Process Automation
Solution Design
Log Analysis
LLMs (Gemma, Llama, Mistral or equivalent)
LangGraph, CrewAI, AutoGen, or similar technologies
Advantages
Knowledge of AuraQuantic.
Experience in a regulated environment.
Knowledge of governance and compliance issues related to AI.
Languages
Fluent English is mandatory.
Professional French appreciated.
 """

gaps = analyze_gaps(resume_text, job_description)


from resume_engine import resume_updater

collect_skills = resume_updater.collect_skills

confirmed = collect_skills(gaps["missing_skills"])
print("\n--- CONFIRMED SKILLS + PROJECTS ---")
for item in confirmed:
    print(f"{item['skill']}: {item['project']}")