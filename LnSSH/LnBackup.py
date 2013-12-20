#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, imp
import pprint


# #############################################################################
# # setBaseEnv()
# # Impostazione delle PATHs
# # La scriptDir consideriamo la curren a meno che non finisce con /bin.
# # In tal caso saliamo di una subDir.
# #############################################################################
def setBaseEnv():
    (scriptDir, FileName)   = os.path.split(os.path.abspath(sys.argv[0]))
    (Fname, Fext)           = os.path.splitext(FileName)
    MainProgram             = Fname
    
    if scriptDir.endswith(os.sep + 'bin'): scriptDir = scriptDir[:-4]
    if scriptDir.endswith(os.sep + 'Bin'): scriptDir = scriptDir[:-4]
    myPaths = []
    myPaths.append(os.path.normpath(scriptDir) )
    myPaths.append(os.path.normpath('%s/bin'  % (scriptDir) ) )
    myPaths.append(os.path.normpath('%s/conf' % (scriptDir) ) )
    myPaths.append(os.path.normpath('%s/Loreto/ProjectsAppl/_Python/LnFunctions/Functions' % (scriptDir[:2]) ) )
    myPaths.append(os.path.normpath('%(scriptDir)s/bin/LnFuncs201205.zip' % vars() ))

    
    for path in myPaths:  sys.path.insert(0, path)

    os.environ['PYTHONPATH'] = os.pathsep.join(myPaths)
    os.environ['LnProjectID'] = MainProgram

    fDEBUG = False
    fDEBUG = True
    if fDEBUG:
        print 'MainProgram.....', MainProgram
        print 'PYTHONPATH......'
        for path in os.getenv('PYTHONPATH').split(os.pathsep):
            print "     ", path
    
    
    return MainProgram
    
# pprint.pprint( globals() )
# sys.exit()



################################################################################
# - M A I N
################################################################################
def Main(args):
    mainProgram = setBaseEnv()
    PYTHON_DEBUGGER = os.getenv('PY_DEBUGGER')

    try:
        mainProgram  += '_Main'
        
        if PYTHON_DEBUGGER:
            MAIN = __import__('LnBackupMain')                        # WinPDB - Debugger
        else:
            MAIN = __import__(mainProgram)                        # mainProgram senza FULLPATH e senza EXT
        
        MAIN.Main(mainProgram, sys.argv[1:])

    except ImportError, why: 
        print "IMPORT failed:", why 
        sys.exit()

    print "Process completed."
    sys.exit()
 
    

if __name__ == "__main__":
    Main(sys.argv)