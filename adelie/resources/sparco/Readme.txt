SPARCO - SPARse CheckOut script for WCDMA BTS SC OAM development
================================================================

>  _"This script will allow you to download the least amount of source code
    that you will ever need to work with BTSOM.
    What is downloading 600MB-700MB worth of code in about 10-15 minutes versus
    2GB in about 30 minutes?"_

Version History
---------------
- 2014-08-14 :
    Changed default SVN server to https://svne1.access.nsn.com.

- 2014-07-15 :
    Autodetects if current platform is Linux; removed -l and --linux flags.

- 2014-07-10 :
    Allow MT to be run in Linux similar to Jenkins.

- 2014-07-08 :
    Added 'mt' config to allow building and running WTF and legacy MT
    simultaneously.

- 2014-07-07 :
    Fixes for downloading multiple externals and LinSEE scripts.
    Added notes for LinSEE users.

- 2014-07-04 :
    Feature reduction and script simplification.
    Support for selecting SVN servers. Added installation scripts.

- 2014-07-03 :
    Support for custom maintenance branch and fixed externals
    checkout function.

- 2014-06-17 :
    First release.

What's in the package
---------------------
- **install.bat** : Installer script for Windows
- **install.sh** : Installer script for Linux
- **sparco.py** : Platform-agnostic implementation written in Python.

Requirements
------------
- Python 2.7.6 or better
- Subversion command line client 1.8 or better

LinSEE users
------------
Run these commands prior to usage:
source /opt/svn/linux64/ix86/svn_1.8.9/interface/startup/svn_1.8.9_64.env
source /opt/python/linux64/ix86/python_2.7.4/interface/startup/python_2.7.4.env

Always accept certificates permanently when asked by SVN (don't be scared)

During compilation, don't forget to run source CMake/set-env-linsee-bleeding-edge

Installation
------------
The scripts can be downloaded from
<https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/BTS_SC_OAM/WCDMA/branches/users/latorill/sparco>.

> **Windows**
> 
1. Checkout **sparco** from the provided SVN link.
2. Add the installation folder to the `PATH` variable.
3. Go to the installation folder and run `install.bat`.

> **Linux**:
>
1. Checkout **sparco** from the provided SVN link.
2. Add the installation folder to the `PATH` variable.
3. Go to the installation folder and run `bash install.sh`.

Example usage
-------------
    sparco trunk Startup my_trunk
    sparco trunk Startup my_trunk -c wtf-mt
    sparco trunk Startup my_trunk --config wtf-mt
> This will sparsely checkout all the dependencies of _Startup_ from the
development branch _trunk_.

> The files will be downloaded in `./my_trunk`.

> All files that are necessary for running WTF-style MTs will be downloaded.

> The branch will assume the latest revision.

    sparco trunk Startup my_trunk -r 123456
> This will have the same outcome as the first example except that the branch
will assume the 123456th revision.

    sparco trunk Startup my_trunk -c legacy-mt
    sparco trunk Startup my_trunk --config legacy-mt
> The same as the first example except that the files that are necessary for
running legacy MTs (e.g. Pencil MT) will be downloaded.

    sparco trunk Startup my_trunk -c mt
    sparco trunk Startup my_trunk --config mt
> The same as the first example except that the files that are necessary for
running both WTF and legacy MTs will be downloaded.

    sparco trunk Startup my_trunk -c delivery
    sparco trunk Startup my_trunk --config delivery
> This will only download the files needed for building delivery packages
and/or "knife" builds.

    sparco -h
    sparco --help
> This will print basic usage information.

Notes for Linux users
----------------------
- Always specify the `--linux` flag.
- (LinSEE users) You will need to call
    `source <trunk-path>/C_Application/SC_OAM/CMake/set-env-linsee-bleeding-edge`
    for wtf-mt configuration or
    `source <trunk-path>/C_Application/SC_OAM/CMake/set-env-linsee` for
    delivery configuration.
- (LinSEE users) If the shared libraries for the **Google Protobuffer** are missing, run 
    `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/build/ltesdkroot/Platforms/LINUX/FB_PS_LFS_REL_2013_04_18/sdk2/packages/protobuf/usr/lib`.
- (LinSEE users) If Boost fails to link, delete the generated `CMakeCache.txt` and run
    `export BOOST_ROOT=/opt/boost/linux64/ix86/boost_1.53.0/include`.

Supported development branches
------------------------------
These are the allowed values for the `branch` command line parameter

    trunk
    1104
    1104_80204_01
    1104_EP1
    1104_P8
    1207
    1207_1056
    1207_575
    1207_753
    1302
    1302_126806
    1302_223
    1302_389
    OM_9313_123450S
    OM_9313_140860S
    1301
    1301_1057
    1301_1058_02
    1301_121133_PCD3
    1301_122758_PCD4
    1301_296_01
    1301_320
    1301_484
    1301_484_132076
    1301_484_139720
    1301_842
    1301_842_09
    1301_842_35
    1308
    1308_214
    1308_253
    1308_321
    1308_437
    1308_555
    OM_1301_430
    1401
    1401_225

You can supply a user's or maintenance branch. The format is:
    `branches/users/<your-development-branch>` or
    `branches/maintenance/<maintenance-branch-name>`.

Supported domains/subsystems/components
---------------------------------------
These are the allowed values for the `domain` command line parameter.

    BBC
    CLIC
    CM
    COM
    DB
    ALMAG
    DM_Common
    DM_FSM
    RPMAG
    FM
    FML
    HWM
    II
    LM
    PM
    SIM
    SPM
    SSW
    SWM
    Startup
    SYNC
    SYSM
    SYSM_WCDMA
    TM
    TR
    
********************************************************************************
For comments, questions, and suggestions,
    please contact me at <paolo.latorilla.ext@nsn.com>.

2014, Paolo Gino Latorilla

