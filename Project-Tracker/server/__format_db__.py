from server import app
import database

database.init(app)
print(database.format())
