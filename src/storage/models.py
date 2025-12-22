import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from src.storage.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sha256 = Column(String(64), unique=True, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String(128))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    scans = relationship("Scan", back_populates="file")


class Scan(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"))
    status = Column(String(20), nullable=False)
    predicted_class = Column(String(50))
    probabilities = Column(JSONB)
    explain = Column(JSONB)
    model_version = Column(String(50))
    duration_ms = Column(Integer)
    error = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    file = relationship("File", back_populates="scans")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    version = Column(String(50), primary_key=True)
    algo = Column(String(50), nullable=False)
    metrics = Column(JSONB)
    path = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    is_active = Column(Boolean, default=False, nullable=False)


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    source_url = Column(Text, nullable=False)
    license_note = Column(Text)
    samples_count = Column(Integer)
    meta = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
