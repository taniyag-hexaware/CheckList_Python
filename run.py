from app import app
from config import DEBUG

if __name__ == '__main__':
    # Running app in debug mode
    app.run(debug=DEBUG)