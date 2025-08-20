from playwright.sync_api import sync_playwright
from urllib.parse import unquote, urlparse
import re
import time
from datetime import datetime
import csv
from plyer import notification

# ---------------------------
# Configurações
# ---------------------------
# Lista de clubes com link direto
CLUBES = [
    {"nome": "Portuguesa-RJ", "link": "https://praticas.futebolinterativo.com/parceiro/12"},
    {"nome": "Madureira", "link": "https://praticas.futebolinterativo.com/parceiro/93"},
    {"nome": "Volta Redonda", "link": "https://praticas.futebolinterativo.com/parceiro/56"},
]

# URLs das vagas (imagens)
VAGAS_IMAGENS = [
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fcomunicacaoemkt.jpg",
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fan%C3%A1lise.jpg",
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fgestaoenegocios.jpg",
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fsaudeeperformance.jpg",
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Ftecnicaetatica.jpg"
]

# Link exato da vaga de Análise
URL_ANALISE = "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fan%C3%A1lise.jpg"

#Mapeamento de nomes corretos das vagas
VAGAS_MAP = {
    "comunicacaoemkt.jpg": "Comunicação e Marketing",
    "análise.jpg": "Análise",
    "gestaoenegocios.jpg": "Gestão e Negócios",
    "saudeeperformance.jpg": "Saúde e Performance",
    "tecnicaetatica.jpg":"Tecnica e tatica"
}

# ---------------------------
# Funções auxiliares
# ---------------------------
def nome_vaga_correta(img_src: str) -> str:
    #retorna o nome correto da vaga a partir do URL da imagem
    try:
        nome_arquivo = img_src.split("/")[-1]
        return VAGAS_MAP.get(nome_arquivo,nome_arquivo)
    except:
        return "Desconhecida"

# ---------------------------
# funçao salvar historico
# ---------------------------
def salvar_historico(clube_nome,vagas):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("historico_vagas.csv", mode='a',newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for v in vagas:
            status = "✅" if v["img_src"] else "❌"
            nome_correto = nome_vaga_correta(v["img_src"] or "")
            writer.writerow([data_hora, clube_nome, nome_correto, status])



# ---------------------------    
# Função principal
# ---------------------------
def buscar_vagas():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # roda em background
        page = browser.new_page()
        page.set_default_timeout(20000)

        for clube in CLUBES:
            print(f"\nBuscando vagas no {clube['nome']}...")
            try:
                # Abrir link direto do clube
                page.goto(clube["link"], wait_until="load")
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  # rolar página
                time.sleep(2)

                # Capturar vagas
                vagas = []
                for img_url in VAGAS_IMAGENS:
                    nome_final = img_url.split("/")[-1]
                    img_sel = f'img[src*="{nome_final}"]'  # procura pelo final do URL
                    try:
                        page.wait_for_selector(img_sel, timeout=800)
                        vagas.append({"area": nome_vaga_correta(img_url), "img_src": img_url})
                    except:
                        vagas.append({"area": nome_vaga_correta(img_url), "img_src": None})
                    
                # Mostrar todas as vagas
                print("Vagas disponíveis:")
                for v in vagas:
                    status = "✅" if v["img_src"] else "❌"
                    print(f"- {v['area']}: {status}")

                #salvar historico
                salvar_historico(clube["nome"], vagas)

                # Verifica vaga de Análise
                analise_presente = any(v["img_src"] == URL_ANALISE for v in vagas)

                # Notificação se encontrar
                if analise_presente:
                    notification.notify(
                        title=f"Vaga de Análise encontrada! ({clube['nome']})",
                        message=f"A vaga de Análise no {clube['nome']} está disponível! 🚀",
                        timeout=10
                    )
                    print(f"✅ Vaga de Análise encontrada no {clube['nome']}!")
                else:
                    print(f"❌ Vaga de Análise não encontrada no {clube['nome']}.")

            except Exception as e:
                print(f"❌ Erro ao acessar o clube {clube['nome']}: {e}")

        browser.close()

# ---------------------------
# Execução
# ---------------------------
if __name__ == "__main__":
    buscar_vagas()
