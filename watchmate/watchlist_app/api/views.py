from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from watchlist_app.api.serializers import MovieSerializer
from watchlist_app.models import Movie


@api_view(['GET', 'POST'])
def movie_list(request):
    """ List all movies"""
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({"Error": "Movie does not exist", "status": status.HTTP_404_NOT_FOUND})

    if request.method == "GET":
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        # movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE":
        # movie = Movie.objects.get(pk=pk)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)