#!/usr/bin/env python3
import subprocess, shlex
from pathlib import Path

rel_chat_path = Path("gpt4all/gpt4all/chat")
exe_name = Path("gpt4all-lora-quantized-OSX-m1")
model_name = Path("gpt4all-lora-quantized.bin")
chat_path = Path.home() / rel_chat_path
exe_path = chat_path / exe_name
model_path = chat_path / model_name
import time

from whisper import available_models




# live pipe to stdout
# p = subprocess.Popen(args=shlex.split("find /"))
# p.wait()

# context manager
# with subprocess.Popen(args=shlex.split("ls"), stdout=subprocess.PIPE) as proc:
#     time.sleep(3)
#     print(proc.stdout.readlines())



# start_chat_bot() {
#     LOCATION=${HOME}/gpt4all/gpt4all/chat
#     rm chat.in.txt chat.out.txt 2&> /dev/null
#     mkfifo chat.in.txt
#     mkfifo chat.out.txt
#     sleep 100000 < chat.out.txt &
#     ${LOCATION}/gpt4all-lora-quantized-OSX-m1 -m ${LOCATION}/gpt4all-lora-quantized.bin < chat.in.txt > chat.out.txt 2> /dev/null &
#     sleep 100000 > chat.in.txt &
# }


# #!/usr/bin/env bash
# # source ${HOME}/whisper/venv/bin/activate

# rm chat.in.txt > /dev/null 2>&1
# rm chat.out.txt > /dev/null 2>&1
# rm line.txt > /dev/null 2>&1
# touch chat.out.txt

# get_users_turn() {
#     cat turn.txt
# }
# set_users_turn() {
#     echo "$1" > turn.txt
# }

# set_users_turn 1

# get_user_input() {
#     echo -en "\rSpeak > "
#     ffmpeg -v 0 -t 5 -y -f avfoundation -i ":1" user.in.mp3 > /dev/null 2>&1
#     echo -en "\rYou   > "
#     rm user.in.txt > /dev/null 2>&1
#     whisper --verbose False user.in.mp3 --model tiny.en -f txt --verbose False --fp16 False --language English --threads 2 --output_dir .  > /dev/null 2>&1
#     if [ "$(cat user.in.txt)" == "You" ]; then
#         return
#     fi
#     paste -s -d ' ' user.in.txt > user.in.paste.txt; mv user.in.paste.txt user.in.txt
#     if [ ! -s user.in.txt ]; then
#         return
#     fi
#     echo
#     echo
#     cat user.in.txt
#     echo
#     cat user.in.txt > chat.in.txt
#     set_users_turn 0
# }

# get_entry_from_chat_bot() {
#     while :; do
#         wait_for_user_to_finish
#         touch line.txt
#         while read -r -d ">" -s -t 1 char; do
#             echo -n "$char" | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g' | cat >> line.txt
#             if [ -s line.txt ]; then
#                 echo "BB"
#                 od -c line.txt
#                 wc -c line.txt
#                 cat line.txt
#                 speak_chat_bot_output
#             fi
#         done < chat.out.txt

#         set_users_turn 1

#     done
# }

# wait_for_bot_to_finish () {
#     while [ "$(get_users_turn)" == "0" ]; do
#         sleep 0.1
#     done
# }

# wait_for_user_to_finish () {
#     while [ "$(get_users_turn)" == "1" ]; do
#         sleep 0.1
#     done
# }

# speak_chat_bot_output() {
#     echo "ChatBot > "
#     echo
#     cat line.txt
#     echo
#     say -v Samantha -r 185 -f line.txt
#     # Damayanti Daniel Good Jester Karen  Melina Milena Ralph Samantha Tessa Trinoids Whisper Zarvox 
# }
# get_entry_from_user () {
#     while true
#     do
#         wait_for_bot_to_finish
#         get_user_input
#     done
# } 


# start_chat_bot
# get_entry_from_chat_bot &
# get_entry_from_user

# # ps -ef | egrep "voice_interface.sh|sleep|gpt4all-lora-quantized-OSX|say" | grep -v grep | awk '{print $2}' | xargs kill