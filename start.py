from subprocess import check_output, check_call, call, CalledProcessError, DEVNULL, Popen
import os
import sys 
import multiprocessing
# first, determine how many cores are available
# TODO for windows also, and from network


DEALER_DIR = os.path.dirname(os.path.realpath(__file__))
DEALER_IP_DIR = DEALER_DIR + "/input"
DEALER_IP_OP_DIR = DEALER_IP_DIR + "/op"
DEALER_IP_CMD = DEALER_IP_DIR + "/cmd"

DEALER_MAP_CMD = DEALER_DIR + "/map/cmd"
DEALER_MAP_OP_DIR = DEALER_DIR + "/map/op"

print("TheDealer ROOT:", DEALER_DIR)
print("Input directory:", DEALER_IP_DIR)
print("Input split result directory:", DEALER_IP_OP_DIR)
print("Input cmd:", DEALER_IP_CMD)
print("Map cmd:", DEALER_MAP_CMD)
print("Map OUTPUT directory:", DEALER_MAP_OP_DIR)

def get_map_op_dir(num):
    return DEALER_MAP_OP_DIR + str(num)


def get_ip_files():
    return [os.path.join(DEALER_IP_OP_DIR, f) for f in os.listdir(DEALER_IP_OP_DIR) if os.path.isfile(os.path.join(DEALER_IP_OP_DIR, f))]


def split_input(cores):
    try:
        print("Splitting input..")
        print("Executing:", DEALER_IP_CMD)
        call(["rm", "-r", DEALER_IP_OP_DIR], stderr=DEVNULL)
        check_call(["mkdir", DEALER_IP_OP_DIR])
        check_call([DEALER_IP_CMD, str(cores)], cwd=DEALER_IP_OP_DIR)
        return get_ip_files()
    except CalledProcessError as e:
        print("ERROR: Failed to split input using cmd: '%s', exited with return code: %d" % (e.cmd, e.returncode), file=sys.stderr)
        exit(1)
    except FileNotFoundError:
        print("ERROR: Could not find input split cmd at", DEALER_IP_CMD, file=sys.stderr)
        exit(1)


def get_cores():
    try:
        cores = int(check_output(["nproc"]))
        return cores
    except CalledProcessError as e:
        print("ERROR: Failed to retrieve number of cores on system using cmd: '%s', exited with return code: %d" % (e.cmd, e.returncode), file=sys.stderr)
        exit(1)


def execute_map(num_ip_path):
    num, ip_path = num_ip_path
    with open(ip_path) as ip_file:
        op_dir = get_map_op_dir(num)
        try:
            call(["rm", "-r", op_dir], stderr=DEVNULL)
            check_call(["mkdir", op_dir])
            check_call([DEALER_MAP_CMD], stdin=ip_file, cwd=op_dir)
        except CalledProcessError as e:
            print("ERROR: Failed to execute map cmd: '%s', exited with return code: %d" % (e.cmd, e.returncode), file=sys.stderr)
            return e.returncode
        except FileNotFoundError:
            print("ERROR: Could not find map command at", DEALER_MAP_CMD, file=sys.stderr)
            return 255
    return 0
        

# execute the map program on each input file generated. Number of ip files == number of programs executed
def start_mapping(files):
    pool = multiprocessing.Pool(len(files))
    pool.map(execute_map, zip(range(len(files)), files))


def main():
    cores = get_cores()
    print("Detected cores: %d" % cores)
    files = split_input(cores)
    start_mapping(files)


main()

