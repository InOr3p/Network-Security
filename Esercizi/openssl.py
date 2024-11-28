#!/usr/bin/python3

import subprocess

def main():

    print("encrypting")
    openssl = subprocess.Popen("echo 'Hello' | openssl enc -e --algorithm -aes-256-cbc -k mysecretkey -pbkdf2 -base64", 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8", shell=True)
    print(openssl.communicate()[0])

#(["openssl", "enc", "-e", "--algorithm", "-aes-256-cbc", "-k", "key", "-pbkdf2", "-base64"],
                               


if __name__ == "__main__":
    main()