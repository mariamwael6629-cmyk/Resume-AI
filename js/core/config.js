const API_BASE = 'http://localhost:8000';

let currentPage = 'landing';
let isLight = false;
let currentLang = 'EN';

// Fallback static jobs used only if the backend is unreachable, so the
// demo still looks populated. Real data from GET /api/jobs replaces this
// whenever the backend responds successfully.
const FALLBACK_JOBS = [
  { id: 1, title: 'Senior Frontend Engineer', company: 'Stripe', location: 'Remote', job_type: 'Remote', employment_type: 'Full-Time', salary_min: 140000, salary_max: 180000, tags: ['React','TypeScript','GraphQL','Node.js'], posted_days_ago: 2, match_percent: 94, initial: 'S', grad: 'linear-gradient(135deg,#635bff,#a29bfe)' },
  { id: 2, title: 'Product Designer', company: 'Figma', location: 'San Francisco', job_type: 'Hybrid', employment_type: 'Full-Time', salary_min: 120000, salary_max: 160000, tags: ['Figma','UX','Prototyping'], posted_days_ago: 5, match_percent: 87, initial: 'F', grad: 'linear-gradient(135deg,#f24e1e,#ff7262)' },
  { id: 3, title: 'React Developer', company: 'Vercel', location: 'Remote', job_type: 'Remote', employment_type: 'Full-Time', salary_min: 110000, salary_max: 145000, tags: ['React','Next.js','Vercel','Performance'], posted_days_ago: 7, match_percent: 82, initial: 'V', grad: 'linear-gradient(135deg,#000,#333)' },
  { id: 4, title: 'UX Engineer', company: 'Linear', location: 'Remote', job_type: 'Remote', employment_type: 'Full-Time', salary_min: 130000, salary_max: 170000, tags: ['React','Design Systems','Animation'], posted_days_ago: 3, match_percent: 76, initial: 'L', grad: 'linear-gradient(135deg,#5e6ad2,#7c8bef)' },
];
