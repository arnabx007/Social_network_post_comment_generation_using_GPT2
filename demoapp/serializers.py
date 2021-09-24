from rest_framework import serializers

from .models import postandcomment

class dataSerializer(serializers.ModelSerializer):
   class Meta:
       model = postandcomment
       fields = ('post', 'comment')