#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys
import subprocess
import getpass
import textwrap


class LnStructure:
    pass

logger      = None
calledBy    = None


# #####################################################################
# # runAS('jboss', '/bin/bash', '/tmp/prova.sh', password=None, PWAIT=False)
# #####################################################################
def runAS(gv, userName, command, argsList=[], PWAIT=True, stdOUTfile=None):
    if gv.OpSys.upper() == 'WINDOWS':
        return runASWin(gv, userName, command, argsList=[], PWAIT=True, stdOUTfile=stdOUTfile)
    else:
        return runASUnix(gv, userName, command, argsList=[], PWAIT=True, stdOUTfile=stdOUTfile)



# ====================================================================================
# = runASWin('jboss', '/bin/bash', '/tmp/prova.sh', password=None, PWAIT=False)
# ====================================================================================
def runASWin(gv, userName, command, argsList=[], PWAIT=True, stdOUTfile=None):
    global logger, calledBy
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    LN          = gv.LN
    logger.debug('entered - [called by:%s]' % (calledBy(2)))

    args = argsList

    workingDIR='/tmp'
    workingDIR=None
    workingDIR=''

    #  Creiamo il comando in formato stringa
    CMD = command + ' ' + ' '.join(argsList)

    result = 0

    env = os.environ.copy()
    env[ 'HOME'     ]   = os.environ['USERPROFILE']
    env[ 'LOGNAME'  ]   = os.environ['USERNAME']
    env[ 'USER'     ]   = os.environ['USERNAME']
    env[ 'LORETO'   ]   = "SONO PASSATO"

    report_idsWin('starting ' + str(CMD))
    if stdOUTfile:
        logger.info("RunAS with redirection to: %s" %(stdOUTfile))
            # preparazione per la redirezione output su file
        try:
            f = open(stdOUTfile, 'a')

        except (IOError), why:
            msg = textwrap.dedent("""\r
            user %s cannot access file: %s
            %s
            """ % (getpass.getuser(), stdOUTfile, str(why)) )
            # print LN.cERROR + msg
            logger.error(msg)
            LN.sys.exit(gv, 9001, LN.cERROR + msg)

        stdIN   =   subprocess.PIPE
        stdOUT  =   f
        stdERR  =   f

    else:
        logger.info("RunAS with no OUTPUT redirection")
        stdIN   =   subprocess.PIPE
        stdOUT  =   subprocess.PIPE
        stdERR  =   subprocess.PIPE

    if workingDIR:
        env[ 'PWD'      ]  = workingDIR
        ps = subprocess.Popen(CMD, shell=True, env=env,  stdin=stdIN, stdout=stdOUT, stderr=stdERR, cwd=workingDIR)
    else:
        ps = subprocess.Popen(CMD, shell=True, env=env,  stdin=stdIN, stdout=stdOUT, stderr=stdERR)

    report_idsWin('finished ' + str(CMD))
    logger.info('result:%s' % result)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))



# ====================================================================================
# = runASUnix('jboss', '/bin/bash', '/tmp/prova.sh', password=None, PWAIT=False)
# ====================================================================================
def runASUnix(gv, userName, command, argsList=[], PWAIT=True, stdOUTfile=None):
    import pwd
    global logger, calledBy
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(2)))

    args = argsList

    workingDIR='/tmp'
    workingDIR=None
    workingDIR=''

    #  Creiamo il comando in formato stringa
    CMD = command + ' ' + ' '.join(argsList)

    result = 0
    user = LnStructure()
    (user.NAME, user.PASSWD, user.UID, user.GID, user.GECOS, user.HOME_DIR, user.SHELL) = pwd.getpwnam(userName)

    env = os.environ.copy()
    env[ 'HOME'     ]   = user.HOME_DIR
    env[ 'LOGNAME'  ]   = user.NAME
    env[ 'USER'     ]   = user.NAME
    env[ 'LORETO'   ]   = "SONO PASSATO"

    report_ids('starting ' + str(CMD))

    if stdOUTfile:
        logger.info("RunAS with redirection to: %s" %(stdOUTfile))
        if getpass.getuser() == 'root':
            logger.info("changing owner to file: %s" %(stdOUTfile))
            os.chown(stdOUTfile, user.UID, user.GID)         # change owner


            # preparazione per la redirezione output su file
        try:
            fout = open(stdOUTfile, 'a')

        except (IOError), why:
            msg = textwrap.dedent("""\r
            user %s cannot access file: %s
            %s
            """ % (getpass.getuser(), stdOUTfile, str(why)) )
            print msg
            logger.error(msg)
            sys.exit()

        stdIN   =   subprocess.PIPE
        stdOUT  =   fout
        stdERR  =   fout

    else:
        logger.info("RunAS with no OUTPUT redirection")
        stdIN   =   subprocess.PIPE
        stdOUT  =   subprocess.PIPE
        stdERR  =   subprocess.PIPE

    if workingDIR:
        env[ 'PWD'      ]  = workingDIR
        ps = subprocess.Popen(CMD, shell=True, env=env, preexec_fn=demote(user.UID, user.UID), stdin=stdIN, stdout=stdOUT, stderr=stdERR, cwd=workingDIR)
    else:
        ps = subprocess.Popen(CMD, shell=True, env=env, preexec_fn=demote(user.UID, user.UID), stdin=stdIN, stdout=stdOUT, stderr=stdERR)


    report_ids('finished ' + str(CMD))
    logger.info('result:%s' % result)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))



# ====================================================================================
# = demote(user_uid, user_gid)
# =   provvede a creare un oggetto da passare al preexec_fn
# ====================================================================================
def demote(user_uid, user_gid):
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    def result():
        report_ids('starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
        report_ids('finished demotion')

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return result


def report_ids(msg):
    logger.info('username:%s, uid:%d, gid:%d; =  %s' % (getpass.getuser(), os.getuid(), os.getgid(), msg) )

def report_idsWin(msg):
    logger.info('username:%s =  %s' % (getpass.getuser(), msg) )





