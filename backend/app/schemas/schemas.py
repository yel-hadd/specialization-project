import datetime as dt

from pydantic import BaseModel, ConfigDict, EmailStr


# Auth
class UserCreate(BaseModel):
    # Public self-registration always creates a "staff" account; the role is not
    # accepted from the request body to prevent privilege escalation to admin.
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Core entities
class ClassOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    level: str | None = None
    academic_year: str | None = None


class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    name: str
    coefficient: float
    ects: int | None = None


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_code: str
    first_name: str
    last_name: str
    email: str | None = None
    class_id: int | None = None


class GradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    module_id: int
    value: float
    assessment_type: str | None = None
    period: str | None = None
    date: dt.date | None = None


class AbsenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    module_id: int | None = None
    date: dt.date | None = None
    hours: float
    type: str
    justified: bool


# Imports
class ImportLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filename: str
    type: str
    imported_at: dt.datetime
    rows_processed: int
    rows_rejected: int
    status: str
    error_log: str | None = None


class ImportResult(BaseModel):
    import_id: int
    filename: str
    type: str
    rows_processed: int
    rows_rejected: int
    status: str
    errors: list[str] = []
    warnings: list[str] = []


# Alerts
class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    alert_type: str
    severity: str
    message: str
    threshold_value: float | None = None
    metric_value: float | None = None
    created_at: dt.datetime
    resolved: bool


# Analytics
class StudentDetail(BaseModel):
    student: StudentOut
    class_name: str | None = None
    average: float | None = None
    absence_hours: float
    absence_rate: float
    rank: int | None = None
    class_size: int | None = None
    risk_segment: str
    grades: list[GradeOut]
    absences: list[AbsenceOut]
    progression: list[dict]  # list of {period, average}
    recommendations: list[str]
