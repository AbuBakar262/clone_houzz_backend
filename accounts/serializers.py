import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from accounts.models import User, Projects, Company, GENDER_CHOICES, ROLE_CHOICES, OtpVerification
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.utils import timezone
from accounts.view.utils import generate_six_length_random_number, email_sender, phone_sender


def image_validator(file):
    max_file_size = 1024 * 1024 * 5   # 5MB
    if file.size > max_file_size:
        raise serializers.ValidationError(_('Max File size is 5MB'))


class SignupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True)
    profile_pic = serializers.FileField(validators=[image_validator], required=False, allow_null=True)
    terms_conditions = serializers.BooleanField(required=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=True)
    password = serializers.CharField(max_length=128, label='Password', style={'input_type': 'password'},
                                     write_only=True)
    confirm_password = serializers.CharField(max_length=128, label='Password', style={'input_type': 'password'},
                                     write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'role', 'phone_number', 'profile_pic',
                  'password', 'confirm_password', 'create_profile', 'date_joined', 'terms_conditions', 'home_address',
                  'approved', 'email_verified', 'phone_verified']

    @staticmethod
    def validate_password(data):
        validators.validate_password(password=data, user=User)

        return data

    def validate(self, attrs):
        if attrs['terms_conditions'] is False:
            message = 'Must agree to Terms & Conditions'
            raise serializers.ValidationError(_(message))
        if User.objects.filter(email=attrs['email'].lower()).exists():
            message = 'User With This Email Already Exists'
            raise serializers.ValidationError(_(message))
        if User.objects.filter(username=attrs['username'].lower()).exists():
            message = 'Username Already Exists'
            raise serializers.ValidationError(_(message))
        if len(attrs['email']) > 30:
            message = "Email should be less than 30 characters"
            raise serializers.ValidationError(_(message))
        if len(attrs['username']) > 15:
            message = 'Username must be less than 15 characters'
            raise serializers.ValidationError(_(message))
        if attrs['password'] != attrs['confirm_password']:
            message = 'Password Not Matched'
            raise serializers.ValidationError(_(message))
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username').lower(),
            email=validated_data.get('email').lower(),
            terms_conditions=validated_data.get('terms_conditions'),
            role=validated_data.get('role'),
            gender=validated_data.get('gender'),
            profile_pic=validated_data.get('profile_pic'),
            password=make_password(validated_data.get('password'))
        )
        user.save()
        return user


class CreateProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False)
    profile_pic = serializers.FileField(validators=[image_validator], required=False, allow_null=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    home_address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'role', 'phone_number',
                  'profile_pic', 'create_profile', 'date_joined', 'home_address', 'terms_conditions']

    def validate(self, attrs):
        if User.objects.filter(id=self.context['instance'].user.instance.id).exists():
            user = User.objects.get(id=self.context['instance'].user.instance.id)
            if user.create_profile is True:
                message = 'Profile Already Created'
                raise serializers.ValidationError(_(message))
        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({'phone': _("Phone Number Already Exists")})
        return attrs


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
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=True,
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'role', 'phone_number', 'profile_pic',
                  'password', 'create_profile', 'date_joined', 'terms_conditions', 'home_address',
                  'approved', 'email_verified', 'phone_verified']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if User.objects.filter(username=email.lower()).exists():
            user_email = User.objects.filter(username=email.lower()).first().email
            user = authenticate(email=user_email.lower(), password=password)
        else:
            user = authenticate(email=email.lower(), password=password)
        if not user:
            message = 'Invalid Credentials'
            raise serializers.ValidationError(_(message))
        if user.is_active is False:
            message = 'Account Blocked, Contact Admin'
            raise serializers.ValidationError(_(message))
        return user


class CreateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'image', 'location', 'pro_user']

    def validate(self, attrs):
        if Projects.objects.filter(title=attrs['title']).exists():
            message = 'Project Already Exist'
            raise serializers.ValidationError(_(message))
        if not User.objects.filter(email=attrs['pro_user']).exists():
            message = 'User Not Exist'
            raise serializers.ValidationError(_(message))
        return attrs

class CreateProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=100, required=True)
    image = serializers.ImageField(validators=[image_validator], required=True)
    location = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Projects
        fields = ['title', 'description', 'image', 'location', 'pro_user']

    def validate(self, attrs):
        if Projects.objects.filter(title=attrs['title']).exists():
            message = 'Project Already Exist'
            raise serializers.ValidationError(_(message))
        if not User.objects.filter(email=attrs['pro_user']).exists():
            message = 'User Not Exist'
            raise serializers.ValidationError(_(message))
        return attrs

    def create(self, validated_data):
        obj = Projects.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            image=validated_data['image'],
            location=validated_data['location'],
            pro_user_id=validated_data['pro_user'].id,
        )
        obj.save()
        return obj


class ListProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'image', 'location']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['created_by'] = Company.objects.all().values_list("pro_user__email", "pro_user__id")
        return data


class UpdateDeleteProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'image', 'location']


class CreateCompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    address = serializers.CharField(required=True)
    logo = serializers.ImageField(required=False)
    license_number = serializers.CharField(required=False)
    about_us = serializers.CharField(required=False)
    service_available_in = serializers.CharField(required=True)
    worker_count = serializers.IntegerField(required=True)
    completed_projects = serializers.IntegerField(required=True)
    experience = serializers.IntegerField(required=True)

    class Meta:
        model = Company
        fields = ['name', 'email', 'address', 'logo', 'license_number', 'about_us', 'service_available_in',
                                                                        'worker_count', 'completed_projects',
                                                                        'experience', 'pro_user']

    def validate(self, attrs):
        if Company.objects.filter(name=attrs['name']).exists():
            message = 'Company Already Exist'
            raise serializers.ValidationError(_(message))
        if not User.objects.filter(email=attrs['pro_user']).exists():
            message = 'User Not Exist'
            raise serializers.ValidationError(_(message))
        return attrs


class ListCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'address', 'logo', 'license_number', 'about_us', 'service_available_in',
                                                                              'worker_count', 'completed_projects',
                                                                              'experience']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['created_by'] = Company.objects.all().values_list("pro_user__email", "pro_user__id")
        return data


class UpdateDeleteCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'address', 'logo', 'license_number', 'about_us', 'service_available_in',
                                                                              'worker_count', 'completed_projects',
                                                                              'experience']


class EmailVerifySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = OtpVerification
        fields = ["email"]

    def validate(self, attrs):
        user = self.context['request'].user
        if User.objects.filter(id=user.id).exists():
            if user.email_verified is True:
                message = "Email Already Verified"
                raise serializers.ValidationError(_(message))
        return attrs

    def create(self, validated_data):
        time_expiry = timezone.now() + timezone.timedelta(minutes=1)
        otp = generate_six_length_random_number()

        email_info = {
            "subject": "Verify your OTP",
            "message": f"Your six digit OTP is HH-{otp}",
            "to_email": validated_data['email']
        }
        email_sender(email_info)
        verify_obj = OtpVerification.objects.create(
            otp_user=User.objects.filter(email=validated_data['email']).first(),
            otp=otp,
            expiry=time_expiry,
            email_verified=True
        )
        verify_obj.save()
        return verify_obj


class PhoneVerifySerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)

    class Meta:
        model = OtpVerification
        fields = ["phone"]

    def validate(self, attrs):
        user = self.context['request'].user
        if User.objects.filter(id=user.id).exists():
            if user.phone_verified is True:
                message = "Phone Already Verified"
                raise serializers.ValidationError(_(message))
        return attrs

    def create(self, validated_data):
        time_expiry = timezone.now() + timezone.timedelta(minutes=1)
        otp = generate_six_length_random_number()

        phone_info = {
            "message": f"Your six digit OTP is HH-{otp}",
            "to_phone": validated_data['phone']
        }
        phone_sender(phone_info)

        verify_obj = OtpVerification.objects.create(
            otp_user=User.objects.filter(phone_number=validated_data['phone']).first(),
            otp=otp,
            expiry=time_expiry,
            phone_verified=True
        )
        verify_obj.save()
        return verify_obj


class OtpSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=True)

    class Meta:
        model = OtpVerification
        fields = ['otp']

    def validate(self, attrs):
        otp = OtpVerification.objects.filter(otp=attrs['otp'])
        if otp.exists():
            if otp.first().expiry < timezone.now():
                message = 'OTP Expired'
                raise serializers.ValidationError(_(message))
        if not otp:
            message = 'OTP is Incorrect'
            raise serializers.ValidationError(_(message))
        return attrs
