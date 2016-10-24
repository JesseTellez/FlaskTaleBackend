#config stuff

class Config:
    SECRET_KEY = "SunshineSucks"
    
    @staticmethod
    def init_app(app):
        pass
        
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:cheeseit007@localhost/taleTestBase'
    
config = {
    'development': DevelopmentConfig
}