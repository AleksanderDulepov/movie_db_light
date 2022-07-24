import sqlalchemy
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

import utils
from app.database import db
from app.models import MovieSchema, Movie

movie_ns=Namespace("movies")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):

        movie_query=db.session.query(Movie)

        parameters=request.args

        director_id = parameters.get('director_id')
        genre_id = parameters.get('genre_id')
        year = parameters.get('year')

        if director_id is not None:
            movie_query = movie_query.filter(Movie.director_id == director_id)
        if genre_id is not None:
            movie_query = movie_query.filter(Movie.genre_id == genre_id)
        if year is not None:
            movie_query = movie_query.filter(Movie.year == year)

        results = movie_query.all()
        return movies_schema.dump(results), 200

    def post(self):
        return utils.post_universal(Movie)


@movie_ns.route("/<int:uid>")
class MovieView(Resource):
    def get(self, uid):
        return utils.get_by_id_universal(uid, Movie, movie_schema)

    def put(self, uid):
        try:
            input_data = request.json
            item = db.session.query(Movie).get_or_404(uid)
            item.title = input_data.get('title')

            item.description = input_data.get('description')
            item.trailer = input_data.get('trailer')
            item.year = input_data.get('year')
            item.rating = input_data.get('rating')
            item.genre_id = input_data.get('genre_id')
            item.director_id = input_data.get('director_id')

            db.session.add(item)
            db.session.commit()
            db.session.close()
            return "", 204
        except sqlalchemy.exc.IntegrityError:
            return "Был передан уже существующий в базе id", 405
        except (TypeError, BadRequest, AttributeError):
            return "Переданы данные несоответствующего формата", 405
        except Exception as e:
            return str(e), 405

    def patch(self, uid):
        return utils.patch_universal(uid, Movie)

    def delete(self, uid):
        return utils.delete_universal(uid, Movie)
