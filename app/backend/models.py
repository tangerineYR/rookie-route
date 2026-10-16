from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from database import Base
from error_types import ErrorType


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1, nullable=False)
    submissions = relationship(
        'Submission', back_populates='owner', cascade='all, delete-orphan', passive_deletes=True,
    )


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    code_snippet = Column(Text, nullable=False)
    language = Column(String(20), nullable=False)
    summary = Column(String(2000))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship('User', back_populates='submissions')
    weaknesses = relationship(
        'Weakness', back_populates='submission', cascade='all, delete-orphan', passive_deletes=True,
    )


class Weakness(Base):
    __tablename__ = 'weaknesses'

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    type = Column(Enum(
        ErrorType, native_enum=False, create_constraint=True,
        validate_strings=True, name='error_type', length=100,
    ), index=True, nullable=False)
    line = Column(Integer)
    explanation = Column(Text, nullable=False)
    submission = relationship('Submission', back_populates='weaknesses')
