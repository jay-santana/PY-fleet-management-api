from django.db import models

# Create your models here.
class Taxis(models.Model):
  id = models.AutoField(primary_key=True)
  plate = models.CharField(max_length=20, unique=True)

  def str(self):
    return f"ID: {self.id}, Plate: {self.plate}"
    
class Trajectories(models.Model):
  id = models.AutoField(primary_key=True)
  date = models.DateTimeField()
  latitude = models.FloatField()
  longitude = models.FloatField()
  taxi = models.ForeignKey(Taxis, on_delete=models.CASCADE, related_name='trajectories')

  def str(self):
    return f"Trajectory ID: {self.id}, Date: {self.date}, Latitude: {self.latitude}, Longitude: {self.longitude}, Taxi: {self.taxi}"