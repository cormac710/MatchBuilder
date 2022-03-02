from pynamodb.models import Model

class CommonModel(Model):

    def as_json(self):
        return self.__dict__['attribute_values']

    @classmethod
    def list_as_json(cls, items_itr):
        r = [item.as_json() for item in items_itr]
        return r
