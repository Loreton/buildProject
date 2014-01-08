#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# =================================================================================
# LnZip.py      by Loreto Notarantonio
# Version 0.11 - 2010-10-18 New Version started
# =================================================================================



import os, sys
import zipfile
import fnmatch



def make_zipfile(output_filename, source_dir):
    relroot = os.path.abspath(os.path.join(source_dir, ".."))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)




def LnZipDir(output_filename, source_dir, include=['*'], exclude=[], emptyDir=False):
    relroot = os.path.abspath(os.path.join(source_dir, ".."))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            if emptyDir: zip.write(root, os.path.relpath(root, relroot))            # add directory (needed for empty dirs)
            for file in files:
                filename = os.path.join(root, file)

                    # Exclude pattern (search pattern in file name)
                isValid = True
                for fSpec in exclude:        # togli gli exclude
                    fSpec = fSpec.strip()
                    if fSpec in filename:    # cerca il MATCH nel nome del file
                        isValid = False
                        break

                    # Include pattern (use fnmatch lib)
                if isValid:
                    for fSpec in include:
                        fSpec = fSpec.strip()
                        if fnmatch.fnmatch(filename, fSpec):    # cerca il MATCH nel nome del file
                            arcname = os.path.join(os.path.relpath(root, relroot), file)
                            zip.write(filename, arcname)








import zipfile
if __name__ == '__main__':

    zipFile     = 'l:/Loreto/GIT-REPO-CLONE/build/MP3Catalog.zip'
    outDir     = 'l:/temp'
    source_dir  = 'l:/Loreto/GIT-REPO-CLONE/build/Working/MP3CatalogB'

    ''' OK
    zipFile = outDir + '/make_zipfile.zip'
    outZip = make_zipfile(zipFile, source_dir)
    with zipfile.ZipFile(zipFile, 'r') as myzip:
        print myzip.testzip()
        print myzip.infolist()
        filelist = myzip.namelist()
        for file in filelist:
            print file

    zipFile = outDir + '/LnZip_sample_dir.zip'
    LnZipDir(zipFile,  source_dir, include=['*.sample'], emptyDir=True)

    zipFile = outDir + '/LnZip_sample_NOdir.zip'
    LnZipDir(zipFile, source_dir, include=['*.sample'], emptyDir=False)

    '''
    zipFile = outDir + '/LnZip_specDirs.zip'
    LnZipDir(zipFile, source_dir, include=['*'], exclude=['.git' + os.sep], emptyDir=False)

    sys.exit()


