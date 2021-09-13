import Model
from pygame import mixer
from tkinter import filedialog
import os
from mutagen.mp3 import MP3

class Player:
    def __init__(self):
        mixer.init()
        self.my_model=Model.Model()

    def get_db_status(self):
        return self.my_model.get_db_status()

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_db_connection()

    def set_volume(self,volume_level):
        mixer.music.set_volume(volume_level)

    def add_song(self):
        song_path=filedialog.askopenfilename(title="Select your song......",filetype=[("mp3 files","*.mp3")],multiple=True)
        # if song_path[0]=="":
        #     return
        if len(song_path)==0:
            return
        song_name_list=[]
        for path in song_path:
            song_name=os.path.basename(path)
            self.my_model.add_song(song_name,path)
            song_name_list.append(song_name)
        return song_name_list


    def remove_song(self,song_name):
        self.my_model.remove_song(song_name)

    def get_song_length(self,song_name):
        self.song_path=self.my_model.get_song_path(song_name)
        self.audio_tag=MP3(self.song_path)
        song_length=self.audio_tag.info.length
        return song_length

    def stop_song(self):
        mixer.music.stop()

    def play_song(self):
        mixer.quit()
        mixer.init(frequency=self.audio_tag.info.sample_rate)
        mixer.music.load(self.song_path)
        #mixer.music.set_pos(self.val*1000)
        mixer.music.play(1,int(self.val))

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

    def add_song_to_favourites(self,song_name):
        song_path = self.my_model.get_song_path(song_name)
        result=self.my_model.add_song_to_favourites(song_name,song_path)
        return result

    def load_songs_from_favourites(self):
        result=self.my_model.load_songs_from_favourites()
        return result,self.my_model.song_dict


    def remove_songs_from_favourites(self,song_name):
        result=self.my_model.remove_songs_from_favourites(song_name)
        return result

    def get_song_count(self):
        return self.my_model.get_song_count()


    def set_skipped(self,val):
        self.val=val








