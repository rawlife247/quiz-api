from django.core.management import BaseCommand
from faker import Faker

from quiz.models import Category


class Command(BaseCommand):
    help = 'Create categories'

    def add_arguments(self, parser):
        parser.add_argument('num_categories', type=int, help='Number of categories to create')

    def handle(self, *args, **options):
        num_categories = options['num_categories']
        faker = Faker()

        for _ in range(num_categories):
            Category.objects.get_or_create(name=faker.word().capitalize())

        self.stdout.write(self.style.SUCCESS('Categories have been created...'))
