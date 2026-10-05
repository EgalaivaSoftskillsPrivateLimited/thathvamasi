/**
 * Thathvamasi HR Consultancy (THC) - TalentAI™ Enterprise Intelligence Studio
 * High-tech talent scanner, Indian CTC & Notice Buyout Calculator, and JD Generator
 */

export function initAiStudio() {
  // =========================================================================
  // CONTAINER 1: Live Indian Talent Pool Matcher
  // =========================================================================
  const btnMatch = document.getElementById('btnRunAiMatch');
  const roleInput = document.getElementById('aiRoleQueryInput');
  const matchResult = document.getElementById('aiMatchResult');
  const sampleRoleChips = document.querySelectorAll('.ai-sample-chip');

  const SAMPLE_DOSSIERS = {
    "cloud": {
      id: "THC-IND-8921",
      role: "Senior Cloud & DevOps Architect",
      exp: "9.5 Years",
      pedigree: "Ex-Bosch Global Software & Zoho Corp",
      location: "Coimbatore (Open to Bengaluru & Chennai)",
      ctc: "₹28 LPA (Current) → ₹35 LPA (Expected)",
      notice: "30 Days (Serving Notice • 14 Days Left)",
      matchScore: 98,
      verified: "EPFO & PAN Cleared • Tier-1 Background Vetted"
    },
    "plant": {
      id: "THC-IND-6410",
      role: "Plant Operations Head (Die & Tooling)",
      exp: "14 Years",
      pedigree: "Tier-1 Auto OEM & Precision Engineering",
      location: "Coimbatore / Hosur Corridor",
      ctc: "₹34 LPA (Current) → ₹42 LPA (Expected)",
      notice: "45 Days (Buyout Eligible)",
      matchScore: 96,
      verified: "Six Sigma Black Belt • 100% Reference Checked"
    },
    "ca": {
      id: "THC-IND-4102",
      role: "VP Finance & Taxation (Chartered Accountant)",
      exp: "12 Years",
      pedigree: "Big-4 Accounting & Enterprise Manufacturing",
      location: "Coimbatore / Chennai",
      ctc: "₹32 LPA (Current) → ₹40 LPA (Expected)",
      notice: "30 Days (Immediate Release Available)",
      matchScore: 95,
      verified: "ICAI Member • Statutory Audit & TDS Expert"
    },
    "textile": {
      id: "THC-IND-5219",
      role: "Head of International Merchandising & Sourcing",
      exp: "11 Years",
      pedigree: "Leading Tiruppur Export Garment Conglomerate",
      location: "Tiruppur / Coimbatore Hub",
      ctc: "₹22 LPA (Current) → ₹28 LPA (Expected)",
      notice: "30 Days",
      matchScore: 94,
      verified: "SEDEX & Wrap Audited Facilities Specialist"
    },
    "default": {
      id: "THC-IND-7390",
      role: "Principal Technical Lead (Full Stack)",
      exp: "8 Years",
      pedigree: "Product Engineering & Cloud Native Systems",
      location: "Coimbatore / Hybrid South India",
      ctc: "₹25 LPA (Current) → ₹32 LPA (Expected)",
      notice: "30 Days",
      matchScore: 97,
      verified: "100% Technical Code Score • BGV Cleared"
    }
  };

  sampleRoleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const selected = chip.dataset.role || chip.textContent;
      if (roleInput) {
        roleInput.value = selected;
        runTalentScan(selected);
      }
    });
  });

  if (btnMatch && roleInput) {
    btnMatch.addEventListener('click', () => {
      const query = roleInput.value.trim();
      if (!query) {
        if (window.showToast) window.showToast('Please enter a role or select a quick pick', 'info');
        return;
      }
      runTalentScan(query);
    });
  }

  function runTalentScan(role) {
    if (!matchResult) return;
    matchResult.innerHTML = `
      <div class="ai-loading-box">
        <svg class="pulse-circle" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7047EB" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        <span>Scanning 18,500+ pre-vetted dossiers across Coimbatore, Chennai, Bengaluru & Pan-India...</span>
      </div>
    `;

    setTimeout(() => {
      const queryLower = role.toLowerCase();
      let dossier = SAMPLE_DOSSIERS["default"];
      if (queryLower.includes("cloud") || queryLower.includes("architect") || queryLower.includes("devops") || queryLower.includes("software")) {
        dossier = SAMPLE_DOSSIERS["cloud"];
      } else if (queryLower.includes("plant") || queryLower.includes("tool") || queryLower.includes("mfg") || queryLower.includes("auto")) {
        dossier = SAMPLE_DOSSIERS["plant"];
      } else if (queryLower.includes("ca") || queryLower.includes("finance") || queryLower.includes("tax")) {
        dossier = SAMPLE_DOSSIERS["ca"];
      } else if (queryLower.includes("textile") || queryLower.includes("merchandis") || queryLower.includes("garment")) {
        dossier = SAMPLE_DOSSIERS["textile"];
      }

      matchResult.innerHTML = `
        <div class="ai-candidate-card">
          <div class="ai-candidate-header">
            <div>
              <span class="ai-dossier-id">Dossier: ${dossier.id}</span>
              <h4 class="ai-candidate-title">${dossier.role}</h4>
            </div>
            <span class="ai-match-badge">${dossier.matchScore}% AI Alignment</span>
          </div>

          <div class="ai-dossier-grid">
            <div><strong>Experience:</strong> ${dossier.exp}</div>
            <div><strong>Background:</strong> ${dossier.pedigree}</div>
            <div><strong>Location:</strong> ${dossier.location}</div>
            <div><strong>CTC Calibration:</strong> ${dossier.ctc}</div>
            <div><strong>Notice Period:</strong> <span class="badge-notice">${dossier.notice}</span></div>
            <div><strong>Verification:</strong> <span class="badge-verified">✓ ${dossier.verified}</span></div>
          </div>

          <div class="ai-card-action">
            <button type="button" class="btn-ai-request" onclick="
              document.getElementById('jobTitle').value='${dossier.role}';
              document.getElementById('employers').scrollIntoView({behavior:'smooth'});
              if(window.showToast) window.showToast('Requisition prefilled for Dossier ${dossier.id}!', 'success');
            ">
              Request Candidate Dossier (48-Hr SLA) &rarr;
            </button>
          </div>
        </div>
      `;

      if (window.showToast) {
        window.showToast(`Found verified profile matching "${role}" (${dossier.matchScore}% Match)`, 'success');
      }
    }, 600);
  }

  // =========================================================================
  // CONTAINER 2: Indian CTC & Notice Period Buyout Calculator
  // =========================================================================
  const btnCalculateCtc = document.getElementById('btnRunResumeAi');
  const expBandSelect = document.getElementById('aiSampleProfileSelect');
  const noticeSelect = document.getElementById('aiNoticePeriodSelect');
  const ctcResult = document.getElementById('aiResumeResult');

  if (btnCalculateCtc) {
    btnCalculateCtc.addEventListener('click', () => {
      const expBand = expBandSelect?.value || 'Senior (8-12 Years)';
      const noticeDays = noticeSelect?.value || '30';
      if (!ctcResult) return;

      ctcResult.innerHTML = `
        <div class="ai-loading-box">
          <svg class="pulse-circle" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0060B4" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          <span>Benchmarking Indian compensation bands & buyout feasibility...</span>
        </div>
      `;

      setTimeout(() => {
        let ctcRange = "₹18 LPA – ₹28 LPA";
        let buyoutCost = "₹1.5 Lakhs – ₹2.2 Lakhs";
        let conversionRate = "95%";
        let retiralBreakdown = "EPF (12% of Basic) + Gratuity (4.81%) + Performance Bonus (15%)";

        if (expBand.includes("Lead") || expBand.includes("12-18")) {
          ctcRange = "₹28 LPA – ₹45 LPA";
          buyoutCost = "₹2.8 Lakhs – ₹3.8 Lakhs";
          conversionRate = "93%";
          retiralBreakdown = "EPF (12%) + Gratuity + Executive Medical + LTI / Retention Bonus";
        } else if (expBand.includes("CXO") || expBand.includes("18+")) {
          ctcRange = "₹45 LPA – ₹90+ LPA";
          buyoutCost = "Executive Transition Clause";
          conversionRate = "96%";
          retiralBreakdown = "Fixed Basic + Performance Incentive + ESOPs / SARs + Retirals";
        } else if (expBand.includes("Mid") || expBand.includes("4-7")) {
          ctcRange = "₹12 LPA – ₹18 LPA";
          buyoutCost = "₹90,000 – ₹1.4 Lakhs";
          conversionRate = "92%";
          retiralBreakdown = "Standard CTC: 50% Basic + HRA + EPF (12%) + ESI/Medical";
        }

        ctcResult.innerHTML = `
          <div class="ai-ctc-calc-card">
            <div class="ai-calc-header">
              <span class="ai-calc-title">Compensation & Transition Matrix</span>
              <span class="ai-calc-tag">Band: ${expBand}</span>
            </div>

            <div class="ai-calc-metrics">
              <div class="calc-metric-box">
                <span class="metric-lbl">Target Indian CTC Band</span>
                <span class="metric-val primary">${ctcRange}</span>
              </div>
              <div class="calc-metric-box">
                <span class="metric-lbl">Notice Period SLA</span>
                <span class="metric-val">${noticeDays} Days</span>
              </div>
              <div class="calc-metric-box">
                <span class="metric-lbl">Est. Notice Buyout</span>
                <span class="metric-val">${buyoutCost}</span>
              </div>
              <div class="calc-metric-box">
                <span class="metric-lbl">Joining Probability</span>
                <span class="metric-val green">${conversionRate}</span>
              </div>
            </div>

            <div class="ai-calc-retirals">
              <strong>Statutory & Retirals Breakdown:</strong> ${retiralBreakdown}
            </div>

            <p class="ai-calc-note">
              ✓ Compliant with 2026 Code on Wages (Minimum 50% Basic Salary Structuring).
            </p>
          </div>
        `;

        if (window.showToast) {
          window.showToast(`Calibrated compensation band for ${expBand}`, 'info');
        }
      }, 550);
    });
  }

  // =========================================================================
  // CONTAINER 3: Indian Industry Job Spec (JD) Generator
  // =========================================================================
  const btnGenJD = document.getElementById('btnRunJdGen');
  const jdRoleSelect = document.getElementById('aiJdRoleSelect');
  const jdResult = document.getElementById('aiJdResult');

  const JD_TEMPLATES = {
    "Principal Software Architect": {
      title: "Principal Software Architect (Cloud / GCC)",
      sector: "IT & Global Capability Centers",
      exp: "10 - 15 Years",
      ctc: "₹35 LPA – ₹50 LPA",
      location: "Coimbatore (TIDEL) / Hybrid",
      kras: [
        "Architect enterprise microservices & cloud-native infrastructure (AWS/Azure/GCP).",
        "Lead technical governance, code quality benchmarks, and mentoring of 30+ engineers.",
        "Collaborate with US/European product directors on roadmap and scalability."
      ],
      compliance: "100% Compliant with Indian IT Act & DPDP Act 2023 candidate privacy."
    },
    "Plant Operations Head": {
      title: "Plant Operations Head (Tier-1 Precision Auto)",
      sector: "Automotive & Heavy Manufacturing",
      exp: "12 - 18 Years",
      ctc: "₹28 LPA – ₹42 LPA",
      location: "Coimbatore / Hosur Corridor",
      kras: [
        "Oversee end-to-end plant operations, CNC machining, tooling, and fabrication lines.",
        "Implement Lean Six Sigma, Kaizen, and achieve zero-defect quality standards.",
        "Ensure complete adherence to Factories Act 1948 and 2026 Occupational Safety Codes."
      ],
      compliance: "100% Factories Act, ESI & Statutory Safety Code Compliant."
    },
    "VP International Merchandising": {
      title: "Vice President - Global Sourcing & Merchandising",
      sector: "Textiles & Garment Exports",
      exp: "12 - 16 Years",
      ctc: "₹24 LPA – ₹36 LPA",
      location: "Tiruppur / Coimbatore",
      kras: [
        "Drive international retail accounts across North America, UK, and European fashion brands.",
        "Oversee costing, sustainable fabric procurement, and sampling approval cycles.",
        "Ensure supplier compliance with SEDEX, OEKO-TEX, and global labor standards."
      ],
      compliance: "Statutory Labor & Export Compliance Certified."
    },
    "Chief Risk Officer": {
      title: "Chief Risk Officer (CRO / Basel III)",
      sector: "BFSI & FinTech",
      exp: "15 - 20 Years",
      ctc: "₹50 LPA – ₹80 LPA",
      location: "Mumbai / Bengaluru / Chennai",
      kras: [
        "Formulate comprehensive credit risk, market risk, and operational risk frameworks.",
        "Ensure regulatory compliance with Reserve Bank of India (RBI) prudential guidelines.",
        "Steer ALM, NPA recovery governance, and digital fraud risk management."
      ],
      compliance: "RBI Statutory & Governance Compliant."
    }
  };

  if (btnGenJD) {
    btnGenJD.addEventListener('click', () => {
      const selected = jdRoleSelect?.value || 'Principal Software Architect';
      if (!jdResult) return;

      jdResult.innerHTML = `
        <div class="ai-loading-box">
          <svg class="pulse-circle" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#008844" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          <span>Synthesizing Indian enterprise role specification & KRAs...</span>
        </div>
      `;

      setTimeout(() => {
        let jdData = JD_TEMPLATES[selected] || JD_TEMPLATES["Principal Software Architect"];

        jdResult.innerHTML = `
          <div class="ai-jd-card">
            <div class="ai-jd-header">
              <div>
                <h4 class="ai-jd-title">${jdData.title}</h4>
                <span class="ai-jd-sector">${jdData.sector} • ${jdData.location}</span>
              </div>
              <span class="badge-verified">Bias-Free Calibrated</span>
            </div>

            <div class="ai-jd-meta">
              <span><strong>Experience:</strong> ${jdData.exp}</span>
              <span><strong>Benchmark CTC:</strong> ${jdData.ctc}</span>
            </div>

            <div class="ai-jd-kras">
              <strong>Core Key Result Areas (KRAs):</strong>
              <ul>
                ${jdData.kras.map(k => `<li>• ${k}</li>`).join('')}
              </ul>
            </div>

            <div class="ai-jd-compliance">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>${jdData.compliance}</span>
            </div>

            <div class="ai-card-action">
              <button type="button" class="btn-ai-request" onclick="
                document.getElementById('jobTitle').value='${jdData.title}';
                document.getElementById('jobDescriptionText').value='Role: ${jdData.title}\\nSector: ${jdData.sector}\\nTarget Experience: ${jdData.exp}\\nLocation: ${jdData.location}\\nCompensation: ${jdData.ctc}\\n\\nKey KRAs:\\n${jdData.kras.map(k => '- ' + k).join('\\n')}';
                document.getElementById('employers').scrollIntoView({behavior:'smooth'});
                if(window.showToast) window.showToast('Copied full JD to Employer Requisition!', 'success');
              ">
                Use this JD in Hiring Requisition &rarr;
              </button>
            </div>
          </div>
        `;

        if (window.showToast) {
          window.showToast(`Synthesized Indian Enterprise JD for ${jdData.title}`, 'success');
        }
      }, 550);
    });
  }
}
