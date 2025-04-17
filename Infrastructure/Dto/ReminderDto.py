from Infrastructure.Config import Base
from sqlalchemy import Column, Integer, Boolean, Time, ForeignKey


class ReminderDto(Base):
    __tablename__ = "reminders"

    self_id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.self_id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.self_id", ondelete="CASCADE"), nullable=False)
    trigger_time = Column(Time, nullable=False)
    is_sent = Column(Boolean, nullable=False)
