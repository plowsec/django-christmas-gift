from django.db import models


class Person(models.Model):

    name = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=50, decimal_places=2)

    def __str__(self):
        return self.name


class Gift(models.Model):

    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    bought = models.BooleanField(default=False)
    wrapped = models.BooleanField(default=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
