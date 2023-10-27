import datetime
from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID, uuid4

class UserCreate(BaseModel):
    idx: int
    username: str = None
    password: str = None


class User(UserCreate):
    balance: Decimal
    created_at: datetime.datetime

class CourseCreate(BaseModel):
    title: str
    description: str
    price: Decimal

class Course(CourseCreate):
    idx: int
    slug: UUID

class LessonBlockCreate(BaseModel):
    title: str
    description: str

class LessonBlock(LessonBlockCreate):
    idx: int
    slug: UUID
    course: int
    video_url: str
    preview: str


class UserCourseCreate(BaseModel):
    user: int
    course: int


class UserCourse(BaseModel):
    idx: int
    purchased_at: datetime.datetime


class UserOTPVerify(BaseModel):
    idx: int
    password: str
    otp: str

class UserPaymentRequestCreate(BaseModel):
    user: int
    course: int

class UserPaymentRequest(UserPaymentRequestCreate):
    idx: int 
    is_success: bool
    receipt: str
    date: datetime.datetime

class UserPaymentRequestPatch(BaseModel):
    is_success: bool = False


