def change(s):
    k = ''
    for i in s:
        if i == '\n':
            k += '<br/>'
        elif i == ' ':
            k += '&nbsp;'
        else:
            k += i
    return k
