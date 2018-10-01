from website import create_app

app = create_app()


@app.cli.command()
def initdb():
    from website.models import db
    db.create_all()
