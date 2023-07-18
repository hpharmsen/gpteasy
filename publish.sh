pip install twine build
/bin/rm -f dist/*
python bumpversion.py patch
python -m build
twine upload dist/*
git commit -v -a -m "publish `date`"
git push
echo "run pip install --no-cache --force-reinstall gpteasy"
