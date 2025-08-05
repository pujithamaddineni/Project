# 🌐 Language Translator with Streamlit

This project is a multilingual **Language Translator** built with **Streamlit**, allowing users to translate between languages using **text, speech (from file or microphone), and speech output**.

---

## 🚀 Features

* **Text Translation**: Translate text input into the selected target language.
* **Speech-to-Text Translation**: Upload audio files to extract and translate the spoken content.
* **Speech-to-Speech Translation**: Speak directly into the microphone to translate and hear the translated response.
* **Text-to-Speech**: Convert entered text into speech.

---

## 🛠 Technologies Used

* [Streamlit](https://streamlit.io/) – for building the web interface.
* [Googletrans](https://pypi.org/project/googletrans/) – for text translation.
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) – for recognizing speech.
* [pyttsx3](https://pypi.org/project/pyttsx3/) – for converting text to speech.
* [langdetect](https://pypi.org/project/langdetect/) – for automatic language detection.
* [pydub](https://pypi.org/project/pydub/) – for audio file conversion (used in other features).

---

## 🔧 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/pujithamaddineni/Project.git
cd Project
```

2. **Create Virtual Environment (Optional)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

**Note:** You may need to install additional audio dependencies like `pyaudio`.

---

### 4. Install FFmpeg (Required for audio file handling with pydub)
#### 📦 On Windows:
1. Download FFmpeg zip from: https://ffmpeg.org/download.html
2. Extract it and copy the `bin` path (e.g., `C:\ffmpeg\bin`)
3. Add it to **System Environment Variables** → **Path**
4. Open new terminal and test:
```bash
ffmpeg -version
```

## ▶️ Running the App

```bash
streamlit run proj2.py
```

---

## 🎙 Microphone Permissions

For the Speech-to-Speech feature to work:

* Grant microphone access to the Python process (check OS settings).
* Run it locally; web-hosted versions may not support real-time microphone input.

---

## 📂 File Structure

```
├── final.py             # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

---
## 🎯 Notes
- Works best locally due to microphone access limitations in browsers.
- For deployment on Streamlit Cloud, replace mic input with file upload.

## 🙌 Acknowledgements

* [Google Translate API](https://translate.google.com/)
* [OpenAI Whisper](https://github.com/openai/whisper) 
* Community contributors of Streamlit and open-source speech libraries

## 🔗 Demo Video
[▶️ Watch the Demo](https://drive.google.com/file/d/1uB5n76_weVGa_y2rwOR24J_l0WCo2xEl/view?usp=sharing)

---



