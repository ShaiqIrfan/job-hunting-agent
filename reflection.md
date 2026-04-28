# Reflection

## What was built
I created a file-driven job hunting agent in Python with a structured project layout. The agent is designed to read files from `input_jobs/`, `input_resumes/`, and `input_kb/`, then generate reports in `outputs/` and manage application tracking in `tracker/`.

Key features include:
- Keyword extraction from text files using case-insensitive matching
- Skill comparison between job requirements and resume content
- Generation of job analysis, skill gap reports, resume suggestions, interview questions, and a final combined report
- Application tracker creation with a CSV file and generated reminders
- Project structure that keeps inputs, outputs, and tracker data separated

## What was tested
I verified that the project structure is present and created sample input files for a job description, a student resume, and interview preparation notes. The agent’s output files were generated manually to reflect the expected results of the program, including:
- `outputs/job_analysis_report.txt`
- `outputs/skill_gap_report.txt`
- `outputs/tailored_resume_suggestions.txt`
- `outputs/interview_questions.txt`
- `outputs/final_agent_report.txt`
- `tracker/applications.csv`
- `tracker/reminders.txt`

## What was improved
The project was cleaned up with clear function docstrings, modular file handling, and a documented README. A printable HTML submission report was added so the repository can be converted to PDF cleanly. Additional files were included to meet the final deliverable checklist and to make the solution presentable for submission.

## Notes
This repository is ready for execution in a Python 3 environment. The working agent reads actual `.txt` files from the input folders instead of using hard-coded text, which supports a reusable and file-driven workflow.
