import os
import sys
import subprocess
from pytube import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch

def search_youtube_videos(singer_name, num_videos):
    print("Searching YouTube for video URLs...")
    videosSearch = VideosSearch(singer_name, limit=num_videos)
    results = videosSearch.result()
    video_urls = [video['link'] for video in results['result']]
    return video_urls

def download_videos(video_urls):
    print(f"Downloading {len(video_urls)} videos...")
    for url in video_urls:
        yt = YouTube(url)
        yt.streams.filter(only_audio=True).first().download()

def convert_to_audio():
    print("Converting videos to audio...")
    for file in os.listdir():
        if file.endswith(".mp4"):
            audio_name = os.path.splitext(file)[0] + ".mp3"
            video = AudioSegment.from_file(file)
            video.export(audio_name, format="mp3")
            os.remove(file)

def cut_audio(duration):
    print(f"Cutting first {duration} seconds from all audios...")
    for file in os.listdir():
        if file.endswith(".mp3"):
            audio = AudioSegment.from_file(file)
            cut_audio = audio[:duration*1000]
            cut_audio.export(file, format="mp3")

def merge_audios(output_file):
    print("Merging all audios...")
    files = [file for file in os.listdir() if file.endswith(".mp3")]
    merged_audio = AudioSegment.empty()
    for file in files:
        merged_audio += AudioSegment.from_file(file)
    merged_audio.export(output_file, format="mp3")
    
    print(f"Merged audio saved as {output_file}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        return
    
    singer_name = sys.argv[1]
    num_videos = int(sys.argv[2])
    duration = int(sys.argv[3])
    output_file = sys.argv[4]

    if num_videos <= 0:
        print("Number of videos must be greater than 0.")
        return
    if duration <= 0:
        print("Audio duration must be greater than 0 seconds.")
        return

    try:
        video_urls = search_youtube_videos(singer_name, num_videos)
        download_videos(video_urls)
        convert_to_audio()
        cut_audio(duration)
        merge_audios(output_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()