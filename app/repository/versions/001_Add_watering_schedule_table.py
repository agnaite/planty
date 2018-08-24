from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    plantusers = Table('plant_users', meta, autoload=True)
    wateringc = Column('watering_schedule', String(128))
    wateringc.create(plantusers)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    plantusers = Table('plant_user', meta, autoload=True)
    plantusers.c.watering.drop()
