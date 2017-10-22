# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ulises:fumies9933@backtest.cfgmbp9mytsp.eu-west-2.rds.amazonaws.com:3306/agricultores'

# Uncomment the line below if you want to work with a local DB
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'qWWpLZHEI3JufhPSVintw45i1OZxjjGJ7SMllUfo'
