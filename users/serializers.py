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
        fields = ['id', 'email', 'first_name', 'city', 'avatar']
        read_only_fields = fields


class UserListSerializer(ModelSerializer):
    payment = PaySerializer(many=True, source='user')

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'avatar', 'payment']
