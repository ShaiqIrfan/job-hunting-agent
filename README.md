# Job Hunting Agent

A file-driven job hunting agent written in Python.

## Project Structure

- `app.py`: Main application file
- `input_jobs/`: Folder for job descriptions
- `input_resumes/`: Folder for resumes
- `input_kb/`: Folder for knowledge base files
- `outputs/`: Folder for output files
- `tracker/`: Folder for tracking data
- `reflection.md`: Project reflection and final submission notes
- `report.html`: Printable submission report for PDF export

## Usage

1. Place job descriptions in `input_jobs/` as `.txt` files.
2. Place resumes in `input_resumes/` as `.txt` files.
3. Place knowledge base notes in `input_kb/` as `.txt` files.
4. Run the agent with:

```bash
python app.py
```

5. The agent creates report files in `outputs/` and tracking files in `tracker/`.

## Requirements

- Python 3.x
- No external dependencies required

## Final Submission

This repository includes the required deliverables:

- A GitHub repository with a working Python agent
- At least one job description file in `input_jobs/`
- At least one resume file in `input_resumes/`
- At least one knowledge base file in `input_kb/`
- Generated report files in `outputs/`
- Application tracker records in `tracker/applications.csv`
- Reminder file in `tracker/reminders.txt`
- A printable PDF-ready `report.html`
- A reflection document in `reflection.md`
