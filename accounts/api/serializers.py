from django.contrib.auth.models import User
from rest_framework import serializers, exceptions


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserSerializerForPublic(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'username')


class LoginSerializer(serializers.Serializer):
    # check if username and password exists
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'user': 'User does not exist'
            })
        return data


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # will be called when is_valid is called
    def validate(self, data):
        if User.objects.filter(username=data['email'].lower()).exists():
            raise exceptions.ValidationError({
               'email': 'This email address has been used'
            })
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'This username has been used'
            })
        return data

    def create(self, validated_data):
        # save as lower case
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return user