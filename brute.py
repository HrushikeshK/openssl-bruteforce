####################################################################################
# Author: hkh4cks                                                                  #
# Usage: python2.7 brute.py <wordlist> <cipher list> <encrypted file> 2> /dev/null #
####################################################################################

from __future__ import print_function
from multiprocessing import Process, Manager
import subprocess
import sys
import os


if len(sys.argv) != 4:
    print("Usage: {} <path to wordlist> <path to cipher list> <path to encrypted file>".format(sys.argv[0]))
    exit(1)


wordlist = open(sys.argv[1], 'r').read().strip().split('\n')
ciphers = open(sys.argv[2], 'r').read().strip().split('\n')
enc_file = sys.argv[3]
dev_null = open('/dev/null', 'w')

print(ciphers)

def crack(loots, cipher):
    print("Running pid: {}\tCipher: {}".format(os.getpid(),cipher))
    filename = cipher
    for word in wordlist:
        try:
            if word != '':
                cmd = "echo " + word + " | openssl enc -d -a -" + cipher + " -in " + enc_file + " -out " + filename + " -pass stdin"
                op = subprocess.check_output(cmd, stderr=dev_null, shell=True)
                op = subprocess.check_output("file " + filename,shell=True)
                if 'ASCII text' in op:
                    print("-" * 50)
                    print("Password found with algorithm {}: {}".format(cipher,word))
                    print("Data: \n{}".format(open(filename, 'r').read()))
                    print("-" * 50)
                    loots[cipher] = word

                else:
                    if os.path.isfile(filename):
                        subprocess.check_output("rm " + filename, stderr=dev_null, shell=True)
                        #os.system("rm " + filename)

                exit(1)

        except subprocess.CalledProcessError:
            continue


def main():
    manager = Manager()
    loots = manager.dict()
    threads = list()
    for cipher in ciphers:
        if cipher != '':
            p = Process(target=crack, args = (loots, cipher))
            threads.append(p)
            p.start()
            p.join()
    print("-" * 50)
    print("Found {} ciphers with passwords".format(len(loots)))
    for loot in loots.keys():
        print("Cipher: {}\tPassword: {}".format(loot,loots[loot]))

if __name__ == '__main__':
    main()
