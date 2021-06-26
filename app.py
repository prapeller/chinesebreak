from source import app
from sqlalchemy import text
from source import db

if __name__ == '__main__':
    app.run(debug=True)
