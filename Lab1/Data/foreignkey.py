class ForeignKey():
    """
    Represents a foreign key
    """
    def __init__(self, name_fk_entity, name_fk, name_entity):
        self.name_fk_entity = name_fk_entity
        self.name_fk = name_fk
        self.name_entity = name_entity

    def get_fk_value(self, obj):
        """
        Returns the foreign key value
        """
        return getattr(obj, self.name_fk)

    def has_fk_value(self, obj):
        """
        Checks if the object has the foreign key value
        """
        return hasattr(obj, self.name_fk)