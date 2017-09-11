import os
import _pickle as pickle
from Data.foreignkey import ForeignKey

class DataHolder():
    """
    Represents data and its' relationships
    """
    def __init__(self):
        self.data = {}
        self.foreign_keys = []

    def serialize(self, file_name: str):
        """
        Serializes the state of the data with relationships in the file
        """
        with open(file_name, 'wb') as file:
            pickle.dump({'data': self.data, 'foreign_keys': self.foreign_keys}, file)

    def deserialize(self, file_name: str):
        """
        Deserializes the state of the data with relationships from the file
        """
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                dump = pickle.load(file)
                self.data = dump['data']
                self.foreign_keys = dump['foreign_keys']
        else:
            raise ValueError('File does not exist')

    def __validate_object(self, name, obj):
        if name not in self.data:
            self.data[name] = []

        if not hasattr(obj, 'id'):
            raise ValueError('No id field')

        connected_keys = [foreign_key for foreign_key in self.foreign_keys
                          if foreign_key.name_fk_entity == name]
        for foreign_key in connected_keys:
            if not foreign_key.has_fk_value(obj):
                raise ValueError('No FK field')
            fk_id = foreign_key.get_fk_value(obj)
            connected_entity = self.get(foreign_key.name_entity, fk_id)
            if connected_entity is None:
                raise ValueError('FK validation failed. The entity %s with id %i does not exist.'
                                 % (foreign_key.name_entity, fk_id))


    def add(self, name: str, obj):
        """
        Adds an object to collection
        """
        self.__validate_object(name, obj)
        max_id = max(self.data[name], key=lambda x: x.id, default=0)
        obj.id = (0 if max_id == 0 else max_id.id) + 1
        self.data[name].append(obj)

    def get_all(self, name: str):
        """
        Returns all objects from collection
        """
        if name not in self.data:
            return []

        return self.data[name][:]

    def is_key_for_foreignkey(self, name: str):
        """
        Checks if there is an associated foreign key for this collection
        """
        for foreign_key in self.foreign_keys:
            if foreign_key.name_entity == name:
                return True

        return False

    def __find_by_id(self, name: str, entity_id: int):
        if name not in self.data:
            return None, None

        for idx, item in enumerate(self.data[name]):
            if item.id == entity_id:
                return idx, item

    def exists(self, name: str, entity_id: int):
        """
        Checks if an entity with this id in this collection exists
        """
        return self.get(name, entity_id) is not None

    def get(self, name: str, entity_id: int):
        """
        Returns entity wi th this id from this collection
        """
        try:
            _, item = self.__find_by_id(name, entity_id)
        except TypeError:
            return
        return item

    def remove(self, name: str, entity_id: int):
        """
        Removes the entity with this id from this collection
        """
        try:
            idx, _ = self.__find_by_id(name, entity_id)
        except TypeError:
            return

        self.data[name].pop(idx)

        # Cascade delete connected entities
        for (foreign_key, fk_entity) in \
                [(foreign_key, fk_entity)
                 for foreign_key in self.foreign_keys
                 if foreign_key.name_entity == name
                 for fk_entity in self.data[foreign_key.name_fk_entity]
                 if foreign_key.get_fk_value(fk_entity) == entity_id]:
            self.remove(foreign_key.name_fk_entity, fk_entity.id)

    def make_foreign_key(self, name_fk_entity: str, name_fk: str, name_entity: str):
        """
        Create a foreign key [name_fk] defined on the [name_fk_entity] referring to [name_entity]
        """
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
