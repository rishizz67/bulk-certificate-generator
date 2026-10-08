from pydantic import BaseModel, EmailStr, Field


class Recipient(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    course: str = Field(..., min_length=2, max_length=200)


class JobCreate(BaseModel):
    event_name: str = Field(..., min_length=2, max_length=200)
    organization: str = Field(..., min_length=2, max_length=200)
    recipients: list[Recipient] = Field(..., min_length=1)


class JobResponse(BaseModel):
    job_id: int
    status: str
    total: int
