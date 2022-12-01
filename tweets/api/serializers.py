from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserSerializerForPublic

class TweetSerializer(serializers.ModelSerializer):
    # without the following declaration, user will be an int type
    # user is the foreign key. The declaration of the following line
    # allows program to extract information from the user table
    # and the UserSerializerForPublic defines what fields to be displayed
    user = UserSerializerForPublic()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')

class TweetCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet