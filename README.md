korpora zei sisku
=================

Hosted at:

    [https://korp.alexburka.com](https://korp.alexburka.com)

To add new corpus to "ralju korpora", add them to the directory
`corpus_import/ralju/original`, in a format that parallels the
other entries in that directory, and send me a pull request.

Installation
------------

This is the repository for the "corpus pipeline" of korpora zei sisku.

Try running the `install.sh` script. It should install the pipeline
and put makefiles in the right directories.
If it does not work, visit this page:
http://spraakbanken.gu.se/swe/forskning/infrastruktur/korp/distribution/corpuspipeline.
The additional dependencies you will need are GNU Make, Python 2.7 and Corpus Workbench.

You also need the modified version of jbofi'e, which you can get at https://github.com/danr/jbofihe.
The `jbofihe` and `cmafihe` executables should be in your `$PATH`.

Python dependencies:

    * BeautifulSoup 4
    * unidecode
    * dateutil


You will need to set the `CWB_DATADIR` and `CORPUS_REGISTRY` environment variables,
and also you `PYTHONPATH` to the `corpus_import/annotate/python` directory.
The `SB_MODELS` variable also needs to be set, but it can be set to anything
since we won't be using those models anyway.

Example:

    export PYTHONPATH=$HOME/code/jbokorp/corpus_import/annotate/python:$PYTHONPATH
    export SB_MODELS=$HOME/code/jbokorp/corpus_import/annotate/models
    export CWB_DATADIR=$HOME/corpora/data
    export CORPUS_REGISTRY=$HOME/corpora/registry

Test
----

Go to the `ralju` directory, and issue

    make export

After a while, you should have an `export` directory, with segmented and annotated texts.
Check that it has been reasonably well done.

To install on a remote server, do:

    make installcorpus installtimespans installinfo

You will need to change the remote, its directories and the mysql_db in `Makefile.common`.
