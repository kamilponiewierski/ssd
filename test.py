dict1 = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
}

dict2 = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
}


print(dict1)
print(dict2)


def dict_mean(dict1, dict2, foo):
    return {
        k: foo(dict1.get(k, v), dict2.get(k, v))
        for k, v in dict1.items() | dict2.items()
    }


print(dict_mean(dict1, dict2, lambda *x: sum(x) / len(x)))
