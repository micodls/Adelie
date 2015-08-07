
            FM scripts

  What is it?
  -----------

  FM scripts is a compilation of commands commonly used
  in our daily lives.

  Different Parts
  ---------------

  FM.py - A python-based script used in running commands
          in the CLI.

  setenv.bat - A batch script used in invoking vsvars32.bat
               which sets the users environment for Microsoft
               Visual Studio.

  build.sh - A bash script used in compiling in Linux based
             systems. Created by Ralph Dagdag.

  *Note: setenv.bat and build.sh will be included in FM.py in the
         near future.

  Prerequisites
  -------------

    o Python 2.7.* or higher should be installed. Also, path should
      also be set in environment variables

  Usage
  -----

  [WINDOWS]
  1. Open CLI in C:\work\[working_directory]\scripts
  2. Run setenv.bat
  3. FM [subcommand][parameters]

  ------------------------------------------------------------------------------------------------------------------------------
  |  Subcommand  |     Parameter       |        Description         |      Value     |  Required  |       Sample usage         |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   logs       |  -r/--release       |  release to be compiled    |  [2|3]         |    True    |  FM logs -r3 -tc="MT/..."  | *Note: The quotations are required
  |              |  -tc/--testcase     |  testcase path from MT/UT  |  [path]        |    True    |                            |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   cmake      |  -r/--release       |  release to be compiled    |  [2|3]         |    True    |  FM cmake -r3              |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   gen        |  -r/--release       |  release to be compiled    |  [2|3]         |    True    |  FM gen -r3                |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   build      |  -r/--release       |  release to be compiled    |  [2|3]         |    True    |                            |
  |              |  -w/--warning       |  turns warning prints ON   |                |    False   |  FM build -r3 -e           |
  |              |  -e/--error         |  turns error prints OFF    |                |    False   |                            |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   buildall   |  -r/--release       |  release to be compiled    |  [2|3]         |    True    |                            |
  |              |  -w/--warning       |  turns warning prints ON   |                |    False   |  FM buildall -r2 -w        |
  |              |  -e/--error         |  turns error prints OFF    |                |    False   |                            |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   run        |  -tc/--testcase     |  testcase path from MT/UT  |  [path]        |    True    |  FM run -tc="MT/..."       | *Note: The quotations are required
  |----------------------------------------------------------------------------------------------------------------------------|
  |   runall     |                     |                            |                |            |  FM runall                 |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   rb         |  -r/--reviewboard   |  reviewboard id            |  [rb id]       |    False   |                            |
  |              |  -cl/--changelist   |  svn changelist            |  [changelist]  |    True    |  FM rb -diff=changes.diff  | *Note: -cl and -d are mutually exclusive
  |              |  -d/--diff          |  difference file           |  [diff file]   |    True    |                            |
  |----------------------------------------------------------------------------------------------------------------------------|
  |   co         |  source             |  source URL                |  [source URL]  |    True    |  FM co http://...          |
  |              |  dest               |  destination URL           |  [dest URL]    |    False   |                            |
  ------------------------------------------------------------------------------------------------------------------------------

  Additional Notes :
   o logs     - Opens the log in notepad++. Can be changed to pronto
                terminator if user wants to. See TestCaseOpener::OpenFile
                method in FM.py and change accordingly.

   o cmake    - Creates bin_rel2 or bin_rel3 depends on the release if bin
                folder does not exist.

   o gen      - Requires setenv.bat to be run beforehand.

   o build    - Requires setenv.bat to be run beforehand. Warning/error prints
                can be seen in bin_rel2/FSMr2_build.log or bin_rel3/FSMr3_build.log.

   o buildall - Requires setenv.bat to be run beforehand. Invokes cmake, gen
                and build.

   o runall   - Runs all testcases include MT, UT and UTLeaks. Logs will be places in
                app/exe/test_output.log

   o rb       - If there is no -rb, review will be posted as a new review. Diff file
                must be placed in WCDMA root (the directory containing C_Application, C_Test, ...).

   o co       - Just a SPARSE checkout of important directories so that FM can be compiled.
                Checkout will always be put in C:\work. Change work path if necessary.
                If dest path is empty, it will take the same name as the source URL as long
                as there is no existing directory with the same name.

  [LINUX]
  1. Go to WCDMA root (the directory containing C_Application, C_Test, ...) in LinSEE using Putty
  2. cd scripts
  3. Give permissions to this file by calling
        chmod 777 build.sh
     This command needs to be called only once. (i.e. Succeeding sessions won't require this call any more)
  4. Run the bash script either for FCMD or FCT
       ./build.sh FCMD
            OR
       ./build.sh FCT
     Compilation messages will be stored in FCMD_build.log or FCT_build.log depending on release

  Others
  ------

    o This is an open-source project
    o CLI vs GUI <http://www.computerhope.com/issues/ch000619.htm>
    o For questions, suggestions and comments, contact me at <paolo.de_los_santos@nsn.com>
