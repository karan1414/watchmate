from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
# from rest_framework.decorators import api_view
from rest_framework.views import APIView

from user_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import (WatchlistCPagination,
                                          WatchlistLOPagination,
                                          WatchlistPagination)
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewOrReadOnly
from watchlist_app.api.serializers import (ReviewsSerializer,
                                           StreamPlatformSerializer,
                                           WatchListSerializer)
from watchlist_app.models import Reviews, StreamPlatform, WatchList


class UserReview(generics.ListAPIView):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        # username = self.kwargs['username']

        # return Reviews.objects.filter(review_user__username=username)
        user_name = self.request.query_params.get('username', None)
        return Reviews.objects.filter(review_user__username=user_name)


# update review ?
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewCreateThrottle]
    throttle_scope = 'review-create'
    
    def get_queryset(self):
        return Reviews.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Reviews.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this !")

        watchlist.review_count = watchlist.review_count + 1

        watchlist.average_rating = (watchlist.average_rating + serializer.validated_data['rating'])/ watchlist.review_count

        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [ReviewOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     """ Details for a particular review """
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewsSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     """ Reviews list """
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewsSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class WatchListGV(generics.ListAPIView):
    """ The list of watchlists """
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchlistCPagination

class WatchListAV(APIView):
    """ The list of movies"""
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    pagination_class = WatchlistCPagination
    
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
    permission_classes = [AdminOrReadOnly]
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

# class StreamingPlatformViewVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()

#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

class StreamingPlatformViewVS(viewsets.ModelViewSet):

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]        


class StreamingPlatformListAV(APIView):
    permission_classes = [AdminOrReadOnly]
   
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
    permission_classes = [AdminOrReadOnly]

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
