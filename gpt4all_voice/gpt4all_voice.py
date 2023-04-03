#!/usr/bin/env python3
import subprocess, shlex
from pathlib import Path
import argparse
from gpt4all_voice.transcriber import WhisperStreamingTranscriber
import sys
from typing import Iterator, List, Optional, Union
import queue
import sounddevice as sd
from whisper.audio import N_FRAMES, SAMPLE_RATE
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE
from whisper import available_models
from gpt4all_voice.schema import (
    Context,
    StdoutWriter,
    WhisperConfig,
)
from logging import getLogger
import logging
logger = getLogger(__name__)

logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

rel_chat_path = Path("gpt4all/gpt4all/chat")
exe_name = Path("gpt4all-lora-quantized-OSX-m1")
model_name = Path("gpt4all-lora-quantized.bin")
chat_path = Path.home() / rel_chat_path
exe_path = chat_path / exe_name
model_path = chat_path / model_name

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        type=str,
        choices=sorted(LANGUAGES.keys())
        + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
        default=list(LANGUAGES.keys())[0]
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=available_models(),
        default=available_models()[0]
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["cpu","cuda"],
        default="cpu"
    )
    parser.add_argument(
        "--beam_size",
        "-b",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        action="append",
        default=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    )
    parser.add_argument(
        "--max_nospeech_skip",
        type=int,
        help="Maximum number of skip to analyze because of nospeech",
        default=0,
    )
    parser.add_argument(
        "--vad",
        type=float,
        help="Threshold of VAD",
        default=0.1,
    )
    parser.add_argument(
        "--frame",
        type=int,
        help="The number of minimum frames of mel spectrogram input for Whisper",
        default=N_FRAMES,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file",
        type=Path,
        default=StdoutWriter(),
    )
    parser.add_argument(
        "--mic",
        help="Set MIC device",
    )
    parser.add_argument(
        "--num_block",
        "-n",
        type=int,
        default=3,
        help="Number of operation unit. Lower = Faster",
    )

    options = parser.parse_args()
    return options


def get_context(*, opts) -> Context:
    ctx = Context(
        beam_size=opts.beam_size,
        temperatures=opts.temperature,
        max_nospeech_skip=opts.max_nospeech_skip,
        vad_threshold=opts.vad,
        mel_frame_min_num=opts.frame,
    )
    logger.debug(f"Context: {ctx}")
    return ctx

def get_whisper(opts) -> WhisperStreamingTranscriber:
    config = WhisperConfig(
        model_name=opts.model,
        language=opts.language,
        device=opts.device,
    )
    logger.debug(f"WhisperConfig: {config}")
    return WhisperStreamingTranscriber(config=config)


def transcribe_from_mic(
    *,
    wsp: WhisperStreamingTranscriber,
    sd_device: Optional[Union[int, str]],
    num_block: int,
    ctx: Context,
) -> Iterator[str]:
    q = queue.Queue()

    def sd_callback(indata, frames, time, status):
        if status:
            logger.warning(status)
        q.put(indata.ravel())

    logger.info("Ready to transcribe")
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=N_FRAMES * num_block,
        device=sd_device,
        dtype="float32",
        channels=1,
        callback=sd_callback,
    ):
        idx: int = 0
        while True:
            if not idx % 50:
                logger.debug(f"Audio #: {idx}, The rest of queue: {q.qsize()}")
            audio = q.get()

            for chunk in wsp.transcribe(audio=audio, ctx=ctx):
                yield f"{chunk.start:.2f}->{chunk.end:.2f}\t{chunk.text}\n"
            idx += 1

def main() -> None:
    opts = get_args()
    wsp = get_whisper(opts=opts)
    ctx: Context = get_context(opts=opts)
    with opts.output.open("w") as outf:
        for text in transcribe_from_mic(
            wsp=wsp,
            sd_device=opts.mic,
            num_block=opts.num_block,
            ctx=ctx,
        ):
            outf.write(text)
            outf.flush()





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