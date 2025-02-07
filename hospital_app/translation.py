from .models import Specialty, MedicalRecord, Feedback, Department
from modeltranslation.translator import TranslationOptions, register


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('department_name',)


@register(Specialty)
class SpecialtyTranslationOptions(TranslationOptions):
    fields = ('specialty_name',)


@register(MedicalRecord)
class MedicalRecordTranslationOptions(TranslationOptions):
    fields = ('diagnosis', 'prescribed_medication')


@register(Feedback)
class FeedbackTranslationOptions(TranslationOptions):
    fields = ('comment',)

