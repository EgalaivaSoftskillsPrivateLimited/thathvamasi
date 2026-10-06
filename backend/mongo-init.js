// MongoDB initialization script
// Creates initial admin user and collections

db = db.getSiblingDB('thathvamasi_hr');

// Create collections
db.createCollection('candidates');
db.createCollection('clients');
db.createCollection('blogs');
db.createCollection('users');
db.createCollection('contacts');
db.createCollection('services');
db.createCollection('settings');

// Create admin user
db.users.insertOne({
  email: 'admin@thathvamasi.com',
  password: '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', // admin123
  full_name: 'Administrator',
  role: 'admin',
  is_active: true,
  created_at: new Date(),
  updated_at: new Date()
});

// Create default settings
db.settings.insertOne({
  site_name: 'Thathvamasi HR Consultancy',
  site_description: 'Professional HR Consultancy and Recruitment Services',
  contact_email: 'contact@thathvamasi.com',
  contact_phone: '+91 9876543210',
  office_address: 'Coimbatore, Tamil Nadu',
  created_at: new Date(),
  updated_at: new Date()
});

// Create sample services
const services = [
  {
    name: 'Recruitment & Talent Acquisition',
    description: 'End-to-end recruitment solutions for businesses',
    icon: 'recruitment',
    order: 1,
    is_active: true,
    created_at: new Date()
  },
  {
    name: 'Permanent Staffing',
    description: 'Permanent employment solutions',
    icon: 'staffing',
    order: 2,
    is_active: true,
    created_at: new Date()
  },
  {
    name: 'Temporary / Contract Staffing',
    description: 'Flexible staffing solutions',
    icon: 'contract',
    order: 3,
    is_active: true,
    created_at: new Date()
  },
  {
    name: 'Executive Search',
    description: 'Senior level talent acquisition',
    icon: 'executive',
    order: 4,
    is_active: true,
    created_at: new Date()
  },
  {
    name: 'HR Consulting',
    description: 'HR strategy and consulting services',
    icon: 'consulting',
    order: 5,
    is_active: true,
    created_at: new Date()
  },
  {
    name: 'Payroll / HR Support',
    description: 'Payroll management and HR support',
    icon: 'payroll',
    order: 6,
    is_active: true,
    created_at: new Date()
  }
];

db.services.insertMany(services);

print('✅ MongoDB initialization complete');