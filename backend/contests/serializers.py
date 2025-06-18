from rest_framework import serializers
from .models import Contest, Participation


class ParticipationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Participation
        fields = ['username', 'joined_at']
        read_only_fields = ['joined_at']


class ContestListSerializer(serializers.ModelSerializer):
    participations = ParticipationSerializer(many=True, read_only=True)
    participation_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Contest
        fields = ['id', 'title', 'description', 'start_time', 'price', 'image', 'participations', 'participation_count']
    
    def get_participation_count(self, obj):
        return obj.participations.count()