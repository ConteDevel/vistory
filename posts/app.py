from website import create_app
from website.jsons.errors import UnprocessableEntityJson, NotFoundJson, InternalServerErrorJson
from website.utils import dict_to_list

app = create_app()


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    exc = getattr(err, "exc")
    if exc:
        messages = dict_to_list(exc.messages)
    else:
        messages = ["Invalid request"]
    return UnprocessableEntityJson(messages).to_json(), 422


@app.errorhandler(404)
def page_not_found(err):
    return NotFoundJson([err.description]).to_json(), 404


@app.errorhandler(500)
def page_not_found(err):
    return InternalServerErrorJson([err.description]).to_json(), 500


@app.cli.command()
def initdb():
    from website.models import db
    db.create_all()
