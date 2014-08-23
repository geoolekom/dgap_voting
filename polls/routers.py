from django.conf import settings
 
class DatabaseModelsRouter(object):
    """
    A router to control all database operations on models for different
    databases.
 
    In case a model is not set in settings.DATABASE_MODELS_MAPPING, the router
    will fallback to the `default` database.
 
    Settings example:
 
    DATABASE_MODELS_MAPPING = {'model1': 'db1', 'model2': 'db2'}
    """
 
    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        if settings.DATABASE_MODELS_MAPPING.has_key(model._meta.db_label):
            return settings.DATABASE_MODELS_MAPPING[model._meta.db_label]
        return None
 
    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if settings.DATABASE_MODELS_MAPPING.has_key(model._meta.db_label):
            return settings.DATABASE_MODELS_MAPPING[model._meta.db_label]
        return None
 
    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = settings.DATABASE_MODELS_MAPPING.get(obj1._meta.db_label)
        db_obj2 = settings.DATABASE_MODELS_MAPPING.get(obj2._meta.db_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None
 
    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database."""
        if db in settings.DATABASE_MODELS_MAPPING.values():
            return settings.DATABASE_MODELS_MAPPING.get(model._meta.db_label) == db
        elif settings.DATABASE_MODELS_MAPPING.has_key(model._meta.db_label):
            return False
        return None
