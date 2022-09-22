from rest_framework import serializers
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=True,
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'role', 'phone_number', 'profile_img',
                  'password', 'confirm_password']

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            message = 'Email Already Exist'
            raise serializers.ValidationError(_(message))
        if attrs['password'] != attrs['confirm_password']:
            message = 'Password Not Matched'
            raise serializers.ValidationError(_(message))
        return attrs

    def create(self, validated_data):
        obj = User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            profile_img=validated_data.get('profile_img'),
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            home_address=validated_data.get('home_address'),
            office_address=validated_data.get('office_address'),
            company_name=validated_data.get('company_name'),
            experience=validated_data.get('experience'),
            worker_count=validated_data.get('worker_count'),
            completed_projects=validated_data.get('completed_projects'),
            service_available_in=validated_data.get('service_available_in'),
            license_number=validated_data.get('license_number'),
            about_us=validated_data.get('about_us'),
            company_logo=validated_data.get('company_logo'),
            role=validated_data.get('role'),
            gender=validated_data.get('gender'),
        )
        obj.set_password(validated_data['password'])
        obj.save()
        return obj


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender',
                  'role', 'phone_number', 'profile_img']


class UpdateDeleteProSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=False,
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = ['id', 'confirm_password', 'password', 'company_name', 'experience', 'worker_count', 'completed_projects',
                  'service_available_in', 'license_number', 'about_us', 'company_logo', 'first_name',
                  'last_name', 'phone_number', 'profile_img', 'home_address', 'office_address', 'email', 'username']

    def validate(self, attrs):
        if attrs.get('password', None) != attrs.get('confirm_password', None):
            message = 'Password Do not Match'
            raise serializers.ValidationError(_(message))
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = instance.role
        return data


class UpdateDeleteClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=False,
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = ['id', 'confirm_password', 'password', 'first_name',
                  'last_name', 'phone_number', 'profile_img', 'home_address', 'email', 'username']

    def validate(self, attrs):
        if attrs.get('password', None) != attrs.get('confirm_password', None):
            message = 'Password Do not Match'
            raise serializers.ValidationError(_(message))
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = instance.role
        return data


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['password', 'email', 'username']
