python bumpversion.py patch
python -m build
twine upload -r testpypi dist/*
git commit -v -a -m "publish `date`"
git push