# AI-Native Cyber Insurance Underwriting POC

A modular proof of concept for AI-augmented cyber insurance underwriting that combines rule-based risk scoring, machine learning classification, and optional AI-generated analysis to support underwriting decisions.

## 🎯 Project Overview

This POC demonstrates how artificial intelligence and machine learning can enhance cyber insurance underwriting by:
- **Automating risk scoring** with explainable rule-based engine
- **Classifying risk levels** using ML (Critical/High/Medium/Low)
- **Generating insights** with AI summaries (optional, requires API key)
- **Tracking assessments** with historical data and analytics

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite, Pydantic
- **Frontend**: Streamlit
- **AI/LLM**: LangChain + OpenAI (optional)
- **ML**: Scikit-Learn Random Forest classifier
- **Database**: SQLite

### Project Structure
```
cyber-underwriting-poc/
├── app/
│   ├── api/routes.py              # FastAPI endpoints
│   ├── models/                    # SQLAlchemy models
│   ├── services/                  # Business logic (risk engine, AI, ML)
│   ├── repositories/              # Database access layer
│   ├── prompts/                   # AI prompt templates
│   └── utils/                     # Configuration & logging
├── frontend/app.py                # Streamlit dashboard
├── tests/                         # Unit tests
├── sample_data/                   # Historical underwriting data
├── main.py                        # FastAPI entry point
└── requirements.txt               # Python dependencies
```

## ✨ Features

### 1. Company Assessment Page
- Interactive form with 13 cyber security assessment fields:
  - MFA Enabled, EDR Enabled, Backup Strategy
  - Phishing Training, Incident Response Plan, Patch Management
  - Encryption, Third Party Risk, Previous Claims
  - Company info (name, industry, revenue, employees)
- **Outputs**: Risk Score (0-100), Risk Category, Premium, AI Summary

### 2. Risk Dashboard
- **Table view** of all historical underwriting results
- **Summary metrics**:
  - Total assessments performed
  - Average risk score
  - Total premium calculated
  - Count of critical cases
- Quick insights into portfolio risk

### 3. AI Underwriting Report
- **Company selector** dropdown to view specific reports
- **Detailed analysis**:
  - Risk Score and Category
  - Insurance Premium
  - Executive Summary (AI-generated or default)
  - Recommendations list
- Deep dive into individual assessments

### 4. Home Page
- Overview and quick start guide
- Navigation cards for each section
- 5-step "How It Works" workflow
- Key features highlight

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)

## Setup

1. Navigate to project directory:
   ```bash
   cd cyber-underwriting-poc
   ```

2. Install Python 3.11 and verify:
   ```bash
   python --version
   ```

3. Create and activate virtual environment:

   **macOS/Linux:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

   **Windows (Command Prompt):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the backend API (Terminal 1):
   ```bash
   uvicorn main:app --reload
   ```

6. Start the Streamlit frontend (Terminal 2):

   **macOS/Linux:**
   ```bash
   cd cyber-underwriting-poc
   source venv/bin/activate
   streamlit run frontend/app.py
   ```

   **Windows (Command Prompt):**
   ```cmd
   cd cyber-underwriting-poc
   venv\Scripts\activate.bat
   streamlit run frontend/app.py
   ```

   **Windows (PowerShell):**
   ```powershell
   cd cyber-underwriting-poc
   venv\Scripts\Activate.ps1
   streamlit run frontend/app.py
   ```

## Access the Application

- **Frontend Dashboard**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables (`.env` file)
```
OPENAI_API_KEY=your-api-key-here  # Optional: for AI summaries
OPENAI_MODEL=gpt-4o-mini           # AI model to use
DATABASE_URL=sqlite:///./cyber_underwriting.db
ENVIRONMENT=development
```

**Note**: Leave `OPENAI_API_KEY` empty to use fallback (default) summaries.

## 📊 API Endpoints

### Underwriting
- `POST /underwrite` - Run full underwriting assessment
  - Input: Company info + security questionnaire
  - Output: Risk score, category, premium, AI summary

### Results
- `GET /results` - List all underwriting results
- `GET /results/{result_id}` - Get specific result details

### Assessment
- `POST /assessment` - Save assessment data
- `GET /assessment/{assessment_id}` - Retrieve assessment

### Company
- `GET /companies` - List all companies

## 📈 Data Flow

```
1. User fills assessment form in Streamlit
   ↓
2. Form submitted to FastAPI backend (/underwrite endpoint)
   ↓
3. Backend processes:
   - Saves company & assessment data to SQLite
   - Calculates risk score (rule engine)
   - Generates AI summary (if API key available)
   - Predicts risk category (ML model)
   ↓
4. Results returned to frontend
   ↓
5. Results displayed in dashboard
   ↓
6. Historical data available in Risk Dashboard & AI Report pages
```

## 🔍 Risk Scoring Logic

### Rule-Based Engine
Evaluates 9 security factors:
- MFA, EDR, Backup Strategy, Phishing Training, Incident Response
- Patch Management, Encryption, Third Party Risk, Previous Claims

### Output Categories
- **Critical** (80-100): Immediate security improvements needed
- **High** (60-79): Significant risk mitigation required
- **Medium** (40-59): Standard cyber insurance coverage
- **Low** (0-39): Good security posture

## 📝 Recent Updates (2026-07-15)

### Fixed
- ✅ OpenAI API key configuration error (401 errors)
- ✅ Risk Dashboard was empty placeholder

### Implemented
- ✅ Risk Dashboard with historical results table
- ✅ AI Underwriting Report with detailed analysis
- ✅ Enhanced Home page with guidance
- ✅ New `/results` API endpoint
- ✅ `ResultRepository.get_all()` method for database queries

### Current Status
- ✅ All pages fully functional
- ✅ Data flow working correctly
- ✅ Database persistence working
- ✅ Auto-reload enabled (no restart needed for code changes)

## 📚 Testing

Run unit tests:
```bash
pytest tests/
```

Included tests:
- `test_api.py` - API endpoint tests
- `test_ml_model.py` - ML model tests
- `test_risk_engine.py` - Risk calculation tests
- `test_premium.py` - Premium calculation tests

## 🎓 Sample Data

The project includes historical underwriting data in `sample_data/historical_underwriting.csv` for ML model training.
## 📸 Screenshots

Screenshots are stored in `docs/screenshots/`. Add your screenshots using these names:
- `01-home-page.png` - Home page overview
- `02-company-assessment.png` - Assessment form and results
- `03-risk-dashboard.png` - Risk Dashboard with results table
- `04-ai-report.png` - AI Underwriting Report page
##  Future Enhancements

- [ ] Add charting/visualization to Risk Dashboard
- [ ] Data export (CSV/PDF reports)
- [ ] Advanced filtering and search
- [ ] User authentication & role-based access
- [ ] Real-time API key validation
- [ ] Multi-tenancy support
- [ ] Integration with insurance platforms
- [ ] Compliance reporting (SOC2, ISO 27001)

## 🤝 Contributing

This is a Xebia capstone project. For contributions or questions, contact the development team.

## 📄 License

Internal Xebia project - confidential

---

**Last Updated**: 2026-07-15  
**Status**: ✅ MVP Complete - All Core Features Functional