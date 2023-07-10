from account.models import UserProfile
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = 'Populate the database with fake users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of users to create')
        parser.add_argument('output_file', type=str, help='Output file path')

    def handle(self, *args, **options):
        num_users = options['num_users']
        output_file = options['output_file']
        faker = Faker()

        created_users = 0
        user_data = []

        while created_users < num_users:
            username = faker.user_name()
            email = faker.email()
            password = faker.password()

            if not UserProfile.objects.filter(username=username).exists() and not UserProfile.objects.filter(
                    email=email).exists():
                user = UserProfile.objects.create_user(
                    username=username,
                    email=email,
                    password=password,

                    gender=faker.random_element(['male', 'female', 'other']),
                    biography=faker.text(),
                    contact_number=faker.phone_number(),
                    address=faker.address(),
                    first_name=faker.first_name(),
                    last_name=faker.last_name()
                )
                user_data.append({
                    'username': username,
                    'password': password,
                })
                self.stdout.write(f"User {user.username} created successfully. Password: {password}")
                created_users += 1

        # Save usernames and passwords to file
        try:
            with open(output_file, 'w') as file:
                for data in user_data:
                    file.write(f"Username: {data['username']}, Password: {data['password']}\n")
        except IOError as e:
            self.stderr.write(f"Error: {str(e)}")
            return

        self.stdout.write(self.style.SUCCESS(f"Usernames and passwords saved to {output_file}"))
