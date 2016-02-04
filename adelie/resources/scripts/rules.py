
from xml.etree import ElementTree
import re
import sys

class RulesParser:
    def __init__(self):
        self.tree = ElementTree.parse('C_Application\SC_OAM\FM_FaultManagement\conf\FlexiFDRULES.xml');
        self.efaultid_file = open('I_Interface\Global_Env\Definitions\EFaultId.h')
        self.entry_regex = re.compile('\([^\)]*\)', re.DOTALL)
        self.fdu_param_regex = re.compile(r'\("(.*)";(.*);\s*\)', re.DOTALL)
        self.fdar_param_regex = re.compile(r'\((\d*),(".*")\)', re.DOTALL)
        self.fault_name_regex = re.compile(r'\s*(EFaultId_\S*)\s*=\s*(\d+)')

    def print_fault_info(self, search_fault_ids):
        print('--------------------------------------------------------')
        for fault_id in search_fault_ids:
            self.print_fault_id_with_name(fault_id, 'FAULT_ID')
            self.print_fdu_fault_param(fault_id, 'FAULT_TEXT')
            self.print_delay_param(fault_id, 'START_DELAY')
            self.print_delay_param(fault_id, 'CANCEL_DELAY')
            self.print_severity(fault_id)
            self.print_fdu_fault_param(fault_id, 'OBJECT_TYPE')

            group_id = self.get_fdu_fault_param(fault_id, 'GROUP_ID')
            if group_id:
                group_id = int(group_id)
                self.print_fault_id_with_name(group_id, 'GROUP_ID')
                self.print_alarm_text(group_id)
            else:
                self.print_alarm_text(fault_id)
            print('--------------------------------------------------------')

    def print_fault_id_with_name(self, fault_id, field):
        if fault_id:
            print '%s:\t%d (%s)' % (field, fault_id, self.get_fault_name(fault_id))

    def get_fault_name(self, search_fault_id):
        for line in self.efaultid_file:
            match = self.fault_name_regex.match(line)

            if match:
                fault_id = int(match.group(2))
                if search_fault_id == fault_id:
                    fault_name = match.group(1)
                    return fault_name

        return None


    def print_fdu_fault_param(self, search_fault_id, field):
        param = self.get_fdu_fault_param(search_fault_id, field)
        if param:
            print '%s:\t%s' % (field, param)

    def print_delay_param(self, search_fault_id, field):
        param = self.get_fdu_fault_param(search_fault_id, field)
        if param:
            print '%s:\t%s sec' % (field, int(param)/1000)

    def print_severity(self, search_fault_id):
        param = self.get_fdu_fault_param(search_fault_id, 'SEVERITY')
        if param:
            print 'SEVERITY:\t%s' % param
        else:
            print 'SEVERITY:\tout_of_order'

    def get_fdu_fault_param(self, search_fault_id, field):
        text = self.tree.findall("./FD_SECTION[@OWNER='fdu']/" + field)[0].text

        for match in self.entry_regex.finditer(text):
            entry = match.group(0)
            match = self.fdu_param_regex.match(entry)

            for fault_id in match.group(2).split(';'):
                if search_fault_id == int(fault_id.strip()):
                    fault_text = match.group(1)
                    return fault_text

        return None

    def get_alarm_text(self, search_fault_id):
        text = self.tree.findall("./FD_SECTION[@OWNER='fdar']/ALARMTEXT")[0].text

        for entry in text.splitlines():
            entry = entry.strip()
            if entry == "": continue

            paramMatch = self.fdar_param_regex.match(entry)
            if paramMatch :
                fault_id = int(paramMatch.group(1))
                if search_fault_id == fault_id:
                    alarm_text = paramMatch.group(2)
                    return alarm_text

        return None

    def print_alarm_text(self, search_fault_id):
        param = self.get_alarm_text(search_fault_id)
        if param:
            print 'ALARM_TEXT:\t%s' % param


# main
parser = RulesParser()
# print parser.get_fault_name(48)
search_fault_ids = [int(fault_id) for fault_id in sys.argv[1:]]
parser.print_fault_info(search_fault_ids)

