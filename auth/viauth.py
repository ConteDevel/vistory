from website.app import create_app


app = create_app({'SQLALCHEMY_TRACK_MODIFICATIONS': False})


@app.cli.command()
def initdb():
    from website.models import db
    db.create_all()
