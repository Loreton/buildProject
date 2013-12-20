#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# http://www.saltycrane.com/blog/2010/02/python-paramiko-notes/
# http://code.activestate.com/recipes/191017-backup-your-files/
# http://code.activestate.com/recipes/576810-copy-files-over-ssh-using-paramiko/
# file://L:\LNFree\Pgm\PortablePython\LnExtraPackages_copiarli_in_App-Lib-site-packages\paramiko-1.7.7.1\docs\index.html




import errno
import os, sys, getpass, time
import paramiko
import types


# ################################################################
# - initLog()
# ################################################################
MyLogger = None
import LnLogger_Class as LnLOG
def initLog():
    global MyLogger, LnLoggerCLASS
    try:
        (LnLoggerCLASS, MyLogger) = LnLOG.initLog()
        MyLogger.info("Logger for %-20s has been initialized. - called by %s" % (__name__, LnLOG.calledBy(3)))
    except AttributeError, why:
        print ("\n\n--- ERROR opening Logger for %-20s\n  - [%s]\n  - [%s]" % (__name__, why, LnLOG.calledBy(-2)))
    
if MyLogger == None: initLog()
import LnSys
import LnFile

        # myKeys =[   "l:\LNFree\Security\MyKeys\Loreto\LoretoBI_SSH_FG-NP_id_rsa",
                    # "l:\LNFree\Security\MyKeys\Loreto\F602250_id_rsa",
                # ]

class LnSSH_Helper(object):

    # - Accetta anche hostName = 'user@host:port'
    def __init__(self, hostName, userName='anonymous', Port=22, hostKey=None, Password=None, privKeyList=None, logFileName=None, timeout=2, compress=True):
        """
            Create a ssh client and a sftp client
        """
        self.REPLACE_OLDER  = True
        self.REPLACE    = True

        self.__splitHostName__(hostName, userName, Port)

        if logFileName:
            paramiko.util.log_to_file(os.path.normpath(logFileName))

        self.SSH = paramiko.SSHClient()
        self.SSH.load_system_host_keys()
        self.SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # --------------------------------------
            # - Try connection using MyKeys.
            # - I exception than try with Password
            # --------------------------------------
        try:
            # self.SSH.connect(host, username=user, port=int(port), key_filename=privKeyList, compress=compress, timeout=timeout)    # OK
            self.SSH.connect(self.__hostName__, username=self.__userName__, port=self.__port__, key_filename=privKeyList, compress=compress, timeout=timeout)    # OK
        except Exception, e:
            print '%s' % (e)
            try:
                print "\n--- Trying with password! %s@%s" % (self.__userName__, self.__hostName__)
                if not Password:
                    Password = getpass.getpass('Password for %s@%s: ' % (self.__userName__, self.__hostName__))
                # self.SSH.connect(host, username=user, port=int(port), password=Password, compress=compress, timeout=timeout)    # OK
                self.SSH.connect(self.__hostName__, username=self.__userName__, port=self.__port__, password=Password, compress=compress, timeout=timeout)    # OK

            except Exception, e:
                print '%s' % (e)
                sys.exit()

        self.sFTP = self.SSH.open_sftp()
        self.__getUNAME__()
        
        remoteTIME = self.__getTIME__()
        localTIME  = int(LnSys.timeGetNow(GMT=False))
        self.__offsetTIME__ = localTIME-remoteTIME  # Valore da aggiungere al tempo locale per allinearsi con il remoto
        if self.__offsetTIME__ == 0:
            MyLogger.info('offset.....: %d' % self.__offsetTIME__)
        else:
            MyLogger.warning('offset.....: %d' % self.__offsetTIME__)

    def __getUNAME__(self):
        # uname, errLines = self.execCMD('uname')
        (rCode, errLines, uname) = self.execCMD('uname')
        self.UNAME = uname[0].strip('\n').upper()
        if self.UNAME == 'LINUX':
            self.timeStyle = '--time-style=+'
        elif self.UNAME == 'FREEBSD':
            self.timeStyle = '-D'
        else:
            print "...........", self.UNAME, "not Known"
            self.timeStyle = '-D'

    def __getTIME__(self):
        (rCode, errLines, dateTime) = self.execCMD('date +"%s"')
        
        if rCode:
            msg = ["Errore durante il getTime"]
            msg.extend(errLines)
            LnSys.exit(LnSys.PAUSE_KEYB, msg)
            return 0
        else:    
            # print 'rcode...........', rCode
            # print 'errLines...........', errLines
            # print 'dateTime...........', dateTime[0]
            return int(dateTime[0].strip('\n'))

    # ############################################################################
    # # __splitHostName__()
    # ############################################################################
    def __splitHostName__(self, hostName, userName, Port):
        host = hostName
        user = userName
        port = Port
        if hostName.find('@') >= 0:
            (user, host) = hostName.split('@')

        if host.find(':') >= 0:
            (host, port) = host.split(':')

        if user == '': user = userName
        if host == '': host = hostName
        if port == '': port = Port

        self.__userName__ = user
        self.__hostName__ = host
        self.__port__ = int(port)

    # ############################################################################
    # # close()
    # ############################################################################
    def close(self):
        self.SSH.close()

    # ############################################################################
    # # execCMD()
    # ############################################################################
    def execCMD(self, command):
        """run <command> 
        Execute this command """
        MyLogger.info("Executing SSH Command: %s - called by %s" % (command, LnLOG.calledBy(2)))
        if command:
            try:
                stdin, stdout, stderr = self.SSH.exec_command(command)
                stdin.close()
                outLines = stdout.readlines()
                errLines = stderr.readlines()
                MyLogger.error("ErrLines............%s" % (errLines) )
            except (SSHException), why:
                MyLogger.error("............%s" % (why) )

        else:
            print "usage: run <command>"

        # return (boolean, errLines, outLines)
        return ( len(errLines)>0, errLines, outLines)


    ##############################################################################################################
    # # Preleviamo tutti i files con relativi attibuti anche nelle SubDirs
    ##############################################################################################################
    def getFileList(self, remoteDir, epoch=False, recursive=False):
        MyLogger.info("getFileList on remoteDir: %s - called by %s" % (remoteDir, LnLOG.calledBy(2)))

        fDEBUG = False
        if remoteDir[-1] == '/': remoteDir = remoteDir[:-1]

        if epoch:
            listFiles = 'ls -lA ' + self.timeStyle + '"%s"'                # Epoch (see mktime())
            # -rw-------  1 loreto  users   1756    1326531623          .bash_history
            ( ATTRIB,   xx, USER,   GROUP,  SIZE,   DATETIME,           FNAME, TOT_FIELDS) = 0, 1, 2, 3, 4, 5, 6, 7
        else:
            # -rw-------  1 loreto  users   1756    2012-01-14 02:00:23 .bash_history
            (ATTRIB,    xx, USER,   GROUP,  SIZE,   DATE,      TIME,    FNAME, TOT_FIELDS) = 0, 1, 2, 3, 4, 5, 6, 7, 8
            listFiles = 'ls -lA ' + self.timeStyle + '"%F %T"'                # YYYY-MM-DD HH:MM:SS"

        if recursive:
            listFiles += ' -R'

        cmd = listFiles + ' ' + remoteDir
        if fDEBUG: print cmd

        # ----------------------------------
        # - Lettura directory
        # ----------------------------------
        print "Please wait for a while..."
        # (files, errLines) = self.execCMD(cmd)
        (rCode, errLines, files) = self.execCMD(cmd)
        if rCode > 0:
            print '\n---- error ----'
            for line in errLines:
                print line.strip('\n')

        print " [%10d] rows have to be analyzed" % (len(files))

        # ----------------------------------
        # - Analisi delle righe
        # ----------------------------------
        retList = []
        lun = len(remoteDir)
        subDir = ''
        stepCounter = 1000
        counter = 0
        print "Analyzing files [ '.' == %s ] :" % (stepCounter),
        for line in files:
            counter += 1
            if counter%stepCounter == 0:
                print '.',
            line = line.strip('\n')
            if line == '': continue

                # prendi la riga che contiene la subdir
            if line.startswith(remoteDir):
                if line[-1] == ':': subDir=line[lun:-1]          # eliminiamo anche i ':' finali
                if subDir != '':
                    subDir += '/'
                    if subDir[0] == '/':
                        subDir = subDir[1:]

                if fDEBUG: print '\n-------------', subDir
                continue

            if line[-1] == '~':  continue

                # ----------------------------------------------------------------------------------
                # - con -F si ha come ultimo carattere:
                # - un '/' finale indica una directory
                # - un '*' finale indica un eseguibile
                # - un '@' finale indica un link
                # - un '=' finale indica un socket
                # - un '%' finale indica un whiteout
                # - un '|' finale indica un FIFO
                # - Siccome quando c'è un LINK ad una dir, mi compare il '/' devo indagare meglio
                # if line[FNAME][-1] == '*':  linex[FNAME] = linex[FNAME][:-1]
                # if '/@=%|'.find(linex[FNAME][-1]) >= 0: continue    # NON Affidabile in quanto sul link va capito
                # - Al mometo mi appoggio sul primo char degli attributi
                # ----------------------------------------------------------------------------------
            lineFIELDS = TOT_FIELDS

            firstChar = line[0]

            if firstChar == 'd':
                fileTYPE = 'DIR'
                continue                            # Directory

            elif firstChar == 'l':                  # Link - Capire come comportarsi
                fileTYPE = 'LINK'
                lineFIELDS = TOT_FIELDS + 2
                continue
            else:
                fileTYPE = 'FILE'

                # -------------------------------------------
                # - split della linea nei vari campi
                # -------------------------------------------
            linex = line.split()
            if len(linex) != lineFIELDS: continue

            fullName = subDir + linex[FNAME]

            if fDEBUG: print '.....%-40s - %-10s - %s' % ( fullName, linex[SIZE], linex[DATETIME] )
            retList.append((os.path.normcase(fullName), int(linex[SIZE]), linex[DATETIME]) )
            retList.append( [linex[DATETIME], int(linex[SIZE]), os.path.normcase(fullName) ] )
        print
        return retList












    # ###################################################################
    # # send And Execute Command
    # - copiamo un file da locale ad una dir temporanea e ...
    # - .. lo eseguiamo
    # - Se qualcosa va storto chiediamo di proseguire o chiudere
    # ###################################################################
    def sendAndExecCmd(self, localFile=None, Lines=None, remoteFname=None, simul=True):
        MyLogger.debug("%-20s - called by %s" % (__name__ + ".sendAndExecCmd" , LnLOG.calledBy(2)))
        sepStr = '\n' + " "*51
        MyLogger.debug("localFile......: %s%s"\
                       "Lines..........: %s%s"\
                       "remoteFname....: %s%s")
                       # "SIMULATION.....: %s" % (localFile, sepStr, Lines, sepStr, remoteFname, sepStr, simul) )
        rCode = 99        
        
        if not remoteFname:
            LnSys.exit(LnSys.PAUSE_KEYB, " File Destinazione mancante")
            return
            
        if Lines:
            # -----------------------------------------------
            # - Prepariamo il file da eseguire remotamente
            # -----------------------------------------------
            fTemp = LnFile.getTempFile()
            LnFile.writeListToFile(fTemp, Lines)
            # shutil.rmtree(fTemp)
        
        elif localFile:
            fTemp = localFile
            
        else:
            LnSys.exit(LnSys.PAUSE_KEYB, " File Sorgente mancante")
            return
            
        
        (rCode, remoteFName) = self.putFile(fTemp, remoteRootDir=None, remoteFileName=remoteFname, replace=self.REPLACE)
        if rCode != 0:
            EXEC_STATUS = False
            msg = "Error copying file: %s ---> %s" % (fTemp, remoteFname)
            LnSys.exit(LnSys.PAUSE_KEYB, msg)

        else:
            EXEC_STATUS = True
                # - Esegui comando
            comando = 'python %s' % remoteFName
            (rCode, errLines, outLines) = self.execCMD(comando)
            if rCode == True:
                EXEC_STATUS = False
                print "....................", errLines
                errMsg= [   
                    "********** REMOTE ERROR ******************",
                    "*",
                    " ERROR executing remote command: %s"  % (comando),
                    "*",
                    "********** REMOTE ERROR ******************",
                        ]
                errMsg.extend(errLines)
                LnSys.exit(LnSys.PAUSE_KEYB, errMsg)

        # ###################################
        # choice = LnSys.getKeyboardInput("******* STOP SEnd&Execute *******", keyLIST='C', exitKey='QX', AnswerForDEBUG=None, fDEBUG=True)
        # ###################################
        return EXEC_STATUS

    
    
    
    
    
    
    
    
          


    # #############################
    # # sFTP commands
    # #############################
    def rmDir(self, path):
        """Remove remote directory that may contain files.
        It does not support directories that contain subdirectories
        """
        if self.exists(path):
            for filename in self.sFTP.listdir(path):
                filepath = os.path.join(path, filename)
                self.sFTP.remove(filepath)
            self.sFTP.rmdir(path)
            
            
    # #############################################
    # # writeListToFile (funziona ma è MOLTO lento
    # #############################################
    def writeListToFile(self, remoteDir, fname, rowList, lineSep='\n'):
        """
        Write a file on the remote server
        Create the remote directory if it does not exist
        Return the name of the remote file or None
        The fields supported are: st_mode, st_size, st_uid, st_gid, st_atime, and st_mtime
        """

        MyLogger.info("Writing file %s - called by %s" % (fname, LnLOG.calledBy(3)))
        
        # MyLogger.debug("Writing file %s" % (fname) )

        self.__SFTP_mkDirTree__(remoteDir)
        remoteFName = remoteDir + '/' + fname

        try:
            FILE = self.sFTP.file(remoteFName, mode='wb')
            for line in rowList:
                # print line
                FILE.write(LnSys.to_unicode(line) + lineSep)
            FILE.close()
        
        except IOError, why:
            MyLogger.error("............%s" % (why) )
            return None
            
        MyLogger.info("file %s has been written." % (remoteFName) )        
        
        return remoteFName
      


    # #####################################################################################
    # # putFile command
    # # ssh.putFile(os.path.normpath('L:/Loreto/Procs/Bat/aa.bat'), '/tmp/Loreto/pippo')
    # # Put a files on the remote server
    # # Create the remote directory if it does not exist
    # # Return the name of the remote file or None
    # # replace= REPLACE_OLDER, REPLACE
    # # The fields supported are: st_mode, st_size, st_uid, st_gid, st_atime, and st_mtime
    # # 
    # # fileList        : nome file remoto con o senza FULLPATH. Se è senza FULLPATH allora
    # # remoteFileName  : nome del localFile. Può essere un file solo oppure una LISTA
    # # remoteRootDir   : se valorizzata si aggiunge a remoteFileName.
    # #####################################################################################
    def putFile(self, fileList, remoteRootDir=None, remoteFileName=None, replace=False):
        MyLogger.debug("%-20s - called by %s" % (__name__ + ".putFile" , LnLOG.calledBy(2)))
        sepStr = '\n' + " "*51
        MyLogger.debug("remoteRootDir...: %s%s"\
                       "remoteFileName..: %s%s"\
                       "replace.........: %s%s")
                       # "SIMULATION......: %s" % (remoteRootDir, sepStr, remoteFileName, sepStr, replace, sepStr, SIMULATION) )
        rCode = 99

            # ----------------------------------------------
            # - Check input List or String
            # ----------------------------------------------
        if isinstance(fileList, types.ListType):
            SINGLE_FILE = False
        elif isinstance(fileList, types.StringType):
            SINGLE_FILE = True
            fileList = [fileList]
        else:
            MyLogger.error("fileList in Unknown type: %s" % (fileList ) )
            return 98, None
        
            # ----------------------------------------------
            # - Check remote Dir
            # ----------------------------------------------
        if remoteFileName == None and remoteRootDir == None:
            return 97, None
            
        
        for localFName in fileList:
            localFName = os.path.normpath(localFName)
            offsetTIME = self.__offsetTIME__
            
                # ----------------------------------------------
                # - Check local file
                # ----------------------------------------------
            if os.path.isfile(localFName):
                localSTAT  = os.stat(localFName)
                # localFTIME = int(localSTAT.st_mtime) + offsetTIME
                localFTimeGMT = LnSys.timeConvert(secs=localSTAT.st_mtime, GMT=True) + offsetTIME
            else:
                MyLogger.error("Local file NOT FOUND: %s" % (localFName ) )
                continue
     
                # ----------------------------------------------
                # - set remote file
                # ----------------------------------------------
            if  remoteRootDir and remoteFileName:
                remoteFileName  = remoteFileName
                remoteDir       = remoteRootDir
                
            elif remoteRootDir and not remoteFileName:
                remoteFileName  = os.path.basename(localFName)
                remoteDir       = remoteRootDir
            
            elif not remoteRootDir and remoteFileName:
                remoteDir       = os.path.dirname(remoteFileName)
                remoteFileName  = os.path.basename(remoteFileName)
            
            # if not SIMULATION:
            remoteDir = self.__SFTP_mkDirTree__(remoteDir)
                
            remoteFileName = remoteDir + '/' + remoteFileName
            
            bCOPY = False
            if self.exists(remoteFileName):
                remoteSTAT = self.sFTP.stat(remoteFileName)

                # remoteFTIME = int(remoteSTAT.st_mtime)
                remoteFTimeGMT = LnSys.timeConvert(secs=remoteSTAT.st_mtime, GMT=True)

                if (replace == self.REPLACE):
                    # msg = "sftp.put  file: %s[%s] ---> [%s]%s" % (localFName, localFTimeGMT, remoteFTimeGMT, remoteFileName)
                    msg = "sftp replacing file: [%12d] %s" % (localSTAT.st_size, remoteFileName) 
                    bCOPY = True

                elif (replace == self.REPLACE_OLDER) and (localFTimeGMT > remoteFTimeGMT):
                    msg = "sftp replacing file: [%12d] %s" % (localSTAT.st_size, remoteFileName) 
                    bCOPY = True

                else:
                    # msg = "sftp.skip  file: %s[%s] ---> [%s]%s" % (localFName, localFTimeGMT, remoteFTimeGMT, remoteFileName) 
                    bCOPY = False
            
            else:
                # msg = "sftp adding    file: [%12d] %s ---> %s" % (localSTAT.st_size, localFName, remoteFileName) 
                msg = "sftp adding    file: [%12d] %s" % (localSTAT.st_size, remoteFileName) 
                bCOPY = True
            
            if bCOPY:
                # if SIMULATION:
                    # MyLogger.info("DRY-RUN " + msg)
                # else:
                MyLogger.info(msg)
                remoteSTAT  = self.sFTP.put(localFName, remoteFileName)
                times = [LnSys.timeConvert(secs=localSTAT.st_atime, GMT=True), LnSys.timeConvert(secs=localSTAT.st_mtime, GMT=True)]
                self.sFTP.utime(remoteFileName, times)  # allinea il tempo alla sorgente
                
            
            rCode = 0

        return (rCode, remoteFileName)



    # #############################
    # # getFile command
    # #############################
    def getFile(self, remoteFName, localDir, replace=False):
        """Put a files on the remote server
        Create the remote directory if it does not exist
        Does not support directories that contain subdirectories
        Return the number of files transferred
        replace= OLDER, ALL, NO
        The fields supported are: st_mode, st_size, st_uid, st_gid, st_atime, and st_mtime
        """
        offsetTIME = self.__offsetTIME__

        if self.exists(remoteFName):
            remoteSTAT  = self.sFTP.stat(remoteFName)
            # remoteFTIME = int(remoteSTAT.st_mtime)
            remoteFTimeGMT = LnSys.timeConvert(secs=remoteSTAT.st_mtime, GMT=True, out='SEC') + offsetTIME
        else:
            MyLogger.error("Remote file NOT FOUND: %s" % (remoteFName ) )
            return None

        remFname  = os.path.basename(remoteFName)
        remoteFName = remoteFName.replace('\\', '/')

        if localDir[-1] == '/':
            localFName = localDir +  remFname
        else:
            localFName = localDir + '/' + remFname

        localFName = os.path.normpath(localFName)

        if os.path.isfile(localFName):
            localSTAT  = os.stat(localFName)
            # localFTIME = int(localSTAT.st_mtime) + offsetTIME
            localFTimeGMT = LnSys.timeConvert(secs=localSTAT.st_mtime, GMT=True, out='SEC') + offsetTIME

            if  (replace == self.REPLACE):
                MyLogger.debug("sftp.get  file: %s[%s] --> [%s]%s" % (remoteFName, remoteFTimeGMT, localFTimeGMT, localFName) )
                rCode = self.sFTP.get(remoteFName, localFName)

            elif (replace == self.REPLACE_OLDER) and (remoteFTimeGMT > localFTimeGMT ):
                MyLogger.debug("sftp.get  file: %s[%s] --> [%s]%s" % (remoteFName, remoteFTimeGMT, localFTimeGMT, localFName) )
                rCode = self.sFTP.get(remoteFName, localFName)

            else:
                MyLogger.debug("sftp.skip file: %s[%s] --> [%s]%s" % (remoteFName, remoteFTimeGMT, localFTimeGMT, localFName) )
         
        else:
            MyLogger.debug("sftp.new  file: %s --> %s" % (remoteFName, localFName) )
            rCode = self.sFTP.get(remoteFName, localFName)

            # - Rileggiamo lo status del file
        if os.path.isfile(localFName):
            localSTAT  = os.stat(localFName)
            # localFTIME = int(localSTAT.st_mtime) + offsetTIME
            localFTimeGMT = LnSys.timeConvert(secs=localSTAT.st_mtime, GMT=True, out='SEC') + offsetTIME
        else:
            MyLogger.error("ERROR copying remote file: %s" % (remoteFName ) )
            return None

            # --------------------------------------------------------------------------
            # - Se il DateTime del file remoto e' inferiore al sorgente dai errore.
            # - Purtroppo NON POSSO USARE QUESTI DATI a causa della differenza 
            # - di timing tra il sistema locale e quello remoto.
            # --------------------------------------------------------------------------
        if (localFTimeGMT < remoteFTimeGMT):
            # print "Il tempo e' diverso???"
            MyLogger.warning( "localFTimeGMT:%d - remoteFTimeGMT:%d - diff:%d" % (localFTimeGMT, remoteFTimeGMT, (localFTimeGMT-remoteFTimeGMT) ))

        return localFName


    def __SFTP_mkDirTree__(self, remoteDir):
        """Create a tree of directories"""
        
        
        remoteDir = remoteDir.replace('\\', '/')
        
        if self.exists(remoteDir):
            return remoteDir
            
        dirs = remoteDir.split('/')
        if remoteDir[0:1] == '/':
            dirTree = remoteDir[0:1]
        else:
            dirTree = ''
        
        # MyLogger.info("Creating directory: %s" % (remoteDir) )

        for dir in dirs:
            if dir == '': continue
            dirTree += dir
            if not self.exists(dirTree):
                MyLogger.info("Creating directory: %s" % (dirTree) )
                self.sFTP.mkdir(dirTree)
            dirTree += '/'
            
        return remoteDir

    def putDir(self, localdir, remotedir):
        """Put a directory of files on the remote server
        Create the remote directory if it does not exist
        Does not support directories that contain subdirectories
        Return the number of files transferred
        """
        if not self.exists(remotedir):
            self.sFTP.mkdir(remotedir)
        count = 0
        for filename in os.listdir(localdir):
            self.sFTP.put(
                os.path.join(localdir, filename),
                os.path.join(remotedir, filename))
            count += 1
        return count


    def sFtpTreeList(self, path):
            # dirlist on remote host
        fileLIST = []
        if self.exists(path):
            dirlist = self.sFTP.listdir(path)
            for file in dirlist:
                if file == 'DIR':
                    fileLIST.extend( self.sFtpListDir( os.path.join(path, file) ) )
                else:
                    fileLIST.append( self.sFTP.stat(file) )
                # print file
                # print self.sFTP.stat(file)

        return fileLIST


    def sFtpListDir(self, path):
        fileLIST = []
            # dirlist on remote host
        # dirlist = self.sFTP.listdir(path)
        # print self.sFTP
        if self.exists(path):
            dirlist   = self.sFTP.listdir(path)
            for file in dirlist:
                fileLIST.append(self.sFTP.stat(file))
                # print file
                # print self.sFTP.stat(file)
        return fileLIST


    def exists(self, path):
        """Return True if the remote path exists
        """
        try:
            self.sFTP.stat(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True


if __name__ == "__main__":

    Port = 22
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
        if hostname.find('@') >= 0:
            (userName, hostName) = hostname.split('@')
    else:
        print "\n--------- [user@hostname] parameter missing!"
        sys.exit(-1)

    # print (userName, hostName)

    ##############################
    # # Prova SSH_CLient
    ##############################
    # ssh = LnSSH.LnSSH_Helper()

    myKeys = ''
    myKeys =[  "l:\LNFree\Security\MyKeys\Loreto\LoretoBI_SSH_FG-NP_id_rsa",
               "l:\LNFree\Security\MyKeys\Loreto\F602250_id_rsa",
            ]

    # ssh.connect(hostName, userName, Port=Port, privKeyList=myKeys, logFileName='\\tmp\\LnBackup.log')
    ssh = LnSSH_Helper(hostName, userName, Port=Port, privKeyList=myKeys, logFileName='\\tmp\\LnBackup.log')
    listFiles = 'ls -lAD"%F %T"'    # YYYY-MM-DD HH:MM:SS"
    listFiles = 'ls -lAD"%s"'       # Epoch (see mktime())
    getDirs = 'find . -type d'      # prendi tutte le SubDirs

    remoteBaseDir = '/users/home/loreto/'
    getDirs = 'find %s -type d' % (remoteBaseDir)      # prendi tutte le SubDirs
    getFiles = 'find %s -type f' % (remoteBaseDir)      # prendi tutti i files
    # (dirs, errLines) = ssh.execCMD(getDirs)
    (rCode, errLines, outLines) = ssh.execCMD(getDirs)
    print '\n---- error ----'
    for line in errLines:  print line
    # (files, errLines) = ssh.execCMD(getFiles)
    (rCode, errLines, outLines) = ssh.execCMD(getFiles)
    print '\n---- error ----'
    for line in errLines:  print line.strip('\n')

    # (outLines, errLines) = ssh.execCMD(remoteBaseDir + listFiles)

    print '\n---- out ----'
    for dir in dirs:
        print dir.strip('\n')

    for file in files:
        print file.strip('\n')
        # (stat, errLines) = ssh.execCMD(listFiles + ' ' + file)
        (rCode, errLines, outLines) = ssh.execCMD(listFiles + ' ' + file)
        for line in outLines:  print line.strip('\n')

    # (files, errLines) = ssh.execCMD(listFiles + ' -R')
    (rCode, errLines, files) = ssh.execCMD(listFiles + ' -R')
    for file in files:
        print file.strip('\n')


    ssh.sFtpListDir('.')
    ssh.close()

    sys.exit()
