#!/usr/bin/env bash
# source ${HOME}/whisper/venv/bin/activate

rm chat.in.txt
rm chat.out.txt
rm line.txt
touch chat.out.txt

get_users_turn() {
    cat turn.txt
}
set_users_turn() {
    echo "$1" > turn.txt
}

set_users_turn 1

get_user_input() {
    ffmpeg -t 5 -y -f avfoundation -i ":1" user.in.mp3
    whisper user.in.mp3 --model tiny.en -f txt --verbose False --fp16 False --language English --threads 2 --output_dir .
    paste -s -d ' ' user.in.txt > user.in.paste.txt; mv user.in.paste.txt user.in.txt
    cat user.in.txt 
    cat user.in.txt > chat.in.txt
    set_users_turn 0
}

get_entry_from_chat_bot() {
    while :; do
        wait_for_user_to_finish
        touch line.txt
        while read -r -e -s -t 5 char; do
            echo "$char"  | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g' | cat >> line.txt
            cat line.txt
        done < chat.out.txt
        speak_chat_bot_output
    done
}

wait_for_bot_to_finish () {
    while [ "$(get_users_turn)" == "0" ]; do
        sleep 0.1
    done
}

wait_for_user_to_finish () {
    while [ "$(get_users_turn)" == "1" ]; do
        sleep 0.1
    done
}

speak_chat_bot_output() {
    say -v Daniel -r 185 -f line.txt
    rm line.txt
    set_users_turn 1
    # Damayanti Daniel Good Jester Karen  Melina Milena Ralph Samantha Tessa Trinoids Whisper Zarvox 
}
get_entry_from_user () {
    while true
    do
        wait_for_bot_to_finish
        get_user_input
    done
} 

start_chat_bot() {
    LOCATION=${HOME}/gpt4all/gpt4all/chat
    rm chat.in.txt chat.out.txt 2&> /dev/null
    mkfifo chat.in.txt
    mkfifo chat.out.txt
    sleep 100000 < chat.out.txt &
    echo ${LOCATION}/gpt4all-lora-quantized-OSX-m1 -m ${LOCATION}/gpt4all-lora-quantized.bin
    ${LOCATION}/gpt4all-lora-quantized-OSX-m1 -m ${LOCATION}/gpt4all-lora-quantized.bin < chat.in.txt > chat.out.txt 2> /dev/null &
    sleep 100000 > chat.in.txt &
}

start_chat_bot
get_entry_from_chat_bot &
get_entry_from_user