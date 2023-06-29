# Tools for working with Pytch demos

Set-up:

``` shell
# In root of repo:
poetry install
```

Use to create bundle:

``` shell
python make_bundle.py
```

which will collect all demos into a zip-of-zips and tell you the full
pathname of the final zipfile.


## Use with integration tests of Pytch webapp

``` shell
# In root of repo:
./tools/serve-zips.sh
```

will freshly bundle the demos and then serve the contents of the
resulting zipfile from `localhost:8126`.  This is the base URL which
is used by the integration tests of the main webapp to test the 'try
this suggested demo' functionality.
