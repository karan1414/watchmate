from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_detail, movie_list
from watchlist_app.api.views import (ReviewCreate, ReviewDetail, ReviewList,
                                     StreamingPlatformDetailAV,
                                     StreamingPlatformListAV,
                                     StreamingPlatformViewVS, WatchListAV,
                                     WatchListDetailAv)

router = DefaultRouter()
router.register('stream', StreamingPlatformViewVS, basename='streamplatformview')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('list/<int:pk>', WatchListDetailAv.as_view(), name='movie-detail'),
    path('', include(router.urls)),
    # path('stream/', StreamingPlatformListAV.as_view(), name='streaming-platform-list'),
    # path('stream/<int:pk>', StreamingPlatformDetailAV.as_view(), name='streamplatform-detail'),
    
    # path('reviews', ReviewList.as_view(), name = 'reviews-detail'),
    # path('reviews/<int:pk>', ReviewDetail.as_view(), name='reviewsid-detail'),
    # path()

    path('stream/<int:pk>/reviews', ReviewList.as_view(), name='reviews-list'),
    path('stream/reviews/<int:pk>', ReviewDetail.as_view(), name='reviews-detail'),
    path('stream/reviews/<int:pk>/reviews-create', ReviewCreate.as_view(), name='reviews-create')
]