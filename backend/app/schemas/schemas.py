from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    first_name: str = Field(default="", max_length=80)
    last_name: str = Field(default="", max_length=80)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Resumes ----------
class ResumeAnalysisOut(BaseModel):
    id: int
    filename: str
    ats_score: int
    formatting_score: int
    keywords_score: int
    experience_score: int
    education_score: int
    found_keywords: list[str]
    missing_keywords: list[str]
    suggestions: list[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Jobs ----------
class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    job_type: str
    employment_type: str
    salary_min: int
    salary_max: int
    tags: list[str]
    description: str
    posted_days_ago: int
    match_percent: int | None = None
    saved: bool = False
    applied: bool = False

    class Config:
        from_attributes = True


class ApplicationOut(BaseModel):
    id: int
    job_id: int
    status: str

    class Config:
        from_attributes = True


# ---------- Dashboard ----------
class DashboardOverview(BaseModel):
    ats_score: int
    job_matches: int
    applications_sent: int
    interviews_scheduled: int
    resumes_analyzed: int


# ---------- Builder ----------
class BuilderSaveRequest(BaseModel):
    content: dict


class BuilderDraftOut(BaseModel):
    content: dict
    updated_at: datetime | None = None


# ---------- Admin ----------
class AdminUserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    created_at: datetime
    resume_count: int

    class Config:
        from_attributes = True
