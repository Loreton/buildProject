import getpass, platform, os,sys
# #####################################
# # readIniFile
# #####################################
# import LnPackage as Ln

class myClass():
    pass


# ##############################################################
# # http://prosseek.blogspot.it/2012/10/reading-ini-file-into-dictionary-in.html
# # per avere info sulla trasformazione in dictionary
# ##############################################################
def readIniConfigFile(iniFileName, Ln):
    import ConfigParser
    pColor = Ln.colors.bcolors()
    pColor.GREEN('readIniConfigFile')

    OpSys        = platform.system()
    # if OpSys == 'Windows':   tempDir = os.getenv('TEMP', 'c:\\temp')
    # else:                       tempDir = os.getenv('tmp', '/tmp')


    tempDir = os.getenv('TEMP', 'c:\\temp') if OpSys == 'Windows' else os.getenv('tmp', '/tmp')

    outFname    = os.path.join(tempDir, 'LnTemp_%s.ini' % (getpass.getuser()))

        # -----------------------------------------
        # - copiamo file.ini to temp.ini
        # - facendo lo strip delle righe
        # - per evitare che il parser dia errore
        # -----------------------------------------
    finp = open(iniFileName,"r")
    fout = open(outFname, "wb")
    for line in finp:
        line = line.strip()
        fout.write(line + '\n')

    finp.close()
    fout.close()

    config = ConfigParser.ConfigParser()
    config.read(outFname)


        # ------------------------------------
        # - conversione in un dictionary
        # - per usi futuri
        # ------------------------------------
    variablesToReplace = {}
    myDict = {}
    for section in config.sections():
        print section
        myDict[section] = {}
        for option in config.options(section):
            xx = config.get(section, option)
            for key, value in variablesToReplace.items():
                xx = xx.replace('${' + key + '}', value)
            myDict[section][option] = xx
            # print xx

    LOG = myDict['LOG']
    CFG = myDict['Main']


    # Otteniamo il nome del file di Log e relativi livelli di debug
    try:
        log = myClass()

        log.logDirWindows   = config.get('JBAdminLOG', 'logDirWindows')
        log.logDirLinux     = config.get('JBAdminLOG', 'logDirLinux')

        log.loggerOwner     = config.get('JBAdminLOG', 'loggerOwner')
        log.fileName        = config.get('JBAdminLOG', 'logFileName')
        log.levelFile       = config.get('JBAdminLOG', 'LogLEVEL_file')
        log.levelConsole    = config.get('JBAdminLOG', 'LogLEVEL_console')
        log.loggerID        = config.get('JBAdminLOG', 'loggerID')
        log.maxBytes        = config.getint('JBAdminLOG', 'maxBytes')
        log.nFiles          = config.getint('JBAdminLOG', 'nFiles')

    except (ConfigParser.NoOptionError,
            ConfigParser.NoSectionError,
            ConfigParser.InterpolationMissingOptionError,
            StandardError), why:
        print "ERROR reading %s file" % (iniFileName)
        print why
        sys.exit()

        # Creazione nome del log file con l'utente attaccato.
    (fname, fext) = os.path.splitext(log.fileName)
    log.fileName = "%s_%s%s" % (fname, getpass.getuser(), fext)
    # print log.fileName
    # sys.exit()
    log.logDir = log.logDirWindows if OpSys == 'Windows' else log.logDirLinux

    return log
