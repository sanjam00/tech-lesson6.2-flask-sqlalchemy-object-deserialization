# lib/post_load.py

from marshmallow import Schema, fields, post_load
from pprint import pprint

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging
        
    def give_treat(self):
        self.tail_wagging = True
        
    def scold(self):
        self.tail_wagging = False

# schema
class DogSchema(Schema):
    name = fields.Str()
    breed = fields.Str()
    tail_wagging = fields.Boolean()

    # take a dictionary of deserialized data and return a model instance
    @post_load
    def make_dog(self, data, **kwargs):
        return Dog(**data)

# deserialize to a class instance by defining a @post_load method in the schema
dog_schema = DogSchema()
dog_json = '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
dog = dog_schema.loads(dog_json)
print(type(dog))             # => <class 'dict'>
print(isinstance(dog, Dog))  # => True
pprint(dog)                  # => <models.Dog object at 0x102c28d90>

# call instance methods to change object state, deserialize to JSON using dumps()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
dog.scold()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": false}'
dog.give_treat()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'