from marshmallow import Schema, fields, EXCLUDE, post_load

class CourseSchema(Schema):
    class Meta:
        unkown = EXCLUDE
    course = fields.Str()
    credit = fields.Float()
    credit_hour_total = fields.Float()
    lesson_hour = fields.Float() 
    lab_hour = fields.Float()
    category = fields.Str()
    teacher = fields.Str()
    week = fields.Str() 
    time = fields.Str()
    address = fields.Str()

    @post_load()
    def wrap(self, data, **kwargs):
        data['teacher'] = {'name': data.pop("teacher", None)}
        data["meta"] = {'course': data.pop("course", None), 'credit': data.pop("credit", None)}
        data['time'] = {'week': data.pop('week', None), 'time': data.pop('time', None)}
        return data
