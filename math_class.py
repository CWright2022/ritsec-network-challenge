import socket
import re
import statistics

HOST = '143.110.215.221'
PORT = 10000


def init():
    # initialize the socket
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST, PORT))
    # skip first packet (header and welcome message)
    _ = connection.recv(PORT)


def get_problem_type(data):
    '''
    returns what type of problem we have (range, minimum, maximum, etc)
    '''
    # check for problem type and return it
    if re.match(".*range.*", str(data)):
        return "range"
    elif re.match(".*minimum.*", str(data)):
        return "minimum"
    elif re.match(".*maximum.*", str(data)):
        return "maximum"
    elif re.match(".*mean.*", str(data)):
        return "mean"
    elif re.match(".*median.*", str(data)):
        return "median"
    # return None if we don't know what the problem is
    else:
        return None


def sanitize_data(data):
    '''
    sanitizes data from server so we can just extract the numbers
    '''
    # tokenize data after converting to string. Not sure why I need to use \\n instead of just \n
    tokens = str(data).split("\\n")
    # remove first 2 tokens (some random letter b and problem info) and the last one (random ')
    del tokens[0:2]
    del tokens[-1]
    return tokens


def solve(tokens, problem_type):
    '''
    solves problem, given numbers as tokens and problem_type
    '''
    # convert tokens to integers
    try:
        numbers = [int(x) for x in tokens]
    except:
        print("Error converting tokens to integers - try again in like 5s")
        return None
    match problem_type:
        case "range":
            return max(numbers)-min(numbers)
        case "minimum":
            return min(numbers)
        case "maximum":
            return max(numbers)
        case "mean":
            return sum(numbers)/len(numbers)//1
        case "median":
            return statistics.median(numbers)//1
        case _:
            return None


def main():
    # initialize connection
    init()
    # get first problem
    data = connection.recv(PORT)
    print("Problem:", get_problem_type(data), "of", sanitize_data(data))
    print("Answer:", solve(sanitize_data(data), get_problem_type(data)))
    solution = solve(sanitize_data(data), get_problem_type(data))
    print(solution)
    connection.shutdown(socket.SHUT_RDWR)


if __name__ == "__main__":
    main()
