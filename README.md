# 🎬 AI Video Assistant (Meeting Intelligence)

An AI-powered meeting intelligence tool designed to transform long meetings, lectures, or video podcasts into actionable insights. Simply provide a YouTube URL or a local media file, and this assistant will transcribe the audio, summarize the content, extract key decisions, and let you interactively chat with the transcript using an embedded Retrieval-Augmented Generation (RAG) engine.

## ✨ Features

- **Multi-Source Audio Processing:** Automatically downloads audio from YouTube URLs (via `yt-dlp`) or processes local audio/video files.
- **Accurate Transcription:** Leverages OpenAI's Whisper model to convert speech to text, automatically handling long files by chunking them.
- **Smart Summarization:** Uses Google's Gemini LLM to generate concise, professional meeting summaries.
- **Automated Extraction:** Identifies and extracts:
  - ✅ Action Items (Task, Owner, Deadline)
  - 🔑 Key Decisions
  - ❓ Open/Unresolved Questions
- **Interactive RAG Chat:** Ask questions directly about your meeting. The app builds a local ChromaDB vector store and retrieves relevant context to answer your queries precisely.
- **Beautiful UI:** A sleek, modern Streamlit interface with real-time pipeline status tracking.
- **CLI Support:** Run the pipeline headlessly via `main.py`.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Transcription:** OpenAI Whisper
- **LLM / AI Models:** Google Gemini (`gemini-1.5-flash`), LangChain
- **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
- **Vector Database:** ChromaDB
- **Audio Processing:** PyDub, yt-dlp

## 📂 Project Structure

```text
📦 project-root
 ┣ 📂 core                  # Core AI and processing modules
 ┃ ┣ 📂 __pycache__
 ┃ ┣ 📜 extractor.py        # Prompts Gemini for action items, decisions, and questions
 ┃ ┣ 📜 rag_engine.py       # Handles the RAG pipeline and QA chain
 ┃ ┣ 📜 summarizer.py       # Map-reduce chunk summarization
 ┃ ┣ 📜 transcriber.py      # OpenAI Whisper transcription logic
 ┃ ┗ 📜 vector_store.py     # ChromaDB and HuggingFace embeddings setup
 ┣ 📂 downloads             # Temporary storage for downloaded/chunked audio
 ┣ 📂 utils                 # Helper utilities
 ┃ ┣ 📂 __pycache__
 ┃ ┗ 📜 audio_processor.py  # yt-dlp downloading and PyDub chunking/conversion
 ┣ 📂 vector_db             # Persistent directory for ChromaDB storage
 ┣ 📜 .env                  # Environment variables (API keys)
 ┣ 📜 app.py                # Streamlit web application
 ┣ 📜 main.py               # Command-line interface for the pipeline
 ┣ 📜 requirements.txt      # Python dependencies
 ┗ 📜 test.py               # Testing scripts
```

## 🚀 Installation & Setup

**1. Prerequisites**
You must have `ffmpeg` installed on your system for Whisper and PyDub to process audio.
- **Windows:** Download via [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or use `winget install ffmpeg`
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt update && sudo apt install ffmpeg`

**2. Clone the repository and setup environment**
```bash
git clone <your-repo-url>
cd <your-repo-name>
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up Environment Variables**
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GOOGLE_API_KEY=your_google_api_key_here
WHISPER_MODEL=small  # Optional: tiny, base, small, medium, large
```

## 💻 Usage

### Option 1: Streamlit Web UI (Recommended)
Launch the interactive web application:
```bash
streamlit run app.py
```
1. Paste a YouTube URL or absolute local file path in the sidebar.
2. Click **⚡ Analyse**.
3. Wait for the pipeline to complete (you can view the live progress in the sidebar).
4. Review your summary, action items, and chat with the transcript at the bottom of the page.
<img width="1545" height="5058" alt="FireShot Capture 001 - AI Video Assistant - localhost" src="https://github.com/user-attachments/assets/7f1b0750-167c-41f0-bedf-2c88df721254" />


### Option 2: Command Line Interface
Run the tool directly from your terminal:
```bash
python main.py
```
![Uploading page_3.png…]()


You will be prompted to enter a URL or file path. The analysis results will be printed to your console, followed by an interactive chat loop.

## ⚠️ Notes on API Limits
This application utilizes sleep delays (`time.sleep(10)`) during the extraction and summarization phases. This is an intentional design choice to prevent `429 RESOURCE_EXHAUSTED` errors if you are using the free tier of the Google Gemini API. 
