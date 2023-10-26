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