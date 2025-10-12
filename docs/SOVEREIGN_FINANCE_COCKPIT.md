# Sovereign Finance Cockpit

This document describes a web-based application designed to empower individuals to take control of their financial sovereignty.

---

## Features

- **User Profile:** Store your personal information for easy use in all generated documents.
- **Creditor Address Book:** Manage a list of your creditors and their contact information.
- **Vehicle Financing Analysis:**
  - **TILA Disclosure Validation:** Analyze vehicle financing contracts for compliance with the Truth in Lending Act (TILA).
  - **Remedy Generation:** Generate remedy letters for TILA violations.
  - **Contract Scanning:** Scan contracts for specific terms such as hidden fees, misrepresentation, and arbitration clauses.
- **Credit Report Analysis (FCRA):**
  - **Dispute Letter Generation:** Generate dispute letters for inaccuracies found on your credit report, in accordance with the Fair Credit Reporting Act (FCRA).
- **FDCPA Debt Collector Log:**
  - **Violation Logging:** Log instances of abusive or unfair debt collection practices as defined by the Fair Debt Collection Practices Act (FDCPA).
  - **Cease and Desist Letters:** Prepare and generate Cease and Desist letters to debt collectors.
- **Monthly Bill Endorsement:**
  - **Bill Endorsement:** Upload and digitally endorse bills and other financial instruments.
  - **Negotiability Validation:** Validate the negotiability of financial instruments.
  - **Tender Letters and Notices:** Generate tender letters and notices for non-negotiable instruments.
- **Legal Resources:** Access a curated list of commentary and case law relevant to financial sovereignty.
- **Sovereign Loop:** Track your progress through the key stages of financial remedy: Intake, Validate, Remedy, Log, and Reflect.

---

## Setup and Running

### 1. Clone the repository:
```bash
git clone https://github.com/kdmartin-boop/sovereign-financial-cockpit.git
cd sovereign-financial-cockpit
```

### 2. Install backend dependencies:
This project uses Python and Flask for the backend.
```bash
pip install -r requirements.txt
```

### 3. Install frontend dependencies and build:
The frontend is built with React and Vite.
```bash
npm install
npm run build
```

### 4. Create the `uploads` directory:
The application requires an `uploads` directory to store uploaded files.
```bash
mkdir uploads
```

### 5. Run the project:
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000` in your web browser.
