import os
import json
import csv
import io
from datetime import datetime
from database.queries import get_goal, save_study_plan, delete_study_plan, get_study_plan
from database.models import StudyPlan

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_syllabus() -> dict:
    """Loads the GATE CSE syllabus from JSON."""
    syllabus_path = os.path.join(BASE_DIR, "data", "gate_cse_syllabus.json")
    if os.path.exists(syllabus_path):
        with open(syllabus_path, "r") as f:
            return json.load(f)
    return {}

def generate_study_plan(user_id: int, intensity: str) -> dict:
    """Generates a rule-based study plan and stores it in the database."""
    goal = get_goal(user_id)
    if not goal:
        return {"success": False, "message": "GATE Goal not found. Please setup your goal first."}
        
    syllabus = load_syllabus()
    if not syllabus:
        return {"success": False, "message": "Syllabus data missing."}
        
    current_year = datetime.now().year
    target_year = goal.target_gate_year
    
    # Calculate months remaining
    months_remaining = (target_year - current_year) * 12
    # If target year is current year, assume at least 6 months for the MVP
    if months_remaining <= 0:
        months_remaining = 6
        
    # Determine hours based on intensity
    hours_per_topic = 5
    if intensity == "Serious":
        hours_per_topic = 8
    elif intensity == "Rank < 1000":
        hours_per_topic = 12
    elif intensity == "Rank < 100":
        hours_per_topic = 18
        
    # Clear existing plan
    delete_study_plan(user_id)
    
    subjects = list(syllabus.keys())
    
    # Reserve last 2 months for revision
    study_months = max(1, months_remaining - 2)
    
    # Allocate subjects to months
    for i, subject in enumerate(subjects):
        assign_month = (i % study_months) + 1
        topics = syllabus[subject]
        
        for topic in topics:
            plan = StudyPlan(
                user_id=user_id,
                month_number=assign_month,
                subject_name=subject,
                topic_name=topic,
                planned_hours=hours_per_topic,
                status="Not Started"
            )
            save_study_plan(plan)
            
    # Allocate Revision
    for rev_month in range(study_months + 1, months_remaining + 1):
        plan = StudyPlan(
            user_id=user_id,
            month_number=rev_month,
            subject_name="Final Revision & Mock Tests",
            topic_name="PYQ Practice and Full Length Mocks",
            planned_hours=hours_per_topic * 4,
            status="Not Started"
        )
        save_study_plan(plan)
        
    return {"success": True, "message": "Study plan generated successfully."}

def export_plan_to_csv(plans) -> str:
    """Exports the given plans to a CSV formatted string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Month", "Subject", "Topic", "Planned Hours", "Status"])
    for p in plans:
        writer.writerow([f"Month {p.month_number}", p.subject_name, p.topic_name, p.planned_hours, p.status])
    return output.getvalue()
