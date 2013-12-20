#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# http://code.activestate.com/recipes/191017-backup-your-files/
# http://code.activestate.com/recipes/576810-copy-files-over-ssh-using-paramiko/

# import base64
# import getpass
import os
# import socket
import sys
# import traceback
# import pprint 
import paramiko

import LnSSH_paramiko as LnSSH
    
if __name__ == "__main__":
    
    # setup logging
    logFileName = '\\tmp\\LnBackup.log'
    LnSSH.initLog(logFileName)

    if len(sys.argv) > 1:
        hostName = sys.argv[1]
            # PER FACILITA'
        if hostName.upper() == 'ESIL588':
            os.environ[hostName] = 'root,lagom588'
        Port = 22
    else:
        (hostName, Port) = LnSSH.getHostName()
    
    # print (hostName, Port)
    

    (userName, Password) = LnSSH.getUserPassw(hostName)
    # print (userName, Password)
    # print os.getenv(hostName)
    
    myKeys = ''
    myKeys =[  "l:\LNFree\Security\MyKeys\Loreto\LoretoBI_SSH_FG-NP_id_rsa", 
               "l:\LNFree\Security\MyKeys\Loreto\F602250_id_rsa",
            ]
            

    hostKey = LnSSH.getHostKey(hostName)
    
    
    
    ##############################
    # # Prova SSH_CLient
    ##############################

    ssh = LnSSH.ssh_session(hostName, userName, Port=Port, hostKey=hostKey, Password=Password, privKeyList=myKeys)
    
    stdin, stdout, stderr = ssh.exec_command('ls -latr *')
    stdin.flush()
    
    outLines = stdout.readlines()
    errLines = stderr.readlines()
    ssh.close()
    
    print '\n---- error ----'
    for line in errLines:
        print line
    print '\n---- out ----'
    for line in outLines:
        print line

    sys.exit()
    