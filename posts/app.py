from website import create_app
from website.jsons.errors import UnprocessableEntityJson
from website.utils import dict_to_list

app = create_app()


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    # webargs attaches additional metadata to the `data` attribute
    exc = getattr(err, "exc")
    if exc:
        # Get validations from the ValidationError object
        messages = dict_to_list(exc.messages)
    else:
        messages = ["Invalid request"]
    return UnprocessableEntityJson(messages).to_json(), 422


@app.cli.command()
def initdb():
    from website.models import db
    db.create_all()
