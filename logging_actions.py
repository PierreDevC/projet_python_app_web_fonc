from functools import wraps
from flask import request
import logging

logging.basicConfig(filename='user_actions.log', level=logging.INFO)

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        action = func.__name__
        logging.info(f"User ID: {user_id}, Action: {action}")
        return func(*args, **kwargs)
    return wrapper
