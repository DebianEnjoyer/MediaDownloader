import yt_dlp
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()


def download_video(url, output_folder, format_type, playlist, progress_callback=None):

    def hook(d):
        if progress_callback is not None:
            progress_callback(d)

    if playlist == "Yes":
        no_playlist = False
        output_template = (
            f"{output_folder}/%(playlist_title)s/"
            f"%(playlist_index)03d - %(title)s.%(ext)s"
        )
    else:
        no_playlist = True
        output_template = f"{output_folder}/%(title)s.%(ext)s"

    if format_type == "mp3":
        options = {
            "outtmpl": output_template,
            "format": "bestaudio/best",
            "noplaylist": no_playlist,
            "ffmpeg_location": ffmpeg_path,
            "progress_hooks": [hook],
            "retries": 10,
            "fragment_retries": 3,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

    else:  # mp4
        options = {
            "outtmpl": output_template,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "noplaylist": no_playlist,
            "ffmpeg_location": ffmpeg_path,
            "progress_hooks": [hook],
            "retries": 10,
            "fragment_retries": 3,
        }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])