from rest_framework.routers import DefaultRouter
from .views import (BookListViewSet, MemberListViewSet, LoanListViewSet, 
                    ReservationListViewSet, LibrarianListViewSet, FineListViewSet,
                    MemberLogin, LibrarianLogin)
from django.urls import path, include

router = DefaultRouter()
router.register(r'books', BookListViewSet, basename = 'book')
router.register(r'members', MemberListViewSet, basename = 'member')
router.register(r'loans', LoanListViewSet, basename = 'loan')
router.register(r'reservations', ReservationListViewSet, basename = 'reservation')
router.register(r'librarians', LibrarianListViewSet, basename = 'librarian')
router.register(r'fines', FineListViewSet, basename = 'fine')

# router.register(r'member-login', MemberLoginViewSet, basename='member-login')
# router.register(r'librarian-login', LibrarianLoginViewSet, basename='librarian-login')

# urlpatterns = [
#     path('member-login/', MemberLoginViewSet.as_view({'post': 'create'}), name='member-login'),
#     path('librarian-login/', LibrarianLoginViewSet.as_view({'post': 'create'}), name='librarian-login'),
# ] + router.urls
# # urlpatterns = router.urls

urlpatterns = [
    path('member-login/', MemberLogin, name='member-login'),
    path('librarian-login/', LibrarianLogin, name='librarian-login'),
] + router.urls