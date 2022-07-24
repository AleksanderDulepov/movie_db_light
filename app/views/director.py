import sqlalchemy
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

import utils
from app.database import db
from app.models import DirectorSchema, Director

director_ns=Namespace("directors")

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        return utils.get_all_universal(Director, directors_schema)

    def post(self):
        return utils.post_universal(Director)


@director_ns.route("/<int:uid>")
class DirectorView(Resource):
    def get(self, uid):
        return utils.get_by_id_universal(uid, Director, director_schema)

    def patch(self, uid):
        return utils.patch_universal(uid, Director)

    def put(self, uid):
        try:
            input_data = request.json
            item = db.session.query(Director).get_or_404(uid)
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
        return utils.delete_universal(uid, Director)