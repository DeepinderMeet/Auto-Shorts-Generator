
# Automatic Yt Shorts Generator


from moviepy.video.VideoClip import ColorClip
# from moviepy.video.VideoClip import ColorClip
from google import genai
from elevenlabs import ElevenLabs
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

#  API KEYS  are here


GEMINI_API_KEY = "PASTE_YOUR_GEMINI_KEY"
ELEVENLABS_API_KEY = "sk_770313ee02ecafc06c0a00233850da9f69af148755ff63ef"

#  Scripts will be here and will be hardcoded till now


script_text = "Imagine karo ek aisi flight jo take-off toh karti hai par 37 saal baad land hoti hai. Pan Am Flight 914. 1955 mein New York se udi, gayab ho gayi, aur seedha 1992 mein Venezuela mein land hui. Pilot ne ATC se pucha 'Abhi kaunsa saal chal raha hai?' Jab use pata chala ki 37 saal beet chuke hain, wo dar gaya aur wapis plane lekar ud gaya. Aaj tak uska koi nishaan nahi mila. Log ise time travel kehte hain, toh kuch ise sirf ek urban legend. Par socho, agar tumhare saath aisa ho toh? Ek pal mein poori duniya badal gayi. Tum ise sach maante ho ya sirf ek kahani? Follow karo aisi aur mysteries ke liye."

print("\nSCRIPT:\n", script_text)

# Text to speech conversion using the Elevenlabs API key

tts_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

audio_stream = tts_client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    model_id="eleven_multilingual_v2",
    text=script_text
)

with open("voice.mp3", "wb") as f:
    for chunk in audio_stream:
        f.write(chunk)

print("Voice generated ✅")

# Video Generation Code

# Loading video
video = VideoFileClip("background.mp4").resized((720, 1280))

# Loading the  audio
audio_clip = AudioFileClip("voice.mp3")

# Match duration
video = video.with_duration(audio_clip.duration)

# Word by Word Captions

words = script_text.split()
duration = audio_clip.duration
time_per_word = duration / len(words)

text_clips = []

y_position = 900  # lower than center (Shorts style)

for i, word in enumerate(words):

    # WORD TEXT
    txt = TextClip(
        text=word,
        font=r"C:\Windows\Fonts\Arialbd.ttf",
        font_size=68,          # little bigger
        color="white",
        method="caption",
        size=(420, 140)       # ✅ FIX: fixed height
        # align="center"
    )
    txt = txt.resized(lambda t: 1 + 0.06 * min(t / 0.12, 1))
    txt = txt.with_position(("center", "72%"))




    # Small dynamic background box (fits word)
    box = ColorClip(
        size=(txt.w + 40, txt.h + 20),  # padding around word
        color=(0, 0, 0)
    ).with_opacity(0.65)

    start_time = i * time_per_word

    # POP-IN ANIMATION (scale)
    txt = (
        txt.with_start(start_time)
           .with_duration(time_per_word)
           .resized(lambda t: 0.6 + 0.4 * min(t * 6, 1))  # 🔥 animation
           .with_position(("center", y_position))
    )

    box = (
        box.with_start(start_time)
           .with_duration(time_per_word)
           .with_position(("center", y_position - 10))
    )

    text_clips.extend([box, txt])


# Combine
final_video = CompositeVideoClip(
    [video, *text_clips]
).with_audio(audio_clip)



# Export
final_video.write_videofile(
    "final_short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

print("SHORT VIDEO CREATED as : final_short.mp4")
