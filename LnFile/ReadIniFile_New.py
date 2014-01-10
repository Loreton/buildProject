import getpass, platform, os,sys
# #####################################
# # readIniFile
# #####################################
# import LnPackage as Ln

class myClass():
    pass

import getpass, ConfigParser
import ConfigParser

class MyParser(ConfigParser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


# ##############################################################
# # http://prosseek.blogspot.it/2012/10/reading-ini-file-into-dictionary-in.html
# # per avere info sulla trasformazione in dictionary
# ##############################################################
def readIniConfigFile_New(gv, iniFileName):
    Prj         = gv.Prj
    LN          = gv.LN
    # logger      = gv.LN.logger          #  Ancora non lo abbiamo
    calledBy    = gv.LN.sys.calledBy

    OpSys        = platform.system()

    tempDir = os.getenv('TEMP', 'd:\\temp') if OpSys == 'Windows' else os.getenv('tmp', '/tmp')

    outFname = os.path.join(tempDir, 'LnTemp_%s.ini' % (getpass.getuser()))

        # -----------------------------------------
        # - copiamo file.ini to temp.ini
        # - facendo lo strip delle righe
        # - per evitare che il parser dia errore
        # -----------------------------------------
    finp = open(iniFileName,"r")
#    fout = open(outFname, "wb")
    aOut = []


    keyFirstNoBLANK = 0
    lineCounter = 0
    CONTINUATION_LINE = False
    emptyLine       = '^[ \\t]*$'
    commentedLine   = '^[ \\t]*(#|;)'
    import string, re
    for line in finp:
        if re.match(emptyLine,      line): continue
        if re.match(commentedLine,  line): continue
        firstChar = line.strip()[0]

        newLine = re.sub('^[ \\t]*([0-9A-Za-z]*:|=)', '\\1', line)
        aOut.append(newLine.rstrip(' \n'))


        '''
        line = line.rstrip()
        if firstChar in (string.ascii_letters + string.digits):
            token = LN.str.splitString(line, [': ', '= '],  maxsplit=1) # ':' + BLANK oppure '=' + BLANK
            nToken = len(token)
            if nToken == 2:
                line = line.strip()
            else:
                pass

        aOut.append(line)
        '''
    finp.close()

    for line in aOut:        print line
    sys.exit()

    aOut2 = '\n'.join(aOut)

        # Write a temporary FileName
    import tempfile
    fd, filename = tempfile.mkstemp()
    try:
        os.write(fd, aOut2)
        os.close(fd)
        # ...run the subprocess and wait for it to complete...
    finally:
        pass
        # os.remove(filename)

    print filename
    sys.exit()



    # config = ConfigParser.ConfigParser()
    config = ConfigParser.SafeConfigParser()
    config.read(outFname)

    # myDict2 = MyParser(config)

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
            print '...........', option
            xx = config.get(section, option)
            for key, value in variablesToReplace.items():
                xx = xx.replace('${' + key + '}', value)
            myDict[section][option] = xx
            # print xx

    LOG = myDict['LOG']
    CFG = myDict['Main']



    myDict3 = {}
    for section in config.sections():
        myDict3[section] = {}
        for option in config.options(section):
            myDict3[section][option] = config.get(section, option)

    return config, myDict
