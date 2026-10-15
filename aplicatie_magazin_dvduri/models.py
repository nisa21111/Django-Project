from django.db import models

# Create your models here.
class Ambalaj(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nivel_rezistenta__lte=10) & models.Q(nivel_rezistenta__gte=1),
                name='limite_rezista_ambalaj',
                violation_error_message="Nivelul de rezistență trebuie să fie între 1 și 10 inclusiv!"
            )
        ]
    nume=models.CharField(max_length=200, unique=True)
    culoare=models.CharField(max_length=100, null=True)
    nivel_rezistenta=models.PositiveIntegerField(
        help_text="Valori între 1 și 10. Un număr mai mare indică rezistență mai mare",
        null=True
    )
    descriere = models.TextField(null=True)
   
    def __str__(self):
        return f"{self.nume}: {self.culoare}"
