import os
from dotenv import load_dotenv

load_dotenv()

def str2bool(s):
    if not s:
        return False
    return s.lower() in ["true"]

def Env(key: str, type: str = "str"):
    val = os.getenv(key)
    if type == "bool":
        return str2bool(val)
    if type == "int":
        return int(val)
    return val