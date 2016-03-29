
import socket

def check_catapult_status(ip_address="10.68.152.157", port="5000", command="ALV"):
    """This keyword will check Catapult's status, check whether need to restart.

    | Input Parameters | Man. | Description |
    |    ip_address    |  No  | IP Address of Catapult |
    |       port       |  No  | Control Port of Catapult |
    |     command      |  No  | Command to be executed |

    Example
    | Check Catapult Status | 10.68.152.157 | 5000 | ALV |
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ret = sock.sendto(command, (ip_address, int(port)))
    except:
        raise Exception, 'socket open failed'

    try:
        sock.settimeout(2)
        data, server = sock.recvfrom(255)
        if data:
            # received data: ALK
            if data == "ALK":
                return True
        else:
            print 'no any data received'
    except:
        print 'no any data received'
    finally:
        sock.close()

    return False


if __name__ == "__main__":
    pass

