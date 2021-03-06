import os
import inspect


this_file_path = inspect.getfile(inspect.currentframe())
resource_path = os.path.dirname(this_file_path)
bts_log_path = os.path.join(resource_path, "tools", "BTSlog", "btslog.exe")
qtp_path = os.path.join(os.path.dirname(os.path.dirname(resource_path)), 'QTP')

_G_DICT = {'RL15': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'Nemuadmin',
                    'FTM_PASSWORD': 'nemuuser',
                    'FTM_CONFIG_FILE_DIR': '/usr/local/etc/config',
                    'RRU_1': '192.168.255.69',
                    'RRU_2': '192.168.255.71',
                    'RRU_3': '192.168.255.73',
                    'RRU_USERNAME': 'root',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCF',
                    'COUNTER_REFRESH_PERIOD': '15',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL15',
                   },
           'RL25': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.16',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.254.129',
                    'RRU_2': '192.168.254.137',
                    'RRU_3': '192.168.254.141',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL25',
                   },
           'RL25_SPRINT': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.16',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.254.129',
                    'RRU_2': '192.168.254.137',
                    'RRU_3': '192.168.254.141',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL25_SPRINT',
                   },
           'RL35': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.253.196',
                    'RRU_2': '192.168.253.204',
                    'RRU_3': '192.168.253.212',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL35',
                   },
           'RL35_CMCC': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.254.129',
                    'RRU_2': '192.168.254.137',
                    'RRU_3': '192.168.254.141',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL35_CMCC',
                   },
           'RL45': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.254.129',
                    'RRU_2': '192.168.254.137',
                    'RRU_3': '192.168.254.141',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL45',
                   },
           'RL45_IR': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.254.129',
                    'RRU_2': '192.168.254.137',
                    'RRU_3': '192.168.254.141',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL45',
                   },
           'RL45_FSIH': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.254.129',
                    'RRU_2': '192.168.254.137',
                    'RRU_3': '192.168.254.141',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTF:~ >',
                    'GUI_LIB_BASE'   : 'RL45',
                   },
           'RL55_FSIH': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.254.129',
                    'RRU_2': '192.168.254.137',
                    'RRU_3': '192.168.254.141',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTF:~ >',
                    'GUI_LIB_BASE'   : 'RL55',
                   },
           'RL55': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.253.196',
                    'RRU_2': '192.168.253.204',
                    'RRU_3': '192.168.253.212',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL55',
                   } ,

           'RL65': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.253.196',
                    'RRU_2': '192.168.253.204',
                    'RRU_3': '192.168.253.212',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL55',
                   },

           'RL65_FSIH': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.253.196',
                    'RRU_2': '192.168.253.204',
                    'RRU_3': '192.168.253.212',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL55',
                   },

           'TL16A': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.253.196',
                    'RRU_2': '192.168.253.204',
                    'RRU_3': '192.168.253.212',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL55',
                   },

           'TL16A_FSIH': {'FCMD_USERNAME': 'toor4nsn',
                    'FCMD_PASSWORD': 'oZPS0POrRieRtu',
                    'BTS_FTM':'192.168.255.129',
                    'FTM_USERNAME': 'toor4nsn',
                    'FTM_PASSWORD': 'oZPS0POrRieRtu',
                    'FTM_CONFIG_FILE_DIR': '/flash/trs_data/db',
                    'RRU_1': '192.168.253.196',
                    'RRU_2': '192.168.253.204',
                    'RRU_3': '192.168.253.212',
                    'RRU_USERNAME': '',
                    'RRU_PASSWORD': '',
                    'RRU_TELNET_PORT': '2323',
                    'SCF_FILE_NAME': 'SCFC',
                    'COUNTER_REFRESH_PERIOD': '60',
                    'FCMD_PROMPT':'root@FCTB:~ >',
                    'GUI_LIB_BASE'   : 'RL55',
                   },


          }

def get_variables(sw_release):
    static_variables = {'BTSSHELL_RESOURCES_DIR': os.path.dirname(os.path.abspath(__file__)),
                        'BTSLOG_EXE_DIR': bts_log_path,
                        'BTSLOG_DIR': 'd:\\temp\\BTSlogs\\',
                        'BTS_FILEDIRECTORY_DIR': '/flash',
                        'ONAIR_CHECK':['PBCH', 'now OnAir'],
                        }

    _R_DICT = _G_DICT[sw_release]
    dynamic_variables = {'SW_RELEASE':    sw_release,
                         'netact_test_path' : os.path.join(qtp_path, _R_DICT['GUI_LIB_BASE'], "QTPScripts95_TDD_Prod","NetAct",""),
                         'siteman_test_path': os.path.join(qtp_path, _R_DICT['GUI_LIB_BASE'],"QTPScripts95_TDD_Prod","SiteMan",""),
                         'applicationlauncher_test_path': os.path.join(qtp_path, _R_DICT['GUI_LIB_BASE'],"QTPScripts95_TDD_Prod","ApplicationLauncher",""),
                         'audittrail_test_path': os.path.join(qtp_path, _R_DICT['GUI_LIB_BASE'],"QTPScripts95_TDD_Prod","AuditTrail",""),
                         'sitebrowser_test_path': os.path.join(qtp_path, _R_DICT['GUI_LIB_BASE'],"QTPScripts95_TDD_Prod","SiteBrowser",""),
                         'ftm_test_path': os.path.join(qtp_path, _R_DICT['GUI_LIB_BASE'],"QTPScripts95_TDD_Prod","FTM",""),
                         }
    dynamic_variables.update(_R_DICT)
    variables = {}
    variables.update(static_variables)
    variables.update(dynamic_variables)

    return variables

