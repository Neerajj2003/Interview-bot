# Interview-bot

The DOTCOD Interview Bot is more than just a mock interview tool — it’s your personalized AI career coach. Leveraging state-of-the-art technology like Google Gemini, FAISS, and LangChain, this assistant creates tailored, intelligent, and interactive interview experiences based on your actual resume and the specific job role you're targeting.

Whether you're preparing for your first job, switching careers, or just refining your skills, this bot gives you:

✅ A focused and distraction-free environment

🔁 Unlimited practice rounds with instant feedback storage

📥 Downloadable Q&A logs for self-review or mentorship

💡 Real-time question generation driven by semantic understanding

Built with love and innovation at DOTCOD Innovations, this tool represents the future of career development — one where AI doesn't replace the candidate, but amplifies your potential.

🚀 Polish your pitch. Sharpen your story. Own your interview.


# What It Does

AI Interview Assistant using Gemini, FAISS, LangChain, and Streamlit
Upload Resume + Job Description → Auto-generate interview questions
Interactive mock interview with Q&A + downloadable summary


# Tech Stack

LLM: Google Gemini (embedding-001, gemini-2.0-flash)
Framework: LangChain + Streamlit
Vector Search: FAISS
PDF Parsing: PyPDFLoader
Env Management: python-dotenv


# How It Works

Upload PDFs → Extract & Chunk text
Embed with Gemini → Store in FAISS
Generate questions via LangChain chain
User answers → Stores Q&A
Export summary after interview


# Setup

bash
Copy
Edit
git clone <repo>
pip install -r requirements.txt
#.env file
GOOGLE_API_KEY=your_key
streamlit run app.py


# requirements.txt

nginx
Copy
Edit
streamlit
langchain
langchain-google-genai
faiss-cpu
python-dotenv
PyPDF2


# File Structure

bash
Copy
Edit
├── app.py
├── .env
├── requirements.txt
├── README.md

<img width="1883" height="799" alt="Screenshot 2025-07-29 234654" src="https://github.com/user-attachments/assets/bb31548c-3fbe-4bfe-bbfa-bd2a3ae6164c" />





# Output
Mock Interview with tailored questions
Editable Q&A form
Summary report (.txt)
