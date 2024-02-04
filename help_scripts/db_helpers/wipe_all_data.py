"""
BACKUP:
    python manage.py makemigrations && python manage.py migrate

    INITIAL DATA:
    python manage.py dumpdata core solver -o db_backup/initial_data.json.xz

    TEST DATA:
    python manage.py dumpdata core solver -o db_backup/test_data.json.xz

run:
    python manage.py runscript help_scripts.db_helpers.wipe_all_data
"""

import logging

# from django_celery_beat.models import (
#     IntervalSchedule,
#     CrontabSchedule,
#     PeriodicTasks,
#     ClockedSchedule,
#     SolarSchedule,
# )

logger = logging.getLogger(__name__)


def run() -> None:
    # IntervalSchedule.objects.all().delete()
    # CrontabSchedule.objects.all().delete()
    # PeriodicTasks.objects.all().delete()
    # ClockedSchedule.objects.all().delete()
    # SolarSchedule.objects.all().delete()

    logger.info(f"Done")
    return None
