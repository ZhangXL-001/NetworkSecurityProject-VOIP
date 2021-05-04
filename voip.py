# -*- coding: utf-8 -*- 
import pyaudio
import wave
import ffmpeg
import pydub
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 8000  # Record at 44100 samples per second
seconds = 4
filename = "output.wav"

p = pyaudio.PyAudio()

print('请开始说话')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

sound = AudioSegment.from_file('output.wav', format='wav')
play(sound)
sound.export('output2.amr', format='amr')