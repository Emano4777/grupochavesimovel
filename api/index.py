import os
from flask import Flask, render_template, request

# Pastas
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# =========================
# PÁGINA DE IMÓVEIS (/)
# =========================
MARCA_IMOVEIS = "Grupo Chaves Imóveis"
WHATSAPP_PHONE = "+5517981359872"
MENSAGEM_BASE_IMOVEIS = "Oi vi seu anuncio la no site sobre a casa a venda e tenho interesse"

IMOVEIS = [
    # UNIQUE
    {
        "id": "unique-felicita-terreo",
        "grupo": "Unique Felicità",
        "categoria": "venda",
        "titulo": "Apartamento • Unique Felicità (Térreo)",
        "preco": "R$ 240.000,00",
        "condominio": "R$ 350,00",
        "localizacao": "Região dos Dahmas, represa, mercado Oba, próximo ao Mc Donald e ao Carrefour.",
        "descricao_curta": "2 quartos (1 com ar), sala, cozinha com armário, banheiro, lavanderia e varanda.",
        "itens": [
            "Térreo","Sala","Cozinha c/ armário","Banheiro",
            "Dois quartos (um com ar condicionado)","Lavanderia","Varanda",
            "Vaga de garagem e visitantes","2 piscinas, 2 churrasqueiras, playground, bicicletário",
            "Quadra de basquete, petplace","3 elevadores, mercadinho Stok, segurança 24h",
        ],
        "imagens": [
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757164161/WhatsApp_Image_2025-09-06_at_09.16.29_gchysq.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757164162/WhatsApp_Image_2025-09-06_at_09.16.28_1_ipfhfv.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757164454/WhatsApp_Image_2025-09-06_at_09.16.25_3_oppwqd.jpg",
        ],
    },
    {
        "id": "unique-felicita-12andar",
        "grupo": "Unique Felicità",
        "categoria": "venda",
        "titulo": "Apartamento • Unique Felicità (12º Andar)",
        "preco": "R$ 275.000,00",
        "condominio": "R$ 350,00",
        "localizacao": "Região dos Dahmas, represa, mercado Oba, próximo ao Mc Donald e ao Carrefour.",
        "descricao_curta": "12º andar, 2 quartos, sala, cozinha com armário, banheiro, lavanderia e varanda.",
        "itens": [
            "12º Andar","Sala","Cozinha c/ armário","Banheiro",
            "Dois quartos","Lavanderia","Varanda","Vaga de garagem e visitantes",
            "2 piscinas, 2 churrasqueiras, playground, bicicletário",
            "Quadra de basquete, petplace","3 elevadores, mercadinho Stok, segurança 24h",
        ],
        "imagens": [
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757164162/WhatsApp_Image_2025-09-06_at_09.16.25_1_r27fmu.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757164162/WhatsApp_Image_2025-09-06_at_09.16.26_xsfhrh.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757164161/WhatsApp_Image_2025-09-06_at_09.16.24_zlcpe8.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757164161/WhatsApp_Image_2025-09-06_at_09.16.25_t8f5wz.jpg"
        ],
    },
    # FORA DO UNIQUE
    {
        "id": "rio-fiora-terreo-quintal",
        "grupo": "Rio Fiora (Rios di Itália)",
        "categoria": "aluguel",
        "titulo": "Apartamento Térreo c/ Quintal • Cond. Rio Fiora",
        "preco": "R$ 1.500,00 (aluguel – condomínio incluso)",
        "condominio": "Incluso",
        "localizacao": "Rua Patrícia Rodrigues Fontes, 605 – Próx. TV TEM, Compre Mix e Constroeste.",
        "descricao_curta": "2 quartos, sala c/ ar, cozinha e banheiro com planejados + área privativa (quintal).",
        "itens": [
            "02 Quartos","01 Banheiro c/ box e planejados","Sala c/ ar condicionado",
            "Cozinha c/ planejados","Área privativa (Quintal)","01 Vaga de garagem",
            "Lazer completo no condomínio","Piscina, Playground, Quadra poliesportiva",
            "Espaço gourmet, Câmeras","Portaria 24h, Acessibilidade",
        ],
        "imagens": [
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757536768/WhatsApp_Image_2025-09-06_at_11.07.43_k0bflf.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757536768/WhatsApp_Image_2025-09-06_at_11.07.43_1_yildfi.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757536768/WhatsApp_Image_2025-09-06_at_11.07.44_folbmy.jpg"
        ],
    },
    {
        "id": "casa-boa-vista-consolacao",
        "grupo": "Boa Vista",
        "categoria": "venda",
        "titulo": "Casa • Região do Boa Vista (Rua Consolação)",
        "preco": "R$ 540.000,00 (financiável)",
        "condominio": "—",
        "localizacao": "Próx. à Santa Casa e Menezes de Bezerra; mercados, escolas, farmácias e comércio.",
        "descricao_curta": "152 m² construídos • 270 m² terreno • 3 qtos (1 suíte), 3 banheiros e 2 vagas.",
        "itens": [
            "03 Quartos c/ uma suíte","03 Banheiros","Sala ampla","Cozinha ampla",
            "Área de lavanderia","02 Vagas de garagem","Jardim","Toda em Blindex",
            "Porcelanato interno e externo","Portão eletrônico","Cerca elétrica e câmeras de segurança",
        ],
        "imagens": [
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757537251/WhatsApp_Image_2025-09-10_at_15.24.24_1_eyopon.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757537245/WhatsApp_Image_2025-09-10_at_15.24.19_t6s0fi.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757537244/WhatsApp_Image_2025-09-10_at_15.24.21_1_wfbmfx.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757537244/WhatsApp_Image_2025-09-10_at_15.24.20_1_c5mxoo.jpg",
            "https://res.cloudinary.com/dizfq460q/image/upload/v1757537244/WhatsApp_Image_2025-09-10_at_15.24.21_2_g2i5ul.jpg"
        ],
    },
]

def filtrar_imoveis(itens, q="", cat=""):
    q = (q or "").strip().lower()
    cat = (cat or "").strip().lower()
    def casa_match(i):
        texto = " ".join([i["titulo"], i["localizacao"], i["descricao_curta"], " ".join(i["itens"])]).lower()
        ok_q = (q in texto) if q else True
        ok_cat = (i["categoria"] == cat) if cat in {"venda", "aluguel"} else True
        return ok_q and ok_cat
    return [i for i in itens if casa_match(i)]

@app.route("/")
def imoveis_home():
    wa_base = f"https://api.whatsapp.com/send?phone={WHATSAPP_PHONE}&text="
    grupos = sorted({i["grupo"] for i in IMOVEIS})
    total_imoveis = len(IMOVEIS)
    q = request.args.get("q", "")
    cat = request.args.get("cat", "")
    filtrados = filtrar_imoveis(IMOVEIS, q=q, cat=cat)
    total_venda = len([i for i in IMOVEIS if i["categoria"] == "venda"])
    total_aluguel = len([i for i in IMOVEIS if i["categoria"] == "aluguel"])
    return render_template(
        "index.html",
        marca=MARCA_IMOVEIS,
        imoveis=filtrados,
        wa_base=wa_base,
        mensagem_base=MENSAGEM_BASE_IMOVEIS,
        grupos=grupos,
        total_imoveis=total_imoveis,
        total_venda=total_venda,
        total_aluguel=total_aluguel,
        q=q,
        cat=cat,
    )

# =========================
# PÁGINA RECLAMEVOO (/voo)
# =========================
MARCA_VOO = "Grupo Chaves ReclameVoo"
MENSAGEM_BASE_VOO = "Oi! Vi o site do Grupo Chaves ReclameVoo e quero ajuda com meu voo"
# =========================
# WHATSAPP (USADO EM / E /voo)
# =========================
WHATSAPP_PHONE_RAW = "+5517981359872"  # como você gosta de guardar
WHATSAPP_PHONE_E164 = "".join(filter(str.isdigit, WHATSAPP_PHONE_RAW))  # -> 5517981359872

def build_wa_base():
    # usar o endpoint oficial; sem '+'
    return f"https://api.whatsapp.com/send?phone={WHATSAPP_PHONE_E164}&text="
HERO_IMAGENS = [
    "https://res.cloudinary.com/dizfq460q/image/upload/v1757540571/voo-cancelado_d4iaas.jpg",
    "https://res.cloudinary.com/dizfq460q/image/upload/v1757540589/images_upmmhm.jpg",
    "https://res.cloudinary.com/dizfq460q/image/upload/v1757540590/Bagagem-Danificada-1024x683_dntxp2.jpg"
]

DESTAQUES = [
    {"icon": "fa-plane-circle-exclamation", "title": "Direitos do passageiro", "text": "Cancelamento, atraso, overbooking e bagagem."},
    {"icon": "fa-scale-balanced", "title": "Sem custo inicial", "text": "Análise gratuita do seu caso."},
    {"icon": "fa-clock", "title": "Acompanhamento rápido", "text": "Tudo direto pelo WhatsApp."},
]

FAQ = [
    {"q": "Tenho direito a indenização?", "a": "Em regra, atraso acima de 4h, cancelamento, embarque negado e extravio geram direitos. Analisamos sem custo."},
    {"q": "Quanto posso receber?", "a": "Varia conforme danos materiais/morais e provas. Estimamos depois da análise."},
    {"q": "Quanto tempo leva?", "a": "Podemos tentar acordo rápido; em ação judicial, prazos variam por comarca."},
    {"q": "Precisa pagar antes?", "a": "Não. Trabalhamos por êxito: só há honorários se você receber."}
]

@app.route("/voo")
def voo():
    wa_base = build_wa_base()
    return render_template(
        "voo.html",
        marca=MARCA_VOO,
        wa_base=wa_base,
        mensagem_base=MENSAGEM_BASE_VOO,
        hero_imagens=HERO_IMAGENS,
        destaques=DESTAQUES,
        faq=FAQ
    )

if __name__ == "__main__":
    app.run(debug=True)
