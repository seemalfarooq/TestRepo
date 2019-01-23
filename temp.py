import unittest
from lib import constants as const
from lib.config import BaseConfig
from lib import utility
import re
import util
from lib import framework as fw
from lib.appliance import access
from lib.appliance import search_emails as se
import pprint

__author__ = 'seemal.farooq'


class Enums(object):
    emps_name = 'EMPS'
    test_sample = utility.download_file_from_controller('FileSize')


class TestFileSize(unittest.TestCase, fw.BrowserTests):
    host = None
    c_time = None
    sender = None
    recipient = None
    pether3 = None
    clear = ['logging local info', 'logging files rotation force']
    copy_logs = ['rm -rf test_logs', 'mkdir test_logs', 'cp /var/log/messages /var/home/root/test_logs/']
    get_sub_id = "select id from analyses.submission_done where sha256='48d8d138aace9b291c116c63b590224492074d153915fa1c3d282c798f194c30' and file_type=0 order by id desc;"
    get_status_code = "select status_code from malware_analyses where original_name='FileSize' and sha256='48d8d138aace9b291c116c63b590224492074d153915fa1c3d282c798f194c30' order by id desc;"
    get_error_code = "select error_code from analyses.submission_done where sha256='48d8d138aace9b291c116c63b590224492074d153915fa1c3d282c798f194c30' and file_type=0 order by id desc;"

    @classmethod
    def setUpClass(cls):
        cls.timeout = 30
        cls.wait_for_email = 60
        mail = utility.get_email_details()

        cls.refresh_interval = 5

        super(TestFileSize, cls).setUpClass()
        cls.config = BaseConfig()
        cls.pether3 = cls.config.pether3
        cls.host = cls.config.host
        utility.remove_ssh_keys(cls.host)

        cls.init_browser()
        access.login2(cls.browser)

        cls.chan, cls.client = utility.connect(cls.host, 22, const.LMS_USERNAME, const.LMS_PASSWORD)
        utility.execute(cls.chan, 'en')
        utility.execute(cls.chan, '_shell', '#')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        utility.disconnect(cls.chan, cls.client)
        access.logout(cls.browser)
        cls.browser.quit()
        super(TestFileSize, cls).tearDownClass()


    @classmethod
    def exec_conf_cmd(cls, cmd, user=None, password=None):
        if user is None:
            user = const.LMS_USERNAME
        if password is None:
            password = const.LMS_PASSWORD

        res = utility.execute_lst_cmds_conf_t(cls.host, cmd, user, password, 22)
        return res

    def execute_cmds_shell(self, cmds):
        out = utility.execute_lst_cmds_shell(
            self.host, 22, const.LMS_USERNAME, const.LMS_PASSWORD, cmds
        )
        utility.log_info(pprint.pformat(zip(cmds, out)))
        return out




    def test_cli_configuration(self):
        check_def = ['show analysis config']
        cmd_run = self.exec_conf_cmd(check_def)
        verify = {}
        regex = ['Max overall file size\s+: 5',
                'Max DA file size\s+: 32']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

    def test_cli_configuration_less_than_default(self):
        change = ['analysis file max-size 3','analysis file max-size da 2','show analysis config']
        cmd_run = self.exec_conf_cmd(change)
        verify = {}
        regex = ['Max overall file size\s+: 3',
                'Max DA file size\s+: 2']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

    def test_max_limit(self):
        change = ['analysis file max-size 1024','analysis file max-size da 100','show analysis config']
        cmd_run = self.exec_conf_cmd(change)
        verify = {}
        regex = ['Max overall file size\s+: 1024',
                'Max DA file size\s+: 100']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

    def test_invalid_max_filesize(self):
        change = ['analysis file max-size 1025']
        cmd_run = self.exec_conf_cmd(change)
        verify = {}
        regex = ['% Bad value "1025".  Value must be between 1 and 1024']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

    def test_invalid_max_filesize_da(self):
        change = ['analysis file max-size da 101']
        cmd_run = self.exec_conf_cmd(change)
        verify = {}
        regex = ['% Bad value "101".  Value must be between 1 and 100']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))


        change_to_def = ['analysis file max-size 5','analysis file max-size da 32','show analysis config']
        cmd_run = self.exec_conf_cmd(change_to_def)
        verify = {}
        regex = ['Max overall file size\s+: 5',
                'Max DA file size\s+: 32']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

    def file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verification
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"def file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verification
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"

        error_code = utility.execute_sql(self.chan, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verificationdef file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verificationdef file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)def file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verification
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"

        error_code = utility.execute_sql(self.chan, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verification
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verification
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"

        error_code = utility.execute_sql(self.chan, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verification
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"

        error_code = utility.execute_sql(self.chdef file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verification
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"

        error_code = utility.execute_sql(self.chan, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verification
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))an, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}def file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verification
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"

        error_code = utility.execute_sql(self.chan, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [def file_size_greater_than_overall_max_file_size(self):
        utility.email_analysis_delete_all(self.host)
        self.exec_conf_cmd(self.clear)
        change = ['analysis file max-size 2','analysis file max-size da 1']
        self.exec_conf_cmd(change)
        mail = utility.get_email_details()
        util.send_email(
            mail.subject, mail.body,
            mail.sender, mail.recipient,
            Enums.test_sample,
            host=self.host, mta_ip=self.pether3
        )
        #self.wait(5)
        self.execute_cmds_shell(self.copy_logs)

        # CLI Verification
        sub_id = utility.execute_sql(self.chan, self.get_sub_id)
        st = sub_id[0]['id']

        cli_status= ['show submission id ' + st]
        cmd_run = self.exec_conf_cmd(cli_status)
        verify = {}
        regex = ['Status\s+: file_too_large', 'md5sum\s+: 6a71416cd84147f7297b75b5a200580b']
        for r in regex:
            verify[r] = bool(re.search(r, cmd_run[-1]))

        utility.log_info('{}'.format(verify))
        self.assertTrue(all(verify.values()))

        # DB Verification
        status_code = utility.execute_sql(self.chan, self.get_status_code)
        st = status_code[0]['status_code']
        self.assertTrue(st=='14')
        print "status_code verified"

        error_code = utility.execute_sql(self.chan, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verification
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verification
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verification
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))

        error_code = utility.execute_sql(self.chan, self.get_error_code)
        #print "error_code", error_code
        st = error_code[0]['error_code']
        self.assertTrue(st=='46')
        print "error_code verified"

        # Log Verification
        log_test1 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Email/Malware Done: total url: 0 total attach: 1 is_malicious: 0, error_code 46" >> /var/home/root/test_logs/temp1.txt',
        'cat /var/home/root/test_logs/temp1.txt']

        res = self.execute_cmds_shell(log_test1)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        log_test2 = [
        'cat /var/home/root/test_logs/messages | '
        'grep -i "Analysis incomplete for one or more objects. Error: FILE_TOO_LARGE" >> /var/home/root/test_logs/temp2.txt',
        'cat /var/home/root/test_logs/temp2.txt']

        res = self.execute_cmds_shell(log_test2)
        ve = {}
        for v in res:
            ve[v] = v in res[-1]
        utility.log_info('{}'.format(ve))
        self.assertTrue(all(ve.values()))

        # UI Verification
        se.navigate(self.browser)
        se.wait_for_email(self.browser, mail.sender)
        se_data = se.get_table_data_search_emails(self.browser)
        self.assertIn('Scan Incomplete', str(se_data))