def is_positive_number(value):
    try:
        return float(value) >= 0
    except:
        return False

def is_not_empty(value):
    return bool(value and str(value).strip())
