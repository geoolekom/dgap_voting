from import_export import resources

from accounts.models import StudentInfo


class StudentInfoResource(resources.ModelResource):
    class Meta:
        model = StudentInfo
        fields = 'group', 'last_name', 'first_name', 'patronymic', 'email', 'vk_url', 'course', 'room', 'sex',
        import_id_fields = 'email', 'vk_url',

    SEX_MAPPING = {
        'М': StudentInfo.MALE,
        'Ж': StudentInfo.FEMALE,
    }

    COLUMN_LABELS = {
        'group': 'Группа',
        'last_name': 'Фамилия',
        'first_name': 'Имя',
        'patronymic': 'Отчество',
        'email': 'Физтех-почта',
        'vk_url': 'VK',
        'course': 'Курс',
        'room': 'Комната',
        'sex': 'Пол',
    }

    def before_import_row(self, row, **kwargs):
        row['Пол'] = self.SEX_MAPPING.get(row['Пол']) or ''
        row['VK'] = row['VK'] or ''

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        field = super().field_from_django_field(field_name, django_field, readonly)
        field.column_name = cls.COLUMN_LABELS.get(field_name, field_name)
        return field
