from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from account.models import UserProfile


class Category(models.Model):
    """
    Represents a category for quizzes.
    Use Case: Categorizing quizzes based on different topics or subjects.
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a tag for quizzes.
    Use Case: Tagging quizzes with relevant keywords or labels for easier searching and organization.
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    """
    Represents a quiz containing multiple questions.
    Use Case: Creating and managing quizzes with titles, descriptions, time limits, and associations to categories and tags.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.PositiveIntegerField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class QuestionType(models.TextChoices):
    """
    Represents the types of questions that can be used in quizzes.
    Use Case: Providing predefined options for the types of questions that can be created.
    """

    MULTIPLE_CHOICE = 'MC', _('Multiple Choice')
    TRUE_FALSE = 'TF', _('True/False')
    OPEN_ENDED = 'OE', _('Open-Ended')


class Question(models.Model):
    """
    Represents a question within a quiz.
    Use Case: Storing individual questions with associated quizzes, text content, types, and point values.
    """

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    type = models.CharField(max_length=2, choices=QuestionType.choices)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.text


class Answer(models.Model):
    """
    Represents an answer for a question.
    Use Case: Capturing possible answers for each question, along with an indicator of correctness.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text


class Participant(models.Model):
    """
    Represents a participant who takes a quiz.
    Use Case: Managing participants' involvement in quizzes, tracking start and end times, and recording scores.
    """

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


class Feedback(models.Model):
    """
    Represents feedback provided by a participant for a quiz.
    Use Case: Collecting participants' ratings and comments for quizzes to gather feedback and improve future quizzes.
    """

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f"Feedback for Quiz {self.quiz.title} by {self.participant.user.username}"
