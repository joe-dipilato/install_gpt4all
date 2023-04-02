#!/usr/bin/env sh
# source ${HOME}/whisper/venv/bin/activate

LOCATION=${HOME}/gpt4all/gpt4all/chat
rm chat.in.txt chat.out.txt 2&> /dev/null
mkfifo chat.in.txt
${LOCATION}/gpt4all-lora-quantized-OSX-m1 -m ${LOCATION}/gpt4all-lora-quantized.bin < chat.in.txt > chat.out.txt & # | tee chat.out.txt > /dev/null &
sleep 100000 > chat.in.txt

echo "my command" > chat.in.txt
tail -f chat.out.txt
tail -f chat.in.txt
# sleep infinity > chat.in.txt &
# tail -f chat.out.txt
# sleep 5
# echo "is anybody there?\\n" >> chat.pipe

