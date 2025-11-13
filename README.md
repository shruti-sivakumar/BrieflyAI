# BrieflyAI

BrieflyAI is a full-stack web application that generates high-quality summaries from text, URLs, and documents using state-of-the-art AI models. Compare BART and Pegasus summaries side-by-side, save your history, and provide feedback to help improve the system.

---

## Features

- **Multiple Input Methods**: Summarize raw text, web articles (URLs), or upload files (TXT, PDF, DOCX)
- **Dual AI Models**: Compare summaries from BART-large-CNN and Pegasus-XSum
- **Smart Caching**: Redis-powered caching for faster repeat summarizations
- **User Authentication**: Supabase auth with magic link sign-in
- **History Tracking**: View all your past summaries in one place
- **Feedback System**: Rate summaries and help improve the models
- **Download & Copy**: Export summaries as text files or copy to clipboard
- **Responsive Design**: Simple and elegant UI built with Next.js 14 and Tailwind CSS

---

## Screenshots
Some screenshots of the results:

### Text Summary
![Text Summary](screenshots/text_summary.jpg)

### URL Summary
![URL Summary](screenshots/url_summary.jpg)

### URL Summary
![File Summary](screenshots/file_summary.jpg)

### User History
![User History](screenshots/history.jpg)

---

## Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS** + **shadcn/ui**
- **Zustand** (State management)
- **Supabase** (Authentication)
- **Axios** (API calls)

### Backend
- **FastAPI** (Python)
- **Transformers** (Hugging Face models)
- **PyTorch**
- **PostgreSQL** (via Supabase)
- **Redis** (Caching)
- **SQLAlchemy** (ORM)
- **newspaper3k** (URL extraction)
- **PyPDF2** & **python-docx** (File parsing)

---

## Prerequisites

- **Next.js** 18+ and npm
- **Python** 3.9+
- **PostgreSQL** database (Supabase account)
- **Redis** instance (local or cloud)
- **Supabase** account for authentication

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shruti-sivakumar/brieflyai.git
cd brieflyai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit `backend/.env`:**

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@YOUR_HOST.supabase.co:5432/postgres?sslmode=require
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379
SUPABASE_JWT_SECRET=your-supabase-jwt-secret
```

**Run the backend:**

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
```

**Edit `frontend/.env.local`:**

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

**Run the frontend:**

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg2://user:pass@host:5432/db` |
| `SECRET_KEY` | Application secret key | `your-random-secret-key` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SUPABASE_JWT_SECRET` | JWT secret from Supabase | Found in Supabase dashboard |

### Frontend (`frontend/.env.local`)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API endpoint | `http://localhost:8000/api` |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | Found in Supabase dashboard |

---

## Project Structure

```
brieflyai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   ├── auth.py            # Authentication logic
│   │   │   ├── config.py          # Configuration
│   │   │   └── database.py        # Database setup
│   │   ├── ml/
│   │   │   ├── bart_model.py      # BART model wrapper
│   │   │   └── pegasus_model.py   # Pegasus model wrapper
│   │   ├── models/
│   │   │   └── database.py        # SQLAlchemy models
│   │   ├── services/
│   │   │   ├── extraction.py      # Text extraction
│   │   │   └── summarization.py   # Main service logic
│   │   ├── utils/
│   │   │   └── cache.py           # Redis caching
│   │   └── main.py                # FastAPI app
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── app/
│   │   ├── history/
│   │   │   └── page.tsx           # History page
│   │   ├── globals.css
│   │   ├── layout.tsx             # Root layout
│   │   └── page.tsx               # Home page
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   ├── AuthControls.tsx
│   │   ├── FeedbackDialog.tsx
│   │   └── SummaryCard.tsx
│   ├── lib/
│   │   ├── api.ts                 # API client
│   │   ├── store.ts               # Zustand store
│   │   ├── supabase.ts            # Supabase client
│   │   └── utils.ts
│   ├── package.json
│   └── .env.example
│
└── README.md
```

---

## API Endpoints

### Summarization

- `POST /api/summarize/text` - Summarize raw text
- `POST /api/summarize/url` - Summarize content from URL
- `POST /api/summarize/file` - Summarize uploaded file

### History & Feedback

- `GET /api/summaries/{user_id}` - Get user's summary history
- `POST /api/summaries/{summary_id}/feedback` - Submit feedback

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Performance Tips

- **First Load**: Models download on first run (~2GB). Subsequent loads are instant.
- **GPU Acceleration**: Backend automatically uses CUDA if available
- **Caching**: Summaries are cached for 24 hours to improve response times
- **Rate Limiting**: Consider implementing rate limits in production
  
---

<div align="center">
  <p>Built with ♥︎ using FastAPI • Next.Js • Pegasus • BART • Redis • Supabase</p>
</div>