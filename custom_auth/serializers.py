from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'password', 'mobile_number', 'first_name', 'last_name','email'
        )
        extra_kwargs ={
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            mobile_number=validated_data['mobile_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_mobile_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Mobile number is not valid, it must be 10 digits.")
        return value
    

class UpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'mobile_number', 'password', 'email'
        )
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                attrs['user']=user
            else:
                raise serializers.ValidationError({"message":"Invalid Credentials"})
        else:
            raise serializers.ValidationError({"message":"username and password must be present"})
        return attrs