
from AK import (
    extract_text,
    preprocess_text,
    extract_skills,
    rank_resumes,
    generate_pdf_report,
    load_skill_set,
    identify_skill_gaps,
    collect_feedback,
    detect_overqualification,
    check_resume_formatting,
    generate_summary_report,
)

# Paths to test files
test_resumes = ["test_resume1.pdf", "test_resume2.pdf"]  # Replace with actual paths
test_job_description_path = "test_job_description.txt"  # Replace with actual path
test_skill_file_path = "test_skills.txt"  # Replace with actual path
test_feedback_log = "test_feedback_log.txt"

# Sample test cases
def test_extract_text():
    for resume in test_resumes:
        text = extract_text(resume)
        assert text, f"Failed to extract text from {resume}"
    print("Extract text test passed.")

def test_preprocess_text():
    sample_text = "This is a test! With punctuation and stopwords."
    processed = preprocess_text(sample_text)
    assert "test" in processed and "punctuation" in processed, "Preprocessing failed"
    print("Preprocess text test passed.")

def test_extract_skills():
    sample_text = "I am skilled in Python, Machine Learning, and SQL."
    skill_set = {"Python", "Machine Learning", "SQL", "Java"}
    extracted = extract_skills(sample_text, skill_set)
    assert set(extracted) == {"Python", "Machine Learning", "SQL"}, "Skill extraction failed"
    print("Extract skills test passed.")

def test_rank_resumes():
    sample_resumes = ["I have experience in Python.", "Skilled in Java."]
    job_description = "Looking for a Python developer."
    ranked = rank_resumes(sample_resumes, job_description)
    assert ranked[0][1] > ranked[1][1], "Ranking logic failed"
    print("Rank resumes test passed.")

def test_generate_pdf_report():
    ranked_resumes = [("Resume 1", 0.8), ("Resume 2", 0.6)]
    skill_gaps = ["Data Analysis", "Machine Learning"]
    generate_pdf_report(ranked_resumes, skill_gaps, "test_report.pdf")
    print("PDF report generation test passed.")

def test_load_skill_set():
    skill_set = load_skill_set(test_skill_file_path)
    assert skill_set, "Failed to load skills"
    print("Load skill set test passed.")

def test_identify_skill_gaps():
    extracted_skills = {"Python", "SQL"}
    required_skills = {"Python", "SQL", "Data Analysis"}
    gaps = identify_skill_gaps(extracted_skills, required_skills)
    assert gaps == ["Data Analysis"], "Skill gap identification failed"
    print("Identify skill gaps test passed.")

def test_collect_feedback():
    collect_feedback(1, "Good candidate", test_feedback_log)
    print("Feedback collection test passed.")

def test_detect_overqualification():
    resume_text = "Senior Developer with advanced skills."
    job_description = "Looking for an entry-level developer."
    is_overqualified = detect_overqualification(resume_text, job_description)
    assert is_overqualified, "Overqualification detection failed"
    print("Detect overqualification test passed.")

def test_check_resume_formatting():
    resume_text = "John Doe\nEducation: XYZ University\nExperience: 5 years\nSkills: Python"
    issues = check_resume_formatting(resume_text)
    assert "No formatting issues detected." in issues, "Formatting check failed"
    print("Check resume formatting test passed.")

def test_generate_summary_report():
    ranked_resumes = [("Resume 1", 0.8), ("Resume 2", 0.6)]
    skill_gaps = ["Data Analysis", "Machine Learning"]
    generate_summary_report(ranked_resumes, skill_gaps, "test_summary_report.json")
    print("Summary report generation test passed.")

if __name__ == "__main__":
    print("Running tests...")
    test_extract_text()
    test_preprocess_text()
    test_extract_skills()
    test_rank_resumes()
    test_generate_pdf_report()
    test_load_skill_set()
    test_identify_skill_gaps()
    test_collect_feedback()
    test_detect_overqualification()
    test_check_resume_formatting()
    test_generate_summary_report()
    print("All tests passed.")
