from flask import Flask
from flask_restx import Api
from app.config import Config
from app.database import db
from app.views.director import director_ns
from app.views.genre import genre_ns
from app.views.movie import movie_ns


def create_app(config):
    # создание приложения
    application = Flask(__name__)
    # конфиги
    application.config.from_object(config)  # (конфигурация загружается из обьекта)
    application.app_context().push()  # применение загруженных конфигов

    return application


def configure_app(application_):
    db.init_app(application_)   #конфигурирование приложения в БД
    api = Api(application_) #конфигурирование приложения в Api

    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)

if __name__ == '__main__':
    app_config = Config()  # создание обьекта класса Config
    app = create_app(app_config)  # вызов функции создания и настройки приложения Flask
    configure_app(app)  # вызов функции конфигурирования приложения с БД, APi
    app.run()
