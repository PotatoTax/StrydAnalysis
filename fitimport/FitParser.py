import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile
from fitparse import FitFile

from app.models import Activity, Lap, Record


def parse_fit(file: InMemoryUploadedFile):
    decoded = FitFile(file.read())

    records = [r for r in decoded.get_messages()]

    activity = load_activity(records)
    activity.save()

    laps = load_laps(records)
    for lap in laps:
        lap.activity = activity
        lap.save()

    records = load_records(records)
    for j in range(len(laps)):
        for i in range(laps[j].record_start, laps[j].record_end + 1):
            records[i].activity = activity
            records[i].lap = laps[j]
            records[i].save()


def load_activity(records):
    activity_data = None

    for r in records:
        if r.name == 'session':
            activity_data = r
            break

    activity = Activity()

    activity.start_time = activity_data.get_value('start_time')
    activity.elapsed_time = activity_data.get_value('total_elapsed_time')
    activity.start_position_lat = activity_data.get_value('start_position_lat') * 180 / (2**31)
    activity.start_position_long = activity_data.get_value('start_position_long') * 180 / (2**31)
    activity.timer_time = activity_data.get_value('total_timer_time')
    activity.distance = activity_data.get_value('total_distance')
    activity.strides = activity_data.get_value('total_strides')
    activity.speed = activity_data.get_value('enhanced_avg_speed')
    activity.max_speed = activity_data.get_value('enhanced_max_speed')
    activity.calories = activity_data.get_value('total_calories')
    activity.ascent = activity_data.get_value('total_ascent')
    activity.descent = activity_data.get_value('total_descent')
    activity.lap_count = activity_data.get_value('num_laps')
    activity.heart_rate = activity_data.get_value('avg_heart_rate')
    activity.max_heart_rate = activity_data.get_value('max_heart_rate')
    activity.cadence = activity_data.get_value('avg_running_cadence')
    activity.max_cadence = activity_data.get_value('max_running_cadence')
    activity.aerobic_training_effect = activity_data.get_value('total_training_effect')
    activity.anaerobic_training_effect = activity_data.get_value('total_anaerobic_training_effect')

    return activity


def load_laps(records):
    laps = []

    for lap in [r for r in records if r.name == 'lap']:
        current_lap = Lap()

        current_lap.start_time = lap.get_value('start_time')
        current_lap.end_time = lap.get_value('timestamp')
        current_lap.start_position_lat = lap.get_value('start_position_lat')
        current_lap.start_position_long = lap.get_value('start_position_long')
        current_lap.end_position_lat = lap.get_value('end_position_lat')
        current_lap.end_position_long = lap.get_value('end_position_long')
        current_lap.elapsed_time = lap.get_value('total_elapsed_time')
        current_lap.timer_time = lap.get_value('total_timer_time')
        current_lap.distance = lap.get_value('total_distance')
        current_lap.strides = lap.get_value('total_strides')
        current_lap.speed = lap.get_value('enhanced_avg_speed')
        current_lap.max_speed = lap.get_value('enhanced_max_speed')
        current_lap.calories = lap.get_value('total_calories')
        current_lap.ascent = lap.get_value('total_ascent')
        current_lap.descent = lap.get_value('total_descent')
        current_lap.heart_rate = lap.get_value('avg_heart_rate')
        current_lap.max_heart_rate = lap.get_value('max_heart_rate')
        current_lap.cadence = lap.get_value('avg_running_cadence')
        current_lap.max_cadence = lap.get_value('max_running_cadence')
        current_lap.lap_trigger = lap.get_value('lap_trigger')
        current_lap.power = lap.get_value('Lap Power')

        laps.append(current_lap)

    recs = [r for r in records if r.name == 'record']
    for lap in laps:
        ground_time = 0
        air_power = 0
        form_power = 0

        j = 0
        while j < len(recs) and recs[j].get_value('timestamp') < lap.start_time:
            j += 1
        lap.record_start = j
        while j < len(recs) and recs[j].get_value('timestamp') <= lap.end_time:
            ground_time += recs[j].get_value('Ground Time')
            air_power += recs[j].get_value('Air Power')
            form_power += recs[j].get_value('Form Power')
            j += 1
        if j == lap.record_start:
            break
        lap.record_end = j - 1
        lap.ground_contact = ground_time / lap.timer_time
        lap.air_power = air_power / lap.timer_time
        lap.form_power = form_power / lap.timer_time

    return laps


def load_records(records):
    recs = []
    for r in records:
        if r.name != 'record':
            continue

        record = Record()
        # TODO: get timezone from FIT file
        time_zone = datetime.timezone(datetime.timedelta(hours=-5))
        ts = r.get_value('timestamp')
        record.timestamp = datetime.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, ts.microsecond, time_zone)
        record.position_lat = r.get_value('position_lat') * 180 / (2**31)
        record.position_long = r.get_value('position_long') * 180 / (2 ** 31)
        record.distance = r.get_value('distance')
        record.speed = r.get_value('enhanced_speed')
        record.altitude = r.get_value('enhanced_altitude')
        record.heart_rate = r.get_value('heart_rate')
        record.cadence = r.get_value('cadence')
        record.power = r.get_value('Power')
        record.ground_time = r.get_value('Ground Time')
        record.air_power = r.get_value('Air Power')
        record.form_power = r.get_value('Form Power')

        recs.append(record)

    return recs
