# Этот код для вызова каждые 5 минут, по сути можно перенести ближе к тг
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Infrastructure.Config import async_session_factory
from Infrastructure.Repositories.LessonRepository import LessonRepository
from Infrastructure.Repositories.TimeSlotRepository import TimeSlotRepository
from Infrastructure.Repositories.ReminderRepository import ReminderRepository
from Application.Jobs.ReminderJob import ReminderJob

async def reminder_job_runner():
    """
    Функция-обёртка, создающая необходимые репозитории и выполняющая процесс отправки напоминаний.
    Выполнение происходит через ReminderJob, который:
      - Создаёт напоминания для предстоящих уроков,
      - Ищет напоминания, для которых наступило время отправки,
      - Вызывает метод отправки уведомлений,
      - Помечает напоминания как отправленные.
    """
    async with async_session_factory() as session:
        # Создаем реализации репозиториев, используя асинхронную сессию
        lesson_repo = LessonRepository(session)
        time_slot_repo = TimeSlotRepository(session)
        reminder_repo = ReminderRepository(session)
        # Создаем экземпляр ReminderJob, который использует интерфейсы из Core
        job = ReminderJob(lesson_repo, time_slot_repo, reminder_repo)
        # Выполняем логику отправки напоминаний
        await job.run()

def start_reminder_scheduler():
    """
    Настраивает и запускает APScheduler, который вызывает reminder_job_runner() каждые 5 минут.
    """
    scheduler = AsyncIOScheduler()
    # Добавляем задачу, которая будет выполняться каждые 5 минут
    scheduler.add_job(reminder_job_runner, 'interval', minutes=1)
    scheduler.start()
    print("Сервис отправки уведомлений запущен (напоминания обрабатываются каждые 5 минут).")

if __name__ == '__main__':
    async def main():
        # Запускаем планировщик уведомлений
        start_reminder_scheduler()
        # Чтобы event loop не завершался, ждем бесконечно (или пока не прервется)
        while True:
            await asyncio.sleep(60)

    asyncio.run(main())
