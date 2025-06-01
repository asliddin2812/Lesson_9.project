from rest_framework import serializers

from .models import Construction

class ConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Construction
        fields = '__all__'
