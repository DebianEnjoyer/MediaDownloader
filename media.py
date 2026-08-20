import yt_dlp
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

def download_video(url, output_folder, format_type,progress_callback=None):
    def hook(d):
        if progress_callback is not None:
            progress_callback(d)

    if format_type == "mp3":
        options = {
            "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
            "format": "bestaudio/best",
            "noplaylist": True,
            "ffmpeg_location": ffmpeg_path,
            "progress_hooks":[hook],
            "fragment_retries": 3,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",               
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:  # mp4
        options = {
            "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "noplaylist": True,
            "ffmpeg_location": ffmpeg_path,
            "progress_hooks":[hook],
            "fragment_retries":3,
        }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])