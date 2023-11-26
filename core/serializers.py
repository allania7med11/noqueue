from rest_framework import serializers
from .models import Queue, QueueCitation
from django.utils.text import slugify

class QueueSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True) 
    class Meta:
        model = Queue
        fields = ["title", "slug"]
    
    def create(self, validated_data):
        title = validated_data["title"]
        slug = slugify(title)
        validated_data["slug"] = slug
        validated_data["created_by"] = self.context["request"].user
        queue = Queue.objects.create(**validated_data)
        return queue


class QueueCitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueCitation
        fields = ["queue", "number", "state"]
    
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
