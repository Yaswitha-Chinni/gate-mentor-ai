from database.queries import get_progress, update_progress, get_topic_by_name, update_study_plan_status, get_study_plan
from database.models import Progress
from datetime import datetime

def sync_progress_status(user_id: int, plan_id: int, topic_name: str, new_status: str, study_hours: int = 0):
    """Updates both StudyPlan and Progress tables simultaneously to ensure data consistency."""
    # Update Study Plan table
    update_study_plan_status(plan_id, new_status)
    
    # Update Progress Table
    topic_id = get_topic_by_name(topic_name)
    if topic_id:
        comp_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_status == "Completed" else None
        prog = Progress(
            user_id=user_id,
            topic_id=topic_id,
            status=new_status,
            completion_date=comp_date,
            study_hours=study_hours
        )
        update_progress(prog)
        return True
    return False

def get_subject_progress(user_id: int) -> dict:
    """Calculates completion percentage per subject."""
    plans = get_study_plan(user_id)
    subjects = {}
    
    for p in plans:
        if p.subject_name == "Final Revision & Mock Tests":
            continue
            
        if p.subject_name not in subjects:
            subjects[p.subject_name] = {"total": 0, "completed": 0}
            
        subjects[p.subject_name]["total"] += 1
        if p.status == "Completed":
            subjects[p.subject_name]["completed"] += 1
            
    result = {}
    for subj, counts in subjects.items():
        if counts["total"] > 0:
            result[subj] = int((counts["completed"] / counts["total"]) * 100)
        else:
            result[subj] = 0
            
    return result

def calculate_overall_completion(user_id: int) -> int:
    """Calculates overall progress percentage based on completed topics."""
    plans = get_study_plan(user_id)
    valid_plans = [p for p in plans if p.subject_name != "Final Revision & Mock Tests"]
    
    if not valid_plans:
        return 0
        
    completed = len([p for p in valid_plans if p.status == "Completed"])
    return int((completed / len(valid_plans)) * 100)
