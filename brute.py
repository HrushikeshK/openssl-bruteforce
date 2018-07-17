####################################################################################
# Author: hkh4cks                                                                  #
# Usage: python2.7 brute.py <wordlist> <cipher list> <encrypted file> 2> /dev/null #
####################################################################################

from __future__ import print_function
from multiprocessing import Process
import subprocess
import sys
import os


if len(sys.argv) != 4:
    print("Usage: {} <path to wordlist> <path to cipher list> <path to encrypted file>".format(sys.argv[0]))
    exit(1)

wordlist = open(sys.argv[1], 'r').read().split('\n')[:-1]
ciphers = open(sys.argv[2], 'r').read().split('\n')[:-1]
enc_file = sys.argv[3]
dev_null = open('/dev/null', 'w')

def crack(cipher):
    print("Running pid: {}\tCipher: {}".format(os.getpid(),cipher))
    filename = cipher
    for word in wordlist:
        try:
            cmd = "echo " + word + " | openssl enc -d -a -" + cipher + " -in " + enc_file + " -out " + filename + " -pass stdin"
            op = subprocess.check_output(cmd, stderr=dev_null, shell=True)
            op = subprocess.check_output("file " + filename,shell=True)
            if 'ASCII text' in op:
                print("Password found with algorithm {}: {}".format(cipher,word))
                print("Data: \n{}".format(open(filename, 'r').read()))
                print("------------------------------------------")
                found.append((cipher,word))

            else:
                if os.path.isfile(filename):
                    #subprocess.check_output("rm " + filename)
                    os.system("rm " + filename)

            exit(1)

        except subprocess.CalledProcessError:
            continue


found = list()
threads = list()
for cipher in ciphers:
    p = Process(target=crack, args = (cipher,))
    threads.append(p)
    p.start()
    p.join()
print("Found {} ciphers with passwords".format(len(found)))
print(found)
for cipher,passwd in found:
    print("Cipher: {}\tPassword: {}".format(cipher,passwd))
