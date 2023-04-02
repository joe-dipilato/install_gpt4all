#!/usr/bin/env python3
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
import sys
from time import sleep
root = Path.home() / "gpt4all/gpt4all/chat/"
cmd = root / "gpt4all-lora-quantized-OSX-m1"
model = root / "gpt4all-lora-quantized.bin"

newcmd = (str(cmd) + " -m " + str(model))
print(newcmd)

def main():
    # proc = Popen([str("sleep 3; echo hi")],
    proc = Popen(["echo a; echo b;" + str(cmd) + " -m " + str(model)],
                 shell=True,
                 stdin=PIPE,
                 stdout=PIPE,
                 stderr=PIPE)

    # To avoid deadlocks: careful to: add \n to output, flush output, use
    # readline() rather than read()
    # proc.stdin.write(b'2+2\n')
    # proc.stdin.flush()

    print(proc.stdout.readline().decode('UTF-8'), end="")
    # sleep(1)
    # proc.stdin.write(b'len("foobar")\n')
    # proc.stdin.flush()
    print(proc.stdout.readline().decode('UTF-8'), end="")
    # sleep(1)
    print(proc.stdout.readline().decode('UTF-8'), end="")
    # sleep(1)
    print(proc.stdout.readline().decode('UTF-8'), end="")
    print(proc.stdout.readline().decode('UTF-8'), end="")
    while True:
        print(proc.stdout.readline().decode('UTF-8'), end="")
        print(proc.stderr.readline().decode('UTF-8'), end="")
        sleep(0.5)
        print(proc)
    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)

main()
sys.exit()
p = Popen([str(cmd)], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
while True:
    p.stdout.readline().rstrip()

sys.exit()

# p.communicate('mike')[0].rstrip()
