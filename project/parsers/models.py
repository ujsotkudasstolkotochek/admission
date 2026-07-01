from django.db import models

class University(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    program_name = models.CharField(max_length=200)
    url = models.URLField()
    budget_places = models.PositiveIntegerField(null=True, blank=True)
    min_score_passed = models.FloatField(null=True, blank=True)
    avg_score_passed = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} {self.name} – {self.program_name}"

class Applicant(models.Model):
    STATUS_CHOICES = (
        ('common', 'Общий конкурс'),
        ('target', 'Целевое'),
        ('special', 'Особая квота'),
        ('no_exam', 'Без вступительных'),
        ('unknown', 'Неизвестно'),
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='applicants')
    position = models.PositiveIntegerField(null=True, blank=True)
    code = models.CharField(max_length=20)
    score = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='common')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['program', 'position']