import streamlit as st
import tempfile
import os
import whisper
from pydub import AudioSegment
from googletrans import Translator, LANGUAGES
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import speech_recognition as sr
from langdetect import detect,DetectorFactory
import playsound
import time

DetectorFactory.seed = 0  

target_languages = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}
# Configure the page
st.set_page_config(page_title="Language Translator", layout="wide")

# Title
st.markdown("""
    <h1 style='text-align: center; font-size: 48px; font-weight: bold; color: #4CAF50;'>🌐 Language Translator</h1>
""", unsafe_allow_html=True)

# Define navbar options
options = ["Text", "Speech - Text", "Speech - Speech", "Text - Speech"]

# Horizontal navigation bar
selected_option = st.radio("Choose an option:", options, index=0, horizontal=True)

# Initialize translator
translator = Translator()

# Fetch available languages
target_languages = {name.capitalize(): code for code, name in LANGUAGES.items()}

# Function to play translated speech
def speak(text, lang):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = "translated_audio.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        st.error(f"Error during TTS: {e}")

# --- TEXT TRANSLATION ---
if selected_option == "Text":
    st.subheader("Text Translation")
    input_text = st.text_area("Enter text to translate:", placeholder="Type your text here...")
    target_language = st.selectbox("Select target language:", options=target_languages.keys())
    
    if st.button("Translate Text"):
        if input_text:
            try:
                translated_text = translator.translate(input_text, dest=target_languages[target_language]).text
                st.success("Translated Text:")
                st.markdown(f"<p style='font-size: 20px; color: #4CAF50;'>{translated_text}</p>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter text to translate.")

# --- SPEECH TO TEXT TRANSLATION ---
elif selected_option == "Speech - Text":
    st.subheader("Speech-to-Text Translation")
    model = whisper.load_model("base")
    target_language = st.selectbox("Select target language:", options=target_languages.keys(), key="speech_lang")
    audio_file = st.file_uploader("Upload an audio file (wav/mp3/ogg):", type=["wav", "mp3", "ogg"])
    
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name
        
        temp_audio_wav_path = temp_audio_path.replace(".mp3", ".wav").replace(".ogg", ".wav")
        
        if temp_audio_path.endswith((".mp3", ".ogg")):
            sound = AudioSegment.from_file(temp_audio_path)
            sound.export(temp_audio_wav_path, format="wav")
        else:
            temp_audio_wav_path = temp_audio_path
        
        try:
            with st.spinner("Processing audio..."):
                result = model.transcribe(temp_audio_wav_path)
                recognized_text = result["text"]
                st.success("Recognized Speech:")
                st.text_area("Extracted Text:", recognized_text, height=150)
                
                translated_text = translator.translate(recognized_text, dest=target_languages[target_language]).text
                st.success("Translated Text:")
                st.markdown(f"<p style='font-size: 20px; color: #4CAF50;'>{translated_text}</p>", unsafe_allow_html=True)
                
                st.download_button("Download Transcribed Text", recognized_text, file_name="transcribed_text.txt")
                st.download_button("Download Translated Text", translated_text, file_name="translated_text.txt")
        except Exception as e:
            st.error(f"Error recognizing speech: {str(e)}")
        finally:
            os.remove(temp_audio_wav_path)
            if temp_audio_path != temp_audio_wav_path:
                os.remove(temp_audio_path)

# --- SPEECH TO SPEECH TRANSLATION ---
elif selected_option == "Speech - Speech":
    st.subheader("Speech-to-Speech Translation")
    
    # Select target language BEFORE recording
    target_language = st.selectbox("Select target language:", options=target_languages.keys(), key="speech_to_speech")

    if st.button("Start Speaking"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎙️ Speak now...")
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                st.write("Processing speech...")

                # 🔥 Recognize speech without fixed language (auto-detect)
                try:
                    text = recognizer.recognize_google(audio)  # Auto-detect input language
                    st.success(f"Original Speech: {text}")
                except sr.UnknownValueError:
                    st.error("Sorry, could not understand what you said.")
                    text = ""
                except sr.RequestError as e:
                    st.error(f"Could not request results; {e}")
                    text = ""

                if text:
                    # 🔥 Clean text before detection
                    cleaned_text = text.strip()

                    # 🔥 Attempt language detection with retry
                    detected_lang = "unknown"
                    for _ in range(3):  # Retry up to 3 times if detection fails
                        try:
                            detected_lang = detect(cleaned_text)
                            break
                        except Exception:
                            time.sleep(0.5)  # Small delay before retry
                    
                    if detected_lang == "unknown":
                        detected_lang = 'te'  # Fallback to Telugu if detection fails

                    st.info(f"Detected Language: {detected_lang}")

                    # 🔥 Translate to target language
                    try:
                        # ✅ If direct detection fails, force auto-mode
                        translated_text = GoogleTranslator(source=detected_lang, target=target_languages[target_language]).translate(cleaned_text)
                        
                        # ✅ Fallback mechanism if output == input
                        if translated_text.strip().lower() == cleaned_text.strip().lower():
                            if detected_lang != 'en':
                                # 🔥 Force Telugu → English fallback
                                translated_text = GoogleTranslator(source='te', target=target_languages[target_language]).translate(cleaned_text)
                            else:
                                translated_text = GoogleTranslator(source='auto', target=target_languages[target_language]).translate(cleaned_text)

                        st.success(f"Translated Text: {translated_text}")

                    except Exception as e:
                        st.error(f"Translation failed: {e}")
                        translated_text = ""

                    if translated_text:
                        # 🔥 Generate translated audio file
                        audio_path = "translated_audio.mp3"
                        tts = gTTS(text=translated_text, lang=target_languages[target_language], slow=False)
                        tts.save(audio_path)

                        # Display audio player and download option
                        with open(audio_path, "rb") as file:
                            b64 = base64.b64encode(file.read()).decode()
                            st.audio(audio_path, format="audio/mp3")
                            download_link = f'<a href="data:audio/mp3;base64,{b64}" download="translated_audio.mp3">🎵 Download Speech</a>'
                            st.markdown(download_link, unsafe_allow_html=True)

                        # 🔥 Replay Button
                        if st.button("Replay Translation"):
                            playsound.playsound(audio_path)

                        # Clean up the file
                        os.remove(audio_path)

            except Exception as e:
                st.error(f"Error: {e}")

# --- TEXT TO SPEECH TRANSLATION ---
elif selected_option == "Text - Speech":
    st.subheader("Text-to-Speech Translation")
    text = st.text_area("Enter text to translate:", "Hello, how are you?")
    dest_lang = st.selectbox("Select target language:", options=target_languages.keys(), key="tts_lang")
    
    if st.button("Translate and Speak"):
        try:
            translated_text = GoogleTranslator(source="auto", target=target_languages[dest_lang]).translate(text)
            st.success(f"*Translated Text:* {translated_text}")
            
            tts = gTTS(text=translated_text, lang=target_languages[dest_lang], slow=False)
            audio_path = "translated_speech.mp3"
            tts.save(audio_path)
            
            with open(audio_path, "rb") as file:
                b64 = base64.b64encode(file.read()).decode()
                download_link = f'<a href="data:audio/mp3;base64,{b64}" download="translated_speech.mp3">🎵 Download Speech</a>'
                st.audio(audio_path, format="audio/mp3")
                st.markdown(download_link, unsafe_allow_html=True)
            os.remove(audio_path)
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.markdown("<hr style='border: 1px solid #4CAF50; margin: 40px 0;'>", unsafe_allow_html=True)
