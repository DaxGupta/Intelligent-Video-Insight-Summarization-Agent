import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url:str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',    
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': False, 
        
        # COMMENT OUT OR REMOVE COOKIES
        # 'cookiesfrombrowser': ('firefox',),
        
        # Keep this to bypass JS requirements using mobile APIs
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'web']
            }
        },
        'rm_cachedir': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        
        # Safely replace whatever extension was downloaded (webm, m4a, opus) with .wav
        base_name, _ = os.path.splitext(ydl.prepare_filename(info))
        filename = base_name + '.wav'
        
    return filename


def convert_to_wav(input_file:str) -> str:
    "convert audio file to wav format using PyDub with mono channel and 16kHz sample rate"
    output_path= os.path.splitext(input_file)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(16000)  # Convert to mono and set frame rate
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int=10)-> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms=chunk_minutes * 60 * 1000  # Convert minutes to milliseconds
    chunks = []

    for i , start in enumerate(range(0, len(audio), chunk_ms)):
        end = min(start + chunk_ms, len(audio))
        chunk = audio[start:end]
        chunk_path = f"{os.path.splitext(wav_path)[0]}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    
    return chunks


def process_audio(source: str, chunk_minutes: int=5) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print(f"Downloading audio from YouTube URL: {source}")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV format...")
        wav_path = convert_to_wav(source)

    print(f"Chunking audio into {chunk_minutes}-minute segments...")
    chunks = chunk_audio(wav_path, chunk_minutes)
    print(f"Audio ready. {len(chunks)} chunks created.")
    return chunks