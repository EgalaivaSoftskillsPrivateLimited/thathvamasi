# Standard Operating Procedure (SOP)
## Frontend Architecture, Intake Pipelines & HR Operations
**Organization:** Thathvamasi HR Consultancy (THC)  
**Location:** Coimbatore, Tamil Nadu, India  
**Document Ref:** THC-SOP-FE-2026-V1  
**Version:** 1.0.0  
**Effective Date:** October 5, 2026  
**Review Cycle:** Annual / Upon Major Architecture Revision  

---

## 1. Document Control & Objective

### 1.1 Purpose
This Standard Operating Procedure (SOP) governs the technical codebase architecture, directory taxonomy, lead intake pipelines, candidate resume management, corporate hiring requisition workflows, and administrative operations of the **Thathvamasi HR Consultancy (THC)** web platform.

### 1.2 Target Audience
- Frontend Engineering & DevOps Teams
- Talent Acquisition Directors & HR Consultants
- Content Management Specialists
- Administrative Stakeholders

---

## 2. SOP-01: Architectural Taxonomy & Directory Structure

The project is structured according to modular enterprise frontend engineering principles, separating assets, configurations, core libraries, user interface components, and operations.

```
thathvamasi/
├── .github/                         # Continuous Integration / Continuous Deployment
│   └── workflows/
│       └── deploy.yml              # Automated build & verification pipeline
├── .vscode/                        # IDE Configuration & Workspace Standards
│   └── settings.json               # Formatting, line wrap, and validation rules
├── docs/                           # Documentation & Compliance Manuals
│   └── SOP_FRONTEND_AND_OPERATIONS.md # Master Technical & Operational SOP
├── frontend/                       # Frontend Web Application Root
│   ├── public/                     # Public Static Assets (Served at root '/')
│   │   ├── images/                 # Categorized Brand & Media Assets
│   │   │   ├── logo/               # Brand monograms & corporate seals
│   │   │   ├── heroes/             # High-resolution hero visuals
│   │   │   ├── team/               # Executive leadership & consulting team
│   │   │   └── campus/             # Tech campus & ecosystem photography
│   │   ├── favicon.ico             # Browser tab favicon
│   │   └── robots.txt              # Search engine indexing directives
│   ├── services/                   # Multi-Page Practice HTML Entry Points
│   │   ├── index.html              # Services Overview & Practice Hub
│   │   ├── executive-search.html   # Practice Deep Dive Pages...
│   ├── src/                        # Source Code Root
│   ├── components/                 # Component Library
│   │   ├── ui/                     # Primitives (Toast, Modal, Dialog)
│   │   │   ├── Toast.js            # Global notification dispatcher
│   │   │   └── Modal.js            # Accessible dialog controller
│   │   ├── layout/                 # Structural Layout Controllers
│   │   ├── sections/               # Page Section Controllers
│   │   │   ├── Services.js         # Interactive capability cards & filter tabs
│   │   │   └── Insights.js         # Thought leadership blog grid & search
│   │   ├── forms/                  # Lead Capture & Intake Form Controllers
│   │   │   ├── CandidateRegistrationForm.js # Multi-step candidate registration
│   │   │   ├── ClientRequisitionForm.js     # Corporate hiring intake form
│   │   │   └── ContactForm.js               # General inquiry & WhatsApp dispatch
│   │   └── admin/                  # Command Center & Operations Module
│   │       └── AdminDashboard.js   # Analytics, table filters, status & CSV export
│   ├── styles/                     # Vanilla CSS Modular Design System
│   │   ├── variables.css           # Design tokens, color palette, gradients, glassmorphism
│   │   ├── base.css                # Typography reset, layout containers, animations
│   │   ├── components.css          # Navbars, buttons, cards, dropzones, steppers
│   │   ├── admin.css               # KPIs, bar charts, data tables, status badges
│   │   └── responsive.css          # Breakpoints for tablet, mobile, and desktop
│   ├── lib/                        # Shared Utilities & Infrastructure
│   │   ├── storage.js              # LocalStorage state manager & event bus
│   │   ├── validation.js           # Email, phone, file size & type validators
│   │   └── csvExporter.js          # RFC 4180 compliant CSV generator
│   ├── config/                     # Domain & Business Configurations
│   │   ├── site.config.js          # Brand identity, address, phone, social URLs
│   │   └── services.config.js      # Detailed service descriptions & deliverables
│   ├── data/                       # Initial Domain Seed Data
│   │   └── mockData.js             # Realistic candidates, clients, blogs, and metrics
│   └── main.js                     # Master Application Entry Point
├── .env.example                    # Environment variable template
├── .gitignore                      # Git exclusion rules
├── index.html                      # Semantic HTML5 Master Document
├── package.json                    # NPM package metadata and build scripts
└── README.md                       # Repository overview & setup guide
```

---

## 3. SOP-02: Candidate Application & Resume Ingestion Workflow

### 3.1 Step-by-Step Flow
1. **Intake Trigger:** The candidate navigates to the `#candidates` section or clicks "Submit Resume".
2. **Step 1 - Personal & Contact Authentication:**
   - Full Name: Minimum 2 characters.
   - Email: Standard RFC email regex validation.
   - Mobile: 10 to 13 digits Indian telephone validation format.
   - Current Location & Preferred Location.
3. **Step 2 - Professional Calibrations:**
   - Highest Qualification (Degree dropdown).
   - Experience Bracket (0-2 years, 3-5 years, 6-9 years, 10-15 years, 15+ years).
   - Current Employer & Current Designation.
   - Current CTC (LPA) & Expected CTC (LPA).
   - Notice Period (Immediate, 15, 30, 45, 60, 90 days).
   - Core Skills (Tags separated by comma).
4. **Step 3 - Resume File Verification & DPDP Consent:**
   - Permitted formats: `.pdf`, `.doc`, `.docx`.
   - Size limit: 5MB maximum.
   - Drag-and-drop or file picker interaction.
   - Checkbox verification confirming adherence to the Indian Digital Personal Data Protection (DPDP) Act.
5. **System Response & Storage:**
   - Generates unique reference code: `THC-CAN-xxxxx`.
   - Persists entry into storage pipeline.
   - Displays confirmation dialog showing Reference ID and next steps.
   - Emits `thc:data-changed` event to update the HR Admin Command Center in real time.

---

## 4. SOP-03: Employer Hiring Requisition & SLA Management Workflow

### 4.1 Requirement Intake Protocol
1. **Corporate Client Submission:**
   - Company Name, Contact Person, Official Corporate Email, Direct Mobile.
   - Position Title, Number of Vacancies (1-100), Target Location.
   - Industry Vertical selection (IT, Manufacturing, Textile, Healthcare, BFSI).
   - Indicative Budget / CTC Range and Expected Joining Timeline.
   - Detailed Job Description or summary of mandatory skills.
2. **Requisition Dispatch:**
   - System validates business email and required role parameters.
   - Assigns unique corporate requisition tracking code: `THC-REQ-xxxxx`.
   - Sets initial status to `open`.
   - Triggers customer confirmation dialog highlighting the **48-Hour Shortlist Guarantee**.
3. **Internal SLA Milestones:**
   - **T + 2 Hours:** Dedicated Senior Account Director initiates requirement intake call with client.
   - **T + 24 Hours:** Candidate database queried, 4-tier qualification assessment executed.
   - **T + 48 Hours:** Initial calibrated batch of 3-5 validated dossiers submitted to the client.

---

## 5. SOP-04: HR Admin Command Center Operational Manual

### 5.1 Accessing the Admin Console
- Click the **"HR Admin Portal"** button located in the top announcement bar or footer.
- The platform shifts into administrative inspection mode without page reloading.

### 5.2 Candidate Pipeline Status Transitions
Candidates progress through defined lifecycle states:
- `new`: Initial intake; profile pending initial recruiter review.
- `contacted`: Recruiter has held preliminary intake screening call.
- `shortlisted`: Profile verified through 4-Tier Matrix; presented to client.
- `rejected`: Profile does not meet baseline criteria or failed verification.

### 5.3 Exporting Pipeline to CSV
1. In the Admin Portal, select the **"Candidates"** tab.
2. Filter or search as needed.
3. Click **"Export CSV"**.
4. The system triggers an instant download of `THC_Candidates_Registry_YYYY-MM-DD.csv`, formatted with standard headers for importing into enterprise ATS/CRM systems (Workday, Zoho Recruit, Greenhouse, Salesforce).

---

## 6. SOP-05: Content & Blog Publishing Protocol

### 6.1 Publishing New Market Insights
1. Navigate to Admin Portal -> **"Publish Blog"** tab.
2. Provide:
   - **Article Title:** Compelling, search-optimized title.
   - **Category:** Select from `HR Compliance`, `Hiring Trends`, `Recruitment Strategy`, or `Career Guidance`.
   - **Reading Time:** Estimated read time (e.g., "5 min read").
   - **Author:** Desk or specialist attribution.
   - **Excerpt:** 2-3 sentence executive synopsis.
   - **Body Content:** Complete body text (HTML tags supported).
3. Click **"Publish Insight Now"**.
4. The article is immediately indexed in the insights catalog, searchable, and readable via the interactive reader modal.

---

## 7. SOP-06: Local Development, Environment Setup & Deployment

### 7.1 Local Development Prerequisites
- **Node.js:** v20.x or higher
- **npm:** v10.x or higher

### 7.2 Execution Runbook
```bash
# 1. Clone repository
git clone https://github.com/EgalaivaSoftskillsPrivateLimited/thathvamasi.git
cd thathvamasi

# 2. Install dependencies
npm install

# 3. Start local development server with Hot Module Replacement (HMR)
npm run dev

# 4. Create production build
npm run build

# 5. Preview production build locally
npm run preview
```

### 7.3 Deployment Targets
The production bundle is generated in the `dist/` directory and can be deployed directly to:
- **Vercel:** Connect GitHub repository; Root Directory: `./`, Build Command: `npm run build`, Output Directory: `dist`.
- **Cloudflare Pages / Netlify / AWS S3 + CloudFront:** Standard static SPA deployment.

---

## 8. SOP-07: Data Privacy & Security Compliance

1. **DPDP Compliance (India):** All candidate records are collected under explicit affirmative consent via the checkbox requirement.
2. **File Sanitization:** Files are validated on extension (`.pdf`, `.doc`, `.docx`) and restricted to under 5MB to prevent denial-of-service and malicious payload delivery.
3. **No External Leaks:** Sensitive candidate phone numbers and compensation details are displayed exclusively within the administrative console.

---

## 9. SOP-08: Maintenance & Troubleshooting

| Issue / Symptom | Potential Cause | Remediation Procedure |
|---|---|---|
| Admin metrics show zero records | LocalStorage cleared or disabled | Storage auto-rehydrates from `INITIAL_CANDIDATES` on refresh. |
| Resume upload rejected | File format or size exceeding 5MB | Ensure candidate uploads valid `.pdf`, `.doc`, or `.docx` under 5MB. |
| Form submission blocked | Missing mandatory fields | Check validation toasts; complete Name, Valid Email, and 10-digit Phone. |
| Build failure on CI/CD | Node version mismatch | Ensure CI runner uses Node.js 20.x or later. |

---

*End of Standard Operating Procedure Document.*  
*Signed: Technical Architecture & HR Operations Committee, Thathvamasi HR Consultancy.*
