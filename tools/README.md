# Tools for working with Pytch demos

Set-up:

``` shell
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Use to create bundle:

``` shell
python make_bundle.py
```

which will collect all demos into a zip-of-zips and tell you the full
pathname of the final zipfile.
