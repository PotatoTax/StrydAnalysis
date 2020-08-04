from django.db import models

class Activity(models.Model):
    start_time = models.DateTimeField('Time started')
    start_position = models.
    bounding_box = models.
    elapsed_time = models.
    timer_time = models.
    distance = models.
    strides = models.
    speed = models.
    max_speed = models.
    calories = models.
    ascent = models.
    descent = models.
    lap_count = models.
    sport = models.
    heart_rate = models.
    max_heart_rate = models.
    cadence = models.
    max_cadence = models.
    aerobic_training_effect = models.
    anaerobic_training_effect = models.
