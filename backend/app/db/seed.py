from app.core.database import SessionLocal
from app.db.init_db import init_db
from app.models import JobPosting

MOCK_JOBS = [
    dict(title="Senior Frontend Engineer", company="Stripe", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=140000, salary_max=180000,
         tags="React,TypeScript,GraphQL,Node.js", posted_days_ago=2,
         description="Build and scale Stripe's customer-facing dashboards using React and TypeScript."),
    dict(title="Product Designer", company="Figma", location="San Francisco",
         job_type="Hybrid", employment_type="Full-Time", salary_min=120000, salary_max=160000,
         tags="Figma,UX,Prototyping", posted_days_ago=5,
         description="Design intuitive product experiences for millions of Figma users."),
    dict(title="React Developer", company="Vercel", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=110000, salary_max=145000,
         tags="React,Next.js,Vercel,Performance", posted_days_ago=7,
         description="Work on Next.js core and developer experience tooling."),
    dict(title="UX Engineer", company="Linear", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=130000, salary_max=170000,
         tags="React,Design Systems,Animation", posted_days_ago=3,
         description="Build delightful, fast UI components and design systems."),
    dict(title="Backend Engineer", company="Notion", location="San Francisco",
         job_type="On-Site", employment_type="Full-Time", salary_min=135000, salary_max=175000,
         tags="Python,SQL,AWS,REST API", posted_days_ago=4,
         description="Design and scale Notion's backend services and data pipelines."),
    dict(title="Data Scientist", company="Airbnb", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=140000, salary_max=190000,
         tags="Python,Machine Learning,SQL", posted_days_ago=1,
         description="Build machine learning models to improve guest matching and pricing."),
    dict(title="DevOps Engineer", company="Datadog", location="New York",
         job_type="Hybrid", employment_type="Full-Time", salary_min=125000, salary_max=165000,
         tags="Docker,Kubernetes,AWS,CI/CD", posted_days_ago=6,
         description="Own CI/CD pipelines and Kubernetes infrastructure at scale."),
    dict(title="Full-Stack Engineer", company="Shopify", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=120000, salary_max=160000,
         tags="React,Node.js,GraphQL,Ruby", posted_days_ago=8,
         description="Build merchant-facing features across Shopify's commerce platform."),
    dict(title="Mobile Engineer (iOS)", company="Duolingo", location="Pittsburgh",
         job_type="On-Site", employment_type="Full-Time", salary_min=115000, salary_max=155000,
         tags="Swift,iOS,Mobile", posted_days_ago=10,
         description="Build delightful learning experiences for iOS users."),
    dict(title="Engineering Manager", company="GitHub", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=160000, salary_max=210000,
         tags="Leadership,Agile,React,Node.js", posted_days_ago=12,
         description="Lead a team of engineers building developer tools used by millions."),
    dict(title="QA Automation Engineer", company="Asana", location="Remote",
         job_type="Remote", employment_type="Contract", salary_min=90000, salary_max=120000,
         tags="Python,CI/CD,Testing", posted_days_ago=9,
         description="Build automated test suites to ensure product quality at scale."),
    dict(title="Machine Learning Engineer", company="Anthropic", location="San Francisco",
         job_type="Hybrid", employment_type="Full-Time", salary_min=170000, salary_max=230000,
         tags="Python,Machine Learning,PyTorch", posted_days_ago=2,
         description="Research and build large-scale machine learning systems."),
    dict(title="Cloud Solutions Architect", company="Snowflake", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=150000, salary_max=200000,
         tags="AWS,Azure,GCP,SQL", posted_days_ago=15,
         description="Design cloud-native data architecture solutions for enterprise clients."),
    dict(title="Junior Frontend Developer", company="Canva", location="Remote",
         job_type="Remote", employment_type="Full-Time", salary_min=70000, salary_max=95000,
         tags="React,JavaScript,CSS,HTML", posted_days_ago=3,
         description="Join our frontend team building creative tools for millions of users."),
    dict(title="Security Engineer", company="Cloudflare", location="Austin",
         job_type="On-Site", employment_type="Full-Time", salary_min=140000, salary_max=185000,
         tags="Security,Python,AWS", posted_days_ago=11,
         description="Protect Cloudflare's global network and customer infrastructure."),
]


def seed_jobs():
    init_db()
    db = SessionLocal()
    try:
        if db.query(JobPosting).count() > 0:
            return
        for job_data in MOCK_JOBS:
            db.add(JobPosting(**job_data))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_jobs()
    print("Database initialized and seeded.")
