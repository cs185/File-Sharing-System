def cut_ext(string):
    ext = string.rsplit('.', 1)[1]
    string = string.rstrip('{0}'.format(ext))
    string = string.strip('.')
    return string


def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
