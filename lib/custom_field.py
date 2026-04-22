# lib/custom_field.py 

from marshmallow import Schema, fields, post_load
from datetime import date
from pprint import pprint

# model 

class Cat:
    def __init__(self, name, dob, favorite_toys = []):
        self.name = name
        self.dob = dob
        self.favorite_toys = favorite_toys

# schema

class CatSchema(Schema):
    name = fields.Str(required=True, error_messages={"required": "Name is required."})
    dob = fields.Date(format="%Y-%m-%d")
    favorite_toys = fields.List(fields.Str())
    likes_toys = fields.Function(lambda obj : len(obj.favorite_toys) > 0, dump_only = True)
    age = fields.Method("calculate_age", dump_only = True)

    def calculate_age(self, obj):
        today = date.today()
        return today.year - obj.dob.year - ((today.month, today.day) < (obj.dob.month, obj.dob.day))
    
    @post_load
    def make_cat(self, data, **kwargs):
        return Cat(**data)
    
schema = CatSchema()
    
#deserialize
cat_1 = schema.load({"name": "Meowie", "dob": "2020-11-28", "favorite_toys": ["ball", "squeaky mouse"]})
cat_2 = schema.load({"name": "Whiskers", "dob": "2015-4-15", "favorite_toys": []})

#serialize
pprint(schema.dump(cat_1))
# => {'age': 2,
# =>  'dob': '2020-11-28',
# =>  'favorite_toys': ['ball', 'squeaky mouse'],
# =>  'likes_toys': True,
# =>  'name': 'Meowie'}

pprint(schema.dump(cat_2))
# => {'age': 8,
# => 'dob': '2015-04-15',
# => 'favorite_toys': [],
# => 'likes_toys': False,
# => 'name': 'Whiskers'}
