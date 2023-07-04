from django.core.management import BaseCommand, call_command
from faker import Faker
from quiz.models import Category, Tag, Quiz, QuestionType, Question, Answer
import random

from account.models import UserProfile


class Command(BaseCommand):
    help = 'Populate the database with sample data for the Quiz app'

    def add_arguments(self, parser):
        parser.add_argument('num_quizzes', type=int, help='Number of quizzes to create')
        parser.add_argument('num_questions_per_quiz', type=int, help='Number of questions per quiz')

    def handle(self, *args, **options):
        num_quizzes = options['num_quizzes']
        num_questions_per_quiz = options['num_questions_per_quiz']
        faker = Faker()

        if not UserProfile.objects.exists():
            call_command('create_users', 10, 'users.txt')

        if not Tag.objects.exists():
            call_command('create_tags', 5)

        if not Category.objects.exists():
            call_command('create_categories', 5)

        # Create quizzes
        for _ in range(num_quizzes):
            title = faker.sentence()
            description = faker.paragraph()
            time_limit = faker.random_int(min=10, max=60)
            created_by = UserProfile.objects.order_by('?').first()
            categories = Category.objects.order_by('?')[:2]
            tags = Tag.objects.order_by('?')[:3]

            quiz = Quiz.objects.create(
                title=title,
                description=description,
                time_limit=time_limit,
                created_by=created_by,

            )
            quiz.categories.set(categories)
            quiz.tags.set(tags)

            # Create questions
            for _ in range(num_questions_per_quiz):
                text = faker.sentence()
                type = faker.random_element(
                    [QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE])
                points = faker.random_int(min=1, max=10)

                question = Question.objects.create(
                    quiz=quiz,
                    text=text,
                    type=type,
                    points=points,
                )

                # Create answers
                if type == QuestionType.MULTIPLE_CHOICE:
                    answers = [
                        Answer(question=question, text=faker.sentence(), is_correct=True),
                        Answer(question=question, text=faker.sentence(), is_correct=False),
                        Answer(question=question, text=faker.sentence(), is_correct=False),
                        Answer(question=question, text=faker.sentence(), is_correct=False),
                    ]
                elif type == QuestionType.TRUE_FALSE:
                    answers = [
                        Answer(question=question, text='True', is_correct=True),
                        Answer(question=question, text='False', is_correct=False),
                    ]
                else:  # QuestionType.OPEN_ENDED
                    answers = []

                random.shuffle(answers)
                Answer.objects.bulk_create(answers)

        self.stdout.write(
            f"Sample data populated successfully. Created {num_quizzes} quizzes with {num_questions_per_quiz} questions each.")
