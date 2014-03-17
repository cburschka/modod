Building
========

* This will create an egg file for download and installation with easy_install:

    $ python3 setup.py bdist_egg

* This will install the package, either on the system or the user site:

    $ python3 setup.py install [--user]

  (The user site is ~/.local on UNIX and %APPDATA%\Python on Windows.)

* This will create a source distribution, which can be easily downloaded,
  unpacked and used without installation:

    $ python3 setup.py sdist [--format=gzttar|zip]
