import { fileURLToPath } from 'url';
import { resolve, dirname } from 'path';
import { defineConfig } from 'vite';

const rootDir = typeof import.meta.dirname !== 'undefined'
  ? import.meta.dirname
  : dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  },
  preview: {
    port: 4173,
    host: true
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
    minify: true,
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      input: {
        main: resolve(rootDir, 'index.html'),
        admin: resolve(rootDir, 'admin/index.html'),
        notFound: resolve(rootDir, '404.html'),
        services: resolve(rootDir, 'services/index.html'),
        erpCrm: resolve(rootDir, 'services/erp-crm.html'),
        executiveSearch: resolve(rootDir, 'services/executive-search.html'),
        permanentStaffing: resolve(rootDir, 'services/permanent-staffing.html'),
        itRecruitment: resolve(rootDir, 'services/it-recruitment.html'),
        industrialManufacturing: resolve(rootDir, 'services/industrial-manufacturing.html'),
        contractStaffing: resolve(rootDir, 'services/contract-staffing.html'),
        turnkeyRpo: resolve(rootDir, 'services/turnkey-rpo.html'),
        hrCompliance: resolve(rootDir, 'services/hr-compliance.html'),
        payrollManagement: resolve(rootDir, 'services/payroll-management.html'),
        campusHiring: resolve(rootDir, 'services/campus-hiring.html'),
        industryAutoEv: resolve(rootDir, 'industries/auto-ev.html'),
        industryItGcc: resolve(rootDir, 'industries/it-gcc.html'),
        industryEngineeringFoundry: resolve(rootDir, 'industries/engineering-foundry.html'),
        industryTextilesApparel: resolve(rootDir, 'industries/textiles-apparel.html'),
        industryBfsiFintech: resolve(rootDir, 'industries/bfsi-fintech.html'),
        industryPharmaHealthcare: resolve(rootDir, 'industries/pharma-healthcare.html'),
        industryFmcgRetail: resolve(rootDir, 'industries/fmcg-retail.html'),
        industryRenewableEnergy: resolve(rootDir, 'industries/renewable-energy.html'),
        industryInfraConstruction: resolve(rootDir, 'industries/infra-construction.html'),
        industryLogisticsSupplyChain: resolve(rootDir, 'industries/logistics-supply-chain.html'),
        industryElectronicsEms: resolve(rootDir, 'industries/electronics-ems.html'),
        industryChemicalsMaterials: resolve(rootDir, 'industries/chemicals-materials.html'),
        industriesIndex: resolve(rootDir, 'industries/index.html'),
        businessIndex: resolve(rootDir, 'business/index.html'),
        businessCompanyRegistration: resolve(rootDir, 'business/company-registration.html'),
        businessGstTax: resolve(rootDir, 'business/gst-tax.html'),
        businessMcaCompliance: resolve(rootDir, 'business/mca-compliance.html'),
        businessTrademarkIpr: resolve(rootDir, 'business/trademark-ipr.html'),
        businessAccountingCfo: resolve(rootDir, 'business/accounting-cfo.html'),
        businessAuditAssurance: resolve(rootDir, 'business/audit-assurance.html'),
        businessTdsTcs: resolve(rootDir, 'business/tds-tcs.html'),
        businessEsiEpf: resolve(rootDir, 'business/esi-epf.html'),
        businessFinancialAdvisory: resolve(rootDir, 'business/financial-advisory.html'),
      }
    }
  }
});
