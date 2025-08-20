from playwright.sync_api import sync_playwright
from urllib.parse import unquote, urlparse
import re
import time
from plyer import notification

BASE = "https://praticas.futebolinterativo.com"
ESTADO_LINK_TEXT = "RJ"  
PORTUGUESA_IMG = "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/clubes%2Fportuguesarj.png"

URL_ANALISE = "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fan%C3%A1lise.jpg"

VAGAS_IMAGENS = [
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fcomunicacaoemkt.jpg",
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fan%C3%A1lise.jpg",
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fgestaoenegocios.jpg",
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/grohgpofzbof/b/arquivos-sistema/o/cards-areas%2Fsaudeeperformance.jpg"
]

def nome_area_por_img_src(src: str) -> str | None:
    try:
        path = urlparse(src).path
        fname = unquote(path.split("/")[-1])
        base = re.sub(r"\.jpg$|\.jpeg$|\.png$|\.webp$", "", fname, flags=re.I)
        return base
    except Exception:
        return None

def listar_vagas_portuguesa_rj():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=0)
        page = browser.new_page()
        page.set_default_timeout(20000)

        # 1) Home
        page.goto(BASE, wait_until="load")

        # 2) Clicar em "Clubes"
        page.wait_for_selector('a[href="#clubes"]')
        page.click('a[href="#clubes"]')

        # 3) Clicar no estado RJ
        page.get_by_role("link", name=ESTADO_LINK_TEXT, exact=True).click()

        # 4) Clicar na Portuguesa-RJ pela imagem
        sel_img = f'img[src="{PORTUGUESA_IMG}"]'
        page.wait_for_selector(sel_img)
        parceiro_img = page.locator(sel_img)
        parceiro_img.scroll_into_view_if_needed()
        parceiro_img.click()

        # 5) Rolar a página para baixo para carregar todas as vagas
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)  # espera carregar imagens

        # 6) Capturar as vagas
        vagas = []
        for img_url in VAGAS_IMAGENS:
            img_sel = f'img[src="{img_url}"]'
            try:
                page.wait_for_selector(img_sel, timeout=5000)
                vagas.append({
                    "area": nome_area_por_img_src(img_url),
                    "img_src": img_url
                })
            except:
                # imagem não carregou
                vagas.append({
                    "area": nome_area_por_img_src(img_url),
                    "img_src": None
                })

        # 7) Verifica se a vaga "Análise" está presente
        analise_presente = any(v["img_src"] == URL_ANALISE for v in vagas)

        # 8) Voltar
        browser.close()
        return vagas, analise_presente

if __name__ == "__main__":
    vagas, analise = listar_vagas_portuguesa_rj()
    print("=== Vagas encontradas (Portuguesa-RJ) ===")
    for v in vagas:
        print(f"- Área: {v['area']} | Imagem carregada: {'✅' if v['img_src'] else '❌'}")

    if analise:
        notification.notify(
            title="Vaga de Análise encontrada!",
            message="A vaga de Análise na Portuguesa-RJ está disponível! 🚀",
            timeout=10
        )
        print("\n✅ Vaga de Análise encontrada!")
    else:
        print("\n❌ Vaga de Análise não encontrada.")
