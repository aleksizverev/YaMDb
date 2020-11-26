from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import ValidationError

from .models import Comment, Review, User, Category, Title, Genre


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'review_id', 'text', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer with custom validation, to ensure, that a User can
    have only one review per title"""
    author = serializers.StringRelatedField(source='author.username')
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'title', 'author', 'text', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data

        title = get_object_or_404(Title, pk=self.context['view'].kwargs[
            'title_id'])
        review_qs = title.review.filter(author=self.context['request'].user)
        if review_qs.exists():
            raise ValidationError('You have already left the review')

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        extra_kwargs = {'username': {'required': True},
                        'email': {'required': True, 'validators': [
                            UniqueValidator(queryset=User.objects.all())]}}


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
        extra_kwargs = {'email': {'required': True}}


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'confirmation_code')
        extra_kwargs = {'email': {'required': True},
                        'confirmation_code': {'required': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadOperationsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.FloatField(
        source='review__score__avg', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteOperationsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), required=True,
        many=True)

    class Meta:
        fields = '__all__'
        model = Title
