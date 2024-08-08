from flask import Flask
from views import distro_data

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

app.add_url_rule("/", view_func=distro_data)


if __name__ == "__main__":
    app.run()