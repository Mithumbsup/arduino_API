from Server_API_app import db


class Experiment(db.Model):
    """Simple database model to track event attendees."""

    __tablename__ = 'experiment'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String())
    end = db.Column(db.String())
    place = db.Column(db.String())
    # name = db.Column(db.String(80))
    # email = db.Column(db.String(120))

    def __init__(self, start=None, end=None, place=None):
        self.start = start
        self.end = end
        self.place = place

class SensorData(db.Model):
    __tablename__ = 'sensor'
    
    id = db.Column(db.Integer, primary_key=True)
    experimenter_id = db.Column(db.String())
    sensor_name = db.Column(db.String())  # 센서 이름 
    value = db.Column(db.String())        # 센서 받은 값 
    unit = db.Column(db.String())
    sensor_location = db.Column(db.String())
    datetime = db.Column(db.String())

    
    def __init__(self, experimenter_id=None, sensor_name=None, value=None, unit=None, sensor_location=None, datetime=None):
        self.experimenter_id = experimenter_id
        self.sensor_name = sensor_name
        self.value = value
        self.unit = unit
        self.sensor_location = sensor_location
        self.datetime = datetime


    def serialize(self):
        return {
            'id': self.id,
            'experimenter_id':self.experimenter_id,
            'sensor_name':self.sensor_name,
            'value':self.value,
            'unit':self.unit ,
            'sensor_location':self.sensor_location ,
            'datetime':self.datetime,
        }
    
    def meta(self):
        