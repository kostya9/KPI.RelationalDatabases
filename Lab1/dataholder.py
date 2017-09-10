import _pickle as pickle

class ForeignKey():
    def __init__(self, name_fk_entity, name_fk, name_entity):
        self.name_fk_entity = name_fk_entity
        self.name_fk = name_fk
        self.name_entity = name_entity

    def get_fk_value(self, obj):
        return getattr(obj, self.name_fk)

    def has_fk_value(self, obj):
        return hasattr(obj, self.name_fk)

class DataHolder():
    def __init__(self):
        self.data = {}
        self.foreign_keys = []

    def serialize(self, fileName):
        with open(fileName, 'wb') as file:
            pickle.dump(self.data, file)

    def deserialize(self, fileName):
        with open(fileName, 'rb') as file:
            self.data = pickle.load(file)

    def __validate_object(self, name, obj):
        if name not in self.data:
            self.data[name] = []

        if not hasattr(obj, 'id'):
            raise ValueError('No id field')

        for fk in self.foreign_keys:
            if fk.name_fk_entity == name:
                if not fk.has_fk_value(obj):
                    raise ValueError('No FK field')
                id = fk.get_fk_value(obj)
                connected_entity = self.get(fk.name_entity, id)
                if connected_entity is None:
                    raise ValueError('FK validation failed. The entity %s with id %i does not exist.' %(fk.name_entity, id))


    def add(self, name, obj):
        self.__validate_object(name, obj)
        self.data[name].append(obj)

    def get_all(self, name):
        if name not in self.data:
            return []

        return self.data[name][:]


    def __find_by_id(self, name, id):
        if name not in self.data:
            return None, None

        for idx, item in enumerate(self.data[name]):
            if item.id == id:
                return idx, item

    def get(self, name, id):
        try:
            idx, item = self.__find_by_id(name, id)
        except TypeError:
                    return;
        return item

    def remove(self, name, id):
        try:
            idx, item = self.__find_by_id(name, id)
        except TypeError:
            return;

        self.data[name].pop(idx)

        for (fk, fk_entity) in  [(fk, fk_entity) 
            for fk in self.foreign_keys if fk.name_entity == name
            for fk_entity in self.data[fk.name_fk_entity] if fk.get_fk_value(fk_entity) == id]:
            self.remove(fk.name_fk_entity, fk_entity.id)

    def make_foreign_key(self, name_fk_entity, name_fk, name_entity):
        if name_fk_entity not in self.data:
            self.data[name_fk_entity] = []

        if name_entity not in self.data:
            self.data[name_entity] = []

        self.foreign_keys.append(ForeignKey(name_fk_entity, name_fk, name_entity))
        try:
            for entity in self.data[name_fk_entity]:
                self.__validate_object(name_fk_entity, entity)
        except ValueError:
            self.foreign_keys.pop()
            raise ValueError('Cannot add FK on the field. Not all objects can be validated')

