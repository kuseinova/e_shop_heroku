from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)

    class Meta:
        model = User
        fields = (
            'password', 'password_confirmation', 'name',
            'username', 'email', 'name'
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Polzovatel sushestvuet')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Polzovatel sushestvuet s email')
        return value


    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirmation')
        if password != password_confirm:
            raise serializers.ValidationError('password do not match')
        return attrs

    def save(self, **kwargs):
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        name = self.validated_data.get('name')
        user = User.objects.create_user(
            username, email, password, name=name
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    'Невозможно войти.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError('Необходимо ввести "username" и "password".')
        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'name')

