from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance. username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'age', 'profile_picture', 'gender']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name', 'level']


class DepartmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'specialty_name',]


class SpecialtySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty_name',]


class DoctorListSerializer(serializers.ModelSerializer):
    specialty = SpecialtySimpleSerializer(read_only=True, many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialty', 'department', 'shift_start',
                  'shift_start', 'shift_end', 'work_day', 'user']


class DoctorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name',]


class DoctorDetailSerializer(serializers.ModelSerializer):
    specialty = SpecialtySimpleSerializer(read_only=True, many=True)
    department = DepartmentSimpleSerializer()

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialty', 'department', 'shift_start',
                  'shift_start', 'shift_end', 'work_day',]


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'emergency_contact', 'blood_type']


class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name',]


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'user', 'emergency_contact', 'blood_type']


class AppointmentListSerializers(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    doctor = DoctorSimpleSerializer()
    patient = PatientSimpleSerializer()

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'status', 'date_time']


class AppointmentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'status', 'date_time']


# class AppointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = ['patient', 'doctor', 'date_time', 'status']


class MedicalRecordListSerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    doctor = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']


class MedicalRecordCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']


# class MedicalRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicalRecord
#         fields = ['patient', 'doctor', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']


class FeedbackListSerializer(serializers.ModelSerializer):
    doctor = DoctorSimpleSerializer()
    patient = PatientSimpleSerializer()
    # avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['doctor', 'patient', 'rating', 'comment', 'created_at']

    # def get_avg_rating(self, obj):
    #     return obj.get_avg_rating()


class FeedbackDetailSerializer(serializers.ModelSerializer):
    doctor = DoctorSimpleSerializer()
    patient = PatientSimpleSerializer()

    class Meta:
        model = Feedback
        fields = ['doctor', 'patient', 'rating', 'comment', 'avg_rating']


# class FeedbackRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FeedbackRating
#         fields = ['patient', 'rating', 'created_date']


class WardsListSerializers(serializers.ModelSerializer):
    patients = PatientSimpleSerializer(read_only=True, many=True)
    count_patient = serializers.SerializerMethodField()
    total_capacity = serializers.SerializerMethodField()

    class Meta:
        model = Ward
        fields = ['type_ward', 'total_people', 'current_people']


class WardsCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['type_ward', 'total_people', 'current_people']



# class WardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ward
#         fields = ['type_ward', 'total_people', 'current_people']
