from rest_framework import serializers

from account import models


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = models.UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'gender',
                  'biography', 'contact_number', 'address', 'is_superuser', 'is_active', 'date_joined', 'last_login']

        read_only_fields = ['is_superuser', 'is_active', 'date_joined', 'last_login']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = models.UserProfile(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

    def validate_confirm_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        confirm_password = value
        if password != confirm_password:
            raise serializers.ValidationError('Password and confirm Password not matched')
        return value


class ForgotPasswordSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):

        try:
            models.UserProfile.objects.get(email=value)
        except models.UserProfile.DoesNotExist:
            raise serializers.ValidationError('No account associated with the email address')
        return value


class ForgotPasswordConfirmSerializers(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'}, required=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'},
                                             required=True)

    def validate_confirm_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        confirm_password = value
        if password != confirm_password:
            raise serializers.ValidationError('Password and confirm Password not matched')
        return value
