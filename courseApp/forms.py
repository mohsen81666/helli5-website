from django import forms
from .models import *

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class StudentReportForm(forms.Form):
    report_title = forms.ChoiceField()  # Initializes in __init__
    files = MultipleFileField(required=True, label='',
                              help_text="<br>نام فایلها باید شماره دانش آموزی باشد با یکی از فرمتهای png , jpg , pdf." +
                                        "<br>انتخاب فایلها در تعداد کمتر، امکان رخداد خطا را کم می کند.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        report_titles = [(s.title, s.title) for s in Report.objects.all()]
        self.fields['report_title'] = forms.ChoiceField(required=True, label='عنوان کارنامه',
                                                        choices=report_titles,
                                                        help_text="برای اضافه کردن عنوان جدید به بخش ادمین مراجعه کنید.")

