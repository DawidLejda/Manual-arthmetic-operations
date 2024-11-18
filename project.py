import copy
from tabulate import tabulate, SEPARATING_LINE
import os
from rich.console import Console
from time import sleep
import csv
from fpdf import FPDF

console = Console()


def main():
    step_by_step = False
    count_wrong_inputs = 0
    index = 1
    while True:
        try:
            save = False
            write_history = True
            command = input("\nInput math problem: ").rstrip()
            os.system("cls")
            if command == "/steps":
                step_by_step = steps(step_by_step)
                continue
            elif command == "/history":
                history_command, save, step_by_step = history(step_by_step)
                if history_command == "/history":
                    continue
                else:
                    command = history_command
                    write_history = False
                    os.system("cls")
            elif command == "/help":
                help()
                continue

            l1, l2, operation, outputs, row_width = input_to_list(command)

            if write_history:
                with open("history.csv", "a") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["index", "equation"])
                    writer.writerow({"index": index, "equation": command})
                    index += 1

            size = sizing(l1, l2, operation)
            match operation:
                case "+":
                    output = Addition(l1, l2, size)
                case "-":
                    output = Subtraction(l1, l2, size)
                case "*":
                    output = Multiplication(l1, l2, row_width, outputs)
                case "/":
                    output = Division(l1, l2, len(l1))

            if save == False:
                i = 1
                for table in output:
                    if step_by_step == True:
                        console.print(f"{table}\n", style="bold cyan3")
                        loading = (
                            "[bold][dark_green].[/dark_green][green].[/green][spring_green1].[/spring_green1] [/bold]"
                        ) * i
                        console.print(f"{loading}\n")
                        i += 1
                        sleep(1.5)
                    else:
                        final = table
                if step_by_step == False:
                    console.print(final, style="bold cyan3")
            else:
                save_to_pdf(output, step_by_step, command)

            count_wrong_inputs = 0
        except ValueError:
            console.print(
                "Given input is in wrong fromat !", style="bold yellow3 underline"
            )
            count_wrong_inputs += 1
            if count_wrong_inputs == 3:
                console.print(
                    "If you wish to know exact aviable commands type [dark_cyan]/help[/dark_cyan]"
                )
                count_wrong_inputs = 0
        except EOFError:
            try:
                os.remove("history.csv")
            except FileNotFoundError:
                pass
            break
        except ZeroDivisionError:
            console.print(
                "Given input is in wrong fromat !", style="bold yellow3 underline"
            )


def help():
    console.print(
        "\nProgram by default returns only final calculation result\nTo get a result step by step type[dark_cyan] /steps [/dark_cyan]"
    )
    console.print(
        "\nTo view history of calculations type[dark_cyan] /history [/dark_cyan]"
    )
    console.print("\nTo exit program press [dark_cyan]CTRL+Z[/dark_cyan]")
    console.print(
        "\n[bold cyan3]Commands for mathematical operations [/bold cyan3]",
    )
    console.print("Addition :[dark_cyan] number + number [/dark_cyan] ")
    console.print("Subtraction :[dark_cyan] number - number [/dark_cyan] ")
    console.print("Multiplication :[dark_cyan] number * number [/dark_cyan] ")
    console.print("Division :[dark_cyan] number / number [/dark_cyan] ")


def steps(step_by_step):
    step_by_step = not step_by_step
    if step_by_step == True:
        console.print("Solutions will be shown in longer form", style="bold cyan3")
    else:
        console.print("Solutions will be shown in shortened form", style="bold cyan3")

    return step_by_step


def save_to_pdf(output, step_by_step, command):

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_font("helvetica", "I", 14)
    pdf.add_page()
    for table in output:
        if step_by_step == True:
            pdf.write(text=table)
            pdf.ln(20)
        else:
            final = table
    if step_by_step == False:
        pdf.write(text=final)
        pdf.ln(20)
    console.print("File succesfuly saved at", os.path.dirname(__file__))

    if command.find("/") != -1:
        first, last = command.split("/")
        command = f"{first}_div_by_{last}.pdf"
    elif command.find("*") != -1:
        first, last = command.split("*")
        command = f"{first}_x_{last}.pdf"
    else:
        command = f"{command}.pdf"
    pdf.output(command)


def history(step_by_step):
    while True:
        Save = False
        os.system("cls")

        try:
            if command == "/steps":
                step_by_step = steps(step_by_step)
        except UnboundLocalError:
            pass
        console.print(
            "Type index of equation you wish to open or retype [dark_cyan]/history[/dark_cyan] to go back to main menu"
        )
        console.print(
            "To save to pdf file type [dark_cyan]/save[/dark_cyan] [deep_sky_blue2]index_number[/deep_sky_blue2]\n"
        )
        console.print("[deep_sky_blue2]#########################[/deep_sky_blue2]")
        command_logs = []
        with open("history.csv") as file:
            for line in file:
                if line == "\n":
                    continue
                index, equation = line.rstrip().split(",")
                log = {"index": index, "equation": equation}
                command_logs.append(log)
        for log in command_logs:
            console.print(f"{log['index']} - [cyan3]{log['equation']}[/cyan3]")
        console.print("[deep_sky_blue2]#########################[/deep_sky_blue2]")

        command = input("Input: ").rstrip()

        if command == "/history":
            return command, Save, step_by_step
        elif command == "/steps":
            continue
        elif command.startswith("/save"):
            prefix, number = command.split(" ")
            command = number
            Save = True

        if any(log["index"] == command for log in command_logs):
            for log in command_logs:
                if log["index"] == command:
                    return log["equation"], Save, step_by_step


def input_to_list(string):

    operation_detected = False
    l1, l2 = [], []
    string = string.replace(" ", "")

    for char in string.strip(" "):

        if char == "+" or char == "-" or char == "*" or char == "/":
            if char == "-":
                first, last = string.split("-")
                if int("".join(first)) < int("".join(last)):
                    raise ValueError("Only subtractino higher numer - smaller number")
            elif char == "/":
                first, last = string.split("/")
                if int("".join(first)) < int("".join(last)):
                    raise ValueError("Only division higher number - smaller number")
            if operation_detected == False:
                operation = char
                operation_detected = True
            else:
                raise ValueError

        elif operation_detected == False:
            l1.append(int(char))
        else:
            l2.append(int(char))
    try:
        l1_int = int("".join(str(x) for x in l1))
        l2_int = int("".join(str(x) for x in l2))
        output_len = len(str(l1_int * l2_int))
        outputs = len(l2)
        return l1, l2, operation, outputs, output_len
    except UnboundLocalError:
        raise ValueError


def sizing(l1, l2, operation):
    diff = abs(len(l1) - len(l2))
    if len(l1) > len(l2):
        size = len(l1) + 1
        while diff != 0:
            if operation != "*":
                l2.insert(0, 0)
            else:
                l2.insert(0, " ")
            diff -= 1
    else:
        size = len(l2) + 1
        while diff != 0:
            if operation != "*":
                l1.insert(0, 0)
            else:
                l1.insert(0, " ")
            diff -= 1
    return size


def moved(list):

    moved = [" "] * (len(list) + 1)
    i = 1
    for num in list:
        moved[i] = num
        i += 1
    return moved


def replaced(list):
    replaced = [0] * (len(list))
    i = 0
    for num in list:
        if num == " ":
            num = 0
        replaced[i] = int(num)
        i += 1
    return replaced


def string_modification(list1, position, mark=False):
    costumized = list1.copy()

    if mark == False:
        for i in range(len(list1)):
            if position[i] == 1:
                costumized[i] = str("\u0336{}".format(costumized[i]))
    else:
        costumized[position] = f"[{str(costumized[position])}]"

    return costumized


def iteration_count(list):
    new_iterations = 0
    for num in list:
        if type(num) == int:
            new_iterations += 1
    return new_iterations


def indendation_of_sum(output):

    shifted_output = copy.deepcopy(output)

    for i in range(len(output)):
        shifts = i
        row_shifted = 0

        for k in range(len(shifted_output[i]) - 1):
            curr_shift_pos = -1 - k
            if shifted_output[i][-1 - k] != " " and shifted_output[i][-1 - k] >= 10:
                shifted_output[i][-1 - k] -= 10
                if shifted_output[i][curr_shift_pos - 1] != " ":
                    shifted_output[i][curr_shift_pos - 1] += 1
                else:
                    shifted_output[i][curr_shift_pos - 1] = 1

        while shifts > 0:
            curr_array = shifted_output[i].copy()
            for j in range(len(curr_array) - 1):

                curr_shift_pos = -1 - j
                shifted_output[i][curr_shift_pos - 1] = curr_array[curr_shift_pos]

            for to_left in range(row_shifted + 1):
                shifted_output[i][len(shifted_output[i]) - 1 - to_left] = " "
            row_shifted += 1
            shifts -= 1

    return shifted_output


def print_output(l1, l2, output, header, multi=False, row=False, final=False, i=0):

    if multi == False:
        return tabulate(
            [moved(l1), moved(l2), SEPARATING_LINE, moved(output)],
            header,
            numalign="center",
        )
    else:
        if row == False:
            return tabulate(
                [moved(l1), moved(l2), SEPARATING_LINE, output],
                header,
                numalign="center",
            )

        else:

            shifted_output = True
            while type(shifted_output) == bool:
                shifted_output = indendation_of_sum(output)

            if final == False:
                return tabulate(
                    [
                        moved(l1),
                        string_modification(moved(l2), i, True),
                        SEPARATING_LINE,
                        *shifted_output,
                    ],
                    header,
                    numalign="center",
                )
            else:

                last_row = len(shifted_output[len(shifted_output) - 1])
                final_output = [0] * last_row

                for k in range(len(output)):
                    final_output = multi_addition(
                        final_output, shifted_output[k], len(final_output)
                    )

                return tabulate(
                    [
                        moved(l1),
                        moved(l2),
                        SEPARATING_LINE,
                        *shifted_output,
                        SEPARATING_LINE,
                        final_output,
                    ],
                    header,
                    numalign="center",
                )


def multi_addition(l1, l2, size):
    header, output = [" "] * size, [" "] * size
    l1 = replaced(l1)
    l2 = replaced(l2)
    output = replaced(output)
    while len(l2) != len(output):
        header.insert(0, " ")
        l1.insert(0, 0)
        output.insert(0, 0)
        size += 1

    for i in range(size):
        if i == 0:
            continue
        position = size - i

        if header[position] != " ":
            addition = int(header[position]) + l1[position] + l2[position]
        else:
            addition = l1[position] + l2[position]

        if output[position] != " ":
            output[position] = int(output[position])
        else:
            output[position] = 0

        if output[position] + addition < 10:
            output[position] += addition
        else:
            first = str(addition + output[position])[0]
            last = str(addition + output[position])[1]
            header[position - 1] = first
            output[position] += int(last)

    if l1[0] == 0 and l2[0] == 0 and header[0] == " ":
        output[0] = " "
    else:
        output[0] += l1[0] + l2[0]
        if header[0] != " ":
            output[0] += int(header[0])

    return output


def Addition(l1, l2, size):
    header, output = [" "] * size, [" "] * size

    header = [" "] * size
    l1.insert(0, " ")
    l2.insert(0, "+")

    for i in range(size):
        if i == 0:
            continue
        position = size - i

        if header[position] != " ":
            addition = int(header[position]) + l1[position] + l2[position]
        else:
            addition = l1[position] + l2[position]

        if output[position] != " ":
            output[position] = int(output[position])
        else:
            output[position] = 0

        if output[position] + addition < 10:
            output[position] += addition
        else:
            first = str(addition + output[position])[0]
            last = str(addition + output[position])[1]

            if position != 1:
                header[position - 1] = first
            if position == 1:
                output[position - 1] = int(first)
                output[position] += int(last)
            else:
                output[position] += int(last)
        yield print_output(l1, l2, output, header)


def Subtraction(l1, l2, size):
    header, output, srikethrough = [" "] * size, [" "] * size, [0] * size
    l1.insert(0, " ")
    l2.insert(0, "-")

    for i in range(size - 1):
        position = -1 - i
        if abs(position) >= size:
            break

        if l1[position] < l2[position]:
            if header[position] == " " or (
                header[position] != " " and (int(header[position]) < l2[position])
            ):

                while True:
                    if header[position] != " " and (
                        int(header[position]) > l2[position]
                    ):
                        if l1[position - 1] == 0:
                            header[position] += l1[position]
                        break

                    for k in range(len(header) - 1):

                        if header[position] != " " and (
                            int(header[position]) > l2[position]
                        ):
                            break

                        if header[position - k] == " " or (
                            header[position] != " "
                            and (int(header[position]) < l2[position])
                        ):
                            if l1[position - k - 1] == 0:
                                pass
                            else:
                                header[position - 1 - k] = l1[position - 1 - k] - 1
                                srikethrough[position - 1 - k] = 1
                                if header[position] == " ":
                                    header[position - k] = l1[position - k] + 10
                                else:
                                    header[position - k] = header[position - k] + 10
                                break
                        else:
                            try:
                                header[position - k] -= 1
                                srikethrough[position - k] = 1
                                header[position - k + 1] = 10
                                break
                            except IndexError:
                                break

        if header[position] != " ":
            output[position] = header[position] - l2[position]
        else:
            output[position] = l1[position] - l2[position]

        if i == size - 2:
            for j in range(len(output) - 1):
                if j == 0 and output[j] == 0:
                    output[j] = " "
                elif output[j] == 0 and (output[j - 1] == 0 or output[j - 1] == " "):
                    output[j] = " "

        l1_stike = string_modification(l1, srikethrough)
        yield print_output(l1_stike, l2, output, header)


def Multiplication(l1, l2, size, count_outputs):
    output = []
    l1_iterations = iteration_count(l1)
    l1.insert(0, " ")
    l2.insert(0, "x")
    while len(l1) < size - 1:
        l1.insert(0, " ")
        l2.insert(0, " ")
    while size <= len(l1):
        size += 1

    for _ in range(count_outputs):
        output.append([" "] * (size))

    shift = 0
    for i in range(count_outputs + 1):
        header = [" "] * len(output[0])
        if i == 0:
            continue
        l1_position = -1
        l2_position = -1 - shift
        output_position = -1
        for _ in range(l1_iterations):
            if (
                l1[l1_position] == " "
                or l2[l2_position] == " "
                or l2[l2_position] == "⛌"
            ):
                break

            multi = l2[l2_position] * l1[l1_position]
            if multi < 10:
                output[i - 1][output_position] = multi
            else:
                first, last = str(multi)
                if l1[l1_position - 1] == " ":
                    output[i - 1][output_position - 1] = int(first)
                    output[i - 1][output_position] = int(last)
                else:
                    header[output_position - 1] = int(first)
                    output[i - 1][output_position] = int(last)

            if header[output_position] != " ":
                output[i - 1][output_position] = (
                    output[i - 1][output_position] + header[output_position]
                )

            l1_position -= 1
            output_position -= 1
        yield print_output(l1, l2, output[:i], header, True, True, False, (-1 - shift))

        header = [" "] * len(output[0])
        shift += 1

        if i == count_outputs:
            yield print_output(l1, l2, output[:], header, True, True, True)
            break


def number_to_list(string, size):
    i = 0
    list = [0] * size
    for num in str(string):
        list[i] = int(num)
        i += 1
    return list


def dividing(output, next_output, div_x_quotient):
    j = 0
    for _ in range(len(output) - 1):
        if output[_] == " ":
            j += 1
        else:
            break
    output_size = len(div_x_quotient)
    k = 0
    while k < output_size:
        next_output[j] = int(div_x_quotient[k])
        k += 1
        j += 1


def subtracting_division(l1, l2, size):
    (header,output,) = [" "] * size, [" "] * size
    

    for _ in range(size):
        if(len(l1) != size):
            l1.insert(0,0)
        if(len(l2) != size):
            l2.insert(0,0)

        if l1[_] == " ":
            l1[_] = 0
        if l2[_] == " ":
            l2[_] = 0
    size += 1

    for i in range(size - 1):
        position = -1 - i
        if abs(position) >= size:
            break

        if l1[position] < l2[position]:
            if header[position] == " " or (
                header[position] != " " and (int(header[position]) < l2[position])
            ):
                while True:

                    if header[position] != " " and (
                        int(header[position]) > l2[position]
                    ):
                        if l1[position - 1] == 0:
                            header[position] += l1[position]
                        break

                    for k in range(len(header) - 1):

                        if header[position] != " " and (
                            int(header[position]) > l2[position]
                        ):
                            break

                        if header[position - k] == " " or (
                            header[position] != " "
                            and (int(header[position]) < l2[position])
                        ):
                            if l1[position - k - 1] == 0:
                                pass
                            else:
                                header[position - 1 - k] = l1[position - 1 - k] - 1
                                if header[position] == " ":
                                    header[position - k] = l1[position - k] + 10
                                else:
                                    header[position - k] = header[position - k] + 10
                                break
                        else:
                            try:
                                header[position - k] -= 1
                                header[position - k + 1] = 10
                                break
                            except IndexError:
                                break

        if header[position] != " ":
            output[position] = header[position] - l2[position]
        else:
            output[position] = l1[position] - l2[position]

    for j in range(len(output) - 1):
        if j == 0 and output[j] == 0:
            output[j] = " "
        elif output[j] == 0 and (output[j - 1] == 0 or output[j - 1] == " "):
            output[j] = " "

    return output


def Division(l1, l2, size):
    dividend = int("".join(str(x) for x in l1))
    divisor = int("".join(str(x) for x in l2))
    equation = str(dividend) + ":" + str(divisor)
    output, main_line, output = [], [], []
    main_line.append([num for num in equation])
    header = [" "] * (len(str(dividend)) + len(str(divisor)) + 1)

    for _ in range(1, 5):
        if _ == 1:
            output.append(number_to_list(dividend, len(str(dividend))))
        elif _ % 3 == 0:
            output.append(SEPARATING_LINE)
        else:
            output.append([" "] * size)

    shifts = 0
    output_position = 0
    for i in range(size):
        i += shifts

        if i == 0:
            dividend = l1[i]
        else:
            zero = True
            for x in enumerate ((output[output_position]), i):
                if type(x) == int:
                    zero = False         
                
            if zero:
                dividend = 0
            else:
                dividend = int("".join(str(x) for x in output[output_position]))
            

        if dividend >= divisor:
            remainer = dividend % divisor
            header[i] = int((dividend - remainer) / divisor)
            div_x_quotient = str(divisor * header[i])
            if len(div_x_quotient) > 1:
                dividing(
                    output[output_position], output[output_position + 1], div_x_quotient
                )
            else:
                output[output_position + 1][i] = int(div_x_quotient)

        else:
            if i == 0:

                while dividend < divisor:
                    i += 1
                    shifts += 1
                    dividend = int(str(dividend) + str(l1[i]))
                    if dividend >= divisor:
                        remainer = dividend % divisor
                        header[i] = int((dividend - remainer) / divisor)
                        div_x_quotient = str(divisor * header[i])
                        if len(div_x_quotient) > 1:
                            for l in range(len(div_x_quotient)):
                                subtrahend_pos = len(str(dividend)) - 1 - l
                                output[1][subtrahend_pos] = int(div_x_quotient[-1 - l])
                        else:
                            output[1][0] = int(div_x_quotient)
                        break

            else:

                output[output_position].append(output[0][i])
                dividend = int("".join(str(x) for x in output[output_position]))
                remainer = dividend % divisor
                header[i] = int((dividend - remainer) / divisor)
                div_x_quotient = str(divisor * header[i])

                if len(div_x_quotient) > 1:
                    dividing(
                        output[output_position],
                        output[output_position + 1],
                        div_x_quotient,
                    )
                else:
                    output[output_position + 1][i] = int(div_x_quotient)

        sub_pos = 0
        if i == 0:
            sub_pos = len(str(dividend)) - 1
        else:
            for j in range(len(output[output_position + 1]) - 1):
                if output[output_position + 1][-1 - j] == " ":
                    sub_pos += 1
                else:
                    break
            sub_pos = len(output[output_position + 1]) - sub_pos

        output[output_position + 3] = subtracting_division(
            output[output_position][:sub_pos],
            output[output_position + 1][:sub_pos],
            sub_pos,
        )

        if i == size - 1:
            decimal = int("".join(str(x) for x in output[output_position + 3]))
            quotient = int("".join(str(x) for x in header))
            if decimal == 0:
                output[output_position + 3][len(output[output_position + 3]) - 1] = "="
                answer = f"\n\nQuotient of {equation} equals to {quotient}"
            else:
                answer = f"\n\nQuotient of {equation} equals to {quotient} with {decimal}/{divisor} remaining"
            generator_output = f"{tabulate([*main_line, *output[1:]],header,numalign="center")} {answer}"
            yield generator_output
            break
        else:
            generator_output = f"{tabulate([*main_line, *output[1:]],header)}"
            yield generator_output

        output_position += 3
        for _ in range(3):
            if _ == 1:
                output.append(SEPARATING_LINE)
            else:
                output.append([" "] * size)


if __name__ == "__main__":
    main()
