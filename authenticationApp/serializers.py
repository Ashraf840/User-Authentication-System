from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'gender', 'phone', 'password']
        # NB: # only these fields will be responsible to insert data in the db-table,
        #   regardless, of how many extra key-value pairs I defined in the JSON format.

        # hide password while returning instance after user-creation
        extra_kwargs = {
            'password': {'write_only': True,},
        }


    def create(self, validated_data):
        """
        This method sits between the view & the user-model-creation
        """
        # if found 'password', will extract the key-value pair, otherwise returns 'None'
        password = validated_data.pop('password', None)     # 'None' param ref: https://stackoverflow.com/a/11277439
        instance = self.Meta.model(**validated_data)    # create the record without the password
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance     # conceal password while returning instance-data after user-creation
