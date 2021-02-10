import django_tables2 as tables
from .models import Evaluation


class EvaluationTable(tables.Table):
    class Meta:
        model = Evaluation
        sequence = ('id', 'created_by', 'created_at', 'status', 'version')
        exclude = ("jsonData", "person")
        attrs = {"width": "100%"}

    action = tables.TemplateColumn(
        '<a class="button" href="/evaluation/api/eval_pdf/{{record.id}}" target="_blank">Preview</a>&nbsp;'
        '<a class="button" href="/evaluation/api/doh_pdf/{{record.id}}" target="_blank">Generate DOH Form</a>&nbsp;')
