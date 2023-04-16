import nox
PYTHON_VERSIONS = ["3.11", "3.10", "3.9", "3.8", "3.7"]

@nox.session(python=PYTHON_VERSIONS)
def lint(session):
     session.install("flake8")
     session.run("flake8", "--max-line-length", "120", "justdays/period.py")
     session.run("flake8", "--max-line-length", "120", "justdays/day.py")


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    # same as pip install .
    session.install(".")
    session.install("pytest")
    session.run("pytest")

