from db import get_session, Group, User, AdminRole
from sqlalchemy import func
import datetime

def analyze_patterns():
    session = get_session()
    
    # 1. Find cross-group admins
    results = session.query(
        User.username, 
        User.tg_id, 
        func.count(AdminRole.group_id).label('group_count')
    ).join(AdminRole).group_by(User.id).having(func.count(AdminRole.group_id) > 1).all()
    
    patterns = []
    for r in results:
        user_groups = session.query(Group.title).join(AdminRole).filter(AdminRole.user_id == session.query(User.id).filter_by(tg_id=r.tg_id).subquery()).all()
        group_names = ", ".join([g[0] for g in user_groups])
        patterns.append({
            'user': r.username or r.tg_id,
            'count': r.group_count,
            'groups': group_names
        })
    
    session.close()
    return patterns

def find_pre_tge_projects(keywords=["TGE", "listing", "launch", "airdrop"]):
    session = get_session()
    # Simplified search: Look for keywords in group titles for now
    # In a real scenario, we'd scan messages too.
    projects = []
    for keyword in keywords:
        groups = session.query(Group).filter(Group.title.ilike(f"%{keyword}%")).all()
        for g in groups:
            projects.append(g)
    
    session.close()
    return list(set(projects)) # Deduplicate
