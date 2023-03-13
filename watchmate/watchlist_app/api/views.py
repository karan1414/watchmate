from rest_framework import generics, mixins, status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView

from watchlist_app.api.serializers import (ReviewsSerializer,
                                           StreamPlatformSerializer,
                                           WatchListSerializer)
from watchlist_app.models import Reviews, StreamPlatform, WatchList


class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """ Details for a particular review """
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """ Reviews list """
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class WatchListAV(APIView):
    """ The list of movies"""
    def get(self,request):
        movies = WatchList.objects.all()        
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchListDetailAv(APIView):
    """ Details of one movie """

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie)
        except WatchList.DoesNotExist:
            return Response({"Error": "Movie not found!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WatchList.DoesNotExist:
            return Response({"Error": "Movie not found!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            movie.delete()
        except WatchList.DoesNotExist:
            return Response({"Error": "Movie not found!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamingPlatformListAV(APIView):

    def get(self, request):
        platforms = StreamPlatform.objects.all()

        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class StreamingPlatformDetailAV(APIView):

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform)
        except StreamPlatform.DoesNotExist:
            return Response({"Error": "Platform you are looking for not found!"}, status=status.HTTP_404_NOT_FOUND)  
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform, data=request.data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StreamPlatform.DoesNotExist:
            return Response({"Error": "Platform you are looking for not found!"}, status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"Error": "Platform you are looking for not found!"}, status=status.HTTP_404_NOT_FOUND) 
        
        platform.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     """ List all movies"""
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"Error": "Movie does not exist", "status": status.HTTP_404_NOT_FOUND})

#     if request.method == "GET":
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'PUT':
#         # movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == "DELETE":
#         # movie = Movie.objects.get(pk=pk)
#         movie.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)
