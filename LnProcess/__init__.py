# outer __init__.py
# -*- coding: iso-8859-1 -*-
import platform

from runCommand                 import runCommand
from runCommand                 import runCommand_New
from runProcess                 import runProcess
from runAS                      import runAS
from getPidCommandLineArgs      import getPidCommandLineArgs

if platform.system() == 'Windows':
    from getPIDsWin         import getPIDsWin as getPIDs
else:
    from getPIDsUnix        import getPIDsUnix as getPIDs
