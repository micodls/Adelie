
            SRAN scripts

  What is it?
  -----------

  SRAN scripts is a compilation of commands commonly used
  in our daily lives.

  Different Parts
  ---------------

  sran.py - A python-based script used in running commands
            in the CLI.

  Version History
  ---------------

  [Version 1]
    o 23-07-15
    o Includes git configuration and clone

  Requirements
  ------------

    o Python 2.7.* or higher should be installed.

  Installation
  ------------

  sran_scripts checkout link: https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/BTS_SC_OAM/WCDMA/branches/users/pdelos/sran_scripts

  [WINDOWS]
  1. Checkout sran_scripts
  2. Run install.bat

  Usage
  -----

  [WINDOWS]
  sran.py [subcommand] [parameter...]

  ---------------------------------------------------------------------------------------------------------------------
  |  Subcommand  |     Parameter       |    Description    |     Value      |  Required  |       Sample usage         |
  |-------------------------------------------------------------------------------------------------------------------|
  |   config     |                     |                   |                |            |  sran.py config            |
  |-------------------------------------------------------------------------------------------------------------------|
  |   clone      |  source             |  source URL       |  [branch]      |    True    |  sran.py clone nodeoam     |
  |              |  dest               |  destination URL  |  [dest URL]    |    False   |                            |
  ---------------------------------------------------------------------------------------------------------------------

  Additional Notes :
   o config   - Configures global git variables

   o clone    - Clones repository via HTTP. SSH doesn't work in Manila.

  [LINUX]
  **Not yet tested**

  Others
  ------

    o This is an open-source project
    o For questions, suggestions and comments, contact me at <paolo.de_los_santos@nokia.com>
