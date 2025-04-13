from django.contrib.auth.models import User
from django.db import models
from django.utils import formats


class Expense(models.Model):
    """
    Model for tracking expenses
    """

    title = models.CharField(max_length=255, verbose_name="Intitulé")
    license_plate = models.CharField(max_length=10, verbose_name="Plaque d'immatriculation")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    date = models.DateField(verbose_name="Date")
    linked_user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Utilisateur", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    def save(self, *args, **kwargs):
        # Convert license plate to uppercase
        self.license_plate = self.license_plate.upper()
        super(Expense, self).save(*args, **kwargs)

    def __str__(self):
        formatted_date = formats.date_format(self.date, format="l j F Y")
        return f"{self.title} - {self.license_plate} - {formatted_date}"

    class Meta:
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"
        ordering = ['-date']
