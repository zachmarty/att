from djoser.views import UserViewSet
from users.paginators import UserPaginator
from users.serializers import CurrentUserSerializer, User

class UsersViewSet(UserViewSet):
    serializer_class = CurrentUserSerializer
    queryset = User.objects.all()
    pagination_class = UserPaginator
