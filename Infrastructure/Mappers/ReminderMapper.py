from Core.Entities.Reminder import Reminder
from Infrastructure.Dto.ReminderDto import ReminderDto

class ReminderMapper:
    @staticmethod
    def to_entity(dto: ReminderDto) -> Reminder:
        return Reminder.create(
            self_id=dto.self_id,
            lesson_id=dto.lesson_id,
            student_id=dto.student_id,
            trigger_time=dto.trigger_time,
            is_sent=dto.is_sent
        )

    @staticmethod
    def to_dto(ent: Reminder) -> ReminderDto:
        return ReminderDto(
            self_id=ent.self_id,
            lesson_id=ent.lesson_id,
            student_id=ent.student_id,
            trigger_time=ent.trigger_time,
            is_sent=ent.is_sent
        )
