from database.queries import get_user_by_id, update_user_profile
from database.models import User

def calculate_profile_completeness(user: User) -> int:
    """Calculates the percentage of profile completeness."""
    if not user:
        return 0
        
    fields = [
        user.college_name,
        user.degree,
        user.current_branch,
        user.current_year,
        user.current_semester,
        user.graduation_year
    ]
    
    filled = sum(1 for field in fields if field is not None and str(field).strip() != "")
    total_fields = len(fields)
    
    if total_fields == 0:
        return 0
        
    return int((filled / total_fields) * 100)

def save_profile(user_id: int, profile_data: dict) -> dict:
    """Updates the user profile in the database."""
    user = get_user_by_id(user_id)
    if not user:
        return {"success": False, "message": "User not found."}
        
    # Validate required fields
    required = ["college_name", "degree", "current_branch", "current_year", "current_semester", "graduation_year"]
    for req in required:
        if not profile_data.get(req):
            return {"success": False, "message": f"Missing required field: {req.replace('_', ' ').title()}"}

    # Update fields
    user.college_name = profile_data.get("college_name")
    user.college_website = profile_data.get("college_website")
    user.degree = profile_data.get("degree")
    user.current_branch = profile_data.get("current_branch")
    user.current_year = profile_data.get("current_year")
    user.current_semester = profile_data.get("current_semester")
    user.graduation_year = profile_data.get("graduation_year")
    
    success = update_user_profile(user)
    if success:
        return {"success": True, "message": "Profile saved successfully."}
    else:
        return {"success": False, "message": "Database error occurred during profile save."}

def get_profile(user_id: int) -> User:
    """Retrieves the user profile."""
    return get_user_by_id(user_id)
