from django.core.management.base import BaseCommand
from django.utils import timezone
from sensor_configs import models
from datetime import datetime
from accounts.models import User, Profile
from projects.models import UserSensor
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Setup the Database with all relevant settings'

    def add_arguments(self, parser):
        parser.add_argument("-s", '--superuser', action="store_true", help='Superuser')

    def handle(self, *args, **kwargs):
        # Watertypes
        models.Watertype.objects.get_or_create(ews_id=4, name="Standard Type")

        # Sensors
        sensor1, _ = models.Sensor.objects.get_or_create(sensor_name="Sentinel 2", ews_id=266, config_name="sentinel2.json",
                                                         start_date=datetime(2015, 6, 23).date())
        sensors = [sensor1]

        # Create Demo User
        if kwargs["superuser"]:
            user = User.objects.filter(is_superuser=True).first()
        else:
            try:
                user = User.objects.create_user(email='demo@eomap.de', password='Eo4Test!', last_name="DEMO")
                print("User created demo@eomap.de, PW: Eo4Test!")
            except IntegrityError:
                user = User.objects.get(email='demo@eomap.de')

        profile = Profile.objects.get(user=user)
        profile.project_name = "Test"
        profile.region_code = "ttt"
        profile.ews_user_id = 20040
        profile.save()

        # Add Sensor to user without any restrictions
        user_sensor, _ = UserSensor.objects.get_or_create(user=user)
        user_sensor.sensors.add(*sensors)
