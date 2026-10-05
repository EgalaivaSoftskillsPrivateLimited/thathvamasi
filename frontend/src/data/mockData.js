/**
 * Thathvamasi HR Consultancy (THC) - Mock Seed Data & Constants
 */

export const INITIAL_CANDIDATES = [
  {
    id: "THC-CAN-10291",
    name: "Karthik Subramanian",
    email: "karthik.s@outlook.com",
    mobile: "+91 98401 23456",
    whatsapp: "+91 98401 23456",
    currentLocation: "Coimbatore",
    preferredLocation: "Coimbatore / Bangalore",
    qualification: "B.E. Computer Science (PSG Tech)",
    experience: "6 Years",
    currentCompany: "Bosch Global Software",
    currentDesignation: "Senior Full Stack Engineer",
    currentCtc: "18.5 LPA",
    expectedCtc: "24.0 LPA",
    noticePeriod: "30 Days",
    skills: ["React", "Node.js", "AWS", "Microservices", "TypeScript"],
    status: "shortlisted",
    appliedDate: "2026-09-28",
    resumeFileName: "Karthik_Subramanian_Resume_2026.pdf",
    resumeFileSize: "2.4 MB"
  },
  {
    id: "THC-CAN-10292",
    name: "Ananya Rengarajan",
    email: "ananya.hr@gmail.com",
    mobile: "+91 94432 87654",
    whatsapp: "+91 94432 87654",
    currentLocation: "Tiruppur",
    preferredLocation: "Coimbatore",
    qualification: "MBA HR (Amrita School of Business)",
    experience: "8 Years",
    currentCompany: "KPR Mill Ltd",
    currentDesignation: "HR Business Partner (Talent & Compliance)",
    currentCtc: "14.0 LPA",
    expectedCtc: "18.0 LPA",
    noticePeriod: "Immediate",
    skills: ["Talent Acquisition", "Labor Laws", "POSH", "Payroll Automation", "Employee Relations"],
    status: "contacted",
    appliedDate: "2026-09-30",
    resumeFileName: "Ananya_HRBP_Profile.docx",
    resumeFileSize: "1.8 MB"
  },
  {
    id: "THC-CAN-10293",
    name: "Vigneshwaran M.",
    email: "vignesh.mech@yahoo.com",
    mobile: "+91 97890 11223",
    whatsapp: "+91 97890 11223",
    currentLocation: "Coimbatore",
    preferredLocation: "Coimbatore / Chennai",
    qualification: "B.Tech Mechanical Engineering",
    experience: "4.5 Years",
    currentCompany: "Pricol Limited",
    currentDesignation: "Design & Quality Assurance Specialist",
    currentCtc: "9.2 LPA",
    expectedCtc: "12.5 LPA",
    noticePeriod: "60 Days",
    skills: ["AutoCAD", "SolidWorks", "Six Sigma", "PPAP", "Automotive QA"],
    status: "new",
    appliedDate: "2026-10-02",
    resumeFileName: "Vignesh_Mech_Design.pdf",
    resumeFileSize: "3.1 MB"
  },
  {
    id: "THC-CAN-10294",
    name: "Meenakshi Sundaram",
    email: "meenakshi.fin@gmail.com",
    mobile: "+91 98940 44556",
    whatsapp: "+91 98940 44556",
    currentLocation: "Madurai",
    preferredLocation: "Coimbatore",
    qualification: "Chartered Accountant (CA Inter / M.Com)",
    experience: "10 Years",
    currentCompany: "TVS Mobility Group",
    currentDesignation: "Finance & Accounts Manager",
    currentCtc: "19.0 LPA",
    expectedCtc: "25.0 LPA",
    noticePeriod: "45 Days",
    skills: ["Statutory Audit", "GST Filing", "Direct Taxes", "SAP FICO", "Financial Modeling"],
    status: "shortlisted",
    appliedDate: "2026-10-03",
    resumeFileName: "Meenakshi_Finance_Leader.pdf",
    resumeFileSize: "2.1 MB"
  },
  {
    id: "THC-CAN-10295",
    name: "Divya Prakash",
    email: "divya.devops@outlook.in",
    mobile: "+91 95000 66778",
    whatsapp: "+91 95000 66778",
    currentLocation: "Coimbatore",
    preferredLocation: "Coimbatore / Remote",
    qualification: "M.Sc Software Systems (CIT)",
    experience: "3 Years",
    currentCompany: "KGiSL Technologies",
    currentDesignation: "DevOps & Cloud Engineer",
    currentCtc: "8.5 LPA",
    expectedCtc: "12.0 LPA",
    noticePeriod: "Immediate",
    skills: ["Docker", "Kubernetes", "Terraform", "CI/CD", "AWS", "Python"],
    status: "new",
    appliedDate: "2026-10-04",
    resumeFileName: "Divya_DevOps_Cloud.pdf",
    resumeFileSize: "1.5 MB"
  }
];

export const INITIAL_CLIENTS = [
  {
    id: "THC-REQ-39101",
    companyName: "L&T Heavy Engineering",
    contactPerson: "Rajendran S.",
    designation: "Head of Talent Sourcing",
    email: "rajendran.s@lntengineering.com",
    mobile: "+91 98400 99887",
    location: "Coimbatore / Malumichampatti Unit",
    industry: "Engineering & Manufacturing",
    position: "Lead Quality Systems & Welding Specialist",
    vacancies: 3,
    experience: "7 - 10 Years",
    salaryRange: "14 - 18 LPA",
    employmentType: "Permanent",
    timeline: "Within 30 Days",
    jdSummary: "Seeking experienced Quality Assurance engineers with ASME and ISO 9001 audit leadership background.",
    status: "sourcing",
    submittedDate: "2026-09-25"
  },
  {
    id: "THC-REQ-39102",
    companyName: "Cognizant Technology Solutions",
    contactPerson: "Preethi Nair",
    designation: "Senior Staffing Manager",
    email: "preethi.nair@cognizant.com",
    mobile: "+91 99620 54321",
    location: "CHIL SEZ, Saravanampatti, Coimbatore",
    industry: "Information Technology",
    position: "Principal Cloud Architect (Azure / AWS)",
    vacancies: 2,
    experience: "12+ Years",
    salaryRange: "32 - 40 LPA",
    employmentType: "Permanent",
    timeline: "Immediate / 15 Days",
    jdSummary: "Enterprise architectural modernization for global healthcare client. Must have multi-cloud certifications.",
    status: "shortlist_sent",
    submittedDate: "2026-09-29"
  },
  {
    id: "THC-REQ-39103",
    companyName: "Texmo Industries (Taro Pumps)",
    contactPerson: "Senthil Kumar V.",
    designation: "General Manager - Corporate HR",
    email: "senthilkumar@texmo.com",
    mobile: "+91 94430 11990",
    location: "Mettupalayam Road, Coimbatore",
    industry: "Industrial Manufacturing",
    position: "R&D Motor Design Specialist",
    vacancies: 4,
    experience: "5 - 8 Years",
    salaryRange: "12 - 16 LPA",
    employmentType: "Permanent",
    timeline: "Within 45 Days",
    jdSummary: "Submersible pump motor dynamics, electromagnetic simulation, energy efficiency compliance.",
    status: "open",
    submittedDate: "2026-10-02"
  }
];

export const INITIAL_BLOGS = [
  {
    id: "blog-coimbatore-gcc-hub-2026",
    slug: "coimbatore-western-tamil-nadu-gcc-engineering-advantage-2026",
    title: "The Western Tamil Nadu Advantage: Why 75+ GCCs & EV Giants Are Choosing Coimbatore Over Tier-1 Metros in 2026",
    category: "Western Tamil Nadu Hub",
    region: "Western Tamil Nadu (Coimbatore / Tiruppur)",
    readTime: "6 min read",
    author: "S. Ramanathan, Practice Director - Industrial & GCCs",
    date: "Oct 4, 2026",
    excerpt: "With over 75 operational Global Capability Centers targeting 200 by 2032, a 25% lower operational cost base, and single-digit attrition (10-12% vs 22% in Tier-1 metros), Coimbatore has emerged as South India's premier engineering and R&D capability destination.",
    content: `
      <h3>1. The Shift from Headcount Arbitrage to Deep Engineering R&D</h3>
      <p>As of late 2026, Coimbatore's GCC footprint has crossed 75 specialized centers, with industry projections targeting over 200 GCCs by 2032. Unlike early-generation outsourcing hubs focused on back-office operations, Coimbatore's capability centers are strictly engineering-first. Multinational enterprises in industrial automation, aerospace, automotive embedded systems, and medtech are establishing dedicated 50 to 500-seat capability centers (pods) designed for high intellectual property generation.</p>
      
      <h3>2. The Academic Dynamo: 30,000+ STEM Graduates Annually</h3>
      <p>The bedrock of Western Tamil Nadu's tech talent is its unmatched concentration of premier institutions: PSG College of Technology, Coimbatore Institute of Technology (CIT), Government College of Technology (GCT), Amrita Vishwa Vidyapeetham, and Kumaraguru College of Technology. These campuses produce over 30,000 engineering graduates annually with rigorous fundamentals in mechatronics, power electronics, embedded firmware, and computer science.</p>
      
      <h3>3. Workforce Stability: 94.2% 12-Month Retention</h3>
      <p>The most compelling competitive metric cited by global engineering directors is retention. While Tier-1 metros like Bengaluru and Gurugram suffer from chronic attrition rates between 18% and 24%, capability centers in Coimbatore consistently report attrition of just 10% to 12%. Factors driving this include superior urban livability, shorter commutes, and an accelerating reverse migration of senior architects returning from Bengaluru, Chennai, and Singapore.</p>
      
      <h3>4. Identical State Subsidies & Infrastructure</h3>
      <p>Under Tamil Nadu's revised GCC policy framework, Coimbatore receives identical incentive parity to Chennai, including payroll subsidies for high-value tech hires, innovation lab capital grants, and IP patent filing reimbursements. The expansion of Grade-A tech infrastructure across TIDEL Park Coimbatore Phase-II and Saravanampatti CHIL SEZ ensures immediate plug-and-play capacity for global enterprises.</p>
      
      <h3>5. THC's Localized Executive Search Pod</h3>
      <p>Thathvamasi HR Consultancy maintains a vetted registry of over 18,500 senior engineering leaders, plant heads, and software architects rooted in Western Tamil Nadu, offering clients a guaranteed 48-hour shortlist turnaround for critical capability appointments.</p>
    `,
    image: "/images/heroes/thc_hero.jpg"
  },
  {
    id: "blog-chennai-hosur-ev-corridor",
    slug: "chennai-hosur-electric-vehicle-corridor-salary-premium-2026",
    title: "Inside the Chennai–Hosur Electric Mobility Corridor: Navigating the 45% Salary Premium for EV Powertrain & BMS Talent",
    category: "Chennai & Hosur EV Belt",
    region: "Chennai & Hosur (Mobility Corridor)",
    readTime: "7 min read",
    author: "R. Karthikeyan, Lead Partner - Auto & Cleantech",
    date: "Oct 1, 2026",
    excerpt: "Tamil Nadu commands 15.2% of India's electric vehicle manufacturing capacity. Driven by gigafactory expansions in Hosur and Oragadam, battery management (BMS) and high-voltage power electronics specialists command up to a 50% compensation premium over legacy internal combustion engine (ICE) roles.",
    content: `
      <h3>1. The Automotive Capital Re-tools for Electric Mobility</h3>
      <p>Tamil Nadu has firmly consolidated its position as India's EV manufacturing heartland, accounting for more than 15% of national EV demand. The industrial spine connecting Chennai's automotive belts (Oragadam, Sriperumbudur, Maraimalai Nagar) with Hosur's massive gigafactory corridor is operating at maximum hiring velocity. Supported by the PM E-DRIVE framework and state industrial incentives, original equipment manufacturers (OEMs) and Tier-1 component giants are aggressively scaling high-voltage battery assembly lines.</p>
      
      <h3>2. The Severe Talent Crunch in Power Electronics</h3>
      <p>While mechanical engineering and sheet metal tooling talent remains abundant, there is an acute deficit in cross-functional engineers capable of bridging mechanical packaging with high-voltage electrical safety. Highest in demand are Battery Management System (BMS) firmware architects, motor inverter control engineers, DC-DC converter specialists, and cell chemistry validation heads.</p>
      
      <h3>3. 2026 Compensation Benchmarks & Transition Premiums</h3>
      <p>According to THC's Q3 2026 industrial salary index, professionals transitioning from traditional ICE powertrain design to EV systems are commanding starting premiums of 45% to 50%:</p>
      <ul>
        <li><strong>Mid-Level Engineers (4–7 Years Experience):</strong> ₹16.0 – ₹28.0 LPA in BMS firmware, inverter controls, and thermal simulation.</li>
        <li><strong>Senior Technical Leads / Engineering Managers (8–12 Years):</strong> ₹30.0 – ₹52.0 LPA.</li>
        <li><strong>Chief Technology Officers / VP - Powertrain (15+ Years):</strong> ₹60.0 LPA to ₹1.2 Crore + equity incentives.</li>
      </ul>
      
      <h3>4. Overcoming 90-Day Notice Periods via Structured Buyouts</h3>
      <p>Nearly 70% of senior candidates in established automotive companies are locked into 60-to-90-day contractual notice periods. At THC, our executive search methodology incorporates pre-negotiated notice buyout models and transition advisory to ensure critical plant leaders join within 30 to 45 business days.</p>
      
      <h3>5. The Growth of Flexible & Contract-to-Hire Staffing</h3>
      <p>To mitigate execution risk during pilot production ramp-ups, 40% to 50% of new plant requisitions in the Hosur-Chennai belt are being initiated as high-skill contractual engagements with pre-agreed conversion milestones upon commercial production launch.</p>
    `,
    image: "/images/team/thc_leadership.jpg"
  },
  {
    id: "blog-bengaluru-gcc-diamond-model",
    slug: "bengaluru-gcc-diamond-workforce-model-workforce-2026",
    title: "The Demise of the Junior Pyramid: How Bengaluru GCCs Are Adopting the 'Diamond Workforce' Model in 2026",
    category: "Bengaluru GCCs",
    region: "Bengaluru & Hyderabad (Tech Corridors)",
    readTime: "8 min read",
    author: "K. Arvind, Head of Technology Executive Search",
    date: "Sep 28, 2026",
    excerpt: "As autonomous coding agents absorb entry-level programming tasks, Fortune 500 Global Capability Centers in Bengaluru and Hyderabad are retiring the traditional 60% junior pyramid. In its place, the 'Diamond Workforce' (Workforce 2.0) prioritizes mid-to-senior solution architects and AI orchestrators.",
    content: `
      <h3>1. The Evolution from Headcount Pyramids to Capability Diamonds</h3>
      <p>For two decades, Indian capability centers and IT powerhouses operated on a classic pyramid model: a broad foundation of junior engineers (0–3 years) comprising 55% to 65% of total headcount, supervised by a lean layer of technical leads and directors. In 2026, the widespread enterprise adoption of generative AI, automated code validation, and agentic workflows has rendered basic boilerplate coding obsolete. The entry-level tier has narrowed sharply, giving rise to the 'Diamond Model'—where the bulk of headcount resides in the 4-to-10 year experienced engineering band.</p>
      
      <h3>2. Measuring 'Enterprise Value Generated per Professional'</h3>
      <p>Global capability center boards in Bengaluru (Outer Ring Road, Whitefield, Electronic City) no longer reward country heads for raw headcount expansion. The core KPI has pivoted to 'Enterprise Value Generated per Engineer'. A 300-person diamond-structured center today delivers the architectural throughput of an 800-person legacy pyramid center.</p>
      
      <h3>3. The In-Demand Core: AI Orchestration & Systems Architecture</h3>
      <p>Hiring demand is heavily concentrated in specialized roles requiring architectural judgment that automated tools cannot replicate:</p>
      <ul>
        <li><strong>Distributed Systems & Platform Architects:</strong> Designing resilient cloud backbones on AWS and Azure capable of scaling to millions of concurrent requests.</li>
        <li><strong>MLOps & Agentic System Integrators:</strong> Deploying self-hosted open-weights LLMs with strict data sovereignty and latency SLAs.</li>
        <li><strong>Production Validation & Security Leads:</strong> Auditing AI-generated output for compliance with the Indian Digital Personal Data Protection (DPDP) Act and EU AI Act.</li>
      </ul>
      
      <h3>4. Retention Strategies: Ownership Over Title Inflation</h3>
      <p>Because every capability center is competing for the same concentrated layer of 5-to-10-year experienced leaders, compensation alone is no longer an adequate retention moat. High performers demand direct architectural ownership, transparent internal mobility, and direct reporting lines to global engineering heads.</p>
      
      <h3>5. THC's Capability Center Turnkey Pods</h3>
      <p>Thathvamasi's dedicated GCC search practice builds pre-calibrated, multidisciplinary pods (Principal Architect + 3 Senior Full-Stack Specialists + 1 Data Engineer) capable of hitting full velocity within 2 weeks of client contract execution.</p>
    `,
    image: "/images/campus/thc_growth.jpg"
  },
  {
    id: "blog-pune-precision-auto-engineering",
    slug: "pune-chakan-precision-engineering-foundry-cxo-hiring-2026",
    title: "Precision Engineering & Foundry Modernization: Hiring CXOs for Maharashtra's Auto Components Belt (Pune–Chakan–Kolhapur)",
    category: "Pune Industrial",
    region: "Pune & Western Maharashtra (Auto & Foundry)",
    readTime: "6 min read",
    author: "M. S. Sundaram, Senior HR Advisory Partner",
    date: "Sep 24, 2026",
    excerpt: "With a 10.3% annual salary increment leading the nation's industrial manufacturing corridors, the Pune-Chakan-Talegaon belt is aggressively hiring plant directors and chief quality officers skilled in multi-axis CNC robotics, lightweight alloys, and German Tier-1 export standards.",
    content: `
      <h3>1. Heavy Engineering's Digital Modernization</h3>
      <p>The industrial corridor spanning Pune, Chakan, Talegaon, and extending south to the foundry hub of Kolhapur is undergoing its most aggressive capital expenditure cycle in a decade. Driven by automotive export contracts to European and North American OEMs, conventional casting and machining plants are transitioning to automated multi-axis CNC cells, robotic welding stations, and real-time scrap reduction systems.</p>
      
      <h3>2. The Talent Shortage: IATF 16949 & VDA 6.3 Audit Leadership</h3>
      <p>The chief hurdle facing manufacturing conglomerates in this belt is not capital—it is finding Plant Heads and Chief Quality Officers (CQOs) with proven audit track records under rigorous international benchmarks such as IATF 16949 (Automotive Quality Management) and VDA 6.3 (German Automotive Process Audits). Enterprises are paying substantial sign-on premiums for operations leaders who can eliminate ppm defect rates on export lines.</p>
      
      <h3>3. Cross-Corridor Recruitment: Tamil Nadu & Maharashtra Synergy</h3>
      <p>Because Coimbatore and Pune share deeply complementary industrial heritage in pump casting, metallurgy, and precision motor manufacturing, THC frequently facilitates high-level leadership cross-pollination between these two hubs. Metallurgy specialists and plant general managers from Tamil Nadu's industrial clusters find exceptional career scale in Maharashtra's automotive Tier-1 supplier ecosystem.</p>
      
      <h3>4. Succession Planning for Family-Owned Industrial Powerhouses</h3>
      <p>Dozens of mid-market engineering enterprises in the ₹200 Cr to ₹1,500 Cr bracket are actively transitioning management from founding families to professional leadership teams. THC's executive advisory practice specializes in discrete, retained CXO searches that balance professional operational governance with the cultural fabric of family enterprises.</p>
    `,
    image: "/images/heroes/thc_hero.jpg"
  },
  {
    id: "blog-gujarat-chemical-pharma-corridor",
    slug: "gujarat-sanand-dahej-pharma-chemical-semiconductor-talent-2026",
    title: "Scaling Bulk APIs & Semiconductor Clusters: Executive Search Trends Across the Gujarat Industrial Corridor (Sanand–Dahej–Vadodara)",
    category: "Gujarat Industrial",
    region: "Gujarat (Chemical, Pharma & Clean Energy)",
    readTime: "7 min read",
    author: "Dr. Ananya R., Principal Lifesciences Consultant",
    date: "Sep 19, 2026",
    excerpt: "As the Sanand semiconductor corridor and Dahej specialty chemical hub attract over ₹1.2 Lakh Crore in private investments, the demand for USFDA-compliant plant leaders, process safety (HAZOP) directors, and green hydrogen engineers has reached record highs.",
    content: `
      <h3>1. The Chemical & Clean Energy Epicenter</h3>
      <p>Gujarat's industrial spine—anchored by the Dahej Petroleum, Chemicals and Petrochemicals Investment Region (PCPIR), Ankleshwar chemical parks, and the Sanand-Dholera high-tech cluster—is witnessing unprecedented capital deployment. With global pharmaceutical supply chains de-risking active pharmaceutical ingredient (API) procurement, Gujarat's formulation and bulk chemical manufacturers are investing heavily in continuous flow synthesis and closed-loop effluent treatment plants.</p>
      
      <h3>2. USFDA & Process Safety (HAZOP) Regulatory Scarcity</h3>
      <p>Stringent compliance enforcement by the USFDA, European Medicines Agency (EMA), and the Central Pollution Control Board (CPCB) has made regulatory compliance officers the highest-demand executives in Western India. Key requisitions handled by THC in this corridor include:</p>
      <ul>
        <li><strong>Vice President - Global Regulatory Affairs:</strong> Managing multi-site USFDA inspections and ANDA drug filings (₹45 – ₹80+ LPA).</li>
        <li><strong>Head of Process Safety & EHS:</strong> Implementing quantitative risk assessments (QRA) and Process Safety Management (PSM) standards (₹28 – ₹45 LPA).</li>
        <li><strong>Continuous Flow Chemistry Scientists:</strong> Converting batch synthesis to high-yield continuous micro-reactors (₹18 – ₹32 LPA).</li>
      </ul>
      
      <h3>3. Reverse Migration to Plant-Adjacent Executive Hubs</h3>
      <p>Attracting high-caliber R&D and operational leaders away from metro corporate headquarters (Mumbai, Delhi, Bengaluru) to industrial manufacturing hubs like Bharuch, Dahej, and Vadodara requires calibrated compensation packages that include long-term incentive plans (LTIPs), executive housing assistance, and family relocation benefits.</p>
      
      <h3>4. THC's National Retained Search Infrastructure</h3>
      <p>Whether headhunting an API Plant Director for Dahej or a Cleanroom Operations Specialist for Sanand's semiconductor test facilities, THC's confidential executive search pod leverages comprehensive talent intelligence to deliver authenticated candidate dossiers within 48 hours.</p>
    `,
    image: "/images/team/thc_leadership.jpg"
  }
];

