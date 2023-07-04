from django.core.management import BaseCommand
from faker import Faker

from quiz.models import Tag


class Command(BaseCommand):
    help = 'Create tags'

    def add_arguments(self, parser):
        parser.add_argument('num_tags', type=int, help='Number of tags to create')

    def handle(self, *args, **options):
        num_tags = options['num_tags']
        faker = Faker()

        for _ in range(num_tags):
            Tag.objects.get_or_create(name=faker.word().capitalize())

        self.stdout.write(self.style.SUCCESS('Tags have been created...'))