from rest_framework import serializers

from watchlist_app.models import Reviews, StreamPlatform, WatchList


class ReviewsSerializer(serializers.ModelSerializer):

     class Meta:
        model = Reviews
        fields = "__all__"



class WatchListSerializer(serializers.ModelSerializer):
    """ Model Serializer for WatchList objects """
    reviews = ReviewsSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"  # ["field1", "field2"]
        # exclude = ["id"]# exclude = ["field3"]

class StreamPlatformSerializer(serializers.ModelSerializer):
    """ Serializer for streaming objects """
    # watchlist = WatchListSerializer(many=True, read_only =True)
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='streamplatform-detail')
    class Meta:
            model = StreamPlatform
            fields = "__all__"

# class MovieSerializer(serializers.Serializer):
#     """ Serializer for Movie objects"""
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         """Create a Movie"""
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         """Update a Movie"""
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)

#         instance.save()

#         return instance
