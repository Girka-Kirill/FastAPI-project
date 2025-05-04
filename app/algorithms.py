"""
Бизнес-логика распределения задач
"""
from sqlalchemy.orm import Session, joinedload
import numpy as np
from scipy.optimize import linear_sum_assignment
from . import schemas, models

def optimal_task_assignment(db: Session, assignment_request):
    """
    Функция оптимального распределения задач
    """
    user_skills = {}
    user_workload = {}
    task_requirements = {}
    users = db.query(models.User).options(
        joinedload(models.User.skills).joinedload(models.UserSkill.skill)
    ).all()
    tasks = db.query(models.Task).options(
        joinedload(models.Task.required_skills).joinedload(models.TaskSkill.skill)
    ).filter(
        models.Task.id.in_(assignment_request.task_ids),
        models.Task.status == "open"
    ).all()
    if not users or not tasks:
        return []
    # Calculate user skill levels
    for user in users:
        skills = {}
        for user_skill in user.skills:
            skills[user_skill.skill_id] = user_skill.level
        user_skills[user.id] = skills  # Теперь переменная определена
        user_workload[user.id] = len(user.tasks)
    # Calculate task requirements
    for task in tasks:
        requirements = {}
        for task_skill in task.required_skills:
            requirements[task_skill.skill_id] = task_skill.required_level
        task_requirements[task.id] = requirements
    # Create a cost matrix for the assignment problem
    cost_matrix = np.zeros((len(tasks), len(users)))
    for i, task in enumerate(tasks):
        for j, user in enumerate(users):
            # Skill match score (higher is better)
            skill_score = 0
            for skill_id, required_level in task_requirements.get(task.id, {}).items():
                user_level = user_skills.get(user.id, {}).get(skill_id, 0)
                if user_level >= required_level:
                    skill_score += 1
                else:
                    skill_score -= 2  # Penalize for missing skills
            # Workload factor (lower is better)
            workload_max = max(1, sum(user_workload.values()) / len(users))
            workload_factor = user_workload[user.id] / workload_max
            # Priority factor (higher priority tasks should be assigned first)
            priority_factor = task.priority / 5  # Assuming priority 1-5
            # Combine factors into a cost (we want to minimize this)
            cost = -skill_score + workload_factor * 10 - priority_factor * 2
            cost_matrix[i, j] = cost
    # Solve the assignment problem using the Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    # Prepare the results
    assignments = []
    for task_idx, user_idx in zip(row_ind, col_ind):
        task = tasks[task_idx]
        user = users[user_idx]
        assignments.append(schemas.TaskAssignment(
            task_id=task.id,
            user_id=user.id,
            score=-cost_matrix[task_idx, user_idx],  # Convert back to positive score
            assigned_skills=[
                skill.name for skill in user.skills
                if skill.skill_id in task_requirements.get(task.id, {})
            ]
        ))
        # Update the task in the database
        task.owner_id = user.id
        task.status = "assigned"
        db.add(task)
    db.commit()
    return assignments
