from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator

translator = Translator()

def get_videoid(url):
    if 'youtu.be' in url:
        url = url.replace('youtu.be/', 'www.youtube.com/watch?v=')
    video_id = url.split("v=")[1][0:12]
    return video_id

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        selected_transcript = None

        for transcript in transcript_list:
            if transcript.language_code == 'en':
                selected_transcript = transcript.fetch()
                break
        
        if not selected_transcript:
            for transcript in transcript_list:
                other_transcript = transcript.fetch()
                break
            tr= ' '.join([t['text'] for t in other_transcript])
            translated_transcript = translator.translate(tr, dest='en')
            transcript = translated_transcript.text
            return transcript
        else:
            transcript = ' '.join([t['text'] for t in selected_transcript])
            return transcript

    except Exception as e:
        return "Error: " + str(e)