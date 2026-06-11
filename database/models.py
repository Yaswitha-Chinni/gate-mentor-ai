from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    full_name: str
    email: str
    password_hash: str
    mobile: Optional[str] = None
    gender: Optional[str] = None
    college_name: Optional[str] = None
    college_website: Optional[str] = None
    degree: Optional[str] = None
    current_branch: Optional[str] = None
    current_year: Optional[str] = None
    current_semester: Optional[str] = None
    graduation_year: Optional[int] = None
    created_at: Optional[str] = None
    user_id: Optional[int] = None

@dataclass
class GateGoal:
    user_id: int
    target_gate_year: int
    target_papers: str
    target_rank: Optional[int] = None
    target_score: Optional[int] = None
    attempt_type: Optional[str] = None
    created_at: Optional[str] = None
    goal_id: Optional[int] = None

@dataclass
class Subject:
    subject_name: str
    weightage: Optional[int] = None
    subject_id: Optional[int] = None

@dataclass
class Topic:
    subject_id: int
    topic_name: str
    estimated_hours: Optional[int] = None
    topic_id: Optional[int] = None

@dataclass
class StudyPlan:
    user_id: int
    month_number: int
    subject_name: str
    topic_name: str
    planned_hours: Optional[int] = None
    status: str = "Pending"
    plan_id: Optional[int] = None

@dataclass
class Progress:
    user_id: int
    topic_id: int
    status: str
    completion_date: Optional[str] = None
    study_hours: Optional[int] = None
    progress_id: Optional[int] = None

@dataclass
class Resource:
    topic_id: int
    resource_type: str
    title: str
    url: str
    resource_id: Optional[int] = None
