#!/usr/bin/env sh

brew install ffmpeg
pip3 install --upgrade pip
INSTALL_ROOT=${HOME}
mkdir -p ${INSTALL_ROOT}/whisper
cd ${INSTALL_ROOT}/whisper
python3 -m venv venv
source venv/bin/activate

# numba currently doesn't support python 3.11, so downgrade
brew install python@3.10
python3.10 -m pip install git+https://github.com/openai/whisper.git

# Record
ffmpeg -y -f avfoundation -i ":1" out.mp3
date +%S; whisper out.mp3 --model tiny.en -f txt --verbose False --fp16 False --language English --threads 2 --output_dir .;date +%S
cat out.txt
# afplay out.mp3
