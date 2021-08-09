import nox

nox.options.sessions = ["lint"]
locations = "lssrp_app", "lssrp_core", "noxfile.py"


@nox.session(python=["3.9", "3.8", "3.7"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python="3.8")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
