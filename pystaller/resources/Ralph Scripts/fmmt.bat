@echo off

if '%1' == 'r2' (
    set BinDir=C_Application\SC_OAM\bin_r2
    set Board=FCMD
) else if '%1' == 'r3' (
    set BinDir=C_Application\SC_OAM\bin_r3
    set Board=FCT
) else (
    goto INVALID_COMMAND
)

set MtExe=FM_FaultManagement_Test.exe

if '%2' == 'cmake' (
    if exist %BinDir% (
        pushd %BinDir%
        cmake ..
    ) else (
        mkdir %BinDir%
        pushd %BinDir%
        cmake .. -G "Visual Studio 12" -DBOARD=%Board% -DOM_MT_TEST_ENABLE=ON -DUSE_BM=OFF -DINCLUDE_DB_Database=ON -DINCLUDE_FM_FaultManagement=ON
    )

    popd
) else if '%2' == 'gen' (
    echo GENERATING...
    msbuild /m /verbosity:minimal %BinDir%\generate_rhapsody_all.vcxproj
) else if '%2' == 'build' (
    echo BUILDING...
    msbuild /m /verbosity:minimal %BinDir%\T\Fat18\FM_FaultManagement_Test.vcxproj > %1_build.log 2>&1 && echo [-------------------- SUCCESS -------------------]

    echo.
    echo [-------------------- WARNINGS -------------------]
    grep ": warning" %1%_build.log

    echo.
    echo [--------------------- ERRORS --------------------]
    grep -e ": error" -e ": fatal error" %1_build.log

) else if '%2' == 'run' (
    pushd C_Test\SC_OAM\FM_FaultManagement\MT\app\exe

    %MtExe% --nouserattention --spawn=5 -t %3

    popd
) else if '%2' == 'runall' (
    echo RUNNING ALL...
    pushd C_Test\SC_OAM\FM_FaultManagement\MT\app\exe

    %MtExe% --nouserattention --output_format=XML --log_level=all --spawn=5 > ..\..\..\..\..\..\%1_test_output.log 2>&1

    echo [--------------------- MT --------------------] > ..\..\..\..\..\..\%1_failed.log
    grep -P "^tc\s+MT/\S+ +\S+" ..\..\..\..\..\..\%1_test_output.log >> ..\..\..\..\..\..\%1_failed.log

    echo. >> ..\..\..\..\..\..\%1_failed.log
    echo [--------------------- UT --------------------] >> ..\..\..\..\..\..\%1_failed.log
    grep -P "^tc\s+UT/\S+ +\S+" ..\..\..\..\..\..\%1_test_output.log >> ..\..\..\..\..\..\%1_failed.log

    echo. >> ..\..\..\..\..\..\%1_failed.log
    echo [------------------- UTLeaks -----------------] >> ..\..\..\..\..\..\%1_failed.log
    grep -P "^tc\s+UTLeaks/\S+ +\S+" ..\..\..\..\..\..\%1_test_output.log >> ..\..\..\..\..\..\%1_failed.log

    popd

    type  %1_failed.log
) else if '%2' == 'list' (
    pushd C_Test\SC_OAM\FM_FaultManagement\MT\app\exe

    if '%3' == '' (
        %MtExe% --list
    ) else (
        %MtExe% --list -t %3
    )

    popd
) else (
    goto INVALID_COMMAND
)

goto END

:INVALID_COMMAND
echo Invalid command

:END