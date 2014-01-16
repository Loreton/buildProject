#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
sys.dont_write_bytecode = True

# -----------------------------------------------------------------------------------------------------------------------
# Type 1
#     - punto a Ln.logger.LnLogger.function()   se nel prossimo __init__ non metto nulla
#     - punto a Ln.logger.function()            se nel prossimo __init__ inserisco <from    LnLogger        import *> ciao
# -----------------------------------------------------------------------------------------------------------------------
import LnNet                    as net
import LnLogger                 as logger
import LnDictionary             as dict
import LnSys                    as sys
import LnFile                   as file
import LnProcess                as proc
import LnString                 as string
import LnFormat                 as fmt
import LnExcel                  as excel
import LnTime                   as time

# =========================================================================
# Fore:  BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back:  BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
# =========================================================================
import colorama as color

colorama.init(autoreset=True)
FG          = colorama.Fore
BG          = colorama.Back
HI          = colorama.Style
cERROR      = FG.RED
cWARNING    = FG.MAGENTA
cINFO       = FG.GREEN

cBLACK      = FG.BLACK
cRED        = FG.RED
cGREEN      = colorama.Fore.GREEN
cYELLOW     = FG.YELLOW
cBLUE       = FG.BLUE
cMAGENTA    = FG.MAGENTA
cCYAN       = FG.CYAN
cWHITE      = FG.WHITE


cBW       = FG.BLACK + BG.WHITE
cBWH      = FG.BLACK + BG.WHITE + HI.BRIGHT





# -----------------------------------------------------------------------------------------------------------------------
#  Type 2 - al porto del type-1 se devo mascherare una subDirectory
# -----------------------------------------------------------------------------------------------------------------------
# import LnLogger.subDir                as logger        # punto a Ln.logger.function()

# -----------------------------------------------------------------------------------------------------------------------
#  Type 3 - Punto direttamente alla funzione LN.function()
# -----------------------------------------------------------------------------------------------------------------------
# from LnDictionary.printDictionaryTree   import printDictionaryTree  as printTree
# from LnDictionary.printDictionaryTree   import getDictionaryTreeUnderTest  as printTreeUT
# from LnFile.LN_ReadIniFile              import readIniConfigFile    as configFile


