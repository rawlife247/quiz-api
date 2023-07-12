import json
import uuid

from celery import shared_task
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from django.utils import timezone
from datetime import timedelta

from quiz.models import Participant
from quiz.utils import generate_participant_report, send_participant_report_email


@shared_task(bind=True)
def send_participant_report(self, **kwargs):
    participant_id = kwargs.get('participant_id')

    try:
        participant = Participant.objects.get(id=participant_id)
        report_content = generate_participant_report(participant)
        send_participant_report_email(report_content, participant.user.email)

    except Participant.DoesNotExist:
        print('Invalid participant')

    return "Done"


def schedule_report_generation(participant_id):
    current_datetime = timezone.now()
    execution_time = current_datetime + timedelta(hours=2)
    schedule, created = ClockedSchedule.objects.get_or_create(clocked_time=execution_time)

    unique_task_id = uuid.uuid4()
    PeriodicTask.objects.create(
        clocked=schedule,
        name='send report to participant id ' + str(participant_id) + ' at - ' + str(schedule) + " #" + str(
            unique_task_id),
        task='quiz.tasks.send_participant_report',
        kwargs=json.dumps({'participant_id': participant_id}),
        one_off=True
    )
