# AI Study Buddy for Students 🎓

An AI-powered learning assistant designed to help students summarize PDFs, transcribe lecture audio, generate flashcards, create quizzes, and ask questions via an AI Tutor. Built with Streamlit, Python, Gemini 2.5 Flash, LangChain, ChromaDB, and OpenAI Whisper.

## ✨ Features

- **PDF Summarizer**: Extract text and summarize PDFs using Gemini.
- **Lecture Audio to Notes**: Transcribe MP3/WAV/M4A files using Whisper and generate structured notes.
- **Flashcard Generator**: Generate interactive Q&A flashcards from study materials.
- **Quiz Generator**: Generate 10-question multiple-choice quizzes with scoring.
- **AI Tutor (RAG)**: Ask context-aware questions from your uploaded documents using ChromaDB and Gemini.

## 🚀 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yaswitha-Chinni/AI-Study-Buddy-GenAI.git
   cd AI_Study_Buddy
   ```

2. **Install System Dependencies:**
   - **Windows**: Install `ffmpeg` via winget: `winget install ffmpeg` or download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add to PATH.
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

3. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   - Ensure your `.env` file is present in the root directory.
   - It should contain:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

5. **Run the App Locally:**
   ```bash
   streamlit run app.py
   ```
   The app will be available at `http://localhost:8501`.

## 🧪 Testing Instructions

1. **PDF Summarizer**: Navigate to the PDF Summarizer page, upload a sample PDF, and click "Generate Summary". Check if the summary is displayed and downloadable.
2. **Audio Notes**: Navigate to the Lecture Notes page, upload a short MP3/WAV file, and wait for Whisper to transcribe and Gemini to generate notes.
3. **Flashcards & Quizzes**: Use the uploaded documents in the Flashcard or Quiz pages to generate interactive UI elements.
4. **AI Tutor**: Go to the AI Tutor page and ask a question based on the content of the PDF or Audio you uploaded. Ensure it answers based on context.

## ☁️ Google Cloud Run Deployment

**Project ID**: `ai-study-buddy-498914`

### Prerequisites
Make sure you have the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated.

```bash
gcloud auth login
gcloud config set project ai-study-buddy-498914
```

### Option 1: Direct Deploy from Source
You can deploy directly to Cloud Run without manually building the container.

```bash
gcloud run deploy ai-study-buddy \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

*(Note: Replace `YOUR_GEMINI_API_KEY_HERE` with your actual Gemini API key before running the command).*

### Option 2: Using Artifact Registry and Cloud Build
1. Create an Artifact Registry repository (if not already created):
   ```bash
   gcloud artifacts repositories create cloud-run-source-deploy --repository-format=docker --location=us-central1
   ```

2. Submit the build using Cloud Build:
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```

3. Update the Environment Variable in Cloud Run:
   After deployment, set the API key using:
   ```bash
   gcloud run services update ai-study-buddy --region us-central1 --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   ```

### 📸 Expected Screenshots Description
- **Home**: A clean, modern UI explaining the tool features.
- **PDF Summarizer**: File uploader with a progress spinner and a markdown-rendered summary text block with a download button.
- **Lecture Notes**: Audio file uploader with expandable raw transcript view and structured notes display.
- **Flashcards**: Expandable Streamlit components revealing questions and answers interactively.
- **Quiz Generator**: Radio buttons for MCQ options and a final score reveal UI.
- **AI Tutor**: Chatbot-style interface (`st.chat_message`) displaying conversation history and context sources.

### Final Live Application URL
Once deployed successfully, Cloud Run will output a URL like `https://ai-study-buddy-xxxxxx-uc.a.run.app`. This is your live application URL.
