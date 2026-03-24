# 📄 AI Resume Analyzer & Job Search Agent

🚀 **[Live Demo](https://utssss117-ai-agent-for-job-searching-app-giybur.streamlit.app/)**

An intelligent, AI-driven application designed to help job seekers analyze their resumes, match them against live job postings, evaluate ATS compatibility, and automatically draft cover letters.

The application leverages **Streamlit** for a seamless user interface, **Groq (Llama 3.1)** for blazing-fast LLM operations, and **Supabase (pgvector)** for storing and matching job descriptions using vector embeddings.

## 🌟 Key Features

* **Resume Intelligence Extraction**: Upload a PDF resume, and the AI extracts structured data such as experience, skills, and education into a clean JSON format.
* **Live Job Fetching**: Search and fetch live job postings based on keyword and location directly into your local database.
* **Vector-based Job Matching**: Uses embedding models and Supabase `pgvector` to semantically match your extracted resume skills against saved job descriptions.
* **ATS Evaluation Score**: Get a detailed breakdown of how well your resume matches a specific job, including keyword scores, experience alignment, and missing skills.
* **AI Cover Letter Generator**: With a single click, generate a highly personalized, context-aware cover letter tailored for a specific job match.

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM Provider**: Groq (Llama 3.1)
* **Database & Vector Store**: Supabase (PostgreSQL with `pgvector` extension)
* **Embeddings**: Sentence Transformers (or equivalent for generating 384-dimensional vectors)

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* A [Groq API Key](https://console.groq.com/keys)
* A [Supabase](https://supabase.com/) project

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd AI-Agent-for-Job-Searching
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
pip install -r requirements.txt
```

*(Note: Ensure you have packages like `streamlit`, `groq`, `supabase`, `sentence-transformers`, `PyPDF2`/`pdfminer` installed).*

### 3. Database Setup (Supabase)

1. Create a new Supabase project.
2. Go to the SQL Editor in your Supabase dashboard.
3. Copy the contents of the `setup.sql` file and run it. This will:
   * Enable the `pgvector` extension.
   * Create the `jobs` table with vector embeddings support.
   * Create the `match_jobs` Postgres function for similarity search.

### 4. Environment Variables

Create a `.env` file in the root directory and add the following:

```ini
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```
*(Alternatively, you can provide the Groq API key directly via the Streamlit UI).*

### 5. Run the Application

```bash
streamlit run app.py
```

The app will launch in your default web browser at `http://localhost:8501`.

## ☁️ Deploying to Streamlit Cloud

1. Push your code to a GitHub repository (ensure `.env` is ignored by `.gitignore`).
2. Connect your repository to [Streamlit Cloud](https://share.streamlit.io/).
3. In the Streamlit Cloud dashboard, go to **Settings > Secrets** and paste your `.env` content:
   ```toml
   GROQ_API_KEY = "your_key"
   SUPABASE_URL = "your_url"
   SUPABASE_KEY = "your_key"
   ADZUNA_APP_ID = "your_id"
   ADZUNA_APP_KEY = "your_key"
   ```

## 🧠 How It Works

1. **Dashboard**: Launch the app and enter your settings (API Key, Job Search Preferences).
2. **Fetch Jobs**: Click "Fetch Live Jobs" to populate your Supabase database with relevant, real-world postings.
3. **Upload Resume**: Upload your PDF. The app extracts text and uses Groq to structure the unstructured text.
4. **Analysis & Matching**: The embedding engine compares your resume summary to the jobs in the database.
5. **Insights & Action**: Review your ATS score, discover missing skills, and generate a tailored cover letter.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
