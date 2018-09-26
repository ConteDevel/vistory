from viauth import app
from website.app import create_app
from website.config import default

if __name__ == "__main__":
    create_app()
    app.run(debug=default.TESTING)
