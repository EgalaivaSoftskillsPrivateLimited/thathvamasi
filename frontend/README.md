# Thathvamasi HR Consultancy (THC) - Corporate Web Platform

[![Build & Deploy](https://github.com/EgalaivaSoftskillsPrivateLimited/thathvamasi/actions/workflows/deploy.yml/badge.svg)](https://github.com/EgalaivaSoftskillsPrivateLimited/thathvamasi/actions/workflows/deploy.yml)

A state-of-the-art, high-performance corporate web platform and recruitment operations system for **Thathvamasi HR Consultancy (THC)**, headquartered in Coimbatore, Tamil Nadu, India.

---

## 📁 Project File Structure

```
thathvamasi/
├── .github/                         # CI/CD Workflows
│   └── workflows/
│       └── deploy.yml              # Automated build & verification
├── .vscode/                        # IDE Configuration
│   └── settings.json               # Formatting & syntax standards
├── docs/                           # Documentation & Standard Operating Procedures
│   └── SOP_FRONTEND_AND_OPERATIONS.md # Master Operational & Technical SOP
├── frontend/                       # Frontend Web Application Root
│   ├── public/                     # Public Static Assets
│   │   ├── images/
│   │   │   ├── logo/               # Brand logo & monogram assets
│   │   │   │   └── thc_logo.jpg
│   │   │   ├── heroes/             # Hero visual assets
│   │   │   │   └── thc_hero.jpg
│   │   │   ├── team/               # Executive leadership & consulting team
│   │   │   │   └── thc_leadership.jpg
│   │   │   └── campus/             # Tech campus & ecosystem imagery
│   │   │       └── thc_growth.jpg
│   │   ├── favicon.ico             # Browser tab favicon
│   │   └── robots.txt              # SEO crawler instructions
│   ├── services/                   # Multi-Page Service Practices (HTML)
│   ├── src/                        # Application Source Code
│   ├── components/                 # Modular UI & Section Components
│   │   ├── ui/                     # UI Primitives
│   │   │   ├── Toast.js            # Notification dispatcher
│   │   │   └── Modal.js            # Accessible dialog controller
│   │   ├── layout/                 # Layout elements (Header, Footer)
│   │   ├── sections/               # Page Sections
│   │   │   ├── Services.js         # Specialized service cards & category tabs
│   │   │   └── Insights.js         # Market insights grid & search reader
│   │   ├── forms/                  # Interactive Form Handlers
│   │   │   ├── CandidateRegistrationForm.js # Multi-step candidate intake & resume dropzone
│   │   │   ├── ClientRequisitionForm.js     # Corporate hiring requirements intake
│   │   │   └── ContactForm.js               # General inquiry & WhatsApp launcher
│   │   └── admin/                  # Command Center Module
│   │       └── AdminDashboard.js   # Analytics, table search, status matrix & CSV exporter
│   ├── styles/                     # Vanilla CSS Modular Design System
│   │   ├── variables.css           # Tokens, palette, gradients, glassmorphism
│   │   ├── base.css                # Typography reset, layout containers, animations
│   │   ├── components.css          # Navbars, buttons, cards, dropzones, steppers
│   │   ├── admin.css               # KPIs, bar charts, data tables, status badges
│   │   └── responsive.css          # Breakpoints for tablet, mobile, and desktop
│   ├── lib/                        # Shared Utilities & Infrastructure
│   │   ├── storage.js              # LocalStorage state manager & event bus
│   │   ├── validation.js           # Form validation routines
│   │   └── csvExporter.js          # RFC 4180 compliant CSV export
│   ├── config/                     # Domain & Business Configurations
│   │   ├── site.config.js          # Brand identity, address, phone, social URLs
│   │   └── services.config.js      # Service definitions & deliverables
│   ├── data/                       # Initial Domain Seed Data
│   │   └── mockData.js             # Realistic candidates, clients, blogs, metrics
│   └── main.js                     # Master Application Entry Point
├── .env.example                    # Environment variable template
├── .gitignore                      # Git exclusion rules
├── index.html                      # Semantic HTML5 Master Document
├── package.json                    # NPM package metadata and scripts
└── README.md                       # Repository overview & setup guide
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Node.js:** v20.x or higher
- **npm:** v10.x or higher

### 2. Installation
```bash
npm install
```

### 3. Development Server
Start the development server with Hot Module Replacement (HMR):
```bash
npm run dev
```

### 4. Production Build
Compile and bundle optimized production assets into `dist/`:
```bash
npm run build
```

### 5. Preview Production Build
```bash
npm run preview
```

---

## 🚀 Key Features

1. **Brand Identity & Executive Aesthetics:**
   - Deep Executive Sapphire, Royal Champagne Gold, and Emerald Teal palette.
   - Glassmorphic translucent cards, custom CSS custom properties, and micro-animations.

2. **Candidate Portal:**
   - Multi-step registration (Personal details &rarr; Professional background &rarr; Resume upload).
   - Drag-and-drop resume upload zone with file validation (`.pdf`, `.doc`, `.docx` up to 5MB).
   - Instant reference ID generation (`THC-CAN-xxxxx`) and DPDP consent checkbox.

3. **Employer Requisition Portal:**
   - Detailed corporate requirement intake with vacancy count, timeline, and budget.
   - Requisition tracking code (`THC-REQ-xxxxx`) with 48-Hour Shortlist Guarantee.

4. **HR Command Center & Admin Portal:**
   - Real-time KPI analytics (Total Candidates, Active Requisitions, Shortlisted Profiles).
   - Pipeline charts and status distribution metrics.
   - Searchable and filterable candidate database with status update dropdown.
   - **One-click Export to CSV** functionality (`THC_Candidates_Registry_YYYY-MM-DD.csv`).
   - Client requisitions management and blog publishing CMS.

5. **Thought Leadership & HR Insights:**
   - Filterable insights catalog (HR Compliance, Hiring Trends, Strategy).
   - Full article modal reader with estimated reading times.

6. **Coimbatore Corporate Hub:**
   - Integrated contact form, direct telephone links, and one-click WhatsApp launcher.

---

## 📖 Operational Documentation
For comprehensive details on recruitment workflows, candidate intake, employer requisitions, and compliance, see [`docs/SOP_FRONTEND_AND_OPERATIONS.md`](docs/SOP_FRONTEND_AND_OPERATIONS.md).
