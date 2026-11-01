from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
    text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    student_id: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(120))

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("position('@' in email) > 1", name="ck_users_email"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(
        String(20), default="waiting", server_default="waiting"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT")
    )

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
        CheckConstraint(
            "(status IN ('called', 'served', 'no-show')) = (called_at IS NOT NULL)",
            name="ck_tickets_called_at",
        ),
        # A student can hold only one active ticket per service.
        Index(
            "uq_tickets_active_user_service",
            "user_id",
            "service_id",
            unique=True,
            postgresql_where=text("status IN ('waiting', 'called')"),
        ),
    )