import os
class Config(object):
     SECRET_KEY =os.environ.get('0HQbdZewdUuIHCBfLqPxtHnk5JxVXmblKoose')
#SQL CONFIGURATION
basedir =os.path.abspath(os.path.dirname(__file__))

class Config(object):
     SQLALCHEMY_Binds = os.environ.get([
          {'User':      'sqlite:///TroTrousers.db',
           'Fares':      'sqlite:///fares.db',
           'UserReviews':  'sqlite:///userreviews.db',
           'Drivers': 'sqlite:///drivers.db',
           'Routes': 'sqlite:///routes.db',
           'Stations': 'sqlite:///stations.db',
           'StationMasters': 'sqlite:///stationmasters.db',
           'Agents': 'sqlite:///agents.db',
           'Providence':'sqlite:///providence.db',
           '4Sale':'sqlite:///4sale.db', 
           'Survey':'sqlite:///survey.db'}
     ])
SQLALCHEMY_TRACK_MODICATIONS= False

     

