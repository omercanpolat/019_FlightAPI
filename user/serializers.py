from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[
            validate_password
        ],
        style={
            'input_type':'password',
        }
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={
            'input_type':'password',
        }
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            data = {
                "password": "Password fields does not match!"
            }
            raise serializers.ValidationError(data)
        return attrs



# --------- UserSerializer ------------


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        required = False,
        write_only = True,
    )

    class Meta:
        model = User
        exclude = [
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
        ]

    def validate(self, attrs):
        if attrs.get('password', False):
            from django.contrib.auth.password_validation import validate_password
            from django.contrib.auth.hashers import make_password
            password = attrs['password']
            validate_password(password)
            attrs.update({'password': make_password(password)})
        return super().validate(attrs)
    

# --------- UserTokenSerializer ------------


class UserTokenSerializer(TokenSerializer):

    user = UserSerializer(read_only=True)
    
    class Meta(TokenSerializer.Meta):
        fields = ('key','user')