from datetime import datetime
import random
import string

def get_init_res():
    return {
        "data": None,
        "success": False,
        "messages": "",
        "count": None
    }

def convert_simple_date(date: datetime):
    return date.strftime("%m/%d %H:%M")

def random_integer_str(n: int, except_datas=None):
    rand = [random.choice(string.digits) for i in range(n)]
    if except_datas:
        for i in range(1000):
            if rand in except_datas:
                rand = [random.choice(string.digits) for i in range(n)]
            else:
                break
    return "".join(rand)