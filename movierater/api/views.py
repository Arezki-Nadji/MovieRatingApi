from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .models import Rating, Movie
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:

            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                # todo: Raise Validation Error
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Updated', 'result:': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except ValidationError:
                Rating.objects.create(user=user, movie=movie, stars=stars)

                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'its working', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message : You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
