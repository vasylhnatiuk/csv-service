from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    ALL_GENDERS = [gender for gender, _ in GENDER_CHOICES]
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.category.name},{self.first_name},{self.last_name},{self.email},{self.gender},{self.birth_date}"
