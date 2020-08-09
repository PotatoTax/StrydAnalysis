import datetime
from multiprocessing import Pool

from django.core.files.uploadedfile import InMemoryUploadedFile
from fitparse import FitFile

from app.models import Activity, Lap, Record, PowerCurveEntry


class FITParser:
    activity = None
    records = None
    laps = None
    power = None

    def parse_fit(self, file: InMemoryUploadedFile):
        # TODO: Bulk update?
        decoded = FitFile(file.read())

        records = [r for r in decoded.get_messages()]

        self.load_activity(records)
        self.load_laps(records)

        Lap.objects.bulk_create(self.laps)

        self.load_records(records)

        for j in range(len(self.laps)):
            for i in range(self.laps[j].record_start, self.laps[j].record_end + 1):
                self.records[i].lap = self.laps[j]

        Record.objects.bulk_create(self.records)

    def find_max(self, k):
        t = sum(self.power[:k])
        m = t

        for i in range(len(self.records) - k):
            t -= self.power[i]
            t += self.power[i + k]
            if t > m:
                m = t

        return {'duration': k, 'power': m / k}

    def load_curve(self):
        activity_curve = [0 for _ in range(len(self.records) // 5 + 1)]
        self.power = [r.power for r in self.records]

        pool = Pool(processes=4)
        activity_curve = pool.map(self.find_max, [1 if a == 0 else a * 5 for a in range(len(activity_curve))])
        pool.close()
        pool.join()
        activity_curve = sorted(activity_curve, key=lambda x: x['duration'])
        print(activity_curve)
        print(self.activity.max_power)

        power_curve = PowerCurveEntry.objects.all()

        i = 0
        while i < len(power_curve) and i < len(activity_curve):
            if activity_curve[i] > power_curve[i].power:
                power_curve[i].power = activity_curve[i]
                power_curve[i].activity = self.activity
                power_curve[i].save()
            i += 1

        for i in range(len(power_curve), len(activity_curve)):
            entry = PowerCurveEntry()
            entry.activity = self.activity
            entry.power = activity_curve[i]
            entry.duration = 1 if i < 1 else i * 5
            entry.save()

    def load_activity(self, records):
        activity_data = None

        for r in records:
            if r.name == 'session':
                activity_data = r
                break

        self.activity = Activity()

        self.activity.start_time = activity_data.get_value('start_time')
        self.activity.elapsed_time = activity_data.get_value('total_elapsed_time')
        self.activity.start_position_lat = activity_data.get_value('start_position_lat') * 180 / (2 ** 31)
        self.activity.start_position_long = activity_data.get_value('start_position_long') * 180 / (2 ** 31)
        self.activity.timer_time = activity_data.get_value('total_timer_time')
        self.activity.distance = activity_data.get_value('total_distance')
        self.activity.strides = activity_data.get_value('total_strides')
        self.activity.speed = activity_data.get_value('enhanced_avg_speed')
        self.activity.max_speed = activity_data.get_value('enhanced_max_speed')
        self.activity.calories = activity_data.get_value('total_calories')
        self.activity.ascent = activity_data.get_value('total_ascent')
        self.activity.descent = activity_data.get_value('total_descent')
        self.activity.lap_count = activity_data.get_value('num_laps')
        self.activity.heart_rate = activity_data.get_value('avg_heart_rate')
        self.activity.max_heart_rate = activity_data.get_value('max_heart_rate')
        self.activity.cadence = activity_data.get_value('avg_running_cadence')
        self.activity.max_cadence = activity_data.get_value('max_running_cadence')
        self.activity.aerobic_training_effect = activity_data.get_value('total_training_effect')
        self.activity.anaerobic_training_effect = activity_data.get_value('total_anaerobic_training_effect')

        self.activity.max_power = 0
        power = 0

        recs = [r for r in records if r.name == 'record']

        for r in recs:
            if r.get_value('Power') > self.activity.max_power:
                self.activity.max_power = r.get_value('Power')
            power += r.get_value('Power')

        self.activity.power = power / len(recs)

        self.activity.save()

    def load_laps(self, records):
        self.laps = []

        for lap in [r for r in records if r.name == 'lap']:
            current_lap = Lap()

            current_lap.activity = self.activity
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

            self.laps.append(current_lap)

        recs = [r for r in records if r.name == 'record']
        for lap in self.laps:
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

    def load_records(self, records):
        time_zone = datetime.timezone(datetime.timedelta(hours=-5))

        self.records = [
            Record(
                activity=self.activity,
                timestamp=datetime.datetime(
                    1, 1, 1,
                    r.get_value('timestamp').hour,
                    r.get_value('timestamp').minute,
                    r.get_value('timestamp').second,
                    r.get_value('timestamp').microsecond,
                    time_zone
                ),
                position_lat=r.get_value('position_lat') * 180 / (2 ** 31),
                position_long=r.get_value('position_long') * 180 / (2 ** 31),
                distance=r.get_value('distance'),
                speed=r.get_value('enhanced_speed'),
                altitude=r.get_value('enhanced_altitude'),
                heart_rate=r.get_value('heart_rate'),
                cadence=r.get_value('cadence'),
                power=r.get_value('Power'),
                ground_time=r.get_value('Ground Time'),
                air_power=r.get_value('Air Power'),
                form_power=r.get_value('Form Power'),
            )
            for r in records if r.name == 'record'
        ]
        # for r in records:
        #     if r.name != 'record':
        #         continue
        #
        #     record = Record()
        #     # TODO: get timezone from FIT file
        #     time_zone = datetime.timezone(datetime.timedelta(hours=-5))
        #     ts = r.get_value('timestamp')
        #     record.timestamp = datetime.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second,
        #                                          ts.microsecond, time_zone)
        #     record.position_lat = r.get_value('position_lat') * 180 / (2 ** 31)
        #     record.position_long = r.get_value('position_long') * 180 / (2 ** 31)
        #     record.distance = r.get_value('distance')
        #     record.speed = r.get_value('enhanced_speed')
        #     record.altitude = r.get_value('enhanced_altitude')
        #     record.heart_rate = r.get_value('heart_rate')
        #     record.cadence = r.get_value('cadence')
        #     record.power = r.get_value('Power')
        #     record.ground_time = r.get_value('Ground Time')
        #     record.air_power = r.get_value('Air Power')
        #     record.form_power = r.get_value('Form Power')
        #
        #     self.records.append(record)
