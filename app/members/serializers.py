from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions

User = get_user_model()

__all__ = (
    'UserSerializer',
    'UserCreateSerializer',
    'LoginSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    generation = serializers.ChoiceField(choices=User.CHOICES_GENERATION, source='get_generation_display')
    gender = serializers.ChoiceField(choices=User.CHOICES_GENDER, source='get_gender_display')

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'generation',
            'gender',
        )


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(
        style={
            'input_type': 'password',
        },
        write_only=True,
        min_length=6,
        required=True,
    )
    password2 = serializers.CharField(
        style={
            'input_type': 'password',
        },
        write_only=True,
        min_length=6,
        required=True,
    )
    generation = serializers.ChoiceField(choices=User.CHOICES_GENERATION, required=False)
    gender = serializers.ChoiceField(choices=User.CHOICES_GENDER, required=False)

    class Meta:
        model = User

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            data = {
                'detail': '이미 존재하는 email 입니다'
            }
            raise exceptions.ValidationError(data)
        return email

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            data = {
                'detail': '비밀번호와 비밀번호 확인란이 같지 않습니다'
            }
            raise exceptions.ValidationError(data)
        else:
            return attrs

    def save(self, **kwargs):
        email = self.validated_data.get('email', '')
        password = self.validated_data.get('password1', '')
        generation = self.validated_data.get('generation', '')
        gender = self.validated_data.get('gender', '')
        user = User.objects.create_user(
            email=email,
            password=password,
            generation=generation,
            gender=gender,
        )
        return user


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        if access_token:
            user = authenticate(access_token=access_token)
            if not user:
                data = {
                    'detail': '액세스 토큰이 올바르지 않습니다'
                }
                raise serializers.ValidationError(data)
        else:
            data = {
                'detail': '액세스 토큰이 필요합니다'
            }
            raise serializers.ValidationError(data)

        attrs['user'] = user
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={
            'input_type': 'password',
        }
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                if User.objects.filter(email=email):
                    data = {
                        'detail': '올바르지 않은 password 입니다'
                    }
                else:
                    data = {
                        'detail': '가입된 email이 없습니다'
                    }
                raise exceptions.ValidationError(data)
        else:
            data = {
                'detail': 'email과 password를 입력해주세요'
            }
            raise exceptions.ValidationError(data)

        attrs['user'] = user
        return attrs
