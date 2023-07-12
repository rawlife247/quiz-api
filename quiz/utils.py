from django.utils import timezone
from datetime import timedelta

from quiz.models import Participant

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def generate_participant_report(participant):
    user = participant.user

    report_content = {
        'full_name': user.first_name + " " + user.last_name,
        'quiz_title': participant.quiz.title,
        'quiz_total_point': participant.quiz.get_total_points(),
        'score': participant.score,
        'has_passed': participant.has_passed,
        'attempted_quiz': []
    }
    current_datetime = timezone.now()
    last_week_start = current_datetime - timedelta(days=7)

    # Filter participants based on their end_time within the last week
    participants_last_week = Participant.objects.filter(user=user, end_time__gte=last_week_start)[:7]

    for participant_history in participants_last_week:
        quiz = participant_history.quiz
        attempted_quiz = {
            'quiz_title': quiz.title,
            'quiz_total_point': quiz.get_total_points(),
            'score': participant_history.score,
            'has_passed': participant_history.has_passed,
        }
        report_content['attempted_quiz'].append(attempted_quiz)

    return report_content


def send_participant_report_email(report_content, email):
    subject = "Quiz Report"
    email_from = settings.EMAIL_HOST_USER

    html_template = 'sent_participant_analytics.html'
    html_message = render_to_string(html_template, context={'report': report_content})

    recipient_list = [email]

    try:
        message = EmailMessage(subject, html_message, email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        return {"is_sent": True}
    except Exception as e:
        return {"is_sent": False, "message": f"An error occurred while sending the email: {str(e)}"}
