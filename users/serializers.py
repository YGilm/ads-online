from djoser.serializers import UserCreateSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = tuple(UserCreateSerializer.Meta.fields) + ('role',)

    def validate_role(self, value):
        if not value:
            return 'user'
        return value
