cd gddownloader
python tests/__init__.py
# - run coverage
coverage run tests/*.py
coverage report
coveralls