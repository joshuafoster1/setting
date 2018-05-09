import pygsheets



google = pygsheets.authorize()

spreadsheet = google.open('TouchstoneSettingDBinfo')
Data = list(spreadsheet.worksheet('title', 'data'))
Colors = list(spreadsheet.worksheet('title', 'Colors'))
Area = list(spreadsheet.worksheet('title', 'Area'))
Grade = list(spreadsheet.worksheet('title', 'Grade'))
Setter = list(spreadsheet.worksheet('title', 'Setter'))
Anchor = list(spreadsheet.worksheet('title', 'Anchor'))
oid = 0
climbList = []
# class DBClimb:
#     __init__(self, id, climb_route, status, date_created, color, grade)
#         self.id = id
#         self.climb_route = climb_route
#         self.status = status
#         self.date_created = date_created
#         self.color = color
#         self.grade = grade
del Data[0]
# del Anchor[0]
for row in Data:
    date = row[0]
    color = row[1]
    grade = row[2]
    setter = row[3]
    area = row[4]
    anchor = row[5]
    for row in Colors:
        if color == row[1]:
            color = row[0]
    for row in Grade:
        if row[1] == '5.9':
            rowGrade = row[1]
        elif row[1].startswith('5'):
            rowGrade = row[1].split('.')[1]
        else:
            rowGrade = row[1]
        if grade == rowGrade:
            grade = row[0]
    for row in Setter:
        if setter == row[1]:
            setter = row[0]
    for row in Area:
        if area == row[2]:
            area = row[0]
    for row in Anchor:
        if anchor == row[1]:
            anchor = row[0]

    oid = oid + 1

    climbList.append([oid, anchor, 1, date, None, color, grade, area, setter])
print(climbList)
Climbs = spreadsheet.worksheet('title', 'Climbs')
# row = len(Climbs.get_col(column_keys['id'])) + 1 #increment to new row
Climbs.update_cells(crange='A2', values = climbList)
