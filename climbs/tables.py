import django_tables2 as tables
from .models import Climb, Grade
from django_tables2.utils import A
import datetime

DATE = datetime.date.today()

def row_format(record):
    weeks = ((DATE - record.date_created)/7).days
    if weeks > 9:
        return 'table-danger'
    elif weeks > 7:
        return 'table-warning'
    else:
        return 'table-success'

def query_format(record):
    weeks = ((DATE - record['date_created'])/7).days
    if weeks > 9:
        return 'table-danger'
    elif weeks > 7:
        return 'table-warning'
    else:
        return 'table-success'


class WeeksOldColumn(tables.Column):
    def render(self, value, record):
        weeks = (DATE - record.date_created)/7
        return weeks.days

class ClimbTable(tables.Table):
    # AreaDate =  tables.Column(order_by=('date', 'area'))
    edit = tables.LinkColumn('climb_update', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)
    weeks_old = WeeksOldColumn(empty_values=(), order_by=('date_created'))

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = [ 'anchor', 'area', 'grade', 'color', 'setter']
        sequence = ('selection', 'edit', 'weeks_old', 'area', 'grade', 'color', 'setter','anchor' )
        row_attrs = {
            'class': lambda record: row_format(record)
        }

class QueueTable(tables.Table):
    edit = tables.LinkColumn('climb_update', text='Choose', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['date_created', 'grade']


class ClimbRemoveTable(tables.Table):
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['anchor', 'date_created', 'color', 'grade', 'area', 'setter']


class ClimbQuery(tables.Table):

    date_created = tables.Column()
    area__location_name = tables.Column()
    count = tables.Column()
    min_grade = tables.Column()
    max_grade = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'
        row_attrs = {'class': lambda record: query_format(record)
        }

class GradeSpreadTable(tables.Table):
    grade = tables.Column()
