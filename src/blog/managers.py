from django.db.models import Manager
from django.contrib.contenttypes.models import ContentType
from django.db import models
# create manager 

class BlogManager(Manager):
    def publish(self):
        return self.filter(status='p')


class CommentManager(models.Manager):
	
    def filter_by_instance(self , instance):
        comment = ContentType.objects.get_for_model(instance)
        object_id = instance.id
        query = self.filter(content_type=comment, object_id=object_id)
        return query     
