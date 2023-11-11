"""
██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗
██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗
██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║
██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║
╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
"""
import yt_dlp
import os
import time
import tkinter as tk
from tkinter import filedialog, ttk
import datetime
import threading
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
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
        cleanedTitle = info['title'].replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')

        files = os.listdir(dirPath)
        for fileName in files:
            newFileName = fileName.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')
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
        artist_str = ',(&) '.join(artists)
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
        artist = artists[0].split(',(&) ')[0]
        artist = artist.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

        try:
            os.rename(mp3Path, f"{dirPath}/{artist} - {cleanedTitle}.mp3")
            oldDir1 = (f"{dirPath}/{artist} - {cleanedTitle}.mp3")
            newDir1 = (f"{priorDir}/{artist} - {cleanedTitle}.mp3")
            os.rename(oldDir1, newDir1)
        except Exception as e:
            timeVal = int((time.time() % 10) * 10000000000000)
            print(f"Could not rename {info['title']}. Error: {str(e)}. Trying again...")
            os.rename(f"{dirPath}/{artist} - {cleanedTitle}.mp3", f"{dirPath}/({timeVal}){artist} - {cleanedTitle}.mp3")
            oldDir2 = (f"{dirPath}/({timeVal}){artist} - {cleanedTitle}.mp3")
            newDir2 = (f"{priorDir}/({timeVal}){artist} - {cleanedTitle}.mp3")
            if os.path.exists(oldDir2):  # Check if the file exists before attempting to rename again
                try:
                    os.rename(oldDir2, newDir2)
                except Exception as e:
                    print(f"Could not rename {info['title']}. Error: {str(e)}.")
            else:
                print(f"File not found: {oldDir2}")

    print("Download completed successfully.")


def filterPlaylistMp3(urls, dirPath, progress_var, index, playlistTitle):
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
            subdir = os.path.join(dirPath, str(playlistTitle).replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '') + str(sublists.index(sublist)))
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
    if not os.listdir(dirPath):
        os.chmod(dirPath, 0o777)
        os.rmdir(dirPath)

"""
    ███████╗██╗      █████╗  ██████╗    ███████╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
    ██╔════╝██║     ██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
    █████╗  ██║     ███████║██║         ███████╗█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══╝  ██║     ██╔══██║██║         ╚════██║██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║
██╗ ██║     ███████╗██║  ██║╚██████╗    ███████║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝ ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""
def flacProcess(url, dirPath, num, priorDir):    
    ydl_opts = {
        'outtmpl': f'{dirPath}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',  # Download best audio quality
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '9',  # You can adjust the audio quality here (e.g., 1-9)
        }],
        'writethumbnail': True,
        'writeinfojson': True,
        'writesubtitles': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Download the video, thumbnail, and description
        info = ydl.extract_info(url, download=True)
        cleanedTitle = info['title'].replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')

        files = os.listdir(dirPath)
        for fileName in files:
            newFileName = fileName.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')
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

        # Attach image to the .flac file
        flacPath = f"{dirPath}/{cleanedTitle}.flac"
        audio = FLAC(flacPath)
        with open(thumbnailPath, "rb") as imageFile:
            artwork = imageFile.read()
            audio.clear_pictures()
            audio.add_picture(artwork)

        description = info['description'].split("\n")

        title = description[2].strip().split(' · ')[0].strip()
        artists = [a.strip() for a in description[2].strip().split(' · ')[1:]]
        artist_str = ',(&) '.join(artists)
        audio['title'] = title
        audio['artist'] = artist_str

        album = description[4].strip()
        audio['album'] = album

        date = description[8].strip()

        if date.startswith('Released on: '):
            date = date.replace('Released on: ', '')
            releaseObj = datetime.datetime.strptime(date, '%Y-%m-%d')
            audio['date'] = releaseObj.strftime('%Y-%m-%d')

        audio.save()

        os.remove(thumbnailPath)
        os.remove(f"{dirPath}/{cleanedTitle}.info.json")

        artists = audio.get('artist', ['Unknown Artist'])
        artist = artists[0].split(',(&) ')[0]
        artist = artist.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

        try:
            os.rename(flacPath, f"{dirPath}/{artist} - {cleanedTitle}.flac")
            oldDir = (f"{dirPath}/{artist} - {cleanedTitle}.flac")
            newDir = (f"{priorDir}/{artist} - {cleanedTitle}.flac")
            os.rename(oldDir, newDir)
        except Exception as e:
            timeVal = int((time.time() % 10) * 10000000000000)
            print(f"Could not rename {info['title']}. Error: {str(e)}. Trying again...")
            os.rename(flacPath, f"{dirPath}/({timeVal}){artist} - {cleanedTitle}.flac")
            oldDir = (f"{dirPath}/({timeVal}){artist} - {cleanedTitle}.flac")
            newDir = (f"{priorDir}/({timeVal}){artist} - {cleanedTitle}.flac")
            try:    
                os.rename(oldDir, newDir)
            except Exception as e:
                print(f"Could not rename {info['title']}. Error: {str(e)}.")

    print("Download completed successfully.")

def filterPlaylistFlac(urls, dirPath, progress_var, index, playlistTitle):
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
            subdir = os.path.join(dirPath, str(playlistTitle).replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '') + str(sublists.index(sublist)))
            os.makedirs(subdir, exist_ok=True)
            thread = threading.Thread(target=startDownloadFlac, args=(sublist, subdir, count, progress_var, incr, dirPath))
            threads.append(thread)
            thread.start()
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

def startDownloadFlac(urls, dirPath, count, progress_var, incr, priorDir):
    for url in urls:
        progress_var.set(incr*count)
        flacProcess(url, dirPath, count, priorDir)
        count += 1
    if not os.listdir(dirPath):
        os.chmod(dirPath, 0o777)
        os.rmdir(dirPath)

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
        playlistTitle = playlist_info.get('title', 'Unknown Playlist')

        # Filter out duplicate URLs
        unique_urls = set()
        for video in playlist_videos:
            if video and 'url' in video:
                unique_urls.add(video['url'])

    # Store unique URLs in the 'URLs' variable
    URLs = list(unique_urls)
    return URLs, playlistTitle

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
    
    urls, playlistTitle = extractURLs(url_link)
    userIndex = 64
    if(userIndex>len(urls)):
        index = len(urls)
    else:
        index = userIndex

    # Create a separate thread to execute the download process
    if dropdownOption == '.mp3':
        download_thread = threading.Thread(target=filterPlaylistMp3, args=(urls, directory_path, progress_var, index, playlistTitle))
        download_thread.start()
    elif dropdownOption == '.flac':
        print(dropdownOption)
        download_thread = threading.Thread(target=filterPlaylistFlac, args=(urls, directory_path, progress_var, index, playlistTitle))
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

