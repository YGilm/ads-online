from rest_framework import serializers
from .models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для объявлений, предоставляющий подробную информацию о продавце."""
    author_email = serializers.SerializerMethodField()
    author_phone = serializers.SerializerMethodField()
    author_image = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'price', 'description', 'created_at', 'image',
            'author_email', 'author_phone', 'author_image'
        ]

    def get_author_email(self, obj):
        """Возвращает email автора, если таковой имеется."""
        return obj.author.email if obj.author else None

    def get_author_phone(self, obj):
        """Возвращает телефонный номер автора, если таковой имеется."""
        return getattr(obj.author, 'phone', None) if obj.author else None

    def get_author_image(self, obj):
        """Возвращает URL изображения автора, если изображение доступно."""
        if obj.author and hasattr(obj.author, 'image') and obj.author.image:
            return obj.author.image.url
        return None


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов, автоматически назначает пользователя в качестве автора при создании."""
    author_image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'ad', 'created_at', 'author_image']
        read_only_fields = ['author']

    def get_author_image(self, obj):
        """Возвращает URL изображения автора отзыва, если таковое имеется."""
        if obj.author and hasattr(obj.author, 'image') and obj.author.image:
            return obj.author.image.url
        return None

    def create(self, validated_data):
        """Создает отзыв, автоматически назначая автора из текущего пользователя."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Обновляет отзыв, сохраняя при этом данные автора неизменными."""
        return super().update(instance, validated_data)
