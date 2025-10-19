# 🏦 AI-Powered Loan Application Processor

> **🚀 Live Demo:** [https://loan-proceappr-ai-han.streamlit.app/](https://loan-proceappr-ai-han.streamlit.app/)

An AI-powered loan application processing system using Mistral AI's Document AI and Ministral-3B for intelligent risk analysis.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://loan-proceappr-ai-han.streamlit.app/)

> **Note**: The original PRD is preserved below for reference. See "Quick Start" section for setup instructions.

---

## 🚀 Quick Start

### Installation

1. **Create Virtual Environment**:
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure MongoDB**: Update `.env` file with your MongoDB credentials
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=loan_processor
MONGODB_COLLECTION=loan_applications
```

4. **Run Application**:
```bash
# Make sure venv is activated first
source venv/bin/activate  # If not already activated

# Run Streamlit
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Usage

1. Upload 2-3 documents (identity + income required, bank statement optional)
2. Set loan amount using slider
3. Click "Process Application"
4. Review risk assessment results
5. Download JSON report

### Testing

**Sample documents are included** in the `sample_documents/` folder:
- ✅ `sample_passport.pdf` - Sample identity document (325 KB)
- ✅ `sample_fiche_de_paie.pdf` - French payslip / bulletin de salaire (7.3 KB)

You can use these to test the application immediately!

**Additional sample PDFs** available online:
- [Sample Passports](https://www.vfsglobal.com/one-pager/india/australia/passport-services/english/pdf/passport-sample-form.pdf)
- [Sample Pay Slips](https://paysliper.com/payslip-sample-template)
- [Sample Bank Statements](https://www.commercebank.com/-/media/cb/pdf/personal/bank/statement_sample1.pdf)

---

## 🛠️ Environment Management

### Activate Virtual Environment

**Every time** you work on the project, activate the virtual environment first:

```bash
cd "/path/to/IssuranceDocAI"
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

You'll see `(venv)` in your terminal prompt when activated.

### Deactivate Virtual Environment

When done:
```bash
deactivate
```

### Stop the Application

If running in background:
```bash
# Find the process
lsof -ti:8501

# Kill the process
lsof -ti:8501 | xargs kill -9
```

Or simply press `Ctrl+C` if running in terminal.

### Verify Installation

Quick test to verify everything is set up:
```bash
source venv/bin/activate
python test_extraction.py
```

---

## 🐛 Troubleshooting

### Virtual Environment Issues

**Problem**: `venv/bin/activate: No such file or directory`
```bash
# Solution: Create venv first
python3 -m venv venv
```

**Problem**: Wrong Python version
```bash
# Solution: Specify Python 3.12 or later
python3.12 -m venv venv
```

### Port Already in Use

**Problem**: Port 8501 already in use
```bash
# Solution: Use different port
streamlit run app.py --server.port 8502
```

### MongoDB Connection Error

**Problem**: Cannot connect to MongoDB
- Check your `MONGODB_URI` in `.env` file
- Verify your IP is whitelisted in MongoDB Atlas
- Test connection string directly

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`
```bash
# Solution: Make sure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```
