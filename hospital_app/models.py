from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


ROLE_CHOICES = (
    ('doctor', 'doctor'),
    ('patient', 'patient')
)


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models. PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                        MaxValueValidator(110)],
                                            null=True, blank=True)
    profile_picture = models. ImageField(upload_to='profile_images/')
    gender = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Department(models. Model): #Отделение
    department_name = models.CharField(max_length=16)
    level = models. SmallIntegerField(validators=[MinValueValidator(-5),
                                      MaxValueValidator(5)])

    def __str__(self):
        return self.department_name


class Specialty(models. Model):#Специальность
    specialty_name = models. CharField(max_length=64)

    def __str__(self):
        return self.specialty_name


class Doctor(UserProfile):
    DAY_CHOICES = (
        ('ПН', "ПH"),
        ('BT', 'BT'),
        ('CP', 'CP'),
        ('ЧТ', 'ЧТ'),
        ('ПТ', 'ПТ'),
        ('СБ', 'СБ')
    )
    work_day = MultiSelectField(choices=DAY_CHOICES, max_choices=6, max_length=16)
    experience = models. PositiveSmallIntegerField(validators=[MaxValueValidator(50)])
    specialty = models.ManyToManyField(Specialty)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    service_price = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200000)])
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='doctor')

    def __str__(self):
        return f'{self.first_name}, {self.specialty}'

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctor_Profile"


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user')
    emergency_contact = PhoneNumberField()
    BLOOD_CHOICES = (
        ('I+', 'I+'),
        ('I-', 'I-'),
        ('II+', 'II+'),
        ('II-', 'II-'),
        ('III+', 'III+'),
        ('III-', 'III-'),
        ('IV+', 'IV+'),
        ('IV-', 'IV-')
    )
    blood_type = models.CharField(choices=BLOOD_CHOICES, max_length=6)

    def __str__(self):
        return f'{self.first_name}, {self.blood_type}'


class Appointment (models. Model):#Встреча
    patient = models. ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models. ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models. DateTimeField()
    STATUS_CHOICES = (
        ('запланировано', 'запланировано'),
        ('завершено', 'завершено'),
        ('отменено', 'отменено')
    )
    status = models. CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.patient}, {self.doctor}, {self.date_time}'


class MedicalRecord(models. Model):#Медицинская запись
    patient = models. ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models. ForeignKey(Doctor, on_delete=models. CASCADE)
    diagnosis = models. TextField()
    treatment = models. TextField()
    prescribed_medication = models. TextField()
    created_at = models. DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient}, {self.doctor}'


class Feedback(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)],
                                              null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return f'{self.patient}'


    # def get_average_rating(self):
    #     rating = self.rating.all()
    #     if rating.exists():
    #         return round(sum(rating.stars for rating in rating) / rating.count(), 1)
    #     return 0


# class FeedbackRating(models.Model):
#     patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='p_review')
#     # courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_review')
#     rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
#    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient}, {self.rating}'

    def get_avg_ratings(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0
        # рточо маанисин табат

    def get_total_people(self):
        ratings = self.reviews.all()
        if ratings.exists():
            if ratings.count() > 3:
                return f'3+'
            return ratings.count()
        return 0
        # если рейтингдер бар болсо жана алардын саны 3тон коп болсо 3 + деп чыгарат
        # если рейтингдер 3 же андан аз болсо так сандарды чыгарат
        # если рейтинг жок болсо анда 0ду чыгарып берет

    def get_check_good(self):
        ratings = self.reviews.all()
        if ratings.exists():
            num = 0
            for i in ratings:
                if i.rating > 3:
                    num += 1
            return f'{round((num * 100) / ratings.count())}%'
        return f'0%'

    # Эгерде рейтингдер бар болсо, ал 3төн жогору рейтингдердин санын эсептеп, андан кийин ошол санды жалпы рейтингдердин санына бөлүп, пайызын чыгарат.
    # Эгерде рейтингдер жок болсо, анда 0% кайтарат.


class Ward(models.Model):#Сторожить
    TYPE_CHOICES = (
        ('Vip', 'Vip'),
        ('Simple', 'Simple'),
        ('Medium', 'Medium')
    )
    type_ward = models.CharField(max_length=16, choices=TYPE_CHOICES)
    total_people = models.PositiveSmallIntegerField(validators=[MaxValueValidator(20)])
    current_people = models.PositiveSmallIntegerField(validators=[MaxValueValidator(20)])

    def __str__(self):
        return self.type_ward


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    create_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)

