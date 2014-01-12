# ##################################
# # Colori
# ##################################
class colors:
    cHEADER     = '\033[95m'
    cOKBLUE     = '\033[94m'
    cOKGREEN    = '\033[92m'
    cINFO       = '\033[92m'
    cWARNING    = '\033[93m'
    cFAIL       = '\033[91m'
    cENDC       = '\033[0m'

    def disable(self):
        self.cHEADER = ''
        self.cOKBLUE = ''
        self.cOKGREEN = ''
        self.cWARNING = ''
        self.cFAIL = ''
        self.cENDC = ''


    def GREEN(self,  text):
        print self.cOKGREEN + text + self.cENDC

    def INFO(self,  text):
        print self.cINFO + text + self.cENDC

    def WARNING(self, text):
        print self.cWARNING + text + self.cENDC

    def ERROR(self, text):
        print self.cFAIL + text + self.cENDC

    def HEADER(self,  text):
        print self.cHEADER + text + self.cENDC


# pColor = bcolors()
# pColor,GREEN('Ciao')