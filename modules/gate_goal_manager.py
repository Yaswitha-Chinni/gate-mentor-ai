from database.queries import create_goal, get_goal, update_goal
from database.models import GateGoal

def save_user_goal(user_id: int, goal_data: dict) -> dict:
    """Creates or updates a GATE Goal for the user."""
    # Validate required fields
    if not goal_data.get("target_gate_year"):
        return {"success": False, "message": "Target GATE Year is required."}
    
    target_papers = goal_data.get("target_papers", [])
    if not target_papers:
        return {"success": False, "message": "At least one Target Paper is required."}
        
    if not goal_data.get("attempt_type"):
        return {"success": False, "message": "Attempt Type is required."}
        
    papers_str = ",".join(target_papers)
    
    existing_goal = get_goal(user_id)
    if existing_goal:
        # Update existing goal
        existing_goal.target_gate_year = goal_data.get("target_gate_year")
        existing_goal.target_papers = papers_str
        existing_goal.attempt_type = goal_data.get("attempt_type")
        existing_goal.target_rank = goal_data.get("target_rank")
        existing_goal.target_score = goal_data.get("target_score")
        success = update_goal(existing_goal)
        action = "updated"
    else:
        # Create new goal
        new_goal = GateGoal(
            user_id=user_id,
            target_gate_year=goal_data.get("target_gate_year"),
            target_papers=papers_str,
            attempt_type=goal_data.get("attempt_type"),
            target_rank=goal_data.get("target_rank"),
            target_score=goal_data.get("target_score")
        )
        goal_id = create_goal(new_goal)
        success = goal_id is not None
        action = "saved"
        
    if success:
        return {"success": True, "message": f"GATE Goal {action} successfully."}
    else:
        return {"success": False, "message": "Failed to save GATE Goal. Database error."}

def get_user_goal(user_id: int) -> GateGoal:
    """Retrieves the user's current GATE Goal."""
    return get_goal(user_id)
