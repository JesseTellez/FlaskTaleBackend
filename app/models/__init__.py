from flask.ext.sqlalchemy import SQLAlchemy
from app import current_app
#from coaster.sqlalchemy import BaseMixin, BaseNameMixin, BaseScopedNameMixin, BaseScopedIdNameMixin, BaseScopedIdMixin

db = SQLAlchemy(current_app)

#NOTE - the ordering may matter here, avoid circular import
#THE ORDERING DOES MATTER HERE
#put the ones that dont depend on anything on top
from app.models.Addition import *
from app.models.User import *
from app.models.Story import *
from app.models.Genre import *