"""
██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗
██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗
██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║
██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║
╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
"""


import threading
import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, ttk
import os
import yt_dlp
import datetime
import threading
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, APIC



"""
    ███╗   ███╗██████╗ ██████╗     ███████╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
    ████╗ ████║██╔══██╗╚════██╗    ██╔════╝██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
    ██╔████╔██║██████╔╝ █████╔╝    ███████╗█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║
    ██║╚██╔╝██║██╔═══╝  ╚═══██╗    ╚════██║██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║
██╗ ██║ ╚═╝ ██║██║     ██████╔╝    ███████║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝ ╚═╝     ╚═╝╚═╝     ╚═════╝     ╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""




def mp3Process(url, dirPath, num, priorDir):    
    ydl_opts = {
        'outtmpl': f'{dirPath}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',  # Download best audio quality
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # You can adjust the audio quality here (e.g., 128, 192, 256, 320)
        }],
        'writethumbnail': True,
        'writeinfojson': True,
        'writesubtitles': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Download the video, thumbnail, and description
        info = ydl.extract_info(url, download=True)
        cleanedTitle = info['title'].replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')

        files = os.listdir(dirPath)
        for fileName in files:
            newFileName = fileName.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')
            # Get the full paths of the old and new file names
            old_file_path = f"{dirPath}/{fileName}"
            new_file_path = f"{dirPath}/{newFileName}"
            # Rename the file with underscores in its name
            os.rename(old_file_path, new_file_path)

        # Load the downloaded .webp thumbnail image
        thumbnailPath = f"{dirPath}/{cleanedTitle}.webp"
        thumbnail = Image.open(thumbnailPath)


        

        # Calculate cropping dimensions to create a square centered image
        width, height = thumbnail.size
        cropSize = min(width, height)

        # Crop the image
        croppedThumbnail = thumbnail.crop((((width - cropSize) // 2), ((height - cropSize) // 2), ((width + cropSize) // 2), ((height + cropSize) // 2)))

        # Save the cropped thumbnail back as .webp format
        croppedThumbnail.save(thumbnailPath, format='WebP')  

        # Convert WebP to PNG
        webp_image = Image.open(thumbnailPath)
        thumbnailPath = f"{dirPath}/{cleanedTitle}.png"
        webp_image.save(thumbnailPath, 'PNG')
        os.remove(f"{dirPath}/{cleanedTitle}.webp")

        # Print video information
        #print(f"Video Title: {info['title']}")
        #print(f"Cropped Thumbnail Path: {thumbnailPath}")
        #print(f"Description: {info['description']}")

        # Attach image to the .mp3 file
        mp3Path = f"{dirPath}/{cleanedTitle}.mp3"
        audio = MP3(mp3Path, ID3=ID3)
        with open(thumbnailPath, "rb") as imageFile:
            artwork = imageFile.read()
            audio_tags = audio.tags
            if not audio_tags:
                audio_tags = ID3()
                audio.tags = audio_tags
            audio_tags.add(
                APIC(
                    encoding=3,  # utf-8
                    mime='image/png',
                    type=3,  # Cover (front) image
                    desc=u'Cover',
                    data=artwork
                )
            )
            audio.save()
            #print("Added artwork to", mp3Path)

        description = info['description'].split("\n")

        title = description[2].strip().split(' · ')[0].strip()
        artists = [a.strip() for a in description[2].strip().split(' · ')[1:]]
        artist_str = ', '.join(artists)
        audio['TIT2'] = TIT2(encoding=3, text=title)
        audio['TPE1'] = TPE1(encoding=3, text=artist_str)


        album = description[4].strip()
        audio['TALB'] = TALB(encoding=3, text=album)


        date = description[8].strip()

        if date.startswith('Released on: '):
            date = date.replace('Released on: ', '')
            releaseObj = datetime.datetime.strptime(date, '%Y-%m-%d')
            audio['TDRC'] = TDRC(encoding=3, text=releaseObj.strftime('%Y-%m-%d'))

        audio.save(mp3Path)

        os.remove(thumbnailPath)
        os.remove(f"{dirPath}/{cleanedTitle}.info.json")

        artists = audio.get('TPE1', ['Unknown Artist'])
        artist = next((a for a in artists if a.startswith('Earth, Wind & Fire')), artists[0]).split(',')[0]
        artist = artist.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

        try:
            os.rename(mp3Path, f"{dirPath}/{artist} - {cleanedTitle}.mp3")
            oldDir = (f"{dirPath}/{artist} - {cleanedTitle}.mp3")
            newDir = (f"{priorDir}/{artist} - {cleanedTitle}.mp3")
            os.rename(oldDir, newDir)
        except Exception as e:
            print(f"Could not rename {info['title']}. Error: {str(e)}. Trying again...")
            os.rename(mp3Path, f"{dirPath}/({num}){artist} - {cleanedTitle}.mp3")
            oldDir = (f"{dirPath}/({num}){artist} - {cleanedTitle}.mp3")
            newDir = (f"{priorDir}/({num}){artist} - {cleanedTitle}.mp3")
            os.rename(oldDir, newDir)



        

    print("Download completed successfully.")


def filterPlaylistMp3(urls, dirPath, progress_var, index):
    progress_var.set(0)
    incr = (100/(len(urls)))*index
    count = 1

    if index <= 0:
        return "Number of lists should be greater than 0"
    else:
        # Calculate the number of elements in each sublist
        sublist_size = len(urls) // index
        remainder = len(urls) % index

        # Create empty sublists
        sublists = [[] for _ in range(index)]

        # Split the input list into sublists
        start_index = 0
        for i in range(index):
            sublist_end = start_index + sublist_size + (1 if i < remainder else 0)
            sublists[i] = urls[start_index:sublist_end]
            start_index = sublist_end

        threads = []
        for sublist in sublists:
            subdir = dirPath+ "/" + "set" + str(sublists.index(sublist))
            os.makedirs(subdir, exist_ok=True)
            thread = threading.Thread(target=startDownloadMp3, args=(sublist, subdir, count, progress_var, incr, dirPath))
            threads.append(thread)
            thread.start()
        # Wait for all threads to finish
        for thread in threads:
            thread.join()



def startDownloadMp3(urls, dirPath, count, progress_var, incr, priorDir):
    for url in urls:
        progress_var.set(incr*count)
        mp3Process(url, dirPath, count, priorDir)
        count += 1
    os.chmod(dirPath, 0o777)
    os.rmdir(dirPath)





























def filterPlaylistFlac():
    pass







"""
███╗   ███╗ █████╗ ██╗███╗   ██╗    ██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗
████╗ ████║██╔══██╗██║████╗  ██║    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
██╔████╔██║███████║██║██╔██╗ ██║    ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║
██║╚██╔╝██║██╔══██║██║██║╚██╗██║    ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
██║ ╚═╝ ██║██║  ██║██║██║ ╚████║    ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
"""

def extractURLs(playlistUrl):
    # Replace 'PLAYLIST_URL' with the URL of the playlist you want to extract URLs from

    # Set up yt-dlp options
    ydl_opts = {
        'quiet': True,  # Suppress yt-dlp output
        'extract_flat': True,  # Extract only top-level URLs from the playlist
        'get_url': True,  # Get direct URLs to the videos
    }

    # Extract URLs from the playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlistUrl, download=False)
        playlist_videos = playlist_info.get('entries', [])

        # Filter out duplicate URLs
        unique_urls = set()
        for video in playlist_videos:
            if video and 'url' in video:
                unique_urls.add(video['url'])

    # Store unique URLs in the 'URLs' variable
    URLs = list(unique_urls)
    return URLs

"""    # Print the extracted URLs (optional)
    print("Extracted URLs from the playlist:")
    for url in URLs:
        print(url)"""

# Event handler for dropdown selection
def actionDropdownSelect(event):
    global dropdownOption
    selected_option.set(event.widget.get())
    dropdownOption = selected_option.get()

# Event handler for checkbox changes
def ActionCheckboxChange():
    global checkboxStates
    checkboxStates = [checkbox1_var.get(), checkbox2_var.get(), checkbox3_var.get(), checkbox4_var.get()]

# Function to open file explorer to select directory
def selectDir():
    directory = filedialog.askdirectory()
    directoryBox.delete(0, tk.END)  # Clear previous entry
    directoryBox.insert(0, directory)

# Function to update progress bar
def updateProgress(value):
    current_value = progress_bar["value"]
    if current_value < value * 10:
        progress_bar["value"] = current_value + 1
        mainframe.after(10, updateProgress, value)


# Function to start download process in a separate thread
def startDownload():
    directory_path = directoryBox.get()
    url_link = urlBox.get()     

    progress_var = tk.DoubleVar()
    progress_bar.configure(variable=progress_var)
    progress_var.set(0)
    
    urls = extractURLs(url_link)
    index = 64

    # Create a separate thread to execute the download process
    if dropdownOption == '.mp3':
        download_thread = threading.Thread(target=filterPlaylistMp3, args=(urls, directory_path, progress_var, index))
        download_thread.start()
    elif dropdownOption == '.flac':
        download_thread = threading.Thread(target=filterPlaylistFlac, args=(urls, directory_path, progress_var, index))
        download_thread.start()


# Main application window
mainframe = tk.Tk()
mainframe.geometry("800x450")
mainframe.resizable(False, False)
mainframe.title("YTPFLACU")

# Global variables
checkboxStates = [True, True, True, True]
dropdownOption = ''

# Assigns all of the values for the grid. 'i' is the width, 16, and 'j' is the height, 9.
style = ttk.Style()
style.configure('CustomFrame.TFrame', background='black', relief='solid', borderwidth=1)
frames = {(i, j): ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame') for i in range(16) for j in range(9)}
for i, j in frames:
    frames[i, j].grid(row=j, column=i)

# Widgets and UI elements
titleLabel = tk.Label(mainframe, text="YouTube Playlist to .flac Utility (YTPFLACU)", font=("MS Sans Serif", 22, 'bold'))
titleLabel.grid(row=0, column=2, columnspan=12, rowspan=2)

style = ttk.Style()
style.configure("Horizontal.TSeparator", background="green")
horizontalSeparator = ttk.Separator(mainframe, orient='horizontal', style="Horizontal.TSeparator")
horizontalSeparator.grid(row=1, column=1, columnspan=14, rowspan=2, sticky='ew')

style = ttk.Style()
style.configure("Vertical.TSeparator", background="green")
verticalSeparator = ttk.Separator(mainframe, orient='vertical', style="Vertical.TSeparator")
verticalSeparator.grid(row=2, column=7, columnspan=2, rowspan=6, sticky='ns')

urlLabel = ttk.Label(mainframe, text="Playlist URL:", font=("MS Sans Serif", 11))
urlLabel.grid(row=2, column=0, columnspan=3)
urlBox = ttk.Entry(mainframe, width=40)
urlBox.grid(row=2, column=2, columnspan=6)

directoryLabel = ttk.Label(mainframe, text="Output directory:", font=("MS Sans Serif", 11))
directoryLabel.grid(row=3, column=0, columnspan=3)
directoryButton = ttk.Button(mainframe, text="Select through Explorer", command=selectDir)
directoryButton.grid(row=4, column=2, columnspan=6)
directoryBox = ttk.Entry(mainframe, width=37)
directoryBox.grid(row=3, column=2, columnspan=6)

selected_option = tk.StringVar()    
dropdown_label = ttk.Label(mainframe, text="Select a file type:", font=("MS Sans Serif", 11))
dropdown_label.grid(row=5, column=0, columnspan=3)

options = [".mp3", ".flac"]
dropdown = ttk.Combobox(mainframe, textvariable=selected_option, values=options)
dropdown.grid(row=5, column=2, columnspan=6)
dropdown.bind("<<ComboboxSelected>>", actionDropdownSelect)

checkbox_values = [tk.BooleanVar() for _ in range(4)]
checkbox_frame = ttk.Frame(mainframe)
checkbox_frame.grid(row=6, column=2, columnspan=6, rowspan=2)

checkbox_label = ttk.Label(mainframe, text="Select what you want:", font=("MS Sans Serif", 11))
checkbox_label.grid(row=6, column=0, columnspan=3, rowspan=2)

checkbox1_var = tk.BooleanVar()
checkbox1 = ttk.Checkbutton(checkbox_frame, text="Checkbox 1", variable=checkbox1_var, command=ActionCheckboxChange)
checkbox1.grid(row=0, column=0, padx=5, pady=5)

checkbox2_var = tk.BooleanVar()
checkbox2 = ttk.Checkbutton(checkbox_frame, text="Checkbox 2", variable=checkbox2_var, command=ActionCheckboxChange)
checkbox2.grid(row=0, column=1, padx=5, pady=5)

checkbox3_var = tk.BooleanVar()
checkbox3 = ttk.Checkbutton(checkbox_frame, text="Checkbox 3", variable=checkbox3_var, command=ActionCheckboxChange)
checkbox3.grid(row=1, column=0, padx=5, pady=5)

checkbox4_var = tk.BooleanVar()
checkbox4 = ttk.Checkbutton(checkbox_frame, text="Checkbox 4", variable=checkbox4_var, command=ActionCheckboxChange)
checkbox4.grid(row=1, column=1, padx=5, pady=5)

# Start button event handler
start_button = ttk.Button(mainframe, text="Activate Program", command=startDownload)
start_button.grid(row=5, column=10, columnspan=4)

# Progress bar
progress_bar = ttk.Progressbar(mainframe, orient="horizontal", length=250, mode="determinate")
progress_bar.grid(row=4, column=9, columnspan=6)

# Run the application
if __name__ == '__main__':
    mainframe.mainloop()







































































































































































































































































































    """
    ███████╗██╗      █████╗  ██████╗    ███████╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
    ██╔════╝██║     ██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
    █████╗  ██║     ███████║██║         ███████╗█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══╝  ██║     ██╔══██║██║         ╚════██║██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║
██╗ ██║     ███████╗██║  ██║╚██████╗    ███████║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝ ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝




import json
import os
import re
import yt_dlp
import time
import logging
from collections import defaultdict
from moviepy.editor import VideoFileClip
from mutagen.flac import FLAC, Picture


def getPlaylistVideoUrls(playlistUrl):
    # Function to fetch video URLs from a YouTube playlist
    with yt_dlp.YoutubeDL({'extract_flat': 'in_playlist'}) as ydl:
        result = ydl.extract_info(playlistUrl, download=False)
        urls = [item['url'] for item in result['entries']]
        return urls

def addArtworkToFlacFiles(outputDir):
    # Function to add artwork to .flac files and delete image files
    for filename in os.listdir(outputDir):
        if filename.endswith(".flac"):
            flacFile = os.path.join(outputDir, filename)
            imageFile = os.path.join(outputDir, os.path.splitext(filename)[0] + ".png")
            try:
                audio = FLAC(flacFile)
                with open(imageFile, "rb") as f:
                    artwork = f.read()
                pic = Picture()
                pic.type = 3  # Cover (front) image
                pic.mime = 'image/png'
                pic.desc = "Cover"
                pic.data = artwork
                audio.clear_pictures()  # Remove existing pictures
                audio.add_picture(pic)
                audio.save()
                print("Added artwork to", flacFile)
            except Exception as e:
                print(f"Could not add artwork to {flacFile}. Error: {str(e)}")
            if imageFile.lower().endswith('.png'):
                os.remove(imageFile)

# Extracts metadata from .txt files and sets it as metadata tags for the corresponding .flac files in the output directory.
def setMusicMetadata(outputDir):
    # Function to set metadata for .flac files from .txt files
    for file in os.listdir(outputDir):
        if file.endswith('.flac'):
            with open(os.path.join(outputDir, file[:-5] + '.txt'), 'r', encoding='utf16') as f:
                # Extract title and artist metadata from the .txt file
                f.readline()
                f.readline()
                metadata = f.readline().strip().split(' · ')
                title = metadata[0].strip()
                artists = [a.strip() for a in metadata[1:]]
                artists_set = set(artists)
                artist_order = [artist for artist in artists if artist in artists_set]
                artist_str = ', '.join(artist_order)
            audio = FLAC(os.path.join(outputDir, file))
            audio['title'] = title
            audio['artist'] = artist_str
            audio.save()
            os.remove(os.path.join(outputDir, file[:-5] + '.txt'))

# Renames files with the artist name and removes illegal characters
def renameFlacFiles(outputDir):
    # Function to rename .flac files with artist names
    illegalCharsRegex = r'[\\/:*?"<>|]'
    flacFiles = [file for file in os.listdir(outputDir) if file.endswith('.flac')]
    for file in flacFiles:
        try:
            audio = FLAC(os.path.join(outputDir, file))
            artist = re.sub(illegalCharsRegex, '', audio.get('artist', ['Unknown'])[0].split(',')[0])
            oldFilename = os.path.join(outputDir, file)
            newFilename = os.path.join(outputDir, f"{artist} - {file}")
            os.rename(oldFilename, newFilename)
            print(f"Renamed {oldFilename} to {newFilename}")
        except:
            print(f"Failed to rename {file}")

def takeAlbumArt(outputDir):
    # Function to extract album art from .mp4 files
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp4") or filename.endswith(".webm"):
            input_file = os.path.join(outputDir, filename)
            output_file = os.path.join(outputDir, os.path.splitext(filename)[0] + ".png")
            clip = VideoFileClip(input_file)
            clip.save_frame(output_file, t=1)
            clip.close()

def replaceHashtagSymbol(outputDir):
    # Function to replace '#' with '.' in filenames
    for filename in os.listdir(outputDir):
        if "#" in filename:
            newFilename = filename.replace("#", ".")
            os.rename(os.path.join(outputDir, filename), os.path.join(outputDir, newFilename))

def deleteMp4File(outputDir):
    # Function to delete .mp4 files
    for filename in os.listdir(outputDir):
        if filename.endswith(".mp4"):
            mp4File = os.path.join(outputDir, filename)
            os.remove(mp4File)

def deleteIllegalChars(outputDir):
    # Function to delete illegal characters from .txt and .mp3 files
    illegalChars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for filename in os.listdir(outputDir):
        if filename.endswith('.flac') or filename.endswith('.txt'):
            newFilename = filename.translate({ord(char): None for char in illegalChars})
            newFilename = newFilename.replace('⧸', '').replace('／', '').replace('∕', '')
            newFilename = newFilename.replace('⧵', '').replace('∖', '').replace('＼', '')
            newFilename = newFilename.replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '')
            newFilename = newFilename.replace('＊', '').replace('⁎', '').replace('∗', '')
            newFilename = newFilename.replace('？', '')
            newFilename = newFilename.replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'')
            newFilename = newFilename.replace('＞', '').replace('﹥', '').replace('›', '')
            newFilename = newFilename.replace('＜', '').replace('﹤', '')
            newFilename = newFilename.replace('｜', '').replace('│', '').replace('|', '')
            newFilename = newFilename.replace('_','')
            newFilename = newFilename.replace('', '')
            if newFilename != filename:
                os.rename(os.path.join(outputDir, filename), os.path.join(outputDir, newFilename))

def checkPlaylistTitles(playlistUrl):
    # Function to check for duplicate titles in a playlist
    videoUrls = getPlaylistVideoUrls(playlistUrl)
    titles_to_urls = defaultdict(list)
    duplicates = []
    with yt_dlp.YoutubeDL() as ydl:
        for url in videoUrls:
            info = ydl.extract_info(url, download=False)
            title = info.get('title')
            normalized_title = title.lower()  # Convert title to lowercase
            titles_to_urls[normalized_title].append(url)
    for normalized_title, url_list in titles_to_urls.items():
        if len(url_list) > 1:
            duplicates.append((normalized_title, url_list))
    return duplicates

def playlistUrlClean(playlistUrl, outputDir, duplicates):
    full_video_urls = []
    # Set the options for the yt-dlp downloader
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]',
        'outtmpl': outputDir + '%(title)s.%(ext)s',
        'yes_playlist': True
    }

    # Download the videos and collect video URLs
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlistUrl, download=False)
        if 'entries' in result:
            for entry in result['entries']:
                full_video_urls.append(entry['webpage_url'])  # Use 'webpage_url' instead of 'url'
    
    # Remove duplicate video URLs based on the provided list of duplicates
    filtered_full_video_urls = []
    for url in full_video_urls:
        should_skip = any(duplicate_url in url for _, duplicate_url_list in duplicates for duplicate_url in duplicate_url_list)
        if not should_skip:
            filtered_full_video_urls.append(url)

    return filtered_full_video_urls

# Downloads all of the descriptions from the videos.
def downloadVideoDescriptions(videoUrls, outputDir):
    print("downloadVideoDescriptions")
    descriptionDict = {}
    descriptionsFile = os.path.join(outputDir, 'descriptions.json')
    if os.path.exists(descriptionsFile):
        # read description data from file if exists
        with open(descriptionsFile, 'r') as f:
            descriptionDict = json.load(f)
    else:
        # download descriptions from youtube-dl for new videos
        for url in videoUrls:
            # get the video title
            ydl = yt_dlp.YoutubeDL({'quiet': True})
            info_dict = ydl.extract_info(url, download=False)
            videoTitle = str(info_dict['title'])
            videoTitle = videoTitle.strip().replace('/','').replace('\\','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','')
            # create empty text file
            print(videoTitle)
            outputFilePath = os.path.join(outputDir, videoTitle + ".txt")
            with open(outputFilePath, "w") as f:
                pass
            if url in descriptionDict:
                # use description data from dictionary if exists
                videoDescription = descriptionDict[url]
            else:
                # download description data from youtube-dl for new video
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    videoDescription = str(info_dict['description'].strip())
                    # store the description data in the dictionary
                    descriptionDict[url] = videoDescription
                # store the description data in the dictionary
                descriptionDict[url] = videoDescription
            # write description to text file
            with open(outputFilePath, "w", encoding="utf16", errors="replace") as f:
                f.write(videoDescription.replace("\uFFFD", ""))
        # write the descriptions to file
        with open(descriptionsFile, 'w') as f:
            json.dump(descriptionDict, f)
    os.remove(os.path.join(outputDir, "descriptions.json"))

def downloadVideos(playlistUrl, outputDir, duplicates):
    try:
        full_video_urls = []
        
        # Set the options for the yt-dlp downloader
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]',
            'outtmpl': outputDir + '%(title)s.%(ext)s',
            'yes_playlist': True
        }
        
        # Download the videos and collect video URLs
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlistUrl, download=False)
            if 'entries' in result:
                for entry in result['entries']:
                    full_video_urls.append(entry['webpage_url'])  # Use 'webpage_url' instead of 'url'
        
        # Remove duplicate video URLs based on the provided list of duplicates
        filtered_full_video_urls = []
        for url in full_video_urls:
            should_skip = any(duplicate_url in url for _, duplicate_url_list in duplicates for duplicate_url in duplicate_url_list)
            if not should_skip:
                filtered_full_video_urls.append(url)
        
        # Download the remaining videos and audio files
        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': outputDir + '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'preferredquality': '0',
            }],
            'extractaudio': True,
            'audioformat': 'flac',
        }
        
        # Download remaining videos with retries and error handling
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
            retry_count = 3
            while retry_count > 0:
                try:
                    ydl_audio.download(filtered_full_video_urls)
                    break
                except Exception as e:
                    logging.error("An error occurred during audio download: %s", str(e))
                    logging.info("Retrying audio download...")
                    retry_count -= 1
                    time.sleep(5)  # Wait for 5 seconds before retrying
        
        # Download remaining videos with retries and error handling
        ydl_opts_remaining = {
            'format': 'best[ext=mp4]',
            'outtmpl': outputDir + '%(title)s.%(ext)s',
            'yes_playlist': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts_remaining) as ydl_remaining:
            retry_count = 3
            while retry_count > 0:
                try:
                    ydl_remaining.download(filtered_full_video_urls)
                    break
                except Exception as e:
                    logging.error("An error occurred during video download: %s", str(e))
                    logging.info("Retrying video download...")
                    retry_count -= 1
                    time.sleep(5)  # Wait for 5 seconds before retrying
        
        logging.info("Video download completed successfully.")
    except Exception as e:
        logging.error("An error occurred during video download process: %s", str(e))
        # You can choose to re-raise the exception if needed.

def downloadProcess(url, directory_path, progress_var, duplicates):
    try:
        logging.info("Starting downloadProcess for URL: %s", url)
        progress_var.set(0)
        # Step 1: Download videos
        logging.info("Step 1: Downloading videos")
        downloadVideos(url, directory_path, duplicates)
        progress_var.set(10)
        # Step 2: Clean playlist URLs
        logging.info("Step 2: Cleaning playlist URLs")
        urlLists = playlistUrlClean(url, directory_path, duplicates)
        progress_var.set(20)
        # Step 3: Download video descriptions
        logging.info("Step 3: Downloading video descriptions")
        downloadVideoDescriptions(urlLists, directory_path)
        progress_var.set(30)
        # Step 4: Take album art
        logging.info("Step 4: Taking album art")
        takeAlbumArt(directory_path)
        progress_var.set(40)
        # Step 5: Delete MP4 files
        logging.info("Step 5: Deleting MP4 files")
        deleteMp4File(directory_path)
        progress_var.set(50)
        # Step 6: Add artwork to FLAC files
        logging.info("Step 6: Adding artwork to FLAC files")
        addArtworkToFlacFiles(directory_path)
        progress_var.set(60)
        # Step 7: Replace hashtag symbols
        logging.info("Step 7: Replacing hashtag symbols")
        replaceHashtagSymbol(directory_path)
        progress_var.set(70)
        # Step 8: Delete illegal characters
        logging.info("Step 8: Deleting illegal characters")
        deleteIllegalChars(directory_path)
        progress_var.set(80)
        # Step 9: Set music metadata
        logging.info("Step 9: Setting music metadata")
        setMusicMetadata(directory_path)
        progress_var.set(90)
        # Step 10: Rename FLAC files
        logging.info("Step 10: Renaming FLAC files")
        renameFlacFiles(directory_path)
        progress_var.set(100)
        logging.info("downloadProcess completed successfully for URL: %s", url)
    except Exception as e:
        logging.error("An error occurred in downloadProcess for URL: %s - %s", url, str(e))
        # You can choose to re-raise the exception if needed.





def fetch_video_title(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', 'UnknownTitle')

def individualSongDownload(url_link, directory_path):
    urlLists = checkPlaylistTitles(url_link)
    dirPath = directory_path + "duplicates/"
    for normalized_title, url_list in urlLists:
        for url in url_list:
            # Download the audio and video files
            ydl_opts_audio = {
                'format': 'bestaudio/best',
                'outtmpl': dirPath + '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                    'preferredquality': '0',
                }],
                'extractaudio': True,
                'audioformat': 'flac',
            }

            ydl_opts_video = {
                'format': 'best[ext=mp4]',
                'outtmpl': dirPath + '%(title)s.%(ext)s',
                'yes_playlist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                ydl_audio.download([url])

            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl_video:
                ydl_video.download([url])



            # Download and store the video description
            descriptionsFile = os.path.join(dirPath, 'descriptions.json')
            descriptionDict = {}

            if os.path.exists(descriptionsFile):
                with open(descriptionsFile, 'r') as f:
                    descriptionDict = json.load(f)

            ydl = yt_dlp.YoutubeDL({'quiet': True})
            info_dict = ydl.extract_info(url, download=False)
            videoTitle = str(info_dict['title'])
            videoTitle = videoTitle.strip().replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

            outputFilePath = os.path.join(dirPath, videoTitle + ".txt")

            if url in descriptionDict:
                videoDescription = descriptionDict[url]
            else:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    videoDescription = str(info_dict['description'].strip())
                    descriptionDict[url] = videoDescription

            with open(outputFilePath, "w", encoding="utf16", errors="replace") as f:
                f.write(videoDescription.replace("\uFFFD", ""))

            with open(descriptionsFile, 'w') as f:
                json.dump(descriptionDict, f)

            os.remove(os.path.join(dirPath, "descriptions.json"))



            takeAlbumArt(dirPath)    
            deleteMp4File(dirPath)


            filename = dirPath + normalized_title.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

            filenameFlac = filename+".flac"

            print("-"*30)
            print(filename)
            print("-"*30)
            for files in os.listdir(dirPath):
                if filenameFlac.lower() == files.lower():
                    print("-"*30)
                    print(files)
                    print("-"*30)
                    print(filename)
                    print("-"*30)
                    filenameFlac = files  # Set the actual case of the filename
            # Adds artwork to .flac files and deletes the image files
            imageFile = dirPath + normalized_title + ".png"
            print("-"*30)
            print(imageFile)
            print("-"*30)
            # Adds artwork to .flac file
            try:
                audio = FLAC(filenameFlac)
                with open(imageFile, "rb") as f:
                    artwork = f.read()
                # Creates a Picture object with MIME type "image/png"
                pic = Picture()
                pic.type = 3  # Cover (front) image
                pic.mime = 'image/png'
                pic.desc = "Cover"
                pic.data = artwork
                audio.clear_pictures()  # Remove existing pictures
                audio.add_picture(pic)
                audio.save()
                print("Added artwork to", filename)
            except Exception as e:
                print(f"Could not add artwork to {filename}. Error: {str(e)}")
            # Deletes the .png file
            if imageFile.lower().endswith('.png'):
                os.remove(imageFile)

            replaceHashtagSymbol(dirPath)
            deleteIllegalChars(dirPath)


            # Extract title and artist metadata from the .txt file
            print("-"*30)
            print((filename + ".txt"))
            print("-"*30)

            with open((filename + ".txt"), 'r', encoding='utf16') as f:
                # Skip first two lines and extract the third line
                f.readline()
                f.readline()
                metadata = f.readline().strip().split(' · ')
                # Set title metadata as the first element before the first " · " symbol
                title = metadata[0].strip()
                # Set artist metadata as the rest of the elements after the first " · " symbol
                artists = metadata[1:]
                artists = [a.strip() for a in artists]
                artists_set = set(artists)
                # Get the order of appearance of the artists and remove duplicates
                artist_order = []
                for artist in artists:
                    if artist not in artist_order:
                        artist_order.append(artist)
                artists = [a for a in artist_order if a in artists_set]
                artist_str = ', '.join(artists)
            # Set the artist and title metadata for the .flac file
            audio = FLAC(filename + ".flac")
            audio['title'] = title
            audio['artist'] = artist_str
            audio.save()
            # Delete the .txt file after setting the metadata
            os.remove(filename + ".txt")


            illegalCharsRegex = r'[\\/:*?"<>|]'
            try:
                audio = FLAC(filenameFlac)
                # Extract and sanitize first artist name
                artist = re.sub(illegalCharsRegex, '', audio.get('artist', ['Unknown'])[0].split(',')[0])
                oldFilename = filenameFlac
                title = fetch_video_title(url)
                newFilename = os.path.join(dirPath, f"{artist} - {title}" + ".flac")
                os.rename(oldFilename, newFilename)
                print(f"Renamed {oldFilename} to {newFilename}")
            except:
                print(f"Failed to rename {filename}")

def filterPlaylistFlac(url_link, directory_path, progress_var):
    duplicates = checkPlaylistTitles(url_link)
    # Initialize logging
    logging.basicConfig(filename='downloadProcess.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    downloadProcess(url_link, directory_path, progress_var, duplicates)
    individualSongDownload(url_link, directory_path)
"""
