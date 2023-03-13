from django.urls import path

# from watchlist_app.api.views import movie_detail, movie_list
from watchlist_app.api.views import (ReviewDetail, ReviewList,
                                     StreamingPlatformDetailAV,
                                     StreamingPlatformListAV, WatchListAV,
                                     WatchListDetailAv)

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('list/<int:pk>', WatchListDetailAv.as_view(), name='movie-detail'),
    path('stream/', StreamingPlatformListAV.as_view(), name='streaming-platform-list'),
    path('stream/<int:pk>', StreamingPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('reviews', ReviewList.as_view(), name = 'reviews-detail'),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='reviewsid-detail'),
    # path()
]