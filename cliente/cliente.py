import time
import requests

def sincronizar_relogio(servidor_ip):
    def timeMsg(novoTempo, tempoAtual, ajuste):
        msg = (
            f"Tempo atual: {tempoAtual}\n"
            f"Tempo do servidor: {tServer}\n"
            f"Delay calculado: {delay}\n"
            f"Ajuste aplicado: {ajuste}\n"
            f"Novo tempo: {novoTempo}\n"
            "-" * 40
        )
        print(msg, flush=True)

    while True:
        try:
            T1 = time.time()
            resposta = requests.get(f"http://{servidor_ip}:5000/tempo")
            dados = resposta.json()
            tServer = dados["T_server"]
            T2 = dados["T2"]
            T3 = time.time()

            delay = ((T3 - T1) - (T2 - tServer)) / 2

            tempoAtual = time.time()


            ajuste = (tServer + delay - tempoAtual) * 0.1
            novoTempo = tempoAtual + ajuste

            timeMsg(novoTempo, tempoAtual, ajuste)

        except Exception as e:
            print(f"Erro ao sincronizar: {e}", flush=True)

        time.sleep(5)

if __name__ == '__main__':
    servidor_ip = "servidor"
    sincronizar_relogio(servidor_ip)