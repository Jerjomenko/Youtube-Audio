import youtube_dl
import os
import shutil
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooser

Window.size = (500, 700)


KV = """

MDScreen:
    md_bg_color: 54/255, 176/255, 166/255, .32
    FloatLayout:
        canvas:
            Color:
                rgba: 54/255, 176/255, 166/255, .32
            Rectangle:
                source: "img/shad.jpg"
                size: self.size
                pos: self.pos
                
        MDIconButton:
            icon: "youtube"
            user_font_size: "150sp"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .85}
            theme_text_color: "Custom"
            text_color: 1, 0, 0, 1
            
        MDLabel:
            text: "YouTube Downloader"
            pos_hint: {"center_x": .5, "center_y": .67}
            font_size: "40sp"
            line_height: .85
            halign: "center"
            bold: True

        MDLabel:
            id: label
            text: "paste video url"
            pos_hint: {"center_x": .5, "center_y": .57}
            font_size: "30sp"
            line_height: .85
            halign: "center"
            
        MDTextFieldRect:
            id: inp
            size_hint: .9, None
            height: "30sp"
            pos_hint: {"center_x": .5, "center_y": .47}
            multiline: False
            
        MDRaisedButton:
            text: "download mp3"
            size_hint: .3, .07
            pos_hint: {"center_x": .5, "center_y": .37}
            elevation: 20
            on_press: app.grab_audio()

"""


class Yt_Audio(MDApp):

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.get_path()


    def get_path(self):
        curr_path = os.getcwd()
        print(curr_path)
        tree = curr_path.split("\\")
        if tree[0] == "":
            tree = tree[1:]
        print(tree)
        load_location = " ".join(tree[:-2]).replace(" ", "\\")
        print(load_location)
        name = "\\Youtube_Musik"
        os.chdir(load_location)
        path = load_location + name
        try:
            if not os.path.lexists(path):
                os.mkdir(f"{path}")
        except OSError as errstr:
            print(f"Can't creat directory \n{errstr}")
        return path

    def find_file(self, filename):
        c_path = os.getcwd()
        for i in os.scandir(c_path):
            if i.is_file():
                if filename in i.name:
                    file = i.path
                    break
        return file

    def grab_audio(self):
        video_url = self.root.ids.inp.text
        video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
        filename = f"{video_info['title']}.mp3"
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename
        }
        print(filename)

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        first = self.find_file(filename)
        second = self.get_path()+f"\\{filename}"
        print("******************")
        print(first)
        print(second)


        try:
            os.replace(first, second)
        except:
            print("Can't load audio file on this device.")

        #os.chdir(self.get_path()[1])


        self.root.ids.label.text = "Audiofile Downloaded Succesfulll!!!"
        self.root.ids.inp.text = ""



if __name__ == "__main__":
    Yt_Audio().run()