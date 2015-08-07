#!/bin/bash

pushd ../C_Application/SC_OAM

source CMake/set-env-linsee-bleeding-edge
./configure $1 --add-tests=UTMT

if [ "$1" = "FCMD" ]; then
    cd output-FCMD-x86_64-Linux-UTMT
elif [ "$1" = "FCT" ]; then
    cd output-FCT-x86_64-Linux-UTMT
fi

cmake .. -DBOARD=$1 -DOM_MT_TEST_ENABLE=ON -DUSE_BM=OFF -DINCLUDE_DB_Database=ON -DINCLUDE_FM_FaultManagement=ON
make generate_rhapsody_all -j10

echo BUILDING...
make FM_FaultManagement_Test -j10 > ../../../$1_build.log 2>&1 && echo Building successful

popd
