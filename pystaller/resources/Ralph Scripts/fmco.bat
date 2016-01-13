@echo off

svn checkout %1 %2 --depth empty

svn update --set-depth infinity %2/C_Application

svn update --set-depth immediates --parents %2/C_Test/
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/BPFFinder
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/CCSStub
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/CoreMT
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/DBDumpLoader
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/DBHelpers
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/DeprecatedStubs
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/FM_FaultManagement
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/MT_COMMONS
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/SSW_FML_Workaround
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/SSW_SupportSoftware
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/SSW_WORKAROUND
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/TimeSimulator
svn update --set-depth infinity --parents %2/C_Test/SC_OAM/UniversalSimulator

svn update --set-depth infinity %2/I_Interface
svn update --set-depth infinity %2/E_External



