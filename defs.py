def copyList(x):
    y = []
    for i in range(len(x)):
        if type(x[i]) == list:
            y.append(copyList(x[i]))
        else:
            y.append(x[i])
    return y


if __name__ == '__main__':
    a = [1,2,[3, [4, 5]]]
    b = copyList(a)
    print(b)
    b[0] = 'h'
    print(a)
    print(b)
