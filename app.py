import os
import csv
from pathlib import Path

# Constants for folder paths
INPUT_JOBS = Path("input_jobs")
INPUT_RESUMES = Path("input_resumes")
INPUT_KB = Path("input_kb")
OUTPUTS = Path("outputs")
TRACKER = Path("tracker")

# Predefined list of keywords (skills)
KEYWORDS = [
    "python", "machine learning", "sql", "git", "javascript", "html", "css",
    "java", "c++", "data analysis", "pandas", "numpy", "tensorflow", "pytorch",
    "docker", "kubernetes", "aws", "azure", "linux", "agile", "scrum"
]

def ensure_folders():
    """Create folders if they don't exist."""
    folders = [INPUT_JOBS, INPUT_RESUMES, INPUT_KB, OUTPUTS, TRACKER]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

def read_text_files(folder):
    """
    Reads all .txt files from a given folder, combines their content into one string,
    and returns the combined text and the number of files read.
    
    Args:
        folder (Path): The folder path to read .txt files from.
    
    Returns:
        tuple: (combined_text, file_count) where combined_text is the concatenated content
               and file_count is the number of files successfully read.
    """
    combined_text = ""
    file_count = 0
    
    # Iterate through all .txt files in the folder
    for file_path in folder.glob("*.txt"):
        try:
            # Open and read each file with utf-8 encoding
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                combined_text += content + "\n"  # Add newline separator between files
            file_count += 1
        except Exception as e:
            # Handle any errors during file reading
            print(f"Error reading {file_path}: {e}")
    
    return combined_text, file_count

def extract_keywords(text):
    """
    Extracts keywords from the given text using simple string matching.
    
    Args:
        text (str): The text to search for keywords.
    
    Returns:
        list: A list of keywords found in the text (case insensitive).
    """
    found_keywords = []
    text_lower = text.lower()
    
    # Check each keyword for presence in the text
    for keyword in KEYWORDS:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def compare_skills(job_skills, resume_skills):
    """
    Compares job skills with resume skills to find matches, missing skills, and match score.
    
    Args:
        job_skills (list): List of skills required for the job.
        resume_skills (list): List of skills from the resume.
    
    Returns:
        tuple: (matched, missing, score) where:
            - matched: list of skills present in both job and resume
            - missing: list of skills required by job but missing in resume
            - score: percentage match score (0-100)
    """
    # Convert lists to sets for efficient set operations
    job_set = set(job_skills)
    resume_set = set(resume_skills)
    
    # Find matched skills (intersection)
    matched = list(job_set & resume_set)
    
    # Find missing skills (in job but not in resume)
    missing = list(job_set - resume_set)
    
    # Calculate match score percentage
    if job_set:
        score = (len(matched) / len(job_set)) * 100
    else:
        score = 0.0
    
    return matched, missing, score

def generate_job_analysis(job_text, job_skills):
    """
    Generates a formatted job analysis report.
    
    Args:
        job_text (str): The full job description text.
        job_skills (list): List of skills extracted from the job.
    
    Returns:
        str: Formatted job analysis text.
    """
    skills_list = "\n".join(f"- {skill}" for skill in job_skills)
    
    report = f"""Job Analysis

Job Description:
{job_text}

Required Skills:
{skills_list}
"""
    return report

def generate_skill_gap_report(job_skills, resume_skills, matched, missing, score):
    """
    Generates a formatted skill gap analysis report.
    
    Args:
        job_skills (list): Skills required for the job.
        resume_skills (list): Skills from the resume.
        matched (list): Skills present in both.
        missing (list): Skills missing from resume.
        score (float): Match percentage.
    
    Returns:
        str: Formatted skill gap report.
    """
    job_skills_str = ", ".join(job_skills)
    resume_skills_str = ", ".join(resume_skills)
    matched_str = "\n".join(f"- {skill}" for skill in matched)
    missing_str = "\n".join(f"- {skill}" for skill in missing)
    
    report = f"""Skill Gap Report

Job Skills: {job_skills_str}
Resume Skills: {resume_skills_str}

Matched Skills:
{matched_str}

Missing Skills:
{missing_str}

Match Score: {score:.1f}%
"""
    return report

def generate_resume_suggestions(job_skills, missing):
    """
    Generates formatted resume improvement suggestions.
    
    Args:
        job_skills (list): Skills required for the job.
        missing (list): Skills missing from resume.
    
    Returns:
        str: Formatted resume suggestions.
    """
    missing_str = "\n".join(f"- {skill}" for skill in missing)
    
    suggestions = f"""Resume Suggestions

To improve your match for this job, consider adding or highlighting these skills:
{missing_str}

Additional Suggestions:
- Gain experience in these areas through personal projects or online courses
- Update your resume to emphasize relevant experience
- Consider certifications for key missing skills
"""
    return suggestions

def generate_interview_questions(job_skills, kb_text):
    """
    Generates a list of interview questions based on job skills, common HR questions,
    and knowledge base text.
    
    Args:
        job_skills (list): List of skills required for the job.
        kb_text (str): Combined text from knowledge base files.
    
    Returns:
        str: Formatted string containing numbered interview questions.
    """
    questions = []
    
    # Generate technical questions from job skills
    for skill in job_skills:
        questions.append(f"Can you explain your experience with {skill}?")
    
    # Add common HR questions
    hr_questions = [
        "Tell me about yourself.",
        "Why do you want this job?",
        "What are your strengths and weaknesses?",
        "Where do you see yourself in 5 years?",
        "Why did you leave your previous job?"
    ]
    questions.extend(hr_questions)
    
    # Generate questions from first few lines of KB text
    kb_lines = kb_text.split('\n')[:3]  # Take first 3 lines
    for line in kb_lines:
        line = line.strip()
        if line:  # Only add if line is not empty
            questions.append(f"What do you know about: {line}?")
    
    # Format questions as a numbered list
    formatted_questions = "Interview Questions:\n"
    for i, question in enumerate(questions, 1):
        formatted_questions += f"{i}. {question}\n"
    
    return formatted_questions

def create_or_update_tracker():
    """
    Creates the applications tracker CSV file if it doesn't exist,
    with headers and a sample row.
    """
    tracker_file = TRACKER / "applications.csv"
    
    if not tracker_file.exists():
        with open(tracker_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write headers
            writer.writerow([
                'application_id', 'company', 'role', 'source', 'status',
                'applied_date', 'interview_date', 'follow_up_date', 'next_action', 'notes'
            ])
            
            # Add sample row
            writer.writerow([
                '1', 'TechCorp', 'Data Scientist', 'LinkedIn', 'Applied',
                '2024-01-15', '', '', 'Follow up in 1 week', 'Excited about this role'
            ])
        
        print(f"Created tracker file: {tracker_file}")
    else:
        print(f"Tracker file already exists: {tracker_file}")

def generate_reminders():
    """
    Reads the applications tracker and generates reminders based on application status.
    
    Returns:
        str: Formatted reminder text for all applications.
    """
    tracker_file = TRACKER / "applications.csv"
    
    if not tracker_file.exists():
        return "No tracker file found. Please initialize the tracker first."
    
    reminders = []
    
    with open(tracker_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            company = row.get('company', '')
            role = row.get('role', '')
            status = row.get('status', '')
            
            if not status or not company or not role:
                continue  # Skip incomplete rows
            
            if status == "Interview Scheduled":
                reminder = f"Interview Reminder: Prepare for your interview with {company} for the {role} position!"
            elif status == "Not Applied":
                reminder = f"Application Reminder: Don't forget to apply for the {role} position at {company}!"
            elif status == "Applied":
                reminder = f"Follow-up Reminder: Follow up on your application for {role} at {company}."
            else:
                continue  # Skip other statuses
            
            reminders.append(f"- {company} ({role}): {reminder}")
    
    if not reminders:
        return "No reminders needed at this time."
    
    formatted_reminders = "Job Application Reminders:\n" + "\n".join(reminders)
    return formatted_reminders

def run_agent():
    """
    Main function to run the job hunting agent.
    
    Workflow:
    1. Ensures required folders exist
    2. Reads and processes job, resume, and knowledge base files
    3. Extracts and compares skills
    4. Generates comprehensive reports
    5. Saves outputs to files
    6. Initializes application tracker
    7. Generates and saves reminders
    """
    print("Running Job Hunting Agent")
    
    # Ensure folders exist
    ensure_folders()
    
    # Read job, resume, and KB files
    job_text, num_jobs = read_text_files(INPUT_JOBS)
    resume_text, num_resumes = read_text_files(INPUT_RESUMES)
    kb_text, num_kb = read_text_files(INPUT_KB)
    
    print(f"Read {num_jobs} job files, {num_resumes} resume files, {num_kb} KB files")
    
    # Add warnings for missing files
    if num_jobs == 0:
        print("Warning: No job description files found in input_jobs/")
    if num_resumes == 0:
        print("Warning: No resume files found in input_resumes/")
    if num_kb == 0:
        print("Warning: No knowledge base files found in input_kb/")
    
    # Extract keywords
    job_skills = extract_keywords(job_text)
    resume_skills = extract_keywords(resume_text)
    
    print(f"Job skills: {job_skills}")
    print(f"Resume skills: {resume_skills}")
    
    # Compare skills
    matched, missing, score = compare_skills(job_skills, resume_skills)
    
    print(f"Skill match: {score:.1f}%")
    
    # Generate all reports
    job_analysis = generate_job_analysis(job_text, job_skills)
    skill_gap = generate_skill_gap_report(job_skills, resume_skills, matched, missing, score)
    resume_suggestions = generate_resume_suggestions(job_skills, missing)
    interview_questions = generate_interview_questions(job_skills, kb_text)
    
    # Create final agent report
    final_report = f"{job_analysis}\n\n{skill_gap}\n\n{resume_suggestions}\n\n{interview_questions}"
    
    # Save outputs to files
    (OUTPUTS / "job_analysis_report.txt").write_text(job_analysis, encoding='utf-8')
    (OUTPUTS / "skill_gap_report.txt").write_text(skill_gap, encoding='utf-8')
    (OUTPUTS / "tailored_resume_suggestions.txt").write_text(resume_suggestions, encoding='utf-8')
    (OUTPUTS / "interview_questions.txt").write_text(interview_questions, encoding='utf-8')
    (OUTPUTS / "final_agent_report.txt").write_text(final_report, encoding='utf-8')
    
    # Create tracker
    create_or_update_tracker()
    
    # Generate reminders
    reminders = generate_reminders()
    (TRACKER / "reminders.txt").write_text(reminders, encoding='utf-8')
    
    # Print summary
    print("Reports generated and saved to outputs/ folder")
    print("Tracker initialized and reminders saved to tracker/reminders.txt")
    print("\nReminders:")
    print(reminders)

if __name__ == "__main__":
    ensure_folders()
    run_agent()