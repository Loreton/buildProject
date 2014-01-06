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



# ====================================================
# = exec Command
# ====================================================
function execCommand {
    caller=$(printf "%-20s:" ${FUNCNAME[1]})
    Msg=$1
    CMD="$2 $3"

    [  "$savedCaller" != "$caller" ] && echo && echo "$caller" | tee -a ${LOGFILE}

    echo "       $Msg" | tee -a ${LOGFILE}
    echo "       $CMD" | tee -a ${LOGFILE}
    [ "$ACTION" == "--GO" ] && eval ${CMD} | tee -a ${LOGFILE}

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
    local fileSpec=$2
    local destDir=$3

    execCommand "Creating ${destDir} directory"  "mkdir --parent ${destDir}"

        # Effettua una copia dei sorgenti
    # execCommand "Copying [${sourceDir}]  into [${destDir}]"  "cp -Rpv ${sourceDir} ${destDir}"
    # execCommand "Copying [${sourceDir}]  into [${destDir}]"  "cp --parents `find $sourceDir -name $fileSpec` ${destDir}"
    # execCommand "Copying [${sourceDir}]  into [${destDir}]"  "find ${sourceDir} -name \"${fileSpec}\" -exec cp {} ${destDir} \";\""

    # execCommand "Copying [${sourceDir}]  into [${destDir}]" "L:\LNFree\SynchBackup\cwRsync\bin\rsync.exe -avm --include='${fileSpec}' -f 'hide,! */' ${sourceDir} ${destDir}"
    # execCommand "Copying [${sourceDir}]  into [${destDir}]" "/cygdrive/l/LNFree/SynchBackup/cwRsync/bin/rsync.exe -av --include='${fileSpec}' -f 'hide,! */' ${sourceDir} ${destDir}"
    execCommand "Copying [${sourceDir}]  into [${destDir}]" "/cygdrive/l/LNFree/SynchBackup/cwRsync/bin/rsync.exe -av ${fileSpec} -f 'hide,! */' ${sourceDir} ${destDir}"

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

    # execCommand "Creating ${zipName}" "${ZIPCMD} ${ZIPOPTS} ../${zipName} *.py "
    execCommand "Creating ${zipName}" "${ZIPCMD} ${ZIPOPTS} ../bin/${zipName} * '${ZIPINCLUDEOPTS}'"

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

    PRJ_BASEDIR="${baseMainDIR}/${PRJ_NAME}"                             # Project Directory

    LN_PKGNAME="LnFunctions"                                                   # Nome del modulo che deve essere trasformato in pacchetto
    LN_PKGSOURCEDIR="${baseMainDIR}/${LN_PKGNAME}"                    # Directory dei sorgenti del modulo

    LOGDIR="${baseMainDIR}/log"                                             # Directory che contiene il file di log dello script
    LOGFILE="${LOGDIR}/$(basename ${0} .sh).log"                                # Path assoluto dello script di log

    # Comandi utilizzati per ottenere i pacchetti
    ZIPCMD="zip"
    ZIPOPTS="-r -o -q"                                                         # Subdirectories and quite mode
    ZIPOPTS="-r -o "                                                         # Subdirectories and quite mode
    ZIPINCLUDEOPTS=-"i \*.py"
    # ZIPINCLUDEOPTS="-i *.py"

    # Opzioni standard per la creazione dei pacchetti
    TARCMD="tar"
    TAROPTS="-czf"                                                         # Create, GZIP Compression and file output
    TAREXOPTS="--exclude=*.cfgc --exclude=*/Exploded*"

    echo | tee -a ${LOGFILE}
}



############# M A I N ######################
    PRJ_NAME="LnRSync"                                      # Nome del Progetto e della dir con i sorgenti
    PRJ_PKGNAME="LnRSync"                                   # Nome della root directory all'interno del tar e nome del tar.

    ACTION=$1
    [ "$ACTION" == "--GO" ] && echo 'ok'

    setVariables
    workingDirectory="${baseBuildDIR}/WORKing"

    # ############ STEP 1
    execCommand "Rimozione della Working Dir" "rm -rf ${workingDirectory}"

    CopyToBuild             "${PRJ_BASEDIR}" "--exclude='/*.pyc'" "${workingDirectory}/$PRJ_PKGNAME"
    exit
    CopyToBuild             "${PRJ_BASEDIR}/bin" "*" "${workingDirectory}/$PRJ_PKGNAME"
    CopyToBuild             "${PRJ_BASEDIR}/conf" "*" "${workingDirectory}/$PRJ_PKGNAME"
    # CopyToBuild             "${PRJ_BASEDIR}" "--exclude='/SOURCE'" "${workingDirectory}/$PRJ_PKGNAME"

        # = Adding LnPackage to Source dir
    CopyToBuild             "$LN_PKGSOURCEDIR/*" "${workingDirectory}/${PRJ_PKGNAME}/SOURCE/$LN_PKGNAME"

        # = Creating python zipPackage
    createPrjZipPackage     "${workingDirectory}/${PRJ_PKGNAME}/SOURCE"

    # ############ STEP 2
        # = Creating tar project
    createPrjTarFile        "${workingDirectory}"

    execCommand "Rimozione della Working Dir" "rm -rf ${workingDirectory}"

    [ "$ACTION" != "--GO" ] && echo "Ha girato in TEST mode. Immettere --GO per eseguire i comandi."

    exit
