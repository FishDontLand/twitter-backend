from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from tweets.models import Tweet
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetCreateSerializer

# avoid use subclass of viewsets.ModelViewSet, because this allow edition to the dataset
# but in many cases, we don't want an API to have the full access
class TweetViewSet(viewsets.GenericViewSet):
    serializer_class = TweetCreateSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)
        # request.quer_params['user_id'] returns a string
        # The user_id parameter of filter function can be either int or string
        # no need to convert the user_id to int type
        # also, django automatically creates index for foreign key
        tweets = Tweet.objects.filter(
            user_id=request.query_params['user_id']
        ).order_by('-created_at')
        # many = true will return a list of dict
        serializer = TweetSerializer(tweets, many=True)
        # by convention, wrap the list with a key-value structure
        return Response({'tweets': serializer.data})

    def create(self, request):
        serializer = TweetCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'please check input',
                'errors': serializer.errors,
            }, status=400)
        # save method will call create method in TweetCreateSerializer
        tweet = serializer.save()
        return Response(TweetSerializer(tweet).data, status=201)

