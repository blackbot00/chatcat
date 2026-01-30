from app.db.mongo import users_col

QUEUE = []

def add_to_queue(user_id: int):
    if user_id not in QUEUE:
        QUEUE.append(user_id)

def pop_match(user_id: int):
    for uid in QUEUE:
        if uid != user_id:
            QUEUE.remove(uid)
            return uid
    return None

def remove_from_queue(user_id: int):
    if user_id in QUEUE:
        QUEUE.remove(user_id)
