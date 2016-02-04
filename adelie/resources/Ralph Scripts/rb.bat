@echo off
if '%1' == 'new' (
    set command=post-review --server=http://omcpservices.wroclaw.nsn-rdnet.net/reviewboard --target-groups="NIMASOPER_EXT_FM, WR_INDIA" --target-people="penaflor,  lewowski" --testing-done=MT -o
) else (
    set command=post-review --server=http://omcpservices.wroclaw.nsn-rdnet.net/reviewboard -r %1
)

:BEGIN_LOOP
if '%2' == '' (
    goto END_LOOP
)
set command= %command% %2
shift /2
goto BEGIN_LOOP
:END_LOOP

%command%