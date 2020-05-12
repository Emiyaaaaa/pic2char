def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

print(is_all_chinese('i love yiu'))
print(is_all_chinese('i love you'))
print(is_all_chinese('中国'))