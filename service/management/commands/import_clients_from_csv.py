import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from service.models import Category, Client  # Import your Category and Client models


class Command(BaseCommand):
    help = 'Import clients from a CSV file'

    GENDER_CHOICES = [Client.MALE, Client.FEMALE, Client.OTHER]

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)

            client_list = []

            for row in reader:
                category_name, first_name, last_name, email, gender, birth_date = row
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()

                # Check if gender is correct, if not use 'other'
                if gender.lower() not in self.GENDER_CHOICES:
                    gender = Client.OTHER

                # Get or create the Category instance
                category, _ = Category.objects.get_or_create(name=category_name)

                client_list.append(Client(
                    category=category,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    gender=gender,
                    birth_date=birth_date
                ))

            Client.objects.bulk_create(client_list)

            self.stdout.write(self.style.SUCCESS('Clients imported successfully'))
