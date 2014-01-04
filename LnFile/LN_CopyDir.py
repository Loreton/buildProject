#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import shutil

# =================================================================
# - Copy directory
# =================================================================
def copyDir(gv, srcPATH, dstPATH, subDirs=True, exitOnError=False):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy

    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    if not os.path.isdir(srcPATH):
        logger.error( "Source directory doesn't exists [%s]" % (srcPATH) )
        return False

    if subDirs == True:
        logger.debug("copying...Subtree [%s] to [%s]" % (srcPATH, dstPATH) )
        try:
            shutil.copytree(srcPATH, dstPATH)           # La dir non deve esistere
        except (IOError, os.error), why:
            msg = "Can't COPY Subtree [%s] to [%s]: %s" % (srcPATH, dstPATH, str(why))
            logger.warning(msg)
            if exitOnError:
                Ln.sys.exit(9001, msg)
            return False

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return  True



def copytree(gv, src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                shutil.copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))

        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)