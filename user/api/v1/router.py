# user/api/v1/router.py

from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, BookViewSet, TradeViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'trades', TradeViewSet)


urlpatterns = router.urls