import tkinter.messagebox
import os
import time
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
from pygame import mixer
from mutagen.mp3 import MP3


root = ThemedTk(theme="breeze")
paused = False
filename = None

mixer.init()

root.title("mp3 play")
root.geometry("600x300")
root.iconbitmap("images/music_note_Arx_icon.ico")


def browser_file():
    global filename
    filename = filedialog.askopenfilename()
    add_to_playlist(filename)


playlist = []
def add_to_playlist(f):
    _filename = os.path.basename(f)
    index = 0
    playlistBox.insert(index, _filename)
    playlist.insert(index, f)


def about_us():
    tkinter.messagebox.showinfo("About us", "Github: github.com/NguyenDuyCong \nFacebook: facebook.com/TaiTuLangQuen \nGmail: duycong.cn@gmail.com")

def start_count(t):
    global paused
    x = 0
    while x <= t and mixer.music.get_busy():
        if paused:
            continue
        mins, secs = divmod(x, 60)
        mins = round(mins)
        secs = round(secs)
        timeFormat = "{:02d}:{:02d}".format(mins, secs)
        currentTimeLabel["text"] = "Current time - " + timeFormat
        time.sleep(1) 
        x += 1


def show_detail():
    # filenameLable["text"] = "Playing - " + os.path.basename(filename)
    filetype = os.path.splitext(filename)
    print(filetype)
    try:
        if filetype[1] == ".mp3":
            audio = MP3(filename)
            total_length = audio.info.length
        else:
            audio = mixer.Sound(filename)
            total_length = audio.get_length()
        
        # print(total_length)
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)

        timeFormat = "{:02d}:{:02d}".format(mins, secs)
        lengthLabel["text"] = "Total length - " + timeFormat 

        t1 = threading.Thread(target=start_count, args=(total_length,))
        t1.start()
        # start_count(total_length)
    except:
        messagebox.showwarning("Format Error", "Không hỗ trợ mở file của m rồi :))")
 

def play_music():
    global paused
    if paused == True:
        mixer.music.unpause()
        statusbar["text"] = "Resumed song"
        paused = False
    else:        
        try:
            stop_music()
            index_song = playlistBox.curselection()
            index_song = index_song[0]

            selected_song = playlist[index_song]
            
            mixer.music.load(selected_song)
            mixer.music.play()
            statusbar["text"] = "Playing song - " + os.path.basename(selected_song)
            show_detail()
        except:
            tkinter.messagebox.showerror("ngu người", "Chọn bài hát đi tml")


def stop_music():
    mixer.music.stop()
    statusbar["text"] = "Stopped song"


def pause_music():
    global paused 
    paused = True
    mixer.music.pause()
    statusbar["text"] = "Paused song"


def set_vol(value):
    volume = float(value)/100
    mixer.music.set_volume(volume)


def rewind_music():
    global paused
    paused = False
    play_music()
    statusbar["text"] = "Rewinded song"


mute = False
vol = 70
def mute_music():
    global mute
    global vol
    if mute:
        mixer.music.set_volume(vol)
        volumeBtn.configure(image=volumePhoto)
        scale.set(vol)
        mute = False
    else:
        vol = scale.get()
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        mute = True


def on_closing():
    # messagebox.showerror("error", "Do you really want to exit this app ?")
    stop_music()
    root.destroy()


def del_song():
    index_song = playlistBox.curselection()
    index_song = index_song[0]
    playlistBox.delete(index_song)
    playlist.pop(index_song)
    print(playlist)


# status bar
statusbar = ttk.Label(root, text="Welcome to MP3PLAY", relief=SUNKEN, anchor=W, font="Times 10 italic")
statusbar.pack(side=BOTTOM, fill=X, )

# left frame
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=20)

# right frame
rightframe = Frame(root)
rightframe.pack()

topframeR = Frame(rightframe)
topframeR.pack(pady=10)

middleframeR = Frame(rightframe)
middleframeR.pack(pady=20)


# label text
# filenameLable = Label(topframeR, text="Let play with own songs!")
# filenameLable.pack(pady=5)

lengthLabel = ttk.Label(topframeR, text="Total lenght - 00:00", font="verdana 10")
lengthLabel.pack()

currentTimeLabel = ttk.Label(topframeR, text="Current time - 00:00", font="verdana 10")
currentTimeLabel.pack()

# playlist box
playlistBox = Listbox(leftframe, bg='white')
playlistBox.pack()

# buttons left frame
addBtn = ttk.Button(leftframe, text="+ Add", command=browser_file)
addBtn.pack(side=LEFT)
delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack()

# menubar
menubar = Menu(root)
root.config(menu=menubar)

#sub menu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browser_file)
subMenu.add_command(label="Exit", command=root.destroy)

# about us
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About us", command=about_us)

# photos
playPhoto = PhotoImage(file="images/play-button.png")
pausePhoto = PhotoImage(file="images/pause.png")
stopPhoto = PhotoImage(file="images/stop.png")
rewindPhoto = PhotoImage(file="images/rewind.png")
mutePhoto = PhotoImage(file="images/mute.png")
volumePhoto = PhotoImage(file="images/volume.png")

# buttons
playBtn = ttk.Button(middleframeR, image=playPhoto, command=play_music)
playBtn.pack(side=LEFT, padx=5)

stopBtn = ttk.Button(middleframeR, image=stopPhoto, command=stop_music)
stopBtn.pack(side=LEFT, padx=5)

pauseBtn = ttk.Button(middleframeR, image=pausePhoto, command=pause_music)
pauseBtn.pack(side=LEFT, padx=5)

# bottom frame
bottomframe = Frame(root)
bottomframe.pack(padx=10, pady=15)


# rewind button
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.pack(side=LEFT, padx=5)

# mute button
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.pack(side=LEFT, padx=5)

# scale volume
scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.pack(side=LEFT, padx=5)
scale.set(70)
mixer.music.set_volume(0.7)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# a = mixer.Sound("piano.wav")
# print(a.get_length())