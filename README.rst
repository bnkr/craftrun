Craftrun
========

Introduction
------------

A simple python program to manage a minecraft server using screen.

Usage
-----

Clone from git and use ./bin/craftrun.

See --help text for commands and options.  Read the source for more details and
defaults.

A configuration yaml file is required::

  # Used to name things like the screen session
  server_name: vanilla
  # Where is the server
  base_dir: "./serverdata"
  # Where to output backup tarballs data
  backup_dir: "."
  # Relative path to server jar file within the server dir.
  server_jar: minecraft_server.1.7.4.jar
  # Location of java (optional)
  java_bin: "../jre1.7.0_65/bin/java"

Paths are always relative to the directory containing the config file (except as
noted above).

Examples (console output may change)::

  $ ./bin/craftrun -c config.yml -v start
  2014-01-27 23:13:54,816 INFO chdir '/home/mc/craftrun/serverdata'
  2014-01-27 23:13:55,822 INFO probably running
  $ ./bin/craftrun -c config.yml -v stop
  2014-01-27 23:13:18,182 INFO session has stopped
  $ ./bin/craftrun -c config.yml -v backup
  2014-01-27 23:14:38,895 INFO chdir '/home/mc/craftrun'
  2014-01-27 23:14:38,897 INFO turning saving off
  2014-01-27 23:14:38,899 INFO flushing data
  2014-01-27 23:14:38,901 INFO waiting 10s for flush
  2014-01-27 23:14:48,912 INFO making tarball from serverdata
  2014-01-27 23:14:50,455 INFO turning saving on
  $ ls *.tar.*
  vanilla-full-2014-01-27.23-14-38.tar.bz2

Limitations
-----------

* no unit tests :(

* a user can leave the screen session in a state where commands won't work

* can't accurately detect that the server has started properly
