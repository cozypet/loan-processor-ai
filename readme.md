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

---

# PRD: Loan Document Processor Demo - Claude Code Implementation (REVISED)

**Product:** Simple Loan Application Processing Demo with Streamlit UI  
**Target:** Medium article tutorial showcasing Mistral AI capabilities  
**Stack:** Python, Mistral AI (Azure), Streamlit  
**Delivery:** Single-page Streamlit app with minimal UI

---

## 🎯 Executive Summary

Build a **Streamlit web application** that showcases end-to-end loan document processing using Mistral AI's Document AI and Ministral-3B for risk analysis. This demonstrates how financial institutions can automate loan application processing with AI.

**Focus:** Pure Mistral AI showcase - document understanding + intelligent analysis  
**Not About:** Database integrations, MongoDB, or data persistence strategies

---

## 📋 Product Requirements

### Functional Requirements

**Core Workflow:**
1. User uploads 2-3 required loan documents via Streamlit file uploader
2. Extract structured data from each document using Mistral Document AI
3. Analyze combined risk using Ministral-3B with policy-based reasoning
4. Display results in Streamlit UI with clear recommendations

**Required Documents (2-3 minimum):**
1. **Proof of Identity** (ID card, passport, driver's license)
   - Extract: Full name, date of birth, document number, address
   
2. **Proof of Income** (pay slip, employment contract, tax statement)
   - Extract: Employer name, job title, monthly gross income, employment start date
   
3. **Bank Statement** (last 3 months - OPTIONAL but recommended)
   - Extract: Average monthly balance, recurring expenses, existing loan payments

**Risk Assessment Logic:**
- Calculate debt-to-income (DTI) ratio
- Apply bank policy rules:
  - Max DTI: 40%
  - Min employment: 6 months
  - Min monthly income: €2,000
  - Stable income verification
- Generate risk score (0-100), level (LOW/MEDIUM/HIGH)
- Provide recommendation (APPROVE/MANUAL_REVIEW/REJECT)
- Flag policy violations with severity
- Suggest remediation actions

### Non-Functional Requirements

**Code Quality:**
- Clean, tutorial-friendly code structure
- Streamlit best practices (caching, session state)
- Well-commented for Medium article readers
- Production-ready error handling
- Type hints for clarity

**User Experience:**
- Simple, intuitive single-page interface
- Clear upload instructions for each document type
- Real-time processing feedback with progress indicators
- Visual risk indicators (colors, badges)
- Downloadable results summary
- Mobile-friendly layout

**Performance:**
- Use Ministral-3B (fast, efficient, cost-effective)
- Streamlit caching for repeated processing
- Handle PDFs up to 10MB
- Process all documents in < 45 seconds total

**Dependencies:**
- Minimal, well-established libraries only
- `streamlit` for UI
- `mistralai-azure` for Mistral AI
- `python-dotenv` for config
- Standard library otherwise

---

## 🎨 UI/UX Design Specification

### Page Layout

```
┌─────────────────────────────────────────────────────────┐
│  🏦 AI-Powered Loan Application Processor               │
│  Powered by Mistral AI                                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📄 Required Documents                                   │
│                                                          │
│  1. Proof of Identity (Required)                        │
│     [Upload ID Card / Passport / Driver's License]      │
│     Status: ✅ Uploaded: passport.pdf                   │
│                                                          │
│  2. Proof of Income (Required)                          │
│     [Upload Pay Slip / Employment Contract]             │
│     Status: ✅ Uploaded: payslip.pdf                    │
│                                                          │
│  3. Bank Statement (Optional, Recommended)              │
│     [Upload Last 3 Months Statement]                    │
│     Status: ⚪ Not uploaded                             │
│                                                          │
│                 [🚀 Process Application]                 │
│                                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📊 Processing Results                                   │
│                                                          │
│  ╔══════════════════════════════════════════════════╗  │
│  ║  Applicant Information                           ║  │
│  ╠══════════════════════════════════════════════════╣  │
│  ║  Name: Jean Dupont                               ║  │
│  ║  Date of Birth: 1985-03-15                       ║  │
│  ║  Employer: Acme Corp                             ║  │
│  ║  Monthly Income: €3,200                          ║  │
│  ║  Employment Duration: 24 months                  ║  │
│  ╚══════════════════════════════════════════════════╝  │
│                                                          │
│  ╔══════════════════════════════════════════════════╗  │
│  ║  🎯 Risk Assessment                              ║  │
│  ╠══════════════════════════════════════════════════╣  │
│  ║                                                   ║  │
│  ║  Risk Score: 35/100                              ║  │
│  ║  [███████░░░] 🟡 MEDIUM RISK                     ║  │
│  ║                                                   ║  │
│  ║  Debt-to-Income Ratio: 38%                       ║  │
│  ║  (Threshold: 40%)                                ║  │
│  ║                                                   ║  │
│  ║  Recommendation: ⚠️ MANUAL REVIEW                ║  │
│  ║                                                   ║  │
│  ║  Explanation:                                     ║  │
│  ║  Applicant meets most requirements but DTI is    ║  │
│  ║  close to threshold. Recommend verification...   ║  │
│  ║                                                   ║  │
│  ╚══════════════════════════════════════════════════╝  │
│                                                          │
│  🚩 Risk Flags:                                         │
│  🟡 MEDIUM: DTI ratio at 38% (near 40% threshold)       │
│                                                          │
│  💡 Suggested Actions:                                  │
│  • Request recent tax returns for income verification   │
│  • Consider offering smaller loan amount                │
│  • Follow up on employment stability                    │
│                                                          │
│                 [📥 Download Report]                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### UI Components

**Header Section:**
- App title with Mistral AI branding
- Brief description: "Upload loan documents and get instant AI-powered risk assessment"

**Upload Section:**
- 3 file uploaders (2 required, 1 optional)
- Clear labels for each document type
- Upload status indicators (✅ uploaded, ⚪ pending, ❌ error)
- File name display after upload
- Accepted formats: PDF only

**Processing Button:**
- Large, prominent "Process Application" button
- Disabled until minimum 2 documents uploaded
- Shows processing spinner when active

**Results Section (appears after processing):**
- **Applicant Summary Card:** Key extracted data in clean table
- **Risk Assessment Card:** 
  - Large risk score with progress bar
  - Color-coded risk level badge (🟢 LOW / 🟡 MEDIUM / 🔴 HIGH)
  - DTI ratio with visual indicator
  - Clear recommendation with icon
  - Explanation text
- **Risk Flags:** List with severity indicators
- **Suggested Actions:** Bulleted list of next steps
- **Download Button:** Export results as PDF or JSON

**Error Handling:**
- Toast notifications for errors
- Inline validation messages
- Helpful error recovery suggestions

---

## 🏗️ Technical Architecture

### System Flow

```
┌─────────────────────┐
│  User uploads PDFs  │
│  (2-3 documents)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ Streamlit File Uploader     │
│ • Validates file types       │
│ • Stores in session_state    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Process Button Clicked      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ For Each Document:          │
│ Mistral Document AI         │
│ • Extract structured data    │
│ • Type-specific schema       │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Combine Extracted Data      │
│ • Merge from all documents   │
│ • Resolve conflicts          │
│ • Fill missing fields        │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Ministral-3B                │
│ • Risk analysis prompt       │
│ • Policy rule application    │
│ • JSON structured output     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Streamlit Display           │
│ • Format results             │
│ • Show risk assessment       │
│ • Enable download            │
└─────────────────────────────┘
```

### Document-Specific Extraction Schemas

**1. Proof of Identity Schema:**
```json
{
  "document_type": "identity",
  "fields": {
    "full_name": {"type": "string", "required": true},
    "date_of_birth": {"type": "string", "format": "date", "required": true},
    "document_number": {"type": "string", "required": true},
    "document_type": {"type": "string", "enum": ["passport", "id_card", "drivers_license"]},
    "address": {"type": "string", "required": false},
    "nationality": {"type": "string", "required": false},
    "issue_date": {"type": "string", "format": "date", "required": false},
    "expiry_date": {"type": "string", "format": "date", "required": false}
  }
}
```

**2. Proof of Income Schema:**
```json
{
  "document_type": "income",
  "fields": {
    "applicant_name": {"type": "string", "required": true},
    "employer_name": {"type": "string", "required": true},
    "job_title": {"type": "string", "required": true},
    "monthly_gross_income": {"type": "number", "required": true},
    "monthly_net_income": {"type": "number", "required": false},
    "employment_start_date": {"type": "string", "format": "date", "required": true},
    "contract_type": {"type": "string", "enum": ["permanent", "fixed_term", "temporary"], "required": false},
    "payment_date": {"type": "string", "format": "date", "required": false}
  }
}
```

**3. Bank Statement Schema (Optional):**
```json
{
  "document_type": "bank_statement",
  "fields": {
    "account_holder_name": {"type": "string", "required": true},
    "statement_period_start": {"type": "string", "format": "date", "required": true},
    "statement_period_end": {"type": "string", "format": "date", "required": true},
    "average_balance": {"type": "number", "required": false},
    "total_income": {"type": "number", "required": false},
    "total_expenses": {"type": "number", "required": false},
    "recurring_loan_payments": {"type": "number", "required": false},
    "overdraft_occurrences": {"type": "integer", "required": false}
  }
}
```

### Ministral-3B Risk Analysis Output

```json
{
  "risk_score": 35,
  "risk_level": "MEDIUM",
  "debt_to_income_ratio": 0.38,
  "recommendation": "MANUAL_REVIEW",
  "explanation": "Applicant meets most requirements but DTI ratio is close to the 40% threshold. Employment history is stable (24 months) and income is verified. Recommend manual verification of recent financial commitments.",
  "flags": [
    {
      "flag_type": "HIGH_DTI_WARNING",
      "message": "DTI ratio at 38% (near 40% threshold)",
      "severity": "medium"
    }
  ],
  "suggested_actions": [
    "Request recent tax returns for income verification",
    "Consider offering smaller loan amount (€10,000 instead of €15,000)",
    "Follow up on employment stability with employer reference"
  ],
  "policy_compliance": {
    "min_income": {"required": 2000, "actual": 3200, "compliant": true},
    "min_employment_months": {"required": 6, "actual": 24, "compliant": true},
    "max_dti": {"required": 0.40, "actual": 0.38, "compliant": true}
  }
}
```

---

## 🔧 Implementation Specifications

### File Structure
```
loan-processor-streamlit/
├── app.py                    # Main Streamlit application
├── .env                      # Credentials (not in repo)
├── .env.example              # Template for credentials
├── requirements.txt          # Dependencies
├── README.md                 # Setup and usage instructions
└── sample_documents/         # (Optional) Sample PDFs for testing
    ├── sample_passport.pdf
    ├── sample_payslip.pdf
    └── sample_bank_statement.pdf
```

### Environment Variables
```bash
AZURE_MISTRAL_ENDPOINT=https://your-endpoint.inference.ai.azure.com
AZURE_MISTRAL_API_KEY=your-api-key-here
```

### Core Functions

**1. `extract_document_data(pdf_file, document_type: str) -> dict`**
- Read PDF file from Streamlit UploadedFile object
- Select appropriate schema based on document_type
- Call Mistral Document AI with type-specific schema
- Parse and return extracted data
- Handle extraction errors with user-friendly messages

**2. `combine_extracted_data(identity_data: dict, income_data: dict, bank_data: dict | None) -> dict`**
- Merge data from all uploaded documents
- Resolve name conflicts (use identity document as source of truth)
- Calculate additional fields (employment duration in months)
- Fill missing optional fields with defaults
- Return unified applicant profile

**3. `analyze_risk(combined_data: dict, loan_amount: float) -> dict`**
- Build structured prompt with bank policy rules
- Include combined applicant data
- Call Ministral-3B (fast, efficient model)
- Use JSON response format
- Parse and return risk assessment
- Default to REJECT on errors with explanation

**4. `render_results_ui(combined_data: dict, risk_assessment: dict)`**
- Display applicant summary in styled card
- Show risk score with progress bar
- Display risk level with color-coded badge
- Show DTI ratio with visual indicator
- List risk flags with severity icons
- Display suggested actions
- Provide download button for results

**5. `generate_download_report(combined_data: dict, risk_assessment: dict) -> str`**
- Format results as JSON or readable text
- Include timestamp and processing metadata
- Return as downloadable string

**6. Streamlit Main App Flow:**
- Initialize session state for uploaded files
- Render file uploaders with status indicators
- Validate minimum documents uploaded
- Show/hide process button based on validation
- Execute processing pipeline on button click
- Display results with formatted UI
- Handle errors with toast notifications

---

## ✅ Acceptance Criteria

### Must Have
- ✅ Streamlit single-page application
- ✅ 3 file uploaders (2 required: identity + income; 1 optional: bank statement)
- ✅ Clear upload status indicators
- ✅ "Process Application" button (disabled until 2 docs uploaded)
- ✅ Calls Mistral Document AI for each document with type-specific schema
- ✅ Calls Ministral-3B for risk analysis
- ✅ Displays formatted results in Streamlit UI
- ✅ Shows risk score with visual progress bar
- ✅ Color-coded risk level (LOW/MEDIUM/HIGH)
- ✅ Lists risk flags with severity indicators
- ✅ Provides suggested actions
- ✅ Download button for results
- ✅ Uses environment variables for credentials
- ✅ Error handling with user-friendly messages
- ✅ Docstrings for all functions
- ✅ Type hints for function signatures

### Should Have
- ✅ Streamlit caching for repeated processing
- ✅ Processing spinner/progress indicators
- ✅ Loan amount input field (default €15,000)
- ✅ Mobile-responsive layout
- ✅ Clear section headers and visual hierarchy
- ✅ Toast notifications for success/errors
- ✅ Expander widgets for detailed data views

### Nice to Have
- 📝 Sample PDFs for testing (in sample_documents/)
- 📝 README with screenshots
- 📝 .env.example template
- 📝 requirements.txt with pinned versions
- 📝 Streamlit page config (title, icon, layout)
- 📝 Custom CSS for branded styling

### Must Not Have
- ❌ Database persistence (no MongoDB, no SQL)
- ❌ User authentication or sessions
- ❌ Multi-page navigation
- ❌ Batch processing
- ❌ External API integrations (except Mistral)
- ❌ Production deployment configurations
- ❌ Complex state management

---

## 🚀 Success Metrics

**Demo Effectiveness:**
- Can run locally in < 5 minutes (with credentials)
- Processes 2-3 documents in < 45 seconds
- UI is intuitive for non-technical users
- Results are clear and actionable

**Code Quality:**
- Can be explained in a Medium article (< 400 lines)
- Can be understood by intermediate Python developers
- Can be adapted for other document types easily

**Reusability:**
- Can be used as Medium article tutorial code
- Can be demoed live at Mistral AI events
- Can be shared as reference implementation

---

## 🎯 Out of Scope (Explicitly NOT Included)

**v1.0 Does NOT Include:**
- ❌ MongoDB or any database
- ❌ Data persistence between sessions
- ❌ User accounts or authentication
- ❌ Multi-language support
- ❌ Email notifications
- ❌ PDF report generation (only JSON/text download)
- ❌ Batch processing multiple applications
- ❌ Historical application tracking
- ❌ Audit logs
- ❌ Production deployment (Docker, cloud)
- ❌ Advanced analytics or dashboards
- ❌ Integration with loan origination systems

---

## 📋 Pre-Implementation Checklist

**Before Claude Code starts building, confirm:**

- [ ] **Analysis Complete:** Claude Code understands the Streamlit architecture
- [ ] **Todo List Created:** Step-by-step implementation plan with clear checkpoints
- [ ] **Document Types Confirmed:** 3 document types (identity, income, bank statement)
- [ ] **Ministral-3B Validated:** Model name and API confirmed
- [ ] **UI Mockup Understood:** Streamlit layout and component structure clear
- [ ] **Ambiguities Resolved:** All unclear requirements discussed
- [ ] **User Approval:** Implementation plan reviewed and approved

---

## 🤖 Instructions for Claude Code

**Phase 1: Analysis & Planning**
1. Read this PRD thoroughly
2. Research Streamlit best practices for file uploads and multi-step workflows
3. Confirm Ministral-3B model availability and API syntax
4. Create a detailed todo list with:
   - Setup tasks (environment, dependencies)
   - UI implementation tasks (file uploaders, results display)
   - Document extraction tasks (by document type)
   - Risk analysis integration
   - Error handling and validation
   - Testing and refinement
5. Estimate complexity for each task
6. Flag any potential blockers (API unknowns, Streamlit limitations)
7. **WAIT for user validation before coding**

**Phase 2: Implementation** (after approval)
1. Set up Streamlit app structure
2. Implement file upload UI with status tracking
3. Implement document extraction for each type
4. Implement data combination logic
5. Implement risk analysis with Ministral-3B
6. Implement results UI with formatting
7. Add error handling and validation
8. Test with sample documents
9. Create supporting files (README, .env.example, requirements.txt)

**Phase 3: Validation**
1. Run the Streamlit app
2. Test upload workflow with different document combinations
3. Verify extraction accuracy
4. Verify risk analysis output
5. Verify UI display and formatting
6. Test error scenarios
7. Document any deviations from PRD

---

## ❓ Open Questions for Claude Code to Research

1. **Ministral-3B:** Confirm exact model identifier (is it `ministral-3b-latest` or different?)
2. **Mistral Document AI:** Verify `mistral_client.ocr.process()` method signature and response structure
3. **PDF in Streamlit:** Best way to pass UploadedFile to Mistral API (bytes, base64, file-like object?)
4. **Streamlit Caching:** Should we cache extraction results or analysis results?
5. **Download Format:** JSON, text, or both? What format is most useful for users?
6. **Loan Amount Input:** Should this be a fixed field or user-input (adjustable slider)?

---

**Ready for Claude Code analysis and todo list generation.** 🚀

**Key Changes from Original PRD:**
- ✅ Removed all MongoDB references
- ✅ Added Streamlit UI specification
- ✅ Defined 3 document types (identity, income, bank statement)
- ✅ Changed model from Claude Sonnet to Ministral-3B
- ✅ Focused on pure Mistral AI showcase
- ✅ Simplified scope (no database, no persistence)
- ✅ Enhanced UX specification for loan processing workflow