import { resolve } from 'path';
import { defineConfig } from 'vite';

const rootDir = import.meta.dirname;

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(rootDir, 'index.html'),
        services: resolve(rootDir, 'services/index.html'),
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
      }
    }
  }
});
