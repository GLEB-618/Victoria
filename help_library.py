def conversion(text):
    try:
        text = int(text)
        return True
    except ValueError:
        return False

def review(list, text):
    answer = False
    for x in list:
        if x in text:
            answer = True
    return answer