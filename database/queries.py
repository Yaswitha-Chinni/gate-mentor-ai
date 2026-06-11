from database.db import get_connection
from database.models import User, GateGoal, StudyPlan, Progress, Resource
from typing import Optional, List

# Users

def create_user(user: User) -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (full_name, email, password_hash, mobile, gender, college_name, college_website, degree, current_branch, current_year, current_semester, graduation_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.full_name, user.email, user.password_hash, user.mobile, user.gender, user.college_name, user.college_website, user.degree, user.current_branch, user.current_year, user.current_semester, user.graduation_year))
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        conn.close()

def get_user_by_email(email: str) -> Optional[User]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(
            user_id=row[0], full_name=row[1], email=row[2], password_hash=row[3],
            mobile=row[4], gender=row[5], college_name=row[6], college_website=row[7],
            degree=row[8], current_branch=row[9], current_year=row[10],
            current_semester=row[11], graduation_year=row[12], created_at=row[13]
        )
    return None

def get_user_by_id(user_id: int) -> Optional[User]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(
            user_id=row[0], full_name=row[1], email=row[2], password_hash=row[3],
            mobile=row[4], gender=row[5], college_name=row[6], college_website=row[7],
            degree=row[8], current_branch=row[9], current_year=row[10],
            current_semester=row[11], graduation_year=row[12], created_at=row[13]
        )
    return None

# Gate Goals

def create_goal(goal: GateGoal) -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO gate_goals (user_id, target_gate_year, target_papers, target_rank, target_score, attempt_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (goal.user_id, goal.target_gate_year, goal.target_papers, goal.target_rank, goal.target_score, goal.attempt_type))
        goal_id = cursor.lastrowid
        conn.commit()
        return goal_id
    except Exception as e:
        print(f"Error creating goal: {e}")
        return None
    finally:
        conn.close()

def get_goal(user_id: int) -> Optional[GateGoal]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gate_goals WHERE user_id = ? ORDER BY goal_id DESC LIMIT 1", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return GateGoal(
            goal_id=row[0], user_id=row[1], target_gate_year=row[2],
            target_papers=row[3], target_rank=row[4], target_score=row[5],
            attempt_type=row[6], created_at=row[7]
        )
    return None

# Study Plans

def save_study_plan(plan: StudyPlan) -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO study_plans (user_id, month_number, subject_name, topic_name, planned_hours, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (plan.user_id, plan.month_number, plan.subject_name, plan.topic_name, plan.planned_hours, plan.status))
        plan_id = cursor.lastrowid
        conn.commit()
        return plan_id
    except Exception as e:
        print(f"Error saving study plan: {e}")
        return None
    finally:
        conn.close()

def get_study_plan(user_id: int) -> List[StudyPlan]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM study_plans WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    plans = []
    for row in rows:
        plans.append(StudyPlan(
            plan_id=row[0], user_id=row[1], month_number=row[2],
            subject_name=row[3], topic_name=row[4], planned_hours=row[5], status=row[6]
        ))
    return plans

# Progress

def update_progress(progress: Progress):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT progress_id FROM progress WHERE user_id = ? AND topic_id = ?", (progress.user_id, progress.topic_id))
    row = cursor.fetchone()
    
    if row:
        cursor.execute("UPDATE progress SET status = ?, completion_date = ?, study_hours = ? WHERE progress_id = ?", 
                       (progress.status, progress.completion_date, progress.study_hours, row[0]))
    else:
        cursor.execute("INSERT INTO progress (user_id, topic_id, status, completion_date, study_hours) VALUES (?, ?, ?, ?, ?)",
                       (progress.user_id, progress.topic_id, progress.status, progress.completion_date, progress.study_hours))
    conn.commit()
    conn.close()

def get_progress(user_id: int) -> List[Progress]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progress WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    progress_list = []
    for row in rows:
        progress_list.append(Progress(
            progress_id=row[0], user_id=row[1], topic_id=row[2],
            status=row[3], completion_date=row[4], study_hours=row[5]
        ))
    return progress_list

# Resources

def get_resources_by_topic(topic_id: int) -> List[Resource]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resources WHERE topic_id = ?", (topic_id,))
    rows = cursor.fetchall()
    conn.close()
    
    resources = []
    for row in rows:
        resources.append(Resource(
            resource_id=row[0], topic_id=row[1], resource_type=row[2],
            title=row[3], url=row[4]
        ))
    return resources

def update_user_profile(user: User) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE users 
            SET college_name = ?, college_website = ?, degree = ?, 
                current_branch = ?, current_year = ?, current_semester = ?, 
                graduation_year = ?
            WHERE user_id = ?
        ''', (user.college_name, user.college_website, user.degree, 
              user.current_branch, user.current_year, user.current_semester, 
              user.graduation_year, user.user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user profile: {e}")
        return False
    finally:
        conn.close()

def update_goal(goal: GateGoal) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE gate_goals 
            SET target_gate_year = ?, target_papers = ?, target_rank = ?, 
                target_score = ?, attempt_type = ?
            WHERE goal_id = ?
        ''', (goal.target_gate_year, goal.target_papers, goal.target_rank, 
              goal.target_score, goal.attempt_type, goal.goal_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating goal: {e}")
        return False
    finally:
        conn.close()

def delete_study_plan(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM study_plans WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting study plan: {e}")
        return False
    finally:
        conn.close()

def get_topic_by_name(topic_name: str) -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic_id FROM topics WHERE topic_name = ?", (topic_name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def update_study_plan_status(plan_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE study_plans SET status = ? WHERE plan_id = ?", (status, plan_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating study plan status: {e}")
    finally:
        conn.close()
