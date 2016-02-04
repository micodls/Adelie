"""
    Sparse checkout script for WCDMA BTS SC OAM development
    Author: Paolo Gino Latorilla
    Contact: paolo.latorilla.ext@nsn.com
"""

import argparse
import subprocess
import time
import platform


# Main application entry point
def main():
    program_options = _get_program_options()
    is_linux = platform.system().lower() == "linux"

    # Resolve full branch URL from alias
    root_svn_url = program_options["server"]

    if root_svn_url.endswith("/"):
        root_svn_url = root_svn_url[0:-1]

    wcdma_svn_url = root_svn_url + "/isource/svnroot/BTS_SC_OAM/WCDMA"
    branch_name = _expand_branch_alias(program_options["branch"])

    root_folder = program_options["folder"]

    if not len(root_folder):
        root_folder = branch_name.split("/")[-1]

    # Start recording time
    with Timer():
        # Build root directory structure
        _checkout(
            program_options["revision"],
            "immediates",
            wcdma_svn_url + "/" + branch_name,
            root_folder)

        if (program_options["domain"] == "delivery"):
            _update("infinity", root_folder + "/C_Application");
            _update("infinity", root_folder + "/I_Interface")
            _update("infinity", root_folder + "/E_External")
            return

        # Resolve domain alias
        domain = _expand_domain_alias(program_options["domain"])

        # Download SUT commons
        for (target, depth) in _get_common_dependencies():
            _update(depth, root_folder + "/C_Application/" + target)

        # Download all externals of C_Application
        _checkout_externals_of(root_folder + "/C_Application", root_svn_url)

        # Download legacy MT Makefiles
        if (program_options["config"] == "legacy-mt" or
                program_options["config"] == "mt"):
            _update(
                "infinity",
                root_folder + "/C_Application/SC_OAM/Makefiles")

            _update(
                "infinity",
                root_folder + "/C_Platform")

        # Download Linux dependencies
        if is_linux:
            for (target, depth) in [
                    ("/DM_ALMAG/src/static", "immediates"),
                    ("/DM_ALMAG/src/include/DM_ALMAG/FilesPathPrivate.hpp", "immediates"),
                    ("/CM_ConfigurationManagement/src/static", "immediates"),
                    ("/FM_FaultManagement/conf", "immediates"),
                    ("/SIM_SystemInterfaceManagement/src/ASNGeneric",
                        "infinity")]:
                _update(depth, root_folder + "/C_Application/SC_OAM/" + target)

        # Download domain SUT
        _update(
            "infinity",
            root_folder + "/C_Application/SC_OAM/" + domain)

        # Download SUT CMake directory and CI scripts
        _update(
            "infinity",
            root_folder + "/C_Application/SC_OAM/CMake")

        # Download MT commons
        for (target, depth) in _get_common_test_dependencies():
            _update(depth, root_folder + "/C_Test/" + target)

        # Download domain MT
        _update("infinity", root_folder + "/C_Test/SC_OAM/" + domain)

        # Download domain-specific dependencies
        for dependency in {
                "FM": ["C_Application/SC_OAM/CMake"],
                "SSW": ["C_Application/SC_OAM/CMake"],
                "Startup": [
                    "C_Application/SC_OAM/DM_FSM",
                    "C_Application/SC_OAM/SYSM_SystemManagement",
                    "C_Test/SC_OAM/Startup",
                    "C_Test/SC_OAM/DM_FSM",
                    "C_Test/SC_OAM/SYSM_SystemManagement"]}.get(
                        program_options["domain"], []):
            _update("infinity", root_folder + "/" + dependency)

        # Download SACK
        _update("infinity", root_folder + "/E_External")
        _update("infinity", root_folder + "/I_Interface")


# Helper classes
class Timer:
    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, type, value, traceback):
        print "***Total checkout time (seconds) = ", \
            round(time.time() - self.start_time, 4), "***"


# Helper functions
def _get_program_options():
    parser = argparse.ArgumentParser(
        prog="sparco",
        formatter_class=argparse.RawTextHelpFormatter,
        description="SPARse CheckOut for WCDMA BTS SC OAM.\n" +
        "Copyright 2014 Nokia Solutions and Networks.")

    parser.add_argument(
        "branch",
        help="The development branch name. " +
        "See `Readme.txt` for the list of supported branches.")

    parser.add_argument(
        "domain",
        help="The domain that will be checked-out. " +
        "If 'delivery' is specified then no test code will be downloaded." +
        "See `Readme.txt` for the list of supported domains.")

    parser.add_argument(
        "folder",
        nargs="?",
        default="",
        help="The destination folder. " +
        "If nothing is specified then the basename of the " +
        " effective URL will be used.")

    parser.add_argument(
        "-r", "--revision",
        metavar="R",
        type=int,
        default=-1,
        help="The target revision. Defaults to the topmost revision.")

    parser.add_argument(
        "-c", "--config",
        choices=["wtf-mt", "legacy-mt", "mt"],
        default="mt",
        help="The checkout configuration (default: %(default)s).\n" +
        "Configurations available:\n" +
        "  [wtf-mt] : Ideal for running WTF MT.\n" +
        "  [legacy-mt] : Ideal for running legacy MT.\n" +
        "  [mt] : Ideal for running both WTF and legacy MT.\n")

    parser.add_argument(
        "-s", "--server",
        metavar="URL",
        default="https://svne1.access.nsn.com",
        help="The host URL that will be used (default: %(default)s).")

    return vars(parser.parse_args())


def _expand_branch_alias(alias):
    if alias.startswith("branches/"):
        if len(alias) > len("branches/"):
            return alias
        else:
            raise RuntimeError("{} is not a valid branch!".format(alias))
    else:
        prefix = "branches/maintenance"
        retval = {
            "trunk": "trunk",
            "1104": prefix + "/WN7.0_1104",
            "1104_80204_01": prefix + "/WN7.0_1104_80204_01",
            "1104_EP1": prefix + "/WN7.0_1104_EP1",
            "1104_P8": prefix + "/WN7.0_1104_P8",
            "1207": prefix + "/WN7.0_1207",
            "1207_1056": prefix + "/WN7.0_1207_1056",
            "1207_575": prefix + "/WN7.0_1207_575",
            "1207_753": prefix + "/WN7.0_1207_753",
            "1302": prefix + "/WN7.0_1302",
            "1302_126806": prefix + "/WN7.0_1302_126806",
            "1302_223": prefix + "/WN7.0_1302_223",
            "1302_389": prefix + "/WN7.0_1302_389",
            "OM_9313_123450S": prefix + "/WN7.0_OM_9313_123450S",
            "OM_9313_140860S": prefix + "/WN7.0_OM_9313_140860S",
            "1301": prefix + "/WN8.0_1301",
            "1301_1057": prefix + "/WN8.0_1301_1057",
            "1301_1058_02": prefix + "/WN8.0_1301_1058_02",
            "1301_121133_PCD3": prefix + "/WN8.0_1301_121133_PCD3",
            "1301_122758_PCD4": prefix + "/WN8.0_1301_122758_PCD4",
            "1301_296_01": prefix + "/WN8.0_1301_296_01",
            "1301_320": prefix + "/WN8.0_1301_320",
            "1301_484": prefix + "/WN8.0_1301_484",
            "1301_484_132076": prefix + "/WN8.0_1301_484_132076",
            "1301_484_139720": prefix + "/WN8.0_1301_484_139720",
            "1301_842": prefix + "/WN8.0_1301_842",
            "1301_842_09": prefix + "/WN8.0_1301_842_09",
            "1301_842_35": prefix + "/WN8.0_1301_842_35",
            "1308": prefix + "/WN8.0_1308",
            "1308_214": prefix + "/WN8.0_1308_214",
            "1308_253": prefix + "/WN8.0_1308_253",
            "1308_321": prefix + "/WN8.0_1308_321",
            "1308_437": prefix + "/WN8.0_1308_437",
            "1308_555": prefix + "/WN8.0_1308_555",
            "OM_1301_430": prefix + "/WN8.0_OM_1301_430",
            "1401": prefix + "/WN9.0_1401",
            "1401_225": prefix + "/WN9.0_1401_225",
            "1401_295": prefix + "/WN9.0_1401_295",
            "1401_340": prefix + "/WN9.0_1401_340",
            "1401_423": prefix + "/WN9.0_1401_423",
            "9.1": prefix + "/WN9.1_0000",
            "9.1_185": prefix + "/WN9.1_0000_185",
            "9.1_283": prefix + "/WN9.1_0000_283",
            "9.1_PCD4": prefix + "/WN9.1_0000_PCD4",
            "OM_0001_179308S": prefix + "/WNOM_0001_179308S"
        }.get(alias, None)

    if retval is None:
        raise RuntimeError(
            "{} isn't an alias of a maintenance branch.".format(alias))

    return retval


def _expand_domain_alias(alias):
    retval = {
        "BBC": "BBC_BasebandBusConfiguration",
        "CLIC": "CLIC_ClimateControl",
        "CM": "CM_ConfigurationManagement",
        "COM": "COM_Mediator",
        "DB": "DB_Database",
        "ALMAG": "DM_ALMAG",
        "DM_Common": "DM_Common",
        "DM_FSM": "DM_FSM",
        "RPMAG": "DM_RPMAG",
        "FM": "FM_FaultManagement",
        "FML": "FoundationModel",
        "HWM": "HWM_HardwareManagement",
        "II": "InternalInterfaces",
        "LM": "LM_LicenceManagement",
        "PM": "PM_PerformanceManagement",
        "SIM": "SIM_SystemInterfaceManagement",
        "SPM": "SPM_SignalProcessingManagement",
        "SSW": "SSW_SupportSoftware",
        "Startup": "Startup",
        "SWM": "SWM_SoftwareManagement",
        "SYNC": "SYNC_Synchronization",
        "SYSM": "SYSM_SystemManagement",
        "SYSM_WCDMA": "SYSM_WCDMA",
        "TM": "TM_TestManagement",
        "TR": "TR_TechnicalReporting"
    }.get(alias, None)

    if retval is None:
        raise RuntimeError(
            "{} is not a valid BTSOM domain/subsystem/component."
            .format(alias))

    return retval


def _execute(command, abort_on_error=True):
    exit_code = subprocess.Popen(command.split()).wait()
    error_message = '"{}" exited with {}.'.format(command, exit_code)

    if exit_code == 0:
        return

    if abort_on_error:
        raise RuntimeError(error_message)
    else:
        print "***WARNING: ", error_message


def _checkout(revision, depth, url, target):
    if revision > 0:
        rev_str = "--revision={}".format(program_options["revision"])
    else:
        rev_str = ""

    _execute(
        "svn co {} --depth={} {} {}".format(rev_str, depth, url, target))


def _checkout_externals_of(target, root_svn_url):
    (raw_lines, _ignore) = subprocess.Popen(
        ("svn pg --non-interactive --strict svn:externals " + target)
        .split(),
        stdout=subprocess.PIPE).communicate()

    lines = raw_lines.splitlines()

    if lines == []:
        print "***WARNING: No externals found!***"
        return

    for line in lines:
        if line.startswith('#'):
            continue

        try:
            (ext_url, ext_folder) = line.split()

            _execute(
                "svn co --non-interactive --depth=infinity {}{} {}/{}"
                .format(
                    root_svn_url,
                    ext_url,
                    target,
                    ext_folder))

        except ValueError:
            print "***WARNING: No externals found!***"
            return


def _update(depth, target):
    _execute(
        "svn up --non-interactive --trust-server-cert --parents " +
        " --set-depth={} {}"
        .format(depth, target), False)


# Dependencies
def _get_common_dependencies():
    for (target, depth) in [
            ("conf", "immediates"),
            ("SC_OAM", "immediates"),
            ("SC_OAM/DB_Database", "infinity"),
            ("SC_OAM/FoundationModel", "infinity"),
            ("SC_OAM/FM_FaultManagement/src/include/FM_FaultManagement/Unit/InternalFaultIndication.h", "immediates"),
            ("SC_OAM/include", "infinity"),
            ("SC_OAM/Include_Path", "infinity"),
            ("SC_OAM/InternalInterfaces", "infinity"),
            ("SC_OAM/Main", "infinity"),
            ("SC_OAM/SSW_SupportSoftware", "infinity")]:
        yield (target, depth)


def _get_common_test_dependencies():
    for (target, depth) in [
            ("CMakeLists.txt", "immediates"),
            ("SC_OAM", "immediates"),
            ("SC_OAM/BPFFinder/CMakeLists.txt", "immediates"),
            ("SC_OAM/CCSStub/CMakeLists.txt", "immediates"),
            ("SC_OAM/CoreMT/CMakeLists.txt", "immediates"),
            ("SC_OAM/DeprecatedStubs/CMakeLists.txt", "immediates"),
            ("SC_OAM/DBDumpLoader/CMakeLists.txt", "immediates"),
            ("SC_OAM/DBHelpers/CMakeLists.txt", "immediates"),
            ("SC_OAM/MT_COMMONS", "infinity"),
            ("SC_OAM/SSW_FML_Workaround/CMakeLists.txt", "immediates"),
            ("SC_OAM/SSW_SupportSoftware", "infinity"),
            ("SC_OAM/SSW_WORKAROUND/CMakeLists.txt", "immediates"),
            ("SC_OAM/TimeSimulator/CMakeLists.txt", "immediates"),
            ("SC_OAM/UniversalSimulator/CMakeLists.txt", "immediates"),
            ("SC_OAM/UT_Commons", "immediates")]:
        yield (target, depth)


if __name__ == "__main__":
    main()
