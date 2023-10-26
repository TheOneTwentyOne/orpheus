import datetime
import json
import os
import re
import sys
import yt_dlp
import logging
import time
from collections import defaultdict
from moviepy.editor import VideoFileClip
from mutagen.id3 import ID3, APIC, TIT2, TPE1
from mutagen.mp3 import MP3




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_playlist_video_urls(playlist_url):
    try:
        start_time = time.time()
        ydl_opts = {
            'quiet': True,
            'extract_flat': 'in_playlist',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' in result:
                urls = [item['url'] for item in result['entries']]
                elapsed_time = time.time() - start_time
                logging.info(f"Retrieved {len(urls)} video URLs from the playlist in {elapsed_time:.2f} seconds.")
                return urls
            else:
                logging.warning("No entries found in the playlist.")
                return []

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return []



def add_artwork_to_mp3_files(output_dir):
    for mp3_file_name in os.listdir(output_dir):
        if mp3_file_name.endswith(".mp3"):
            mp3_file_path = os.path.join(output_dir, mp3_file_name)
            print(mp3_file_name)

            image_file_name = mp3_file_name[:-4] + ".png"
            image_file_path = os.path.join(output_dir, image_file_name)

            try:
                audio = MP3(mp3_file_path, ID3=ID3)
                with open(image_file_path, "rb") as image_file:
                    artwork = image_file.read()

                # Set the album cover
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
                print("Added artwork to", mp3_file_name)

            except Exception as e:
                print(f"Could not add artwork to {mp3_file_name}. Error: {str(e)}")

            # Deletes the .png file
            if image_file_name.lower().endswith('.png'):
                os.remove(image_file_path)




import os
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC

def set_music_metadata(output_dir):
    try:
        for mp3_file_name in os.listdir(output_dir):
            if mp3_file_name.endswith('.mp3'):
                mp3_file_path = os.path.join(output_dir, mp3_file_name)
                txt_file_path = os.path.join(output_dir, mp3_file_name[:-4] + '.txt')

                if os.path.exists(txt_file_path):
                    # Extract album name from the fifth line and date from the ninth line of the .txt file
                    with open(txt_file_path, 'r', encoding='utf-16') as txt_file:
                        lines = txt_file.readlines()

                    if len(lines) >= 9:
                        album_name = lines[4].strip()
                        date_line = lines[8].strip()

                        # Check if the ninth line contains the date in the correct format
                        if date_line.startswith('Released on: '):
                            try:
                                release_date = date_line.replace('Released on: ', '')
                                # Parse the release date and set album and date metadata for the .mp3 file
                                release_date_obj = datetime.datetime.strptime(release_date, '%Y-%m-%d')
                                audio = ID3(mp3_file_path)
                                audio['TALB'] = TALB(encoding=3, text=album_name)
                                audio['TDRC'] = TDRC(encoding=3, text=release_date_obj.strftime('%Y-%m-%d'))
                                audio.save(mp3_file_path)

                                # Extract title and artist metadata from the .txt file (similar to original code)
                                title = lines[2].strip().split(' · ')[0].strip()
                                artists = [a.strip() for a in lines[2].strip().split(' · ')[1:]]
                                artist_str = ', '.join(artists)

                                # Set the artist and title metadata for the .mp3 file (similar to original code)
                                audio['TIT2'] = TIT2(encoding=3, text=title)
                                audio['TPE1'] = TPE1(encoding=3, text=artist_str)
                                audio.save(mp3_file_path)

                                # Delete the .txt file after setting the metadata
                                os.remove(txt_file_path)

                            except ValueError:
                                print(f"Invalid date format in {txt_file_path}")
                        else:
                            print(f"Date not found in the correct format in {txt_file_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    os.remove(os.path.join(output_dir, "descriptions.json"))






def rename_mp3_files(directory_path):
    try:
        for filename in os.listdir(directory_path):
            if filename.endswith('.mp3'):
                mp3_file = os.path.join(directory_path, filename)
                audio = MP3(mp3_file, ID3=ID3)

                # Extract the first artist name (if available)
                # Get the first artist name from the 'TPE1' tag, considering "Earth, Wind & Fire" as a special case
                artists = audio.get('TPE1', ['Unknown Artist'])
                artist = next((a for a in artists if a.startswith('Earth, Wind & Fire')), artists[0]).split(',')[0]

                # Extract the title from the existing metadata
                title = audio.get('TIT2', ['Unknown Title'])[0]

                # Replace specific characters with their alternative versions
                
                artist = artist.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')
                title = title.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')

                # Create the new filename in the format: "Artist - Title.mp3"
                new_filename = os.path.join(directory_path, f"{artist} - {title}.mp3")

                # Rename the file if it's different from the current filename
                if mp3_file != new_filename:
                    os.rename(mp3_file, new_filename)
                    print(f"Renamed {mp3_file} to {new_filename}")

    except Exception as e:
        print(f"An error occurred in [rename_mp3_files]: {str(e)}")




def extract_album_art(output_dir):
    try:
        for filename in os.listdir(output_dir):
            if filename.lower().endswith((".mp4", ".webm")):
                input_file = os.path.join(output_dir, filename)
                output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")

                with VideoFileClip(input_file) as clip:
                    clip.save_frame(output_file, t=1)

                print(f"Extracted album art from {input_file} to {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")









def delete_video_files(output_dir):
    try:
        for filename in os.listdir(output_dir):
            if filename.lower().endswith((".mp4", ".webm")):
                video_file = os.path.join(output_dir, filename)
                # Delete the video file
                os.remove(video_file)
                print(f"Deleted {video_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")





def delete_illegal_chars(output_dir):

    try:
        for filename in os.listdir(output_dir):
            if filename.endswith(('.mp3', '.txt', '.png')):
                new_filename = filename
                new_filename = new_filename.replace('#', '').replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')

                if new_filename != filename:
                    os.rename(os.path.join(output_dir, filename), os.path.join(output_dir, new_filename))
                    print(f"Renamed {filename} to {new_filename}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")





def check_playlist_titles(playlist_url):
    duplicates = []
    titles_to_urls = defaultdict(list)

    try:
        # Fetch video URLs from the playlist
        video_urls = get_playlist_video_urls(playlist_url)

        with yt_dlp.YoutubeDL() as ydl:
            for url in video_urls:
                info = ydl.extract_info(url, download=False)
                title = info.get('title')

                if title:
                    normalized_title = title.lower()  # Convert title to lowercase
                    titles_to_urls[normalized_title].append(url)

        for normalized_title, url_list in titles_to_urls.items():
            if len(url_list) > 1:
                duplicates.append((normalized_title, url_list))

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return duplicates





def playlist_url_clean(playlist_url, output_dir, duplicates):
    full_video_urls = []

    # Set the options for the yt-dlp downloader
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'yes_playlist': True,
    }

    try:
        # Download the videos and collect video URLs
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
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

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []




def sanitize_filename(filename):
    # Sanitize filename by removing illegal characters
    return filename.strip().replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')




def download_video_descriptions(video_urls, output_dir):
    print("downloadVideoDescriptions")
    description_dict = {}
    descriptions_file = os.path.join(output_dir, 'descriptions.json')
    
    # Check if descriptions data file exists and load it
    if os.path.exists(descriptions_file):
        with open(descriptions_file, 'r') as f:
            description_dict = json.load(f)
    
    # Process video URLs
    for url in video_urls:
        try:
            # Get the video title and sanitize it for file naming
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_title = str(info_dict['title'])
                video_title = sanitize_filename(video_title)

            # Check if description already exists in the dictionary
            if url in description_dict:
                video_description = description_dict[url]
            else:
                # Download description data from youtube-dl for new video
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    video_description = str(info_dict.get('description', '').strip())
                    description_dict[url] = video_description

            # Create or update the .txt file with the video description
            output_file_path = os.path.join(output_dir, f"{video_title}.txt")
            with open(output_file_path, "w", encoding="utf16", errors="replace") as f:
                f.write(video_description.replace("\uFFFD", ""))
        
        except Exception as e:
            print(f"An error occurred while processing {url}: {str(e)}")

    # Write the descriptions dictionary to the file
    with open(descriptions_file, 'w') as f:
        json.dump(description_dict, f)







# Downloads all of the .mp4 and .mp3 files from the specified playlist
def downloadVideos(playlistUrl, outputDir, duplicates):
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
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'extractaudio': True
    }
    

    # Download remaining videos
    ydl_opts_remaining = {
        'format': 'best[ext=mp4]',
        'outtmpl': outputDir + '%(title)s.%(ext)s',
        'yes_playlist': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
        ydl_audio.download(filtered_full_video_urls)
    
    
    with yt_dlp.YoutubeDL(ydl_opts_remaining) as ydl_remaining:
        ydl_remaining.download(filtered_full_video_urls)
    






def downloadProcess(url, directory_path, progress_var, duplicates):
    
    downloadVideos(url, directory_path, duplicates)
    progress_var.set(10)

    urlLists = playlist_url_clean(url, directory_path, duplicates)
    progress_var.set(20)
    
    download_video_descriptions(urlLists, directory_path)
    progress_var.set(30)

    extract_album_art(directory_path)
    progress_var.set(40)

    delete_video_files(directory_path)
    progress_var.set(50)

    add_artwork_to_mp3_files(directory_path)
    progress_var.set(60)

    progress_var.set(70)

    delete_illegal_chars(directory_path)
    progress_var.set(80)

    set_music_metadata(directory_path)
    progress_var.set(90)

    rename_mp3_files(directory_path)
    progress_var.set(100)


def fetch_video_title(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', 'UnknownTitle')

def individual_song_download(url_link, directory_path):
    def clean_filename(filename):
        # Replace invalid characters with underscores
        return filename.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')

    def download_and_store_description(url, dirPath, descriptionDict):
        descriptionsFile = os.path.join(dirPath, 'descriptions.json')

        if url in descriptionDict:
            videoDescription = descriptionDict[url]
        else:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                videoDescription = str(info_dict['description'].strip())
                descriptionDict[url] = videoDescription

        with open(descriptionsFile, 'w') as f:
            json.dump(descriptionDict, f)

        return videoDescription

    urlLists = check_playlist_titles(url_link)
    dirPath = os.path.join(directory_path, "duplicates")

    for normalized_title, url_list in urlLists:
        for url in url_list:
            ydl_opts_audio = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(dirPath, f'{clean_filename(normalized_title)}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '256',
                }],
                'extractaudio': True,
            }

            ydl_opts_video = {
                'format': 'best[ext=mp4]',
                'outtmpl': os.path.join(dirPath, f'{clean_filename(normalized_title)}.%(ext)s'),
                'yes_playlist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                ydl_audio.download([url])

            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl_video:
                ydl_video.download([url])

            descriptionDict = {}
            descriptionsFile = os.path.join(dirPath, 'descriptions.json')

            if os.path.exists(descriptionsFile):
                with open(descriptionsFile, 'r') as f:
                    descriptionDict = json.load(f)

            videoDescription = download_and_store_description(url, dirPath, descriptionDict)

            outputFilePath = os.path.join(dirPath, f'{clean_filename(normalized_title)}.txt')

            with open(outputFilePath, "w", encoding="utf16", errors="replace") as f:
                f.write(videoDescription.replace("\uFFFD", ""))

            os.remove(descriptionsFile)

            extract_album_art(dirPath)
            delete_video_files(dirPath)

            normTitle = normalized_title
            filename = dirPath + "/" + normTitle.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            filenameMp3 = filename + ".mp3"
            print("-" * 30)
            print(filename)
            print("-" * 30)
            
            for files in os.listdir(dirPath):
                if filenameMp3.lower() == files.lower():
                    print("-" * 30)
                    print(files)
                    print("-" * 30)
                    print(filename)
                    print("-" * 30)

            imageFile = filename + ".png"
            print("-" * 30)
            print(imageFile)
            print("-" * 30)

            try:
                audio = MP3(filenameMp3, ID3=ID3)
                with open(imageFile, "rb") as f:
                    artwork = f.read()
                audio.tags.add(
                    APIC(
                        encoding=3,
                        mime='image/png',
                        type=3,
                        desc=u'Cover',
                        data=artwork
                    )
                )
                audio.save()
                print("Added artwork to", filenameMp3)
            except Exception as e:
                print(f"Could not add artwork to {filenameMp3}. Error: {str(e)}")
                sys.exit()

            if imageFile.lower().endswith('.png'):
                os.remove(imageFile)

            delete_illegal_chars(dirPath)

            print("-" * 30)
            print((filename + ".txt"))
            print("-" * 30)
            
            with open(filename + ".txt", 'r', encoding='utf16') as f:
                f.readline()
                f.readline()
                metadata = f.readline().strip().split(' · ')
                title = metadata[0].strip()
                artists = [a.strip() for a in metadata[1:]]
                artists_set = set(artists)
                artist_order = []
                for artist in artists:
                    if artist not in artist_order:
                        artist_order.append(artist)
                artists = [a for a in artist_order if a in artists_set]
                artist_str = ', '.join(artists)

            audio = MP3(filename + ".mp3", ID3=ID3)
            audio.tags.add(TIT2(encoding=3, text=title))
            audio.tags.add(TPE1(encoding=3, text=artist_str))
            audio.save()
            os.remove(filename + ".txt")

            try:
                audio = MP3(filename + ".mp3", ID3=ID3)
                artist_tag = audio.get('TPE1')
                if artist_tag:
                    artist = artist.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')
                else:
                    artist = "Unknown Artist"
                oldFilename = filename + ".mp3"
                title = fetch_video_title(url)
                title = title.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')
                newFilename = os.path.join(dirPath, f"{artist} - {title}.mp3")
                os.rename(oldFilename, newFilename)
                print(f"Renamed {oldFilename} to {newFilename}")
            except Exception as e:
                print(f"Failed to rename {filename}: {str(e)}")

def extract_metadata_from_txt(txt_filepath):
    try:
        with open(txt_filepath, 'r', encoding='utf16') as f:
            f.readline()
            f.readline()
            metadata = f.readline().strip().split(' · ')
            title = metadata[0].strip()
            artists = [a.strip() for a in metadata[1:]]
            return title, ', '.join(artists)
    except Exception as e:
        print(f"An error occurred while extracting metadata: {str(e)}")
        return None, None

def apply_metadata_to_mp3(mp3_filepath, title, artist):
    try:
        audio = MP3(mp3_filepath, ID3=ID3)
        audio.tags.add(TIT2(encoding=3, text=title))
        audio.tags.add(TPE1(encoding=3, text=artist))
        audio.save()
    except Exception as e:
        print(f"An error occurred while applying metadata: {str(e)}")

def rename_mp3_file(mp3_filepath, url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = str(info_dict['title'])
            video_title = video_title.replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')

            new_filename = os.path.join(os.path.dirname(mp3_filepath), f"{video_title}.mp3")
            os.rename(mp3_filepath, new_filename)
            print(f"Renamed {mp3_filepath} to {new_filename}")
    except Exception as e:
        print(f"An error occurred while renaming the MP3 file: {str(e)}")


def filterPlaylistMp3(url_link, directory_path, progress_var):
    duplicates = check_playlist_titles(url_link)
    downloadProcess(url_link, directory_path, progress_var, duplicates)
    individual_song_download(url_link, directory_path)





#     .replace('⧸', '').replace('／', '').replace('∕', '').replace('⧵', '').replace('∖', '').replace('＼', '').replace('꞉', '').replace('∶', '').replace('⁚', '').replace('：', '').replace('ː', '').replace('＊', '').replace('⁎', '').replace('∗', '').replace('？', '').replace('＂', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '').replace('„', '').replace('‟', '').replace('❝', '').replace('❞', '').replace("'",'').replace('＞', '').replace('﹥', '').replace('›', '').replace('＜', '').replace('﹤', '').replace('｜', '').replace('│', '').replace('|', '').replace('_','').replace('', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')