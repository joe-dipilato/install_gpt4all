#!/usr/bin/env sh
# source ${HOME}/whisper/venv/bin/activate

LOCATION=${HOME}/gpt4all/gpt4all/chat
mkfifo chat.pipe
${LOCATION}/gpt4all-lora-quantized-OSX-m1 -m ${LOCATION}/gpt4all-lora-quantized.bin < chat.pipe | tee out.txt &
# ${HOME}/gpt4all/gpt4all/chat/gpt4all-lora-quantized-OSX-m1 < chat.pipe &
sleep infinity > chat.pipe &
sleep 5
echo "is anybody there?\\n" >> chat.pipe


# Record
ffmpeg -y -f avfoundation -i ":1" out.mp3
date +%S; whisper out.mp3 --model tiny.en -f txt --verbose False --fp16 False --language English --threads 2 --output_dir .;date +%S
paste -s -d ' ' out.txt > out.paste.txt; mv out.paste.txt out.txt


say -v Daniel -r 185 -f out.txt
# Damayanti Daniel Good Jester Karen  Melina Milena Ralph Samantha Tessa Trinoids Whisper Zarvox 

# afplay out.mp3
