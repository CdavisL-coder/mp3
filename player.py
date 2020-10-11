from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("700x600")

#initialize pygame
pygame.mixer.init()

#create function to deal with time
def play_time():
	#check to see if song is stopped
	if stopped:
		return
	#grab current song time
	current_time = pygame.mixer.music.get_pos() / 1000

	#convert current song time to standard time formatting
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	#Allows app to find file in directory
	song = playlist_box.get(ACTIVE)
	song = f"C:/mp3/audio/{song}.mp3"

	#find current song length
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length

	#convert to time format
	converted_song_length = time.strftime('%M:%S', time.
		gmtime(song_length))

	#check to see if song is over
	if int(song_slider.get()) == int(song_length):
		stop()
	elif paused:
		#check to see if song is paused
		pass
	else: 
		#move slider 1 second at a time
		next_time = int(song_slider.get()) + 1
		#output new time to song slider and to length of song
		song_slider.config(to=song_length, value=next_time)

		#convert slider position to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

	#add current time to status bar
	if current_time > 0:
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

	#create loop to check the time every second
	status_bar.after(1000, play_time)

#create function to add song to playlist
def add_song():
	song = filedialog.askopenfilename(initialdir='c:/mp3/audio/', title="Choose A Song")

	#Strip directory info
	song = song.replace("C:/mp3/audio/", "")
	song = song.replace(".mp3", "")

	#Add to end of playlist
	playlist_box.insert(END, song)

#create function to add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='c:/mp3/audio/', title="Choose A Song")

	#loop through song list and replace directory info
	for song in songs:
		#Strip directory info
		song = song.replace("C:/mp3/audio/", "")
		song = song.replace(".mp3", "")

		#Add to end of playlist
		playlist_box.insert(END, song)

#create function to delete song
def delete_song():
	#delete one song
	playlist_box.delete(ANCHOR)

#create function to delete all songs
def delete_all_songs():
	#delete all songs
	playlist_box.delete(0, END)

#create play function
def play():
	#set stopped to false since a song is now playing
	global stopped
	stopped = False
	#Allows app to find file in directory
	song = playlist_box.get(ACTIVE)
	song = f"C:/mp3/audio/{song}.mp3"

	#load with pygame mixer
	pygame.mixer.music.load(song)
	#play with pygame mixer
	pygame.mixer.music.play(loops=0)

	#get song time
	play_time()

#create stop var
global stopped
stopped = False
#create stop function
def stop():
	#stops song
	pygame.mixer.music.stop()

	#removes highlight from stopped song
	playlist_box.selection_clear(ACTIVE)

	#add current time to status bar
	status_bar.config(text='')

	#set our slider to zero
	song_slider.config(value=0)
	#set stop var to true
	global stopped
	stopped = True

#create next song function
def next_song():
	#reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	#get current song number
	next_one = playlist_box.curselection()

	#add one to the current song tuple
	next_one = next_one[0] + 1

	#grab the song title from playlist
	song = playlist_box.get(next_one)

	#add directory info
	song = f"C:/mp3/audio/{song}.mp3"

	#load with pygame mixer
	pygame.mixer.music.load(song)
	#play with pygame mixer
	pygame.mixer.music.play(loops=0)

	#removes highlight from stopped song
	playlist_box.selection_clear(0, END)

	#move active bar to next song
	playlist_box.activate(next_one)

	#set active bar to next song
	playlist_box.selection_set(next_one, last=None)

#create previous song function
def previous_song():
	#reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	#get current song number
	next_one = playlist_box.curselection()

	#add one to the current song tuple
	next_one = next_one[0] - 1

	#grab the song title from playlist
	song = playlist_box.get(next_one)
	#add directory info
	song = f"C:/mp3/audio/{song}.mp3"

	#load with pygame mixer
	pygame.mixer.music.load(song)
	#play with pygame mixer
	pygame.mixer.music.play(loops=0)

	#removes highlight from stopped song
	playlist_box.selection_clear(0, END)

	#move active bar to next song
	playlist_box.activate(next_one)

	#set active bar to next song
	playlist_box.selection_set(next_one, last=None)

#create paused variable
global paused
paused = False

#create pause function
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		#pause
		pygame.mixer.music.pause()
		paused = True

#create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#create song slider function
def slide(x):
		#Allows app to find file in directory
	song = playlist_box.get(ACTIVE)
	song = f"C:/mp3/audio/{song}.mp3"

	#load with pygame mixer
	pygame.mixer.music.load(song)
	#play with pygame mixer
	pygame.mixer.music.play(loops=0, start=song_slider.get())

#create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#create playlist box
playlist_box = Listbox(main_frame, bg="#0a2463", fg="#f9f9ef", width=60, selectbackground="#fed766", selectforeground="#247ba0")
playlist_box.grid(row=0, column=0)

#create volume slider frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

#create volume slider
volume_slider = ttk.Scale(volume_frame, value=0.5, from_=1, to=0, orient=VERTICAL, length=125, command=volume)
volume_slider.pack(pady=10)

#create song slider
song_slider = ttk.Scale(main_frame, value=0, from_=0, to=100, orient=HORIZONTAL, length=359, command=slide)
song_slider.grid(row=2, column=0, pady=20)

#create button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

#define button images
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

#create play/stop buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#create song menu drop down
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#add one song
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
#add many songs
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

#create delete songs from menu dropdowns
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

#create status bar
status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#temporary label
my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()