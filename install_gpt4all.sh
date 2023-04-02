#!/usr/bin/env sh
# See: https://github.com/nomic-ai/gpt4all

INSTALL_ROOT=${HOME}
INSTALL_DIR=${INSTALL_ROOT}/gpt4all

# ".torrent" or ""
# "-unfiltered" or ""
MODEL_URL_BASE=https://the-eye.eu/public/AI/models/nomic-ai/gpt4all
TORRENT=.torrent
MODEL_TYPE=-unfiltered
FILE_NAME=gpt4all-lora${MODEL_TYPE}-quantized.bin
DEST_FILE_NAME=gpt4all-lora-quantized.bin
FILE_TARGET=${FILE_NAME}${TORRENT}
DOWNLOAD_URL=${MODEL_URL_BASE}/${FILE_TARGET}
GIT_URL_BASE=git@github.com:nomic-ai
GIT_REPO_NAME=gpt4all
GIT_URL=${GIT_URL_BASE}/${GIT_REPO_NAME}.git
REPO_BIN_DIR=chat
INSTALLER_SCRIPT=gpt4all-lora-quantized-OSX-m1

mkdir -p ${INSTALL_DIR}
cd ${INSTALL_DIR}
git clone ${GIT_URL}
cd ${GIT_REPO_NAME}/${REPO_BIN_DIR}
brew install aria2
aria2c -x16 -s16 --seed-time=0 -o ${DEST_FILE_NAME} ${DOWNLOAD_URL}
rm gpt4all-lora-quantized-OSX-intel gpt4all-lora-quantized-linux-x86 gpt4all-lora-quantized-win64.exe
rm *.torrent 2&> /dev/null

echo "########################################"
echo ./${INSTALLER_SCRIPT} --help
echo ./${INSTALLER_SCRIPT}
echo "########################################"
