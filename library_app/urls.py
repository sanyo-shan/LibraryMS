from rest_framework.routers import DefaultRouter
from .views import (BookListViewSet, MemberListViewSet, LoanListViewSet, 
                    ReservationListViewSet, LibrarianListViewSet, FineListViewSet,
                    MemberLogin, LibrarianLogin,
                    librarian_register, member_login, member_register, librarian_login, home)
from django.urls import path, include

from library_app import views

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
    path('member-login/', member_login, name='member-login'),
    path('librarian-login/', librarian_login, name='librarian-login'),
    path('member-register/', member_register, name='member-register'),
    path('librarian-register/', librarian_register, name='librarian-register'),
    path('home/member/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
] + router.urls