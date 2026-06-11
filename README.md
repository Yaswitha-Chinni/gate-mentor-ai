# GateMaster AI

GateMaster AI is a comprehensive study companion and roadmap generator designed for GATE CSE aspirants. 

It generates personalized, AI-driven timelines, offers rich study materials (PDF notes, MCQs, and Playlists), and provides an interactive AI Study Coach to help students reach their goals.

### 🌐 Live Demo
You can view the fully functional, live version of the platform here:
**[https://gate-mentor-ai-vtywbp3oqq-uc.a.run.app](https://gate-mentor-ai-vtywbp3oqq-uc.a.run.app)**

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript (Vanilla, no framework)
- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **AI Integration:** Google Gemini 2.5 Flash

## How to Run Locally

If you downloaded the repository and want to run it on your own machine:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Google Gemini API Key:**
   Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and export it:
   ```bash
   # Windows PowerShell
   $env:GOOGLE_API_KEY="your-api-key"
   ```

3. **Start the FastAPI Server:**
   ```bash
   uvicorn api:app --reload
   ```

4. **View the Website:**
   Open your browser and navigate to the main URL:
   `http://localhost:8000`
