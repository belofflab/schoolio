import datetime
import uuid
from decimal import Decimal
from typing import List, Optional
from enum import Enum

import ormar
import sqlalchemy
from src.database.connection import database
from src.utils import otp

metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class UserRole(str, Enum):
    ADMIN = "admin"
    SCHOOL_CREATOR = "school_creator"
    TEACHER = "teacher"
    STUDENT = "student"


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    idx: int = ormar.BigInteger(primary_key=True)
    username: str = ormar.String(max_length=255, default=None, nullable=True)
    password: str = ormar.String(max_length=1024, nullable=True)
    balance: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
    last_jwt_token: str = ormar.Text(default="")
    is_active: bool = ormar.Boolean(default=False)
    is_admin: bool = ormar.Boolean(default=False)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    otp_secret: str = ormar.String(max_length=256, nullable=True)

    async def generate_otp_secret(self):
        self.otp_secret = otp.generate()
        await self.update()

    async def validate_otp(self, otp):
        if self.otp_secret:
            return self.otp_secret == otp
        return False


class LessonBlock(ormar.Model):
    class Meta(BaseMeta):
        tablename = "lesson_blocks"

    idx: int = ormar.BigInteger(primary_key=True)
    slug: uuid.UUID = ormar.UUID(default=uuid.uuid4)
    order: int = ormar.Integer()
    title: str = ormar.String(max_length=255)
    description: str = ormar.Text()
    preview: str = ormar.String(max_length=500, nullable=True, default=None)
    video_url: str = ormar.String(max_length=500, nullable=True, default=None)


class Course(ormar.Model):
    class Meta(BaseMeta):
        tablename = "courses"

    idx: int = ormar.BigInteger(primary_key=True)
    slug: uuid.UUID = ormar.UUID(default=uuid.uuid4)
    preview: str = ormar.String(max_length=500, nullable=True, default=None)
    title: str = ormar.String(max_length=255)
    description: str = ormar.Text()
    price: Decimal = ormar.Decimal(max_digits=12, decimal_places=2)
    lesson_blocks: List[LessonBlock] = ormar.ManyToMany(LessonBlock)


class UserCourse(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_courses"

    idx: int = ormar.BigInteger(primary_key=True)
    slug: uuid.UUID = ormar.UUID(default=uuid.uuid4)
    user: User = ormar.ForeignKey(User)
    course: Course = ormar.ForeignKey(Course)
    purchased_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)


class UserPaymentRequest(ormar.Model):
    class Meta(BaseMeta):
        tablename="userpayment_requests"
    idx: int = ormar.BigInteger(primary_key=True)
    user: User = ormar.ForeignKey(User)
    course: Course = ormar.ForeignKey(Course)
    is_success: bool = ormar.Boolean(default=False)
    receipt: str = ormar.String(max_length=1024, nullable=True)
    date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    

# class PaymentDetail(ormar.Model):
#     class Meta(BaseMeta):
#         tablename = "payment_details"
#     idx: int = ormar.BigInteger(primary_key=True)
#     name: str = ormar.String(max_length=255)
#     value: str = ormar.String(max_length=255)