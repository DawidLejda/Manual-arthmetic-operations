from tabulate import tabulate


def moved(list):
    moved = [0] * (len(list) + 1)
    i = 1
    for num in list:
        moved[i] = num
        i += 1
    return moved


def addTwoNumbers(l1, l2):

    diff = abs(len(l1) - len(l2))
    if len(l1) > len(l2):
        size = len(l1) + 1
        while diff != 0:
            l2.insert(0, 0)
            diff -= 1
    else:
        size = len(l2) + 1
        while diff != 0:
            l1.insert(0, 0)
            diff -= 1

    output = [0] * size

    for i in range(size - 1):

        print(tabulate([moved(l1), moved(l2), output], tablefmt="grid"))
        print("\n")
        position = size - i - 1
        if type(l1[len(l1) - 1 - i]) == str:
            a, b = l1[len(l1) - 1 - i].split(" + ")
            addition = int(a) + int(b) + l2[len(l2) - i - 1]
        else:
            addition = l1[len(l1) - 1 - i] + l2[len(l2) - i - 1]

        if output[position] + addition < 10:
            output[position] += addition
        else:
            first = str(addition + output[position])[0]
            last = str(addition + output[position])[1]
            if position == 1:
                output[position] = int(first) + int(last)
            else:
                output[position] += int(last)
                l1[len(l1) - 2 - i] = str(f"{l1[len(l1) - 2 - i]} + {first} ")

    print(tabulate([moved(l1), moved(l2), output], tablefmt="grid"))
