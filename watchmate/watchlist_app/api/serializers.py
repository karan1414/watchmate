from rest_framework import serializers

from watchlist_app.models import Movie


class MovieSerializer(serializers.Serializer):
    """ Serializer for Movie objects"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        """Create a Movie"""
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a Movie"""
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)

        instance.save()

        return instance
