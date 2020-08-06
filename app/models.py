from django.db import models


class Activity(models.Model):
    start_time = models.DateTimeField('Time started')
    start_position_lat = models.FloatField()
    start_position_long = models.FloatField()
    elapsed_time = models.FloatField('Elapsed Time')
    timer_time = models.FloatField('Timed Time')
    distance = models.FloatField('Distance Traveled')
    strides = models.IntegerField()
    speed = models.FloatField()
    max_speed = models.FloatField()
    calories = models.FloatField()
    ascent = models.FloatField()
    descent = models.FloatField()
    lap_count = models.IntegerField()
    heart_rate = models.IntegerField()
    max_heart_rate = models.IntegerField()
    cadence = models.IntegerField()
    max_cadence = models.IntegerField()
    power = models.IntegerField()
    max_power = models.IntegerField()
    aerobic_training_effect = models.FloatField()
    anaerobic_training_effect = models.FloatField()

    def __str__(self):
        return f"Distance: {self.distance}\nSpeed: {self.speed}\nTime: {self.timer_time}"


class Lap(models.Model):
    activity = models.ForeignKey(Activity, models.CASCADE)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_position_lat = models.FloatField()
    start_position_long = models.FloatField()
    end_position_lat = models.FloatField()
    end_position_long = models.FloatField()
    elapsed_time = models.FloatField()
    timer_time = models.FloatField()
    distance = models.FloatField()
    strides = models.IntegerField()
    speed = models.FloatField()
    max_speed = models.FloatField()
    calories = models.IntegerField()
    ascent = models.FloatField()
    descent = models.FloatField()
    heart_rate = models.IntegerField()
    max_heart_rate = models.IntegerField()
    cadence = models.IntegerField()
    max_cadence = models.IntegerField()
    lap_trigger = models.CharField(max_length=50)
    power = models.IntegerField()
    air_power = models.IntegerField()
    form_power = models.IntegerField()
    ground_contact = models.IntegerField()

    record_start = models.IntegerField()
    record_end = models.IntegerField()

    def __str__(self):
        return f"Distance: {self.distance}\nSpeed: {self.speed}\nTime: {self.timer_time}"


class Record(models.Model):
    activity = models.ForeignKey(Activity, models.CASCADE, null=True)
    lap = models.ForeignKey(Lap, models.CASCADE, null=True)

    timestamp = models.DateTimeField()
    position_lat = models.FloatField()
    position_long = models.FloatField()
    distance = models.FloatField()
    speed = models.FloatField()
    altitude = models.FloatField()
    heart_rate = models.IntegerField()
    cadence = models.IntegerField()
    power = models.IntegerField()
    ground_time = models.IntegerField()
    air_power = models.IntegerField()
    form_power = models.IntegerField()

    def __str__(self):
        return f"Distance: {self.distance}\nSpeed: {self.speed}\nTime: {self.timestamp}"
