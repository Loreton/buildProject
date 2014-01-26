#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per la gestione start/stop di un'istanza di JBoss EAP 6.x
#                                               by Loreto Notarantonio 2013, February
# Comando per eseguire uno script all'interno di uno ZIP file:
#        SET PYTHONPATH=JBossStart_LNf.zip python -m JBossStart [parameters]
#     oppure creare un file che si chiama __main__.py e lanciare il comando:
#        python JBossStart_LNf.zip [parameters]
# ######################################################################################

import os, sys
import platform
OpSys        = platform.system()

class myClass(): pass

# NON HO ancora il LOG ATTIVO

import getpass, ConfigParser

# ##########################################################
# # readIniFile
# # return:
# #     nome del file.ini con le indentazioni eliminate
# ##########################################################
def prepareIniConfigFile(gv, iniFileName, userFieldName=None, passwordFieldName=None):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy

    iniMAIN = myClass()

    fileName, ext       = os.path.splitext(iniFileName)
    propertiesFileName  = fileName + '.properties'

        # -----------------------------------------------
        # Se esiste il file.properties vuol dire che il
        # programma ha girato almeno una volta e quindi
        # leggiamo direttamente questo
        # a meno che il file.ini non abbia una data piu recente.
        # -----------------------------------------------
    if os.path.isfile(propertiesFileName):
        iniFileDate         = os.path.getmtime(iniFileName)
        propertiesFileDate  = os.path.getmtime(propertiesFileName)

        if iniFileDate > propertiesFileDate:
            CREATE_PROPERTIES_FILE  = True
            workInputFname = convertHumanFile(iniFileName)  # processiamolo per togliere le indentazioni
        else:
            CREATE_PROPERTIES_FILE = False
            workInputFname = propertiesFileName             # è già pronto senza indentazioni



        # -----------------------------------------------
        # altrimenti leggiamo il file.ini
        # ed alla fine creeremo il file.properties
        # -----------------------------------------------
    else:
        CREATE_PROPERTIES_FILE = True
        workInputFname = convertHumanFile(iniFileName)  # processiamolo per togliere le indentazioni


    logger.console( 'reading... %s' % (workInputFname))
    configID = ConfigParser.ConfigParser()
    configID.read(workInputFname)


    # if configID.has_option('MAIN', 'JBossMonitorUserID'):    UserID   = configID.get('MAIN', 'JBossMonitorUserID')
    # if configID.has_option('MAIN', 'JBossMonitorPassword'):  UserPassword = configID.get('MAIN', 'JBossMonitorPassword')

        # NON è obbligatorio ma se esiste allora criptiamo la password
    UserID = None
    if userFieldName and passwordFieldName:
        if configID.has_option('MAIN', userFieldName):      UserID       = configID.get('MAIN', userFieldName)
        if configID.has_option('MAIN', passwordFieldName):  UserPassword = configID.get('MAIN', passwordFieldName)



        # Se è il primo run allora leggiamo la password da console, la cryptiamo e la riscriviamo nel file
    if CREATE_PROPERTIES_FILE:
        if UserID:
            password = raw_input('Please enter a password for monitoring userid [%s]: ' % (UserID) )
            hashed_password = LN.crypt.encodePassword(password)
            print('The string to store in the db is: ' + hashed_password)
            configID.set('MAIN', passwordFieldName, hashed_password)
        # else:
        #     UserPassword = LN.crypt.decodePassword(UserPassword)

        newSection = 'PAY_ATTENTION'
        configID.add_section(newSection)
        # for i in range(1, 5):
            # configID.set(newSection, '; %04d SI PREGA DI NON MODIFICARE QUESTO FILE' % (i), '')
        configID.set(newSection, 'ATTENZIONE-A', '\nSI PREGA DI NON MODIFICARE QUESTO FILE'*5)
        configID.set(newSection, 'ATTENZIONE-B', '\nModificare solo il file %s' % (iniFileName) *5)
        # configID.set('PAY_ATTENTION', '; 3 SI PREGA DI NON MODIFICARE QUESTO FILE', '')
        # configID.set('PAY_ATTENTION', '; 4 SI PREGA DI NON MODIFICARE QUESTO FILE', '')
        # configID.set('PAY_ATTENTION', '; 5 SI PREGA DI NON MODIFICARE QUESTO FILE', '')
        with open(propertiesFileName, 'w') as configfile:
            configID.write(configfile)

    return propertiesFileName


# #########################################################
def convertHumanFile(fileName):
# #########################################################
    OpSys   = platform.system()
    tempDir = os.getenv('TEMP', 'c:\\temp') if OpSys == 'Windows' else os.getenv('tmp', '/tmp')

        # con l'utente come suffix per evitare eventuali conflitti
    workInputFname = os.path.join(tempDir, 'LnTemp_%s.ini' % (getpass.getuser()))


        # -----------------------------------------
        # - copiamo file.ini to temp.ini
        # - facendo lo strip delle righe
        # - per evitare che il parser dia errore
        # -----------------------------------------
    finp = open(fileName,"r")
    fwork = open(workInputFname, "wb")
    for line in finp:
        line = line.strip()
        fwork.write(line + '\n')

    finp.close()
    fwork.close()

    return workInputFname

