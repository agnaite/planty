# -*- coding: utf-8 -*-
from model import connect_to_db, User, Plant, PlantUser
from twilio.rest import TwilioRestClient
import secret
import datetime
import pytz

account_sid = secret.TWILIO_SID
auth_token = secret.TWILIO_AUTH
_client = TwilioRestClient(account_sid, auth_token)


def send_sms(day, name, num):

    message = _client.messages.create(
        to='+1'+num,
        from_="+16506678554",
        body="🌱 It's time to water your {}! - Planty".format(name)
    )
    print(message.sid)


def schedule_reminders(plant_user):

    user_num = User.query.get(plant_user.user_id).phone
    plant_name = Plant.query.get(plant_user.plant_id).name

    utcmoment_unaware = datetime.datetime.utcnow()
    utcmoment = utcmoment_unaware.replace(tzinfo=pytz.utc)
    today = utcmoment.astimezone(pytz.timezone('America/Los_Angeles')).strftime('%A')

    for day in plant_user.get_watering_days():
        if today == day:
            send_sms(day, plant_name, user_num)


def main():
    for plantuser in PlantUser.query.all():
        if plantuser.get_watering_days():
            schedule_reminders(plantuser)


if __name__ == '__main__':

    from server import app
    connect_to_db(app)

    main()
