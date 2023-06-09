# Filename: scripts/download_transcript.py

import youtube_dl

def download_transcript(video_url):
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'writeautomaticsub': True,
        'outtmpl': 'transcript',  # Output filename (without extension)
        'postprocessors': [{
            'key': 'FFmpegSubtitlesConvertor',
            'format': 'srt'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_id = info_dict['id']
        ydl.download([video_id])

    with open('transcript.en.srt', 'r') as file:
        transcript = file.read()

    return transcript
