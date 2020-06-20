import spotipy
import config
import spotipy.util as util
import time
import lyricsgenius
import os 
import tkinter as tk
from tkinter.font import Font
# from tkinter import ttk
# from tkinter import*


genius = lyricsgenius.Genius(config.genius_api)
genius.verbose = False
scope = 'user-read-currently-playing'
token = util.prompt_for_user_token(config.Spotify_user, scope, client_id=config.client_id,
                                   client_secret=config.client_secret_id, redirect_uri='http://www.google.com/')
spotify = spotipy.Spotify(auth=token)
current_track = spotify.current_user_playing_track()


class SpotifyLyricsCLASS:
    def __init__(self,rooter):
        #pass the root variable for tkinter through the class
        self.rooter = rooter

        #get the info of the song 
        self.URI = str(current_track['item']['id'])
        self.artist = str(current_track['item']['artists'][0]['name'])
        self.song_name = str(current_track['item']['name'])
        self.song = genius.search_song('{} {}'.format(self.artist, self.song_name))
        self.song.lyrics1 = self.song.lyrics

        # set up the scrollbar for the Text 
        self.scroller = tk.Scrollbar(rooter)
        self.scroller.pack(side= tk.RIGHT, fill = "y")
        
        self.txtBox = tk.Text(self.rooter, height = 900, width = 500, yscrollcommand = self.scroller.set)
        self.txtBox.pack(expand = 0, fill = tk.BOTH)
        self.txtBox.insert(tk.END, self.song.lyrics1)
        self.default_font = Font(family = "Arial", size = 15)
        self.scroller.config(command = self.txtBox.yview)
        self.txtBox.configure(state = "disabled", font = self.default_font, bg = "#2B2D2F", fg = "#ffffff")
        #check to see if there is a new song being listened to 
        self.txtBox.after(5000,self.update_lyrics)
   

    def update_lyrics(self):
        #get the current song being listened to 
        current_track2 = spotify.current_user_playing_track()

        #obtain the new info for that track 
        URI = str(current_track2['item']['id'])
        artist = str(current_track2['item']['artists'][0]['name'])
        song_name = str(current_track2['item']['name'])
        song2 = genius.search_song('{} {}'.format(artist, song_name))

        #If the song's URI does not match the old song's URI, update the song
        if(self.URI != URI):
            self.URI = URI #update the old URI 
            self.song.lyrics1 = song2.lyrics #update the old songs lyrics

            #To change the Text tkinder widget, we most change state to normal
            self.txtBox.configure(state = "normal")
            #delete the text that was from the previous song
            self.txtBox.delete("1.0", tk.END)
            #insert the new song's lyrics
            self.txtBox.insert(tk.END, self.song.lyrics1)
            #change the state back to disabled so you cannot edit the lyrics 
            self.txtBox.configure(state = "disabled")
            #update the window to reflect the changes being made
            self.rooter.update()
        #continue to check for new songs every 5 seconds
        self.txtBox.after(5000,self.update_lyrics)
            
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x1400")
    root.configure(bg = "Gray")
    boop = SpotifyLyricsCLASS(root)
    root.title("Spotify Lyrics")
    root.mainloop()
