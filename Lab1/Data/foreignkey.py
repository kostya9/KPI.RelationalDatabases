class ForeignKey():
    def __init__(self, name_fk_entity, name_fk, name_entity):
        self.name_fk_entity = name_fk_entity
        self.name_fk = name_fk
        self.name_entity = name_entity

    def get_fk_value(self, obj):
        return getattr(obj, self.name_fk)

    def has_fk_value(self, obj):
        return hasattr(obj, self.name_fk)