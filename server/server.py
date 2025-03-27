import socket
from datetime import datetime, timezone
import struct
import time

class NTPServer:
    def __init__(self, host='0.0.0.0', port=123):
        self.host = host
        self.port = port
        
    def healthcheck(self):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            test_socket.settimeout(1)
            test_socket.sendto(b'', ('localhost', 123))
            return True
        except:
            return False
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.host, self.port))
            print(f"🛠️ Servidor NTP iniciado em {self.host}:{self.port}", flush=True)
            
            while True:
                try:
                    data, address = s.recvfrom(1024)
                    if len(data) < 48:
                        continue
                        
                    # Constroi pacote de resposta NTP (RFC 5905)
                    packet = bytearray(48)
                    packet[0] = 0x1C  # LI=0, VN=3, Mode=4 (server)
                    
                    # Timestamps NTP (em segundos desde 1900)
                    ntp_time = time.time() + 2208988800  # Conversão para NTP epoch
                    integer_part = int(ntp_time)
                    fractional_part = int((ntp_time - integer_part) * 0xFFFFFFFF)
                    
                    # Preenche os campos do pacote NTP
                    struct.pack_into('!I', packet, 40, integer_part)  # Transmit Timestamp
                    struct.pack_into('!I', packet, 44, fractional_part)
                    
                    s.sendto(packet, address)
                    
                except Exception as e:
                    print(f"Erro: {str(e)}", flush=True)

if __name__ == "__main__":
    server = NTPServer()
    server.start()