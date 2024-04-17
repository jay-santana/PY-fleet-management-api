from rest_framework import serializers

from .models import Taxis, Trajectories

class TaxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxis
        fields = ['id', 'plate']  # Inclue informações específicas que desejo retornar de taxis
class TrajectoriesSerializer(serializers.ModelSerializer):
    taxi = TaxisSerializer()  # Usa o serializer do taxis para serializar o objeto de taxi
    class Meta:
        model = Trajectories
        fields = '__all__' # Inclue todas as informações que desejo retornar de trajectories
