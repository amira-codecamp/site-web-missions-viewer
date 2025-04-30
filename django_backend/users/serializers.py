from djoser.serializers import UserSerializer
from users.models import UsersAccounts


class UsersAccountsSerializer(UserSerializer):
    class Meta:
        model = UsersAccounts
        fields = ('login', 'is_active', 'is_admin')
