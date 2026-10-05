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
      }
    }
  }
});
