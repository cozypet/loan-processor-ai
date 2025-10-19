"""
AI-Powered Loan Application Processor
Powered by Mistral AI

This Streamlit application demonstrates end-to-end loan document processing using:
- Mistral Document AI for document extraction
- Ministral-3B for risk analysis
- MongoDB for data persistence
"""

import streamlit as st
import requests
import base64
import json
import os
from datetime import datetime
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Configuration - supports both local .env and Streamlit Cloud secrets
def get_config(key, default=None):
    """Get configuration from Streamlit secrets or environment variables."""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        # Fall back to environment variables (for local development)
        return os.getenv(key, default)

DOCAI_ENDPOINT = get_config("AZURE_MISTRAL_DOCAI_ENDPOINT")
DOCAI_KEY = get_config("AZURE_MISTRAL_DOCAI_KEY")
MINISTRAL_ENDPOINT = get_config("AZURE_MINISTRAL_ENDPOINT")
MINISTRAL_KEY = get_config("AZURE_MINISTRAL_KEY")
MINISTRAL_MODEL = get_config("AZURE_MINISTRAL_MODEL")
MONGODB_URI = get_config("MONGODB_URI")
MONGODB_DATABASE = get_config("MONGODB_DATABASE", "loan_processor")
MONGODB_COLLECTION = get_config("MONGODB_COLLECTION", "loan_applications")

# Document type schemas for Mistral Document AI
SCHEMAS = {
    "identity": {
        "properties": {
            "full_name": {"type": "string", "description": "Full name of the person"},
            "date_of_birth": {"type": "string", "description": "Date of birth in YYYY-MM-DD format"},
            "document_number": {"type": "string", "description": "Document identification number"},
            "document_type": {"type": "string", "enum": ["passport", "id_card", "drivers_license"], "description": "Type of identity document"},
            "address": {"type": "string", "description": "Residential address"},
            "nationality": {"type": "string", "description": "Nationality"},
            "issue_date": {"type": "string", "description": "Document issue date"},
            "expiry_date": {"type": "string", "description": "Document expiry date"}
        },
        "required": ["full_name", "date_of_birth", "document_number"],
        "title": "IdentityDocument",
        "type": "object",
        "additionalProperties": False
    },
    "income": {
        "properties": {
            "applicant_name": {"type": "string", "description": "Name of the employee/applicant"},
            "employer_name": {"type": "string", "description": "Name of the employer company"},
            "job_title": {"type": "string", "description": "Job title or position"},
            "monthly_gross_income": {"type": "number", "description": "Monthly gross salary/income in euros"},
            "monthly_net_income": {"type": "number", "description": "Monthly net salary/income in euros"},
            "employment_start_date": {"type": "string", "description": "Employment start date in YYYY-MM-DD format"},
            "contract_type": {"type": "string", "enum": ["permanent", "fixed_term", "temporary"], "description": "Type of employment contract"},
            "payment_date": {"type": "string", "description": "Latest payment date"}
        },
        "required": ["applicant_name", "employer_name", "job_title", "monthly_gross_income", "employment_start_date"],
        "title": "IncomeDocument",
        "type": "object",
        "additionalProperties": False
    },
    "bank_statement": {
        "properties": {
            "account_holder_name": {"type": "string", "description": "Name of the account holder"},
            "statement_period_start": {"type": "string", "description": "Statement period start date"},
            "statement_period_end": {"type": "string", "description": "Statement period end date"},
            "average_balance": {"type": "number", "description": "Average account balance in euros"},
            "total_income": {"type": "number", "description": "Total income/deposits during period"},
            "total_expenses": {"type": "number", "description": "Total expenses/withdrawals during period"},
            "recurring_loan_payments": {"type": "number", "description": "Monthly recurring loan payments"},
            "overdraft_occurrences": {"type": "integer", "description": "Number of overdraft occurrences"}
        },
        "required": ["account_holder_name", "statement_period_start", "statement_period_end"],
        "title": "BankStatement",
        "type": "object",
        "additionalProperties": False
    }
}


def extract_document_data(pdf_file, document_type: str) -> Dict:
    """
    Extract structured data from a PDF document using Mistral Document AI.

    Args:
        pdf_file: Streamlit UploadedFile object
        document_type: Type of document ('identity', 'income', 'bank_statement')

    Returns:
        Dictionary containing extracted data

    Raises:
        Exception: If API call fails or extraction errors occur
    """
    try:
        # Read and encode PDF to base64
        pdf_bytes = pdf_file.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        # Get appropriate schema
        schema = SCHEMAS.get(document_type)
        if not schema:
            raise ValueError(f"Unknown document type: {document_type}")

        # Prepare payload
        payload = {
            "model": "mistral-document-ai-2505",
            "document": {
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{pdf_base64}"
            },
            "bbox_annotation_format": {
                "type": "json_schema",
                "json_schema": {
                    "schema": schema,
                    "name": f"{document_type}_extraction",
                    "strict": True
                }
            },
            "include_image_base64": False
        }

        # Call Mistral Document AI
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DOCAI_KEY}"
        }

        response = requests.post(DOCAI_ENDPOINT, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        # Extract structured data from response
        # Try to get annotation data first, fallback to markdown parsing
        if "pages" in result and len(result["pages"]) > 0:
            page = result["pages"][0]

            # Check for images with annotations
            if "images" in page and len(page["images"]) > 0:
                for image in page["images"]:
                    if "image_annotation" in image:
                        return json.loads(image["image_annotation"]) if isinstance(image["image_annotation"], str) else image["image_annotation"]

            # Fallback: return markdown for manual parsing
            if "markdown" in page:
                return {"raw_text": page["markdown"], "document_type": document_type}

        raise ValueError("No data extracted from document")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Document AI API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Extraction error: {str(e)}")


def combine_extracted_data(identity_data: Dict, income_data: Dict, bank_data: Optional[Dict] = None) -> Dict:
    """
    Combine data from multiple documents into a unified applicant profile.

    Args:
        identity_data: Data from identity document
        income_data: Data from income document
        bank_data: Optional data from bank statement

    Returns:
        Combined applicant profile dictionary
    """
    # Use identity document name as source of truth
    full_name = identity_data.get("full_name", income_data.get("applicant_name", "Unknown"))

    # Calculate employment duration in months
    employment_start = income_data.get("employment_start_date", "")
    employment_months = 0
    if employment_start:
        try:
            start_date = datetime.strptime(employment_start, "%Y-%m-%d")
            today = datetime.now()
            employment_months = (today.year - start_date.year) * 12 + (today.month - start_date.month)
        except:
            employment_months = 0

    # Build combined profile
    combined = {
        "full_name": full_name,
        "date_of_birth": identity_data.get("date_of_birth", ""),
        "document_number": identity_data.get("document_number", ""),
        "address": identity_data.get("address", ""),
        "employer_name": income_data.get("employer_name", ""),
        "job_title": income_data.get("job_title", ""),
        "monthly_gross_income": income_data.get("monthly_gross_income", 0),
        "monthly_net_income": income_data.get("monthly_net_income", income_data.get("monthly_gross_income", 0) * 0.7),
        "employment_start_date": employment_start,
        "employment_months": employment_months,
        "contract_type": income_data.get("contract_type", "unknown"),
    }

    # Add bank statement data if available
    if bank_data:
        combined.update({
            "average_balance": bank_data.get("average_balance", 0),
            "total_expenses": bank_data.get("total_expenses", 0),
            "recurring_loan_payments": bank_data.get("recurring_loan_payments", 0),
            "overdraft_occurrences": bank_data.get("overdraft_occurrences", 0)
        })
    else:
        combined.update({
            "average_balance": None,
            "total_expenses": None,
            "recurring_loan_payments": 0,
            "overdraft_occurrences": None
        })

    return combined


def analyze_risk(combined_data: Dict, loan_amount: float) -> Dict:
    """
    Analyze loan application risk using Ministral-3B.

    Args:
        combined_data: Combined applicant data
        loan_amount: Requested loan amount in euros

    Returns:
        Risk assessment dictionary with score, level, recommendation, etc.
    """
    try:
        # Calculate DTI ratio
        monthly_income = combined_data.get("monthly_gross_income", 0)
        existing_loan_payments = combined_data.get("recurring_loan_payments", 0)
        estimated_monthly_payment = loan_amount * 0.02  # Rough estimate: 2% of loan per month
        total_debt = existing_loan_payments + estimated_monthly_payment
        dti_ratio = total_debt / monthly_income if monthly_income > 0 else 1.0

        # Build prompt for Ministral-3B
        prompt = f"""You are a loan risk assessment AI for a bank. Analyze the following loan application and provide a detailed risk assessment.

BANK POLICY RULES:
- Maximum Debt-to-Income (DTI) ratio: 40% (0.40)
- Minimum employment duration: 6 months
- Minimum monthly gross income: €2,000
- Stable income verification required

APPLICANT DATA:
- Name: {combined_data.get('full_name')}
- Date of Birth: {combined_data.get('date_of_birth')}
- Employer: {combined_data.get('employer_name')}
- Job Title: {combined_data.get('job_title')}
- Monthly Gross Income: €{combined_data.get('monthly_gross_income', 0):,.2f}
- Employment Duration: {combined_data.get('employment_months', 0)} months
- Contract Type: {combined_data.get('contract_type', 'unknown')}
- Existing Loan Payments: €{combined_data.get('recurring_loan_payments', 0):,.2f}/month
- Average Bank Balance: €{combined_data.get('average_balance', 'N/A')}
- Overdraft Occurrences: {combined_data.get('overdraft_occurrences', 'N/A')}

LOAN REQUEST:
- Amount: €{loan_amount:,.2f}
- Estimated Monthly Payment: €{estimated_monthly_payment:,.2f}

CALCULATED METRICS:
- Total Monthly Debt: €{total_debt:,.2f}
- Debt-to-Income Ratio: {dti_ratio:.2%}

Provide your assessment as a JSON object with the following structure:
{{
  "risk_score": <number 0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH>",
  "debt_to_income_ratio": <float>,
  "recommendation": "<APPROVE|MANUAL_REVIEW|REJECT>",
  "explanation": "<detailed explanation>",
  "flags": [
    {{"flag_type": "<type>", "message": "<message>", "severity": "<low|medium|high>"}}
  ],
  "suggested_actions": ["<action 1>", "<action 2>"],
  "policy_compliance": {{
    "min_income": {{"required": 2000, "actual": <value>, "compliant": <true|false>}},
    "min_employment_months": {{"required": 6, "actual": <value>, "compliant": <true|false>}},
    "max_dti": {{"required": 0.40, "actual": <value>, "compliant": <true|false>}}
  }}
}}

Return ONLY the JSON object, no additional text."""

        # Call Ministral-3B
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MINISTRAL_KEY}"
        }

        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": MINISTRAL_MODEL,
            "temperature": 0.3,
            "max_tokens": 2000
        }

        response = requests.post(MINISTRAL_ENDPOINT, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        # Extract response content
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]

            # Try to parse JSON from response
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            risk_assessment = json.loads(content)
            return risk_assessment

        raise ValueError("No response from Ministral-3B")

    except requests.exceptions.RequestException as e:
        # Return safe default on API error
        return {
            "risk_score": 100,
            "risk_level": "HIGH",
            "debt_to_income_ratio": dti_ratio,
            "recommendation": "REJECT",
            "explanation": f"Risk analysis failed due to API error: {str(e)}. Application rejected as safety measure.",
            "flags": [{"flag_type": "SYSTEM_ERROR", "message": "Risk analysis system unavailable", "severity": "high"}],
            "suggested_actions": ["Retry analysis", "Contact IT support"],
            "policy_compliance": {}
        }
    except json.JSONDecodeError as e:
        # Return safe default on parsing error
        return {
            "risk_score": 100,
            "risk_level": "HIGH",
            "debt_to_income_ratio": dti_ratio,
            "recommendation": "REJECT",
            "explanation": f"Risk analysis response parsing failed: {str(e)}. Application rejected as safety measure.",
            "flags": [{"flag_type": "SYSTEM_ERROR", "message": "Risk analysis parsing error", "severity": "high"}],
            "suggested_actions": ["Retry analysis", "Contact IT support"],
            "policy_compliance": {}
        }


def save_to_mongodb(application_data: Dict) -> str:
    """
    Save loan application data to MongoDB.

    Args:
        application_data: Complete application data including risk assessment

    Returns:
        Inserted document ID as string
    """
    try:
        # For development: disable SSL certificate verification on macOS
        # In production, use proper certificates
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            tlsAllowInvalidCertificates=True  # Fix for macOS SSL issues
        )
        db = client[MONGODB_DATABASE]
        collection = db[MONGODB_COLLECTION]

        # Add timestamp
        application_data["created_at"] = datetime.utcnow()

        # Insert document
        result = collection.insert_one(application_data)

        client.close()
        return str(result.inserted_id)

    except Exception as e:
        raise Exception(f"MongoDB error: {str(e)}")


def render_results_ui(combined_data: Dict, risk_assessment: Dict, application_id: Optional[str] = None):
    """
    Render the results section with applicant info and risk assessment.

    Args:
        combined_data: Combined applicant data
        risk_assessment: Risk assessment results
        application_id: MongoDB document ID (optional)
    """
    st.markdown("---")
    st.header("📊 Processing Results")

    if application_id:
        st.success(f"✅ Application saved to database (ID: {application_id})")

    # Applicant Information Card
    st.subheader("👤 Applicant Information")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Full Name", combined_data.get("full_name", "N/A"))
        st.metric("Date of Birth", combined_data.get("date_of_birth", "N/A"))
        st.metric("Employer", combined_data.get("employer_name", "N/A"))

    with col2:
        st.metric("Job Title", combined_data.get("job_title", "N/A"))
        st.metric("Monthly Income", f"€{combined_data.get('monthly_gross_income', 0):,.2f}")
        st.metric("Employment Duration", f"{combined_data.get('employment_months', 0)} months")

    # Risk Assessment Card
    st.markdown("---")
    st.subheader("🎯 Risk Assessment")

    risk_score = risk_assessment.get("risk_score", 0)
    risk_level = risk_assessment.get("risk_level", "UNKNOWN")
    dti_ratio = risk_assessment.get("debt_to_income_ratio", 0)
    recommendation = risk_assessment.get("recommendation", "UNKNOWN")

    # Risk score with progress bar
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.metric("Risk Score", f"{risk_score}/100")
        st.progress(risk_score / 100)

    with col2:
        # Color-coded risk level badge
        if risk_level == "LOW":
            st.success(f"🟢 {risk_level}")
        elif risk_level == "MEDIUM":
            st.warning(f"🟡 {risk_level}")
        else:
            st.error(f"🔴 {risk_level}")

    with col3:
        st.metric("DTI Ratio", f"{dti_ratio:.1%}")
        st.caption("Threshold: 40%")

    # Recommendation
    st.markdown("### Recommendation")
    if recommendation == "APPROVE":
        st.success(f"✅ {recommendation}")
    elif recommendation == "MANUAL_REVIEW":
        st.warning(f"⚠️ {recommendation}")
    else:
        st.error(f"❌ {recommendation}")

    # Explanation
    st.markdown("### Explanation")
    st.info(risk_assessment.get("explanation", "No explanation provided"))

    # Risk Flags
    flags = risk_assessment.get("flags", [])
    if flags:
        st.markdown("### 🚩 Risk Flags")
        for flag in flags:
            severity = flag.get("severity", "medium")
            message = flag.get("message", "")
            if severity == "high":
                st.error(f"🔴 HIGH: {message}")
            elif severity == "medium":
                st.warning(f"🟡 MEDIUM: {message}")
            else:
                st.info(f"🟢 LOW: {message}")

    # Suggested Actions
    suggested_actions = risk_assessment.get("suggested_actions", [])
    if suggested_actions:
        st.markdown("### 💡 Suggested Actions")
        for action in suggested_actions:
            st.markdown(f"• {action}")

    # Policy Compliance (in expander)
    policy_compliance = risk_assessment.get("policy_compliance", {})
    if policy_compliance:
        with st.expander("📋 Policy Compliance Details"):
            for policy_name, policy_data in policy_compliance.items():
                if isinstance(policy_data, dict):
                    required = policy_data.get("required", "N/A")
                    actual = policy_data.get("actual", "N/A")
                    compliant = policy_data.get("compliant", False)

                    status = "✅" if compliant else "❌"
                    st.markdown(f"**{policy_name.replace('_', ' ').title()}**: {status}")
                    st.markdown(f"  - Required: {required}")
                    st.markdown(f"  - Actual: {actual}")


def generate_download_report(combined_data: Dict, risk_assessment: Dict) -> str:
    """
    Generate a downloadable JSON report of the application.

    Args:
        combined_data: Combined applicant data
        risk_assessment: Risk assessment results

    Returns:
        JSON string for download
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "applicant_data": combined_data,
        "risk_assessment": risk_assessment
    }
    return json.dumps(report, indent=2)


# Streamlit App
def main():
    """Main Streamlit application."""

    # Page configuration
    st.set_page_config(
        page_title="AI Loan Processor",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Header
    st.title("🏦 AI-Powered Loan Application Processor")
    st.markdown("**Powered by Mistral AI**")
    st.markdown("Upload loan documents and get instant AI-powered risk assessment")

    # Initialize session state
    if "identity_file" not in st.session_state:
        st.session_state.identity_file = None
    if "income_file" not in st.session_state:
        st.session_state.income_file = None
    if "bank_file" not in st.session_state:
        st.session_state.bank_file = None
    if "processing_complete" not in st.session_state:
        st.session_state.processing_complete = False
    if "combined_data" not in st.session_state:
        st.session_state.combined_data = None
    if "risk_assessment" not in st.session_state:
        st.session_state.risk_assessment = None
    if "application_id" not in st.session_state:
        st.session_state.application_id = None

    # Upload Section
    st.markdown("---")
    st.header("📄 Required Documents")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("1. Proof of Identity")
        st.caption("(Required)")
        identity_file = st.file_uploader(
            "Upload ID Card / Passport / Driver's License",
            type=["pdf"],
            key="identity_uploader"
        )
        if identity_file:
            st.success(f"✅ Uploaded: {identity_file.name}")
            st.session_state.identity_file = identity_file
        else:
            st.info("⚪ Not uploaded")

    with col2:
        st.subheader("2. Proof of Income")
        st.caption("(Required)")
        income_file = st.file_uploader(
            "Upload Pay Slip / Employment Contract",
            type=["pdf"],
            key="income_uploader"
        )
        if income_file:
            st.success(f"✅ Uploaded: {income_file.name}")
            st.session_state.income_file = income_file
        else:
            st.info("⚪ Not uploaded")

    with col3:
        st.subheader("3. Bank Statement")
        st.caption("(Optional, Recommended)")
        bank_file = st.file_uploader(
            "Upload Last 3 Months Statement",
            type=["pdf"],
            key="bank_uploader"
        )
        if bank_file:
            st.success(f"✅ Uploaded: {bank_file.name}")
            st.session_state.bank_file = bank_file
        else:
            st.info("⚪ Not uploaded")

    # Loan Amount Input
    st.markdown("---")
    loan_amount = st.slider(
        "💰 Requested Loan Amount (€)",
        min_value=5000,
        max_value=50000,
        value=15000,
        step=1000,
        format="€%d"
    )

    # Process Button
    st.markdown("---")
    can_process = st.session_state.identity_file is not None and st.session_state.income_file is not None

    if st.button("🚀 Process Application", disabled=not can_process, type="primary", use_container_width=True):
        try:
            # Create a container for step-by-step results
            progress_container = st.container()

            with progress_container:
                # Step 1: Extract identity document
                with st.spinner("📄 Extracting identity document..."):
                    identity_data = extract_document_data(st.session_state.identity_file, "identity")
                st.success(f"✅ Identity extracted: {identity_data.get('full_name', 'N/A')}, DOB: {identity_data.get('date_of_birth', 'N/A')}")
                with st.expander("🔍 View identity data"):
                    st.json(identity_data)

                # Step 2: Extract income document
                with st.spinner("📄 Extracting income document..."):
                    income_data = extract_document_data(st.session_state.income_file, "income")
                st.success(f"✅ Income extracted: {income_data.get('employer_name', 'N/A')}, Salary: €{income_data.get('monthly_gross_income', 0):,.2f}")
                with st.expander("🔍 View income data"):
                    st.json(income_data)

                # Step 3: Extract bank statement (if provided)
                bank_data = None
                if st.session_state.bank_file:
                    with st.spinner("📄 Extracting bank statement..."):
                        bank_data = extract_document_data(st.session_state.bank_file, "bank_statement")
                    st.success(f"✅ Bank statement extracted: Balance: €{bank_data.get('average_balance', 'N/A')}")
                    with st.expander("🔍 View bank statement data"):
                        st.json(bank_data)

                # Step 4: Combine data
                with st.spinner("🔄 Combining extracted data..."):
                    combined_data = combine_extracted_data(identity_data, income_data, bank_data)
                st.success(f"✅ Data combined: {combined_data.get('full_name', 'N/A')} - {combined_data.get('employment_months', 0)} months employed")
                with st.expander("🔍 View combined applicant profile"):
                    st.json(combined_data)

                # Step 5: Analyze risk
                with st.spinner("🎯 Analyzing risk with Ministral-3B..."):
                    risk_assessment = analyze_risk(combined_data, loan_amount)
                st.success(f"✅ Risk analysis complete: {risk_assessment.get('risk_level', 'N/A')} risk, Score: {risk_assessment.get('risk_score', 0)}/100")
                with st.expander("🔍 View risk assessment"):
                    st.json(risk_assessment)

                # Step 6: Save to MongoDB
                with st.spinner("💾 Saving to database..."):
                    application_data = {
                        "applicant_data": combined_data,
                        "risk_assessment": risk_assessment,
                        "loan_amount": loan_amount
                    }
                    application_id = save_to_mongodb(application_data)
                st.success(f"✅ Saved to database: ID {application_id[:8]}...")

                # Store in session state
                st.session_state.combined_data = combined_data
                st.session_state.risk_assessment = risk_assessment
                st.session_state.application_id = application_id
                st.session_state.processing_complete = True

            st.success("🎉 Processing complete! Scroll down to see full results.")
            st.balloons()

            # Small delay before rerun to let user see the success message
            import time
            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            st.error("Please check your documents and try again.")
            # Show error details in expander
            with st.expander("🐛 View error details"):
                import traceback
                st.code(traceback.format_exc())

    # Display Results
    if st.session_state.processing_complete and st.session_state.combined_data and st.session_state.risk_assessment:
        render_results_ui(
            st.session_state.combined_data,
            st.session_state.risk_assessment,
            st.session_state.application_id
        )

        # Download Button
        st.markdown("---")
        report_json = generate_download_report(
            st.session_state.combined_data,
            st.session_state.risk_assessment
        )
        st.download_button(
            label="📥 Download Report (JSON)",
            data=report_json,
            file_name=f"loan_application_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    elif not can_process:
        st.warning("⚠️ Please upload at least Identity and Income documents to proceed.")


if __name__ == "__main__":
    main()
