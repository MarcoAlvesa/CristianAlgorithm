import socket
import time
from datetime import datetime, timedelta, timezone
import os
import struct

class NTPClock:
    def __init__(self, initial_drift_hours):
        self.drift = timedelta(hours=initial_drift_hours)
        self.adjustment_rate = 0.05  # 5% de ajuste por ciclo
        self.sync_count = 0

    def get_current_time(self):
        return datetime.now(timezone.utc) + self.drift

    def sync_with_ntp(self, server_host):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(3.0)
                
                # Registra tempo antes do ajuste
                before_adjustment = self.get_current_time()
                
                # Constroi pacote NTP (RFC 5905)
                packet = bytearray(48)
                packet[0] = 0x1B
                
                # Envia requisição
                T0 = datetime.now(timezone.utc)
                s.sendto(packet, (server_host, 123))
                
                # Recebe resposta
                data, _ = s.recvfrom(1024)
                T3 = datetime.now(timezone.utc)
                
                if len(data) < 48:
                    raise ValueError("Pacote NTP inválido")
                
                # Extrai timestamp de transmissão do servidor (T2)
                integer_part = struct.unpack('!I', data[40:44])[0]
                fractional_part = struct.unpack('!I', data[44:48])[0]
                T2 = (integer_part - 2208988800) + (fractional_part / 0xFFFFFFFF)
                T2 = datetime.fromtimestamp(T2, timezone.utc)
                
                # Cálculo do atraso e ajuste
                propagation_delay = (T3 - T0) / 2
                server_time = T2 + propagation_delay
                adjustment_needed = server_time - self.get_current_time()
                
                # Ajuste gradual
                actual_adjustment = adjustment_needed * self.adjustment_rate
                self.drift += actual_adjustment
                self.sync_count += 1
                
                print(f"\nSincronização NTP #{self.sync_count}")
                print(f"Hora do Servidor: {server_time.strftime('%H:%M:%S.%f')[:-3]}")
                print(f"Antes: {before_adjustment.strftime('%H:%M:%S.%f')[:-3]}")
                print(f"Depois: {self.get_current_time().strftime('%H:%M:%S.%f')[:-3]}")
                return True
                
        except Exception as e:
            print(f"Erro NTP: {str(e)}")
            return False

def main():
    initial_drift = int(os.getenv('INITIAL_DRIFT_HOURS', 0))
    clock = NTPClock(initial_drift)
    
    print(f"\nCliente NTP iniciado com drift inicial: {initial_drift}h")
    print(f"Container: {os.getenv('HOSTNAME', 'desconhecido')}")
    print(f"Taxa de ajuste: {clock.adjustment_rate*100}% por ciclo\n")
    
    while True:
        if clock.sync_with_ntp("time-server"):
            time.sleep(10)
        else:
            time.sleep(5)

if __name__ == "__main__":
    main()