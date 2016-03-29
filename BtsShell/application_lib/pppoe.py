from BtsShell import connections

def start_pppoe_connection(connection_name):
    """This keyword opens PPPoE connection.

    | Input Parameters | Man. | Description |
    | connection_name  | Yes  | PPPoE connection name |

    Example
    | Start PPPoE Connection | Connection to tm500_lte_192.168.255.110_0_0 at TM500_AC_192.168.255.110 |
    """
    
    ret = connections.execute_shell_command_without_check('rasdial "%s" tm500 tm500' % connection_name)
    if ret.find('Command completed successfully') < 0:
        raise Exception, "Open PPPoE connection '%s' failed" % connection_name

def stop_pppoe_connection(connection_name):
    """This keyword disconnects PPPoE connection.

    | Input Parameters | Man. | Description |
    | connection_name  | Yes  | PPPoE connection name |

    Example
    | Stop PPPoE Connection | Connection to tm500_lte_192.168.255.110_0_0 at TM500_AC_192.168.255.110 |
    """
    
    connections.execute_shell_command('rasdial "%s" /DISCONNECT' % connection_name)