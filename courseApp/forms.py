from django import forms
from courseApp.models import Reports, StudentReports

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


class reportForm(forms.Form):
    report_title = forms.ChoiceField(required=False, label='کارنامه', choices=[])
    files = MultipleFileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        reports = [(s.title, s.title) for s in
                   Reports.objects.all()]
        self.fields['report_title'] = forms.ChoiceField(required=False, label='کارنامه', choices=reports)


    class Meta:
        # model = StudentReports
        fields = ('report_title', 'files')
