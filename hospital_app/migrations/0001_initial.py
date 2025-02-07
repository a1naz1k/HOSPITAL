# Generated by Django 5.1.5 on 2025-02-06 10:38

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(110)])),
                ('profile_picture', models.ImageField(upload_to='profile_images/')),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=16)),
                ('department_name_en', models.CharField(max_length=16, null=True)),
                ('department_name_ru', models.CharField(max_length=16, null=True)),
                ('level', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(-5), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty_name', models.CharField(max_length=64)),
                ('specialty_name_en', models.CharField(max_length=64, null=True)),
                ('specialty_name_ru', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_ward', models.CharField(choices=[('Vip', 'Vip'), ('Simple', 'Simple'), ('Medium', 'Medium')], max_length=16)),
                ('total_people', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(20)])),
                ('current_people', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(20)])),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('userprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('work_day', multiselectfield.db.fields.MultiSelectField(choices=[('ПН', 'ПH'), ('BT', 'BT'), ('CP', 'CP'), ('ЧТ', 'ЧТ'), ('ПТ', 'ПТ'), ('СБ', 'СБ')], max_length=16)),
                ('experience', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(50)])),
                ('shift_start', models.TimeField()),
                ('shift_end', models.TimeField()),
                ('service_price', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(200000)])),
                ('role', models.CharField(choices=[('doctor', 'doctor'), ('patient', 'patient')], default='doctor', max_length=16)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.department')),
                ('specialty', models.ManyToManyField(to='hospital_app.specialty')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctor_Profile',
            },
            bases=('hospital_app.userprofile',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('emergency_contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('blood_type', models.CharField(choices=[('I+', 'I+'), ('I-', 'I-'), ('II+', 'II+'), ('II-', 'II-'), ('III+', 'III+'), ('III-', 'III-'), ('IV+', 'IV+'), ('IV-', 'IV-')], max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.TextField()),
                ('diagnosis_en', models.TextField(null=True)),
                ('diagnosis_ru', models.TextField(null=True)),
                ('treatment', models.TextField()),
                ('prescribed_medication', models.TextField()),
                ('prescribed_medication_en', models.TextField(null=True)),
                ('prescribed_medication_ru', models.TextField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.patient')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('comment_en', models.TextField(blank=True, null=True)),
                ('comment_ru', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.patient')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='hospital_app.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('запланировано', 'запланировано'), ('завершено', 'завершено'), ('отменено', 'отменено')], max_length=32)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.patient')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.doctor')),
            ],
        ),
    ]
