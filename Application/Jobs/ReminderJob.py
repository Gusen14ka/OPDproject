import asyncio
from datetime import datetime
from Core.Interfaces.ILessonRepository import ILessonRepository
from Core.Interfaces.ITimeSlotRepository import ITimeSlotRepository
from Core.Interfaces.IReminderRepository import IReminderRepository
from Core.UseCases.Reminder.ScheduleRemindersUseCase import ScheduleRemindersUseCase
from Core.Entities.Reminder import Reminder

class ReminderJob:
    def __init__(
        self,
        lesson_repo: ILessonRepository,
        time_slot_repo: ITimeSlotRepository,
        reminder_repo: IReminderRepository
    ):
        self._lesson_repo = lesson_repo
        self._time_slot_repo = time_slot_repo
        self._reminder_repo = reminder_repo
        self._use_case = ScheduleRemindersUseCase(lesson_repo, time_slot_repo, reminder_repo)

    async def run(self):
        # Создаем новые напоминания
        reminders = await self._use_case.execute(hours_ahead=24)
        print(f"Создано напоминаний: {len(reminders)}")

        # Отправляем напоминания, если наступило их время
        now = datetime.now()
        pending_reminders = await self._reminder_repo.get_pending_reminders_async(now)

        if not pending_reminders:
            print("Нет напоминаний для отправки.")
            return

        for reminder in pending_reminders:
            sent = await self._send_notification(reminder)
            if sent:
                await self._reminder_repo.mark_as_sent_async(reminder.self_id)
                print(f"✅ Напоминание {reminder.self_id} отправлено и обновлено.")

    async def _send_notification(self, reminder: Reminder) -> bool:
        # TODO: Подключить реальную систему уведомлений
        print(f"📨 Отправка уведомления студенту {reminder.student_id} (Reminder ID: {reminder.self_id})")
        return True
