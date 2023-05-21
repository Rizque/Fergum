
from django.forms import ModelForm
from .models import WorkerService


class WorkerServiceForm(ModelForm):
    class Meta:
        model = WorkerService
        fields = '__all__'
        exclude = ['worker']

    def __init__(self, *args, **kwargs):
        super(WorkerServiceForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
