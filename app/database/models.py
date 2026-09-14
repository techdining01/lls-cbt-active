from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    func,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class ProductLicense(Base):
    """
    A product license key with activation credits.

    Tracks product keys, their metadata, and remaining activation credits.
    """

    __tablename__ = "product_licenses"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_key: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=2,
    )

    expiry_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    license_metadata: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    activations: Mapped[list["LicenseActivation"]] = relationship(
        back_populates="license",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "credits >= 0",
            name="ck_product_license_credits_non_negative",
        ),
        Index(
            "ix_product_licenses_product_key",
            "product_key",
        ),
    )


class LicenseActivation(Base):
    """
    Records of license activations on specific machines.

    Tracks when and where a license was activated using machine fingerprinting.
    """

    __tablename__ = "license_activations"

    id: Mapped[int] = mapped_column(primary_key=True)

    license_id: Mapped[int] = mapped_column(
        ForeignKey(
            "product_licenses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user_email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    user_name: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
    )

    machine_fingerprint: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    machine_info: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    activated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    last_validated: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    deactivated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    deactivation_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    license: Mapped["ProductLicense"] = relationship(back_populates="activations")

    __table_args__ = (
        Index(
            "ix_license_activations_license_id",
            "license_id",
        ),
        Index(
            "ix_license_activations_machine_fingerprint",
            "machine_fingerprint",
        ),
    )