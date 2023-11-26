from rest_framework import serializers
from .models import Queue, QueueCitation
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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
    number = serializers.IntegerField(read_only=True)
    state = serializers.CharField(read_only=True)
    queue = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'  # Assuming the slug field in your Queue model is named 'slug'
    )
    queue_write_only = serializers.CharField(
        write_only=True
    )
    state = serializers.CharField(read_only=True)

    class Meta:
        model = QueueCitation
        fields = ["queue", "number", "state", "queue_write_only"]
        
    def validate_queue_write_only(self, value):
        """
        Validate that the queue with the specified slug exists.
        """
        try:
            queue = Queue.objects.get(slug=value)
        except Queue.DoesNotExist:
            raise serializers.ValidationError("Queue with this slug does not exist.")
        
        return queue

    def create(self, validated_data):
        user = self.context["request"].user
        queue = validated_data.pop("queue_write_only", None)
        validated_data["queue"] = queue
        existing_citation = QueueCitation.objects.filter(
            created_by=user, queue=queue, state__in=["NS", "SomeOtherState"]
        ).first()
        if existing_citation:
            raise ValidationError("A QueueCitation with the same user, queue, and state not served already exists.")

        last_citation = QueueCitation.objects.filter(queue=queue).order_by('-id').first()
        if last_citation:
            validated_data["number"] = last_citation.number + 1
        else:
            validated_data["number"] = 1
        validated_data["created_by"] = user
        queue_citation = QueueCitation.objects.create(**validated_data)
        return queue_citation