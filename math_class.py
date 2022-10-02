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
    connection.recv(1996)
    connection.settimeout(0.5)


def get_problem_type(sanitized_data):
    '''
    returns what type of problem we have (range, minimum, maximum, etc)
    '''
    problem_string=sanitized_data.pop(0)
    # check for problem type and return it
    if re.match(".*range.*", str(problem_string)):
        return "range"
    elif re.match(".*minimum.*", str(problem_string)):
        return "minimum"
    elif re.match(".*maximum.*", str(problem_string)):
        return "maximum"
    elif re.match(".*mean.*", str(problem_string)):
        return "mean"
    elif re.match(".*median.*", str(problem_string)):
        return "median"
    # return None if we don't know what the problem is
    else:
        return None


def sanitize_data(data):
    '''
    sanitizes data from server so we can just extract the numbers
    '''
    # tokenize data after converting to string. Not sure why I need to use \\n instead of just \n
    tokens = str(data).split("\n")
    # remove first and last token
    del(tokens[0])
    del(tokens[-1])
    return tokens


def solve(tokens, problem_type):
    '''
    solves problem, given numbers as tokens and problem_type
    '''
    # convert tokens to integers
    numbers = [int(x) for x in tokens]
    match problem_type:
        case "range":
            return max(numbers) - min(numbers)
        case "minimum":
            return min(numbers)
        case "maximum":
            return max(numbers)
        case "mean":
            return int(round(statistics.mean(numbers)))
        case "median":
            return int(round(statistics.median(numbers)))
        case _:
            return None
def recieve_all():
    '''
    recieve all data (stolen from alex B, the best man ever)
    '''
    received = b''
    while True:
        try:
            received += connection.recv(4096)
            if re.match(".*RS{.*}.*", str(received)):
                break
        except:
            break
    return received.decode()

def main():
    # initialize connection
    init()
    while True:
        #recieve data
        data = recieve_all()
        print("Raw data: ", data)
        #sanitize data
        sanitized_data = sanitize_data(data)
        print("sanitized data: ", sanitized_data)
        #get problem type
        problem_type = get_problem_type(sanitized_data)
        print("Problem:", problem_type, "of", sanitized_data)
        #solve problem
        solution = solve(sanitized_data, problem_type)
        print("Solution:", solution)
        # send solution
        print("Sending solution:", solution)
        message=str(solution)+"\n"
        connection.sendall(message.encode())
        #if we got the flag, then break
        if re.match(".*RS{.*}", str(data)):
            print("Flag:", data)
            #shutdown connection
            connection.shutdown(socket.SHUT_RDWR)
            break


if __name__ == "__main__":
    main()
