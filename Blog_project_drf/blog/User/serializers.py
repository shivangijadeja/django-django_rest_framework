from rest_framework import serializers
from .models import UserSignup,UserLogin

class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserSignup
        fields='__all__'

    def validate(self,data):
        if any(map(str.isdigit, data['username'])):
            raise serializers.ValidationError({'error':"You can not add number in name"})
        if len(data['contact'])!=10:
            raise serializers.ValidationError({'error':"Please add valid contact number"})

        return data


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserLogin
        fields='__all__'