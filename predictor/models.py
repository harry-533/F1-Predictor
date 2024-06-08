from django.db import models

# Create your models here.
class Driver(models.Model):
    driverId = models.CharField(max_length=64)
    driverName = models.CharField(max_length=64)
    driverCode = models.CharField(max_length=8)
    driverNumber = models.CharField(max_length=8)
    driverDOB = models.CharField(max_length=64)
    driverNationality = models.CharField(max_length=64)
    constructorId = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.driverName}"

class Constructor(models.Model):
    constructorId = models.CharField(max_length=64)
    constructorName = models.CharField(max_length=64)
    constructorId2 = models.CharField(max_length=64, blank=True)
    constructorId3 = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.constructorName}"

class Track(models.Model):
    trackId = models.CharField(max_length=64)
    trackName = models.CharField(max_length=64)
    trackCity = models.CharField(max_length=64)
    trackCountry = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.trackName}"

class TrackResult(models.Model):
    trackId = models.CharField(max_length=64)
    driverId = models.CharField(max_length=64, blank=True)
    constructorId = models.CharField(max_length=64, blank=True)
    avgResult = models.JSONField(default=list)
    avgQuali = models.JSONField(default=list)

    def __str__(self):
        if self.driverId:
            return f"{self.driverId} - {self.trackId}"
        else:
            return f"{self.constructorId} - {self.trackId}"

class SeasonResult(models.Model):
    driverId = models.CharField(max_length=64, blank=True)
    constructorId = models.CharField(max_length=64, blank=True)
    avgResult = models.JSONField(default=list)
    avgQuali = models.JSONField(default=list)

    def __str__(self):
        if self.driverId:
            return f"{self.driverId} - 5 season average"
        else:
            return f"{self.constructorId} - 5 season average"

class CurrentSeason(models.Model):
    driverId = models.CharField(max_length=64, blank=True)
    constructorId = models.CharField(max_length=64, blank=True)
    avgResult = models.FloatField(blank=True)
    avgQuali = models.FloatField(blank=True)
    roundNumber = models.IntegerField()

    def __str__(self):
        if self.driverId:
            return f"{self.driverId} - current season"
        else:
            return f"{self.constructorId} - current season" 
        
class CurrentStanding(models.Model):
    driverId = models.CharField(max_length=64, blank=True)
    constructorId = models.CharField(max_length=64, blank=True)
    position = models.IntegerField()
    points = models.FloatField()

    def __str__(self):
        if self.driverId:
            return f"{self.driverId} - {self.position}({self.points})"
        else:
            return f"{self.constructorId} - {self.position}({self.points})" 

class DriverProfile(models.Model):
    driverId = models.CharField(max_length=64)
    driverImage = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.driverId} - profile"

class TrackProfile(models.Model):
    trackId = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    trackImage = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.trackId} - profile"