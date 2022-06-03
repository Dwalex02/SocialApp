from json import JSONEncoder     
from datetime import date


#The encoder from zooma
class JsonEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return obj.__dict__