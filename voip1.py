#-*- coding: utf-8 -*-

import tkinter as tk
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox 
import pyaudio
import wave
import ffmpeg
import pydub
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import which
from rc4 import encrypt
import socket

window = tk.Tk()
window.title("简易VOIP安全网络通话(1)")

greeting = tk.Label(text="亲爱的用户，您好！如要打电话请输入对方的IP",foreground="yellow",background="green",width=46)
greeting.pack()

ipentry = tk.Entry(fg="#00FF42", bg="black", width=46)
ipentry.pack()
#ip= ipentry.get()

def check_online():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if clientsocket.connect(('127.0.0.1',4096)):
        tk.messagebox.showinfo('检测到对方在线','可以进行通话')
    else:
        tk.messagebox.showinfo('很抱歉','对方暂时不在线，请稍后再试')

checkbutton = tk.Button(text="检测对方是否在线",width=46,height=5,bg="#00FF9C",fg="white",command=check_online)
checkbutton.pack()




getsecond= tk.Label(text='请输入单次通话多少秒',foreground="yellow",background="green",width=46)
getsecond.pack()

secondentry = tk.Entry(fg="black", bg="white", width=46)
secondentry.pack()
second= secondentry.get()

def make_a_call():
    AudioSegment.converter = which("ffmpeg")

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 8000  # Record at 44100 samples per second
    #seconds = 4
    filename = "outputfrom1.wav"

    p = pyaudio.PyAudio()

    print('请开始说话')
    tk.messagebox.showinfo('提示','请开始说话')

    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * second)):
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

    sound = AudioSegment.from_file('outputfrom1.wav', format='wav')
    #play(sound)
    sound.export('outputfrom1.amr', format='amr')

    with open('outputfrom1.amr','rb') as f:
        amr=f.read()
    with open('encryptfrom1.amr','wb') as e:
        e.write(encrypt(amr,'123456789'))
    
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientsocket.connect(('127.0.0.1',4096))
    with open('encryptfrom1.amr','rb') as f:
        while True:
            filedata=f.read(1024)
            if filedata:
                clientsocket.send(filedata)
            else:
                tk.messagebox.showinfo('提示','发送完毕')    
                break
    clientsocket.close()


phonejpg = Image.open("phone.jpg")
phonejpg = phonejpg.resize((30,30))
phonejpg = ImageTk.PhotoImage(phonejpg)
#phjpg = tk.PhotoImage(file=phonejpg)
phonebutton=tk.Button(image=phonejpg,command=make_a_call)
phonebutton.pack()

serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1',4097))
serversocket.listen(1)
while True:
    sock,addr =serversocket.accept()
    pick_up_or_not=tk.messagebox.askyesno('收到IP：'+addr+'的一条语音','您现在要收听吗？')
    if pick_up_or_not == True:
        #接电话
        with open('encryptedfrom1.amr',wb) as w:
            while True:
                filedata = serversocket.recv(1024)
                if filedata:
                    w.write(filedata)
                else :
                    break
        with open('encryptedfrom1.amr','rb') as f:
            amr=f.read()
        with open('decryptfrom2.amr','wb') as e:
            e.write(decrypt(amr,'123456789'))
        sound = AudioSegment.from_file('decryptfrom2.amr', format='amr')
        #play(sound)
        sound.export('decryptfrom2.wav', format='wav')
        play(sound)
        #pass  
    else:    
        #存下来
        with open('encryptedfrom1.amr',wb) as w:
            while True:
                filedata = serversocket.recv(1024)
                if filedata:
                    w.write(filedata)
                else :
                    break
        with open('encryptedfrom1.amr','rb') as f:
            amr=f.read()
        with open('decryptfrom2.amr','wb') as e:
            e.write(decrypt(amr,'123456789'))
        sound = AudioSegment.from_file('decryptfrom2.amr', format='amr')
        #play(sound)
        sound.export('decryptfrom2.wav', format='wav')
        #pass




playjpg = Image.open("play.jpg")
playjpg = playjpg.resize((30,30))
playjpg = ImageTk.PhotoImage(playjpg)
#phjpg = tk.PhotoImage(file=playjpg)
def playaudio():
    sound = AudioSegment.from_file('decryptfrom2.wav', format='wav')
    play(sound)
    
playbutton=tk.Button(image=playjpg,command=playaudio)
playbutton.pack()

window.mainloop()


/*'''serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1',4097))
serversocket.listen(1)
while True:
    sock,addr =serversocket.accept()
    pick_up_or_not=tk.messagebox.askyesno('收到IP：'+addr+'的一条语音','您现在要收听吗？')
    if pick_up_or_not == True:
        #接电话
        with open('encryptedfrom1.amr',wb) as w:
            while True:
                filedata = serversocket.recv(1024)
                if filedata:
                    w.write(filedata)
                else :
                    break
        with open('encryptedfrom1.amr','rb') as f:
            amr=f.read()
        with open('decryptfrom2.amr','wb') as e:
            e.write(decrypt(amr,'123456789'))
        sound = AudioSegment.from_file('decryptfrom2.amr', format='amr')
        #play(sound)
        sound.export('decryptfrom2.wav', format='wav')
        play(sound)
        #pass  
    else:    
        #存下来
        with open('encryptedfrom1.amr',wb) as w:
            while True:
                filedata = serversocket.recv(1024)
                if filedata:
                    w.write(filedata)
                else :
                    break
        with open('encryptedfrom1.amr','rb') as f:
            amr=f.read()
        with open('decryptfrom2.amr','wb') as e:
            e.write(decrypt(amr,'123456789'))
        sound = AudioSegment.from_file('decryptfrom2.amr', format='amr')
        #play(sound)
        sound.export('decryptfrom2.wav', format='wav')
        #pass 
     '''   