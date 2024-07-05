import time
import timeit

from adder import addTwoNumbers

15
l2 = [1, 2, 9]


def main():
    term1_num = input("First number: ")
    term2_num = input("Second number: ")
    l1 = input_to_array(term1_num)
    l2 = input_to_array(term2_num)

    addTwoNumbers(l1, l2)


def input_to_array(l):
    new_l = [0] * len(l)
    i = 0
    for num in l:
        new_l[i] = int(num)
        i += 1
    return new_l


if __name__ == "__main__":
    execution_time = timeit.timeit(main, number=1)

print(f"Executed in {execution_time} seconds")
