from rest_framework import serializers
from .models import Site, Collector, Contact
import re

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['domain']
    
    def create(self, validated_data):
        return Site.objects.create(**validated_data)
    
    def validate_domain(self, value):
        """
        Validate that the domain is a valid Fully Qualified Domain Name
        """
        fqdn_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(fqdn_pattern, value):
            print('NOT VALID')
            raise serializers.ValidationError('Invalid FQDN format.')
        return value

class CollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'