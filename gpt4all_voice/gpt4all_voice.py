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
import re
from gpt4all_voice.schema import ParsedChunk
from multiprocessing import Process

logger = getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.WARNING)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(handler)

rel_chat_path = Path("gpt4all/gpt4all/chat")
exe_name = Path("gpt4all-lora-quantized-OSX-m1")
model_name = Path("gpt4all-lora-quantized.bin")
chat_path = Path.home() / rel_chat_path
exe_path = chat_path / exe_name
model_path = chat_path / model_name

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument( "--language", type=str, default=list(LANGUAGES.keys())[0],
                        choices=sorted(LANGUAGES.keys()) + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]))
    parser.add_argument( "--model", type=str,
                        choices=available_models(), default=available_models()[0] )
    parser.add_argument( "--device", type=str, default="cpu",
                        choices=["cpu","cuda"])
    parser.add_argument( "--beam_size", "-b", type=int, default=10)
    parser.add_argument( "--temperature", "-t", type=float,  default=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                        action="append")
    parser.add_argument( "--max_nospeech_skip", type=int, default=0,
                        help="Maximum number of skip to analyze because of nospeech")
    parser.add_argument( "--vad", type=float,
                        help="Threshold of VAD", default=0.1, )
    parser.add_argument( "--frame", type=int, default=N_FRAMES,
                        help="The number of minimum frames of mel spectrogram input for Whisper")
    parser.add_argument( "--output", "-o",
                        help="Output file", type=Path, default=StdoutWriter())
    parser.add_argument( "--mic",
                        help="Set MIC device")
    parser.add_argument( "--num_block", "-n", type=int, default=3,
                        help="Number of operation unit. Lower = Faster")
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
    wsp: WhisperStreamingTranscriber,
    sd_device: Optional[Union[int, str]],
    num_block: int,
    ctx: Context,
) -> Iterator[ParsedChunk]:
    q = queue.Queue()
    re_words = re.compile("[A-Za-z]")

    def sd_callback(indata, frames, time, status):
        if status:
            logger.warning(status)
        q.put(indata.ravel())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=N_FRAMES * num_block,
        device=sd_device,
        dtype="float32",
        channels=1,
        callback=sd_callback,
    ):
        # idx: int = 0
        # while True:
        #     if not idx % 50:
        #         logger.debug(f"Listening #: {idx}; Queue: {q.qsize()}")
        audio = q.get()
        done = False
        while not done:
            for chunk in wsp.transcribe(audio=audio, ctx=ctx):
                print(chunk.text)
                if re_words.search(chunk.text):
                    done=True
                    yield chunk
                else:
                    logger.debug(f"{chunk.start:.2f}->{chunk.end:.2f}\t{chunk.text}\n")
            if done:
                return

            # idx += 1

def main2() -> None:
    opts = get_args()
    wsp = get_whisper(opts=opts)
    ctx: Context = get_context(opts=opts)
    with opts.output.open("w") as outf:
        for chunk in transcribe_from_mic(
            wsp=wsp,
            sd_device=opts.mic,
            num_block=opts.num_block,
            ctx=ctx,
        ):
            outf.write(chunk.text)
            outf.flush()

from nomic.gpt4all import GPT4All

def main():
    opts = get_args()
    wsp = get_whisper(opts=opts)
    ctx: Context = get_context(opts=opts)
    with GPT4All() as bot:
        with opts.output.open("w") as outf:
            while True:
                response=""
                for chunk in transcribe_from_mic(
                    wsp=wsp,
                    sd_device=opts.mic,
                    num_block=opts.num_block,
                    ctx=ctx,
                ):
                    print(chunk.text)
                    print(f"GPTBot>  ", end="")
                    response = bot.prompt(chunk.text)
                    print(response)
                subprocess.call((shlex.split(f"say -v Samantha -r 185 ") + [response]))
                print(f"Human>  ", end="")

            # Damayanti Daniel Good Jester Karen  Melina Milena Ralph Samantha Tessa Trinoids Whisper Zarvox 

