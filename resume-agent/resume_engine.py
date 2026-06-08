


class resume_updater():
    def collect_skills(missing_skills):
        confirmed = []

        for skill in missing_skills:
            answer = input(f"\nThe job wants '{skill}'. Do you have experience with this? (yes/no): ")

            if answer.strip().lower() == "yes":
                project = input(f"  Describe a recent project where you used {skill} (press Enter or type 'no' to skip): ").strip()
                if project.lower() == "no":
                    project = ""              # "no" means no project, but keep the skill
                confirmed.append({"skill": skill, "project": project})
            # answering "no" to the skill itself → nothing added

        return confirmed


# # test it — using a real gaps list
# resume_text = read_pdf("VigneshMSurie.pdf")
# with open("job.txt", encoding="utf-8") as f:
#     job_description = f.read()

# gaps = analyze_gaps(resume_text, job_description)
# confirmed = collect_skills(gaps["missing_skills"])

# print("\n--- CONFIRMED SKILLS + PROJECTS ---")
# for item in confirmed:
#     print(f"{item['skill']}: {item['project']}")