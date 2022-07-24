import sqlalchemy
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

import utils
from app.database import db
from app.models import GenreSchema, Genre

genre_ns=Namespace("genres")

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        return utils.get_all_universal(Genre, genres_schema)

    def post(self):
        return utils.post_universal(Genre)


@genre_ns.route("/<int:uid>")
class GenreView(Resource):
    def get(self, uid):
        return utils.get_by_id_universal(uid, Genre, genre_schema)

    def patch(self, uid):
        return utils.patch_universal(uid, Genre)

    def put(self, uid):
        try:
            input_data = request.json
            item = db.session.query(Genre).get_or_404(uid)
            item.name = input_data.get('name')
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

    def delete(self, uid):
        return utils.delete_universal(uid, Genre)
