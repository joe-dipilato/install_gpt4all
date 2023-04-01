#!/usr/bin/env sh
# See: https://github.com/nomic-ai/gpt4all

INSTALL_ROOT=${HOME}
INSTALL_DIR=${INSTALL_ROOT}/gpt4all

MODEL_URL_BASE=https://the-eye.eu/public/AI/models/nomic-ai/gpt4all
TORRENT=.torrent # ".torrent" or ""
MODEL_TYPE=-unfiltered # "-unfiltered" or ""
FILE_NAME=gpt4all-lora${MODEL_TYPE}-quantized.bin${TORRENT}
DOWNLOAD_URL=${MODEL_URL_BASE}/${FILE_NAME}
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
aria2c -x16 -s16 ${DOWNLOAD_URL}
./${INSTALLER_SCRIPT} -m ${FILE_NAME}
