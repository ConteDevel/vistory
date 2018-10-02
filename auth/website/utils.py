def dict_to_list(d):
    result = []
    for key, value in d.items():
        temp = "{0}: {1}".format(key, value)
        result.append(temp)
    return result
