from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'snippets')
        #extra_kwargs = {'email': {'required': True}}
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserListSerializer(serializers.HyperlinkedModelSerializer):
#    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields_GET = ('url', 'username')
        fields_POST = ('url', 'username', 'email', 'password')
        fields = fields_POST
        extra_kwargs = {'email': {'allow_null': False, 'required': True}}
        write_only_fields = ('password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializerget(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class GlobalSearchSerializer(serializers.ModelSerializer):

   class Meta:
      model = Snippet
      fields = ['url', 'id']#"__all__"#('id')
