#!/usr/bin/python3

import subprocess
import typer
import os
from rich.console import Console

console = Console()

# steghide embed -ef example.txt -cf image.jpg -p mysecretkey
# echo "body of the email" | mutt -s "subject of the email" your_personal_email_address@something.com -a image.jpg

def main(dst_address: str, subject: str, body: str, ef: str, cf: str):

    if(os.path.exists(ef) and os.path.exists(cf)):
        with console.status(f"Hiding {ef} into {cf}..."):
            steghide = subprocess.Popen(['steghide', 'embed', '-ef', ef, '-cf', cf, '-p', 'key'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            steghide.communicate()
            echo = subprocess.Popen(['echo', body], stdout=subprocess.PIPE)
        console.log("File hidden in the image")

        with console.status(f"Sending email to {dst_address} with attached {cf}..."):
            subprocess.check_output(['mutt', '-s', subject, dst_address, '-a', cf], stdin=echo.stdout, stderr=subprocess.PIPE)
        console.log("Email sent")

    else:
        console.log("Path doesn't exist")


if __name__ == "__main__":
    typer.run(main)