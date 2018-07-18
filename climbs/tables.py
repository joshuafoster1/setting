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

def test2(record):
    color = record['color__color']
    return color.lower()

def test(value):
    if value <1:
        return "table-grad-green-1"
    elif value < 2:
        return "table-grad-green-2"
    elif value < 3:
        return "table-grad-green-3"
    elif value < 4:
        return "table-grad-green-4"
    elif value < 5:
        return "table-grad-green-5"
    elif value < 6:
        return "table-grad-green-6"
    elif value < 7:
        return "table-grad-green-7"
    elif value < 8:
        return "table-grad-green-8"
    elif value < 9:
        return "table-grad-green-9"
    else:
        return "table-grad-green-10"


class WeeksOldColumn(tables.Column):
    def render(self, value, record):
        weeks = (DATE - record.date_created)/7
        return weeks.days

class DataGradientDisplayColumn(tables.Column):
    attrs={'td':{'class':lambda value: test(value)}}
    def render(self, value, record):
        return value

class InProgressTable(tables.Table):
    revert = tables.LinkColumn('revert_climb', text='Revert', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    update = tables.LinkColumn('climb_update', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = [ 'anchor', 'area', 'grade', 'color', 'setter', 'notes']
        sequence = ('update', 'area', 'grade', 'color', 'notes', 'setter','anchor' )


class ClimbTable(tables.Table):
    # AreaDate =  tables.Column(order_by=('date', 'area'))
    update = tables.LinkColumn('climb_update', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    selection = tables.CheckBoxColumn(accessor='pk', orderable = True)
    weeks_old = WeeksOldColumn(empty_values=(), order_by=('date_created'))

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = [ 'anchor', 'area', 'grade', 'color', 'setter', 'date_created']
        sequence = ('selection', 'update', 'date_created', 'weeks_old', 'area', 'grade', 'color', 'setter','anchor' )
        row_attrs = {
            'class': lambda record: row_format(record)
        }

class ClimbQueryTable(ClimbTable):
    # update = tables.LinkColumn('climb_select', text='Edit', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    selection = tables.CheckBoxColumn(accessor='pk', checked=True, orderable = True)
    weeks_old = WeeksOldColumn(empty_values=(), order_by=('date_created'))

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = [ 'anchor', 'area', 'grade', 'color', 'setter']
        sequence = ('selection', 'update', 'weeks_old', 'area', 'grade', 'color', 'setter','anchor' )
        row_attrs = {
            'class': lambda record: row_format(record)
        }

class QueueTable(tables.Table):
    '''Represent recommendation for climbs to be set'''
    choose = tables.LinkColumn('climb_select', text='Choose', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['grade', 'area', 'notes']

class ForemanQueueTable(tables.Table):
    modify = tables.LinkColumn('queue_modify', text='Change', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['grade', 'area', 'notes']

class ClimbRemoveTable(tables.Table):
    # selection = tables.CheckBoxColumn(accessor='id', checked=True, orderable = True)

    class Meta:
        model = Climb
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['date_created', 'color', 'grade', 'area', 'setter', 'anchor']


class ClimbQuery(tables.Table):
    selection = tables.CheckBoxColumn(accessor='date_created', orderable = True)

    date_created = tables.Column()
    area__location_name = tables.Column()
    count = tables.Column()
    min_grade = tables.Column()
    max_grade = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'
        row_attrs = {'class': lambda record: query_format(record)
        }
class NeededClimbsTable(tables.Table):
    grade = tables.Column()
    needed = tables.Column()
    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'

class GradeSpreadTable(tables.Table):
    grade = tables.Column()

class GradePivotTable(tables.Table):
    grade = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'

class ClimbColorTable(tables.Table):
    color__color = tables.Column(verbose_name="Color")
    count = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'
        row_attrs = {'class': lambda record: test2(record)
        }
