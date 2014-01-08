#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# =================================================================================
# LnZipClass.py      by Loreto Notarantonio
# Version 1.0 - 2014-01-05             Version started
# =================================================================================



import os, sys
import zipfile
import fnmatch

class LnZipClass:
    zipID = None

    def open(self, zipFileName):
        self.zipID = zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED)

    def close(self):
        self.zipID.close()

    def addFolderToZip(self, source_dir, include=['*'], exclude=[], emptyDir=False, hiddenDir=True):
        zipID = self.zipID
        # relroot = os.path.abspath(os.path.join(source_dir, "..")) #  questo se vogliamo andare un path sopra
        relroot = os.path.abspath(source_dir)

        for root, dirs, files in os.walk(source_dir):

            if os.path.basename(root)[0] == '.' and not hiddenDir: continue                               #skip hidden directories
            if emptyDir: zipID.write(root, os.path.relpath(root, relroot))              # add directory (needed for empty dirs)

            for fName in files:
                fullPathName = os.path.join(root, fName)
                fullPathName = os.path.join(root, fName)

                    # Exclude pattern (search pattern in file name)
                isValid = True
                for fSpec in exclude:        # togli gli exclude
                    fSpec = fSpec.strip()
                    if fSpec in fullPathName:    # cerca il MATCH nel nome del file
                        isValid = False
                        break

                    # Include pattern (use fnmatch lib)
                if isValid:
                    for fSpec in include:
                        fSpec = fSpec.strip()
                        if fnmatch.fnmatch(fullPathName, fSpec) or fName==fSpec:    # cerca il MATCH nel nome del file
                            arcname = os.path.join(os.path.relpath(root, relroot), fName)
                            zipID.write(fullPathName, arcname)


if __name__ == '__main__':
    myZip = LnZipClass()

    zipFile     = 'l:/temp/MP3Catalog.zip'
    source_dir  = 'l:/Loreto/GIT-REPO-CLONE/MP3Catalog'

    myZip.open(zipFile)
    myZip.addFolderToZip(source_dir, include=['*'], exclude=['.git' + os.sep], emptyDir=False)
    myZip.addFolderToZip('l:/Loreto/ProjectsAppl/_Python/LnFunctions_OldStyle', include=['_callerMain.py'])
    myZip.addFolderToZip('l:/Loreto/ProjectsAppl/_Python/LnFunctions_OldStyle', include=['initLog.py'])
    myZip.close()

