from rest_framework.serializers import ModelSerializer

from .models import User, Pay


class PaySerializer(ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"


class UserSerializers(ModelSerializer):
    payment = PaySerializer(many=True, source='user')

    class Meta:
        model = User
        fields = "__all__"
        extra_fields = ['payment']

        def get_field_names(self, declared_fields, info):
            expanded_fields = super().get_field_names(declared_fields, info)
            return expanded_fields + self.Meta.extra_fields


class PaySerializer(ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"
