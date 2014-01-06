#!/bin/bash
# set -x

# deve creare il package per l'applicazione


# Tree
#       -build
#       -MyProject
#          -bin
#             -startPrj.sh
#          -SOURCE
#              -JMyPrj_Package
#                  -dir1
#                  -dir2
#          -conf
#       -LnPackage_Source
#         -dir1
#         -dir2
#       -makeBin    (thisDIR)     <====

# /cygdrive/l/LNFree/_Tools/Utils/PKZIP25.EXE -add=all  -dir=current -excl=*.pyc -incl=*.py -level=6 -zip=new -attr=all d:\temp\LnRSync.zip" "l:\Loreto\ProjectsAppl\_Python\LN_PythonProjects\LnFunctions\*.*"
# PKZIP25.EXE -add=all  -dir=current -excl=*.pyc -incl=*.py -level=6 -zip=new -attr=all "d:\temp\LnRSync.zip" "l:\Loreto\ProjectsAppl\_Python\LN_PythonProjects\build\WORKing\LnRSync\SOURCE\*.*"
# exit



# ====================================================
# = writeLog
# ====================================================
function writeLOG {
    text=$*
    echo "       $text" | tee -a ${LOGFILE}
}

# ====================================================
# = exec Command
# ====================================================
function execCommand {
    caller=$(printf "%-20s:" ${FUNCNAME[1]})
    Msg=$1
    CMD="$2 $3"

    [  "$savedCaller" != "$caller" ] && writeLOG $caller

    writeLOG $Msg
    writeLOG $CMD
    [ "$ACTION" == "--GO" ] && eval ${CMD} | writeLOG

    savedCaller=$caller
}

# ====================================================
# = clean BUILD Dir
# ====================================================
function cleanWorkDir {
    local buildDir=$1
    local workDir=$2
    local savedDir="$PWD"


       # Se nella cartella ${BUILDDIR} sono gia' presenti i sorgenti vengono eliminati
    if [ -d "${buildDir}" ]; then
        [ "$ACTION" == "--GO" ] && cd "${buildDir}"
        # execCommand "Moving to directory ${buildDir}" 'cd' "${buildDir}" - Quando torna non mi trovo nella dir desiderata
        if [ -d "${workDir}" ]; then
            execCommand "Cleaning directory WorkingDIR: ${workDir}" "rm -fr ${workDir}"
        fi

    else
        echo "${FUNCNAME[0]}: la directory ${buildDir} non esiste"
        exit 1
    fi

    [ "$ACTION" == "--GO" ] && cd ${savedDir}

    return 0
}

# ====================================================
# = Copia file nella dir  di BUILD
# ====================================================
function CopyToBuild {
    local sourceDir=$1
    # local fileSpec=$2
    local destDir=$2

    execCommand "Creating ${destDir} directory"  "mkdir --parent ${destDir}"

        # Effettua una copia dei sorgenti
    execCommand "Copying [${sourceDir}]  into [${destDir}]"  "cp -Rpv ${sourceDir} ${destDir}"

    return
}




# ====================================================
# = Creazione del package.zip
# ====================================================
function createPrjZipPackage {
    local zipDir=$1
    local savedDir="$PWD"
    # local zipName="JBossAdmin.zip"
    # local zipName="${PRJ_NAME}.zip"
    local zipName="${PRJ_PKGNAME}.zip"


        # Entra nella cartella del primo modulo e crea il pacchetto
    echo $PWD
    [ "$ACTION" == "--GO" ] && cd ${zipDir}
    echo $PWD

    # execCommand "Creating ${zipName}" "${ZIPCMD} ${ZIPOPTS} ../bin/${zipName} * ${ZIPINCLUDEOPTS}"

    execCommand "Creating ${zipName}" "${ZIPCMD_DOS} ${ZIPOPTS_DOS} ../bin/${zipName} *"


    [ "$ACTION" == "--GO" ] && cd ${savedDir}

    execCommand "removing source directory: ${zipDir}" "rm -rf ${zipDir}"


}

# ===========================================================================
# = Creazione del project.tgz
# = Il file viene creato una cartella sopra quella richiesta.
# = Se esiste un file allora il vecchio viene salvato con la data attuale.
# ===========================================================================
function createPrjTarFile {
    local tarDir=$1
    local savedDir=""

    # local fileName="${PRJ_PKGNAME}"
    local fileName="${PRJ_NAME}"
    local tarFile="${fileName}.tgz"

    # Entra nella cartella richiesta
    [ "$ACTION" == "--GO" ] && cd ${tarDir}

        # vai una dir up
    [ "$ACTION" == "--GO" ] && cd .. && savedDIR="$PWD"


        # Se esiste un pacchetto obsoleto lo rinomina (nomepacchetto.YYYY_MM_GG-hh_mm)
    if [ -f "${tarFile}" ]; then
        newName="${fileName}_$(date +%Y_%m_%d-%H_%M).tgz"
        execCommand "Saving previous tar file" "mv ${tarFile} ${newName}"

    else
        echo "${FUNCNAME[0]}: No previous ${tarFile} FOUND" | tee -a ${LOGFILE}
    fi

    # "Torniamo nella cartella richiesta
    [ "$ACTION" == "--GO" ] && cd ${tarDir}

    execCommand "Creating Tar file ${savedDIR}/${tarFile}" "${TARCMD} ${TAROPTS} ../${tarFile} * ${TAREXOPTS}"

    [ "$ACTION" == "--GO" ] && cd ${savedDir}

}

# ====================================================
# = Variabili Globali
# = Alcini path sono relativi in quanto devo spostarmi
# = su diverse baseDir per effettuare lo zip
# ====================================================
function setVariables {
    # GET AbsolutePath
    # pushd $(dirname $0) >/dev/null; thisDIR=$(pwd -P) >/dev/null; popd >/dev/null
    thisSCRIPT=$(cd $(dirname "$0"); pwd -P)/$(basename "$0")
    thisDIR=$(dirname "$thisSCRIPT")

        # Definizione dei path necessari
    baseMainDIR="$(dirname ${thisDIR})"                                     # one UP
    baseBuildDIR="${baseMainDIR}/build"                                     # Bulding directory nella quale lo script salva il pacchetto creato
    [ ! -d "$baseBuildDIR" ] && writeLOG "Directory [$baseBuildDIR] non esiste" && exit

    PRJ_BASEDIR="${baseMainDIR}/${PRJ_NAME}"                             # Project Directory

    LN_PKGNAME="LnFunctions"                                                # Nome del modulo che deve essere trasformato in pacchetto
    LN_PKGSOURCEDIR="${baseMainDIR}/${LN_PKGNAME}"                          # Directory dei sorgenti del modulo

    LOGDIR="${baseMainDIR}/log"                                             # Directory che contiene il file di log dello script
    LOGFILE="${LOGDIR}/$(basename ${0} .sh).log"                                # Path assoluto dello script di log

    # Comandi utilizzati per ottenere i pacchetti
    ZIPCMD="zip"

    ZIPOPTS="-r -o -q"                                                         # Subdirectories and quite mode
    ZIPOPTS="-r -o "                                                         # Subdirectories and quite mode
    ZIPINCLUDEOPTS="-i \*.py"

    ZIPCMD_DOS="/cygdrive/l/LNFree/_Tools/Utils/PKZIP25.EXE"
    ZIPCMD_DOS="PKZIP25.EXE"
    ZIPOPTS_DOS="-add=all  -dir=current -excl=*.pyc -incl=*.py -level=6 -zip=new -attr=all"

    # Opzioni standard per la creazione dei pacchetti
    TARCMD="tar"
    TAROPTS="-czf"                                                         # Create, GZIP Compression and file output
    TAREXOPTS="--exclude=*.cfgc --exclude=*/Exploded*"

    writeLOG ""
}




############# M A I N ######################
    PRJ_NAME="LnRSync"                                      # Nome del Progetto e della dir con i sorgenti
    PRJ_PKGNAME="LnRSync"                                   # Nome della root directory all'interno del tar e nome del tar.

    ACTION=$1
    [ "$ACTION" == "--GO" ] && echo 'ok'

        # =================================================
        # = GET AbsolutePath
        # =================================================
    thisSCRIPT=$(cd $(dirname "$0"); pwd -P)/$(basename "$0")
    thisDIR=$(dirname "$thisSCRIPT")                                        # one UP

        # =================================================
        # = Definizione dei path necessari
        # =================================================
    baseMainDIR="$(dirname ${thisDIR})"                                     # one UP
    baseBuildDIR="${baseMainDIR}/build"                                     # Bulding directory nella quale lo script salva il pacchetto creato
    [ ! -d "$baseBuildDIR" ] && writeLOG "Directory [$baseBuildDIR] non esiste" && exit

        # =================================================
        # = setVariables
        # =================================================
    LOGDIR="${baseMainDIR}/log"                                             # Directory che contiene il file di log dello script
    LOGFILE="${LOGDIR}/$(basename ${0} .sh).log"                                # Path assoluto dello script di log
    PRJ_BASEDIR="${baseMainDIR}/${PRJ_NAME}"                             # Project Directory
    workingDirectory="${baseBuildDIR}/WORKing"
    execCommand "Rimozione della Working Dir"                   "rm -rf ${workingDirectory}"


        # =================================================
        # = Effettua la copia dei sorgenti sulla dir di BUILD
        # =================================================
    sourceDir="${PRJ_BASEDIR}/*"
    destDir="${workingDirectory}/${PRJ_PKGNAME}/"
    execCommand "Creating directory ${destDir}"                 "mkdir --parent ${destDir}"
    execCommand "Copying [${sourceDir}]  into [${destDir}]"     "cp -Rp ${sourceDir} ${destDir}"

        # =================================================
        # = Effettua una copia di LnPackage sulla dir di BUILD
        # =================================================
    LN_PKGNAME="LnFunctions"                                                # Nome del modulo che deve essere trasformato in pacchetto
    sourceDir="${baseMainDIR}/${LN_PKGNAME}/*"
    destDir="${workingDirectory}/${PRJ_PKGNAME}/SOURCE/$LN_PKGNAME"
    execCommand "Creating directory ${destDir}"                 "mkdir --parent ${destDir}"
    execCommand "Copying [${sourceDir}]  into [${destDir}]"     "cp -Rp ${sourceDir} ${destDir}"
    execCommand "removing undesired files *.pyc from [${destDir}]"     "rm -rf ${destDir}/*.pyc"

        # =================================================
        # = Creating zipPackage
        # =================================================
    # Comando Funzionante:  PKZIP25.EXE -add=all  -dir=current -excl=*.pyc -incl=*.py -level=6 -zip=new -attr=all "d:\temp\LnRSync.zip" "l:\Loreto\ProjectsAppl\_Python\LN_PythonProjects\build\WORKing\LnRSync\SOURCE\*.*"
    ZIPCMD_DOS="PKZIP25.EXE"
    ZIPOPTS_DOS="-add=all  -dir=current -excl=*.pyc -incl=*.py -level=6 -zip=new -attr=all"
    zipDir="${workingDirectory}/${PRJ_PKGNAME}/SOURCE"
    zipDir="l:\Loreto\ProjectsAppl\_Python\LN_PythonProjects\build\WORKing\LnRSync\SOURCE"
    zipName="${baseBuildDIR}.zip"
    zipName="d:/temp/LnRSync.zip"
    exit

        # ----------------------------------------------------------------
        # - Entra nella cartella del primo modulo e crea il pacchetto
        # ----------------------------------------------------------------
    savedDir="$PWD"
    echo $PWD
    [ "$ACTION" == "--GO" ] && cd ${zipDir}
    echo $PWD

    execCommand "Creating ${zipName}"                           "${ZIPCMD_DOS} ${ZIPOPTS_DOS} ${zipName} ${zipDir}/*.*"
    [ "$ACTION" == "--GO" ] && cd ${savedDir}
    execCommand "removing source directory: ${zipDir}"          "rm -rf ${zipDir}"



        # =================================================
        # = Creating tar package
        # =================================================
    tarDir=${workingDirectory}
    fileName="${PRJ_NAME}"
    tarFile="${fileName}.tgz"
    savedDIR=""

        # Entra nella cartella richiesta
    [ "$ACTION" == "--GO" ] && cd ${tarDir}

        # vai una dir up
    [ "$ACTION" == "--GO" ] && cd .. && savedDIR="$PWD"

        # Se esiste un pacchetto obsoleto lo rinomina (nomepacchetto.YYYY_MM_GG-hh_mm)
    if [ -f "${tarFile}" ]; then
        newName="${fileName}_$(date +%Y_%m_%d-%H_%M).tgz"
        execCommand "Saving previous tar file"                  "mv ${tarFile} ${newName}"

    else
        writeLOG "${FUNCNAME[0]}: No previous ${tarFile} FOUND"
    fi

        # "Torniamo nella cartella richiesta
    [ "$ACTION" == "--GO" ] && cd ${tarDir}


    TARCMD="tar"
    TAROPTS="-czf"                                                         # Create, GZIP Compression and file output
    TAREXOPTS="--exclude=*.cfgc --exclude=*/Exploded*"
    execCommand "Creating Tar file ${savedDIR}/${tarFile}"          "${TARCMD} ${TAROPTS} ../${tarFile} * ${TAREXOPTS}"

    [ "$ACTION" == "--GO" ] && cd ${savedDir}

    exit





