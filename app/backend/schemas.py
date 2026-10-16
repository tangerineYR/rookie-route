from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from error_types import ErrorType


class AIWeakness(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: ErrorType
    line: int | None = Field(default=None, ge=0, le=15000, strict=True)
    explanation: str = Field(min_length=1, max_length=10000, strict=True)


class AIAnalysisResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    summary: str = Field(min_length=1, max_length=2000, strict=True)
    weaknesses: list[AIWeakness] = Field(max_length=100)


class CodeRequest(BaseModel):
    code: str = Field(min_length=1, max_length=15000)
    language: str = Field(min_length=1, max_length=20, pattern=r'^[a-zA-Z0-9+#.-]+$')


class AnalysisResponse(AIAnalysisResult):
    submission_id: int


class StatItem(BaseModel):
    weakness_type: ErrorType
    count: int


class DashboardResponse(BaseModel):
    total_submissions: int
    stats: list[StatItem]


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=72)

    @field_validator('password')
    @classmethod
    def bcrypt_length(cls, value: str) -> str:
        if len(value.encode('utf-8')) > 72:
            raise ValueError('Password must be at most 72 UTF-8 bytes')
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
