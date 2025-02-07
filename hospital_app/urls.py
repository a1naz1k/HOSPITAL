from .views import *
from django.urls import path, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users'),
router.register(r'department', DepartmentViewSet, basename='department'),
router.register(r'specialty', SpecialtyViewSet, basename='specialty'),
#router.register(r'appointment', AppointmentViewSet, basename='appointment'),
#router.register(r'medicalrecord', MedicalRecordViewSet, basename='medicalrecord'),
# router.register(r'feedbeck_rating', FeedbackRatingViewSet, basename='feedbeck_rating'),
#router.register(r'ward', WardViewSet, basename='ward'),

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', include(router.urls)),
    path('doctor/', DoctorListAPIView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', DoctorDetailAPIView.as_view(), name='doct_detail'),

    path('patient/', PatientListAPIView.as_view(), name='patient_list'),
    path('patient/<int:pk>/', PatientDetailAPIView.as_view(), name='patient_detail'),

    path('feedback/', FeedbackListAPIView.as_view(), name='feedback_list'),
    path('feedback/<int:pk>/', FeedbackDetailAPIView.as_view(), name='feedback_detail'),

    path('appointment/', AppointmentListAPIView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/', AppointmentDetailAPIView.as_view(), name='appointment_detail'),
    path('appointment/create/', AppointmentCreateAPIView.as_view(), name='appointment_create'),

    path('medical_record_list/', MedicalRecordListAPIView.as_view(), name='medical_record_list'),
    path('medical_record_list/<int:pk>/', MedicalRecordDetailAPIView.as_view(),name='medical_record_detail'),
    path('medical_record_create/', MedicalRecordCreateAPIView.as_view(), name='medical_record_create'),

    path('ward_list/', WardListAPIView.as_view(), name='departments'),
    path('ward_create/', WardCreateAPIView.as_view(), name='departments'),

]


