from cx_Oracle import *
from traceback import *
from tkinter import simpledialog, messagebox

class Model:
    def __init__(self):
        self.song_dict={}
        self.db_status=True
        self.conn=None
        self.cur=None
        try:
            self.conn=connect("mouzikka/music@127.0.0.1/xe")
            print("Connected Successfully to the DB")
            self.cur=self.conn.cursor()
        except DatabaseError:
            self.db_status=False
            print("DB Error!",format_exc())

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Curson closed")
        if self.conn is not None:
            self.conn.close()
            print("Connection closed")

    def add_song(self,song_name,song_path):
        self.song_dict[song_name] = song_path
        print("Song Added:",self.song_dict[song_name])

    def get_song_path(self,song_name):
        return self.song_dict[song_name]

    def remove_song(self,song_name):
        self.song_dict.pop(song_name)
        print("After deletion:",self.song_dict)

    def search_song_in_favourites(self,song_name):
        self.cur.execute("select song_name from myfavourites where song_name=:1",(song_name,))
        song_tuple=self.cur.fetchone()
        if song_tuple is None:
            return False
        return True

    def add_song_to_favourites(self,song_name,song_path):
        is_song_present=self.search_song_in_favourites(song_name)
        if is_song_present==True:
            return "Song already present in favourites"
        self.cur.execute("select max(song_id) from myfavourites")
        last_song_id=self.cur.fetchone()[0]
        next_song_id=1
        if last_song_id is not None:
            next_song_id=last_song_id+1  #return writted here
        self.cur.execute("insert into myfavourites values(:1,:2,:3)",(next_song_id,song_name,song_path))
        self.conn.commit()
        return "Song successfully added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name, song_path from myfavourites")
        song_present=False
        for song_name,song_path in self.cur:
            self.song_dict[song_name]=song_path
            song_present=True
        if song_present:
            return "List populated from favourites"
        return "No songs present in your favourites"

    def remove_songs_from_favourites(self,song_name):
        self.cur.execute("delete from myfavourites where song_name=:1",(song_name,))
        count=self.cur.rowcount
        if count==0:
            return "Song not present in the favourites"
        else:
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "Song deleted from your favourites"

    def get_song_count(self):
        return len(self.song_dict)
















