# Modules
import json,os
from flask import Flask,request,render_template,send_from_directory
from videoprops import get_audio_properties

# Variables
MOVIE_PATH = "./movies"
image_extensions = [".jpg",".png",".jpeg",".gif"]
movie_extension = [".avi",".mp4",".mkv",".mov"]
codecs = ["aac","mp3"]
dir_files = {}
files = {}

# Create a dictionary for all the movies
def search():
  for i in os.listdir(MOVIE_PATH):
    path_to_movie = f"{MOVIE_PATH}/{i}"
    dir_files = {}
    # Making title
    title = i
    title = title.replace("_"," ")
    title = title.title()
    if os.path.isdir(path_to_movie):
      for f in os.listdir(path_to_movie):
        # Checking for bg image
        ext = '.' + os.path.realpath(f).split('.')[-1:][0]
        if ext in image_extensions:
          dir_files["img"] = f"{path_to_movie}/{f}"
        # Checking for movie file
        if ext in movie_extension:
          props = get_audio_properties(f"{path_to_movie}/{f}")
          if props["codec_name"] not in codecs:
            print(f"{f} has a bad audio codec")
            convert_audio_codec(f"{path_to_movie}/{f}",f"{path_to_movie}/n_{f}","mp3")
          dir_files["movie"] = f"{path_to_movie}/{f}"
        dir_files["title"] = title
      files[path_to_movie] = dir_files

# Adding HTML accepted audio codecs to audio (FFMPEG is a must)
def convert_audio_codec(input_file,output_file,new_codec):
  print(f"Adding {new_codec} audio codec to movie file...")
  os.system(f"ffmpeg -i {input_file} -acodec {new_codec} -vcodec copy {output_file}")
  os.remove(input_file)
  main()

# Flask app
app = Flask(__name__)
app.debug = True

# Main page
@app.route("/")
def main():
  search()
  return render_template("index.html", data=json.dumps(files))

# To be able to get files from different directories
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route("/movies/<path:path>")
def movies_dir(path):
    return send_from_directory("movies", path)

# Start the server
if __name__ == "__main__":
    app.run(host="0.0.0.0")
