from subprocess import check_output, check_call, CalledProcessError
import os
import sys 
# first, determine how many cores are available
# TODO for windows also, and from network

INPUT_DIR = "/input"
INPUT_OP_DIR = INPUT_DIR + "/res"
INPUT_CMD = INPUT_DIR + "/cmd"

print("Starting up...")
DEALER_DIR = os.path.dirname(os.path.realpath(__file__))
DEALER_IP_DIR = DEALER_DIR + INPUT_DIR
DEALER_IP_OP_DIR = DEALER_DIR + INPUT_OP_DIR
DEALER_IP_CMD = DEALER_DIR + INPUT_CMD

print("TheDealer ROOT:", DEALER_DIR)
try:
    cores = int(check_output(["nproc"]))
    print("Detected cores: %d" % cores)
except CalledProcessError as e:
    print("Failed to retrieve number of cores on system using cmd: '%s', exited with return code: %d" % (e.cmd, e.returncode))
    exit(1)

try:
    print("Splitting input:")
    print("Executing:", DEALER_IP_CMD)
    check_call([DEALER_IP_CMD, str(cores)])
except CalledProcessError as e:
    print("Failed to split input using cmd: '%s', exited with return code: %d" % (e.cmd, e.returncode))
    exit(1)

except Exception as e:
    print("Failed while splitting input with:", e)
