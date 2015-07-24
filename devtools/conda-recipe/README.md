This is a recipe for building the current development package into a conda
binary.

The installation on travis-ci is done by building the conda package, installing
it, running the tests, and then if successful pushing the package to binstar
(and the docs to AWS S3). The binstar auth token is generated using:
```
binstar auth -n targetexplorer -o choderalab --max-age 22896000 -c --scopes api:write
```
and should then be saved in the environment variable `BINSTAR_TOKEN`.

You can set up travis to store an encrypted token via
```
gem install travis
travis encrypt BINSTAR_TOKEN=xx
```

where xx is the token output by binstar. The final command should print a line (containing 'secure') for inclusion in your `.travis.yml` file.