#!/usr/bin/python3

import subprocess
import typer


# openssl enc -e --algorithm -aes-256-cbc -k mysecretkey -pbkdf2 -base64 -in plaintext_file.txt -out crypted_file.txt
def encrypt(message: str, port: str, algorithm: str, key: str):
    print("encrypting")
    openssl = subprocess.Popen(f"echo '{message}' | openssl enc -e --algorithm {algorithm} -k {key} -pbkdf2 -base64", 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8", shell=True)
    encrypted = openssl.communicate()[0]
    return encrypted
    

# openssl enc -d --algorithm -aes-256-cbc -k mysecretkey -pbkdf2 -base64 -in crypted_file.txt -out plaintext_file.txt
def decrypt(message: str, port: str, algorithm: str, key: str):
    print("decrypting...")
    openssl = subprocess.Popen(f"echo '{message}' | openssl enc -d --algorithm {algorithm} -k {key} -pbkdf2 -base64", 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8", shell=True)
    decrypted = openssl.communicate()[0].strip()
    return decrypted



# --listen to specify the listen option in terminal when executing
def main(port: str, listen: bool = False, hostname: str = "localhost", key: str = "key", algorithm: str = "-aes-256-cbc"):
    if listen:
        netcat = subprocess.Popen(["netcat", "-l", port], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8")
        while True:
            out = netcat.stdout.readline().strip()
            if out == "" and netcat.poll() is not None:
                break
            print(f"Received from client: {out}")
            decrypted_message = decrypt(out, port, algorithm, key)
            print("Decrypted message: " + decrypted_message)
    else:
        netcat = subprocess.Popen(["netcat", hostname, port], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8")
        while True:
            message = input("Input message: ")
            encrypted_message = encrypt(message, port, algorithm, key)

            # ATTENTION: if you do not add a \n to your message, your netcat socket will stay in wait before sending the message
            netcat.stdin.write(encrypted_message + "\n")
            netcat.stdin.flush()
            print("Encrypted message: " + encrypted_message)



if __name__ == "__main__":
    typer.run(main)