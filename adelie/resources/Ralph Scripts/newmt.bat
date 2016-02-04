@echo off

if '%1' == 'setup' (
    call create_setup_conf.bat C:\NWL\BTS_OAM\Repo\%2
    goto END
) else if '%1' == 'r2' (
    set Prefix=MT_WCDMA
    set BuildCommand=MT_WCDMA_FCMD
    set MtExe=mt.exe
) else if '%1' == 'r3' (
    set Prefix=MT_WCDMA_FCT
    set BuildCommand=MT_WCDMA_FCT
    set MtExe=mt_fct.exe
) else (
    goto INVALID_COMMAND
)

if '%2' == 'clean' (
    bjam %Prefix%_CLEAN -j5
) else if '%2' == 'sutclean' (
    bjam %Prefix%_SUT_CLEAN -j5
) else if '%2' == 'gen' (
    bjam %Prefix%_SUT_GEN -j5
) else if '%2' == 'sutcom' (
    bjam %Prefix%_SUT_COM -j5
    REM )
) else if '%2' == 'build' (
    bjam %BuildCommand% -j5
) else if '%2' == 'run' (
    pushd app\bin
    set Command=%MtExe% --nouserattention --spawn --detect_memory_leaks=0
    goto BEGIN_LOOP
) else if '%2' == 'runs' (
    pushd app\bin
    set Command=%MtExe% --nouserattention --spawn --detect_memory_leaks=0 --repeat=%3
    shift /3
    goto BEGIN_LOOP
) else if '%2' == 'debug' (
    pushd app\bin
    %MtExe% --debug --detect_memory_leak=0 -t %3 --testcase=%4
    popd
) else (
    goto INVALID_COMMAND
)
goto END

:BEGIN_LOOP
if '%3' == 'log' (
    set Command=%Command% --output_format=XML --log_level=all
) else if '%3' == '' (
    goto END_LOOP
) else (
    if '%4' == '' (
        set Command=%Command% --spawn -t %3 --testcase=%4
    ) else (
        set Command=%Command% -t %3 --testcase=%4
    )
    goto END_LOOP
)
shift /3
goto BEGIN_LOOP
:END_LOOP

%Command%
popd
goto END

:INVALID_COMMAND
@echo Invalid Command

:END