from rest_framework.serializers import ModelSerializer

from .models import User, Pay


class PaySerializer(ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserPublicSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'city', 'avatar']
        read_only_fields = fields


class UserDetailSerializer(ModelSerializer):
    payment = PaySerializer(many=True, source='user', read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'payment']
