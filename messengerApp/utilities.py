import socket


class Utilities(object):
    @staticmethod
    def get_local_ip():
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Connect to a remote server (doesn't need to be reachable)
            s.connect(('8.8.8.8', 80))

            # Get the local IP address assigned by the router
            local_ip = s.getsockname()[0]
        except Exception as e:
            print("[Error] ", e)
            local_ip = None
        finally:
            # Close the socket
            s.close()

        return local_ip
