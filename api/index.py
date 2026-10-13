import os
import unicodedata
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
WHATSAPP_EXIBICAO = "(17) 98135-9872"
MENSAGEM_BASE_IMOVEIS = "Olá! Vi o anúncio no site do Grupo Chaves Imóveis e tenho interesse"


def fotos(slug, total):
    """Fotos tratadas (com marca d'água) em static/imoveis/<slug>/01.jpg ... NN.jpg"""
    return [f"/static/imoveis/{slug}/{i:02d}.jpg" for i in range(1, total + 1)]


IMOVEIS = [
    {
        "id": "casa-boa-vista",
        "tipo": "casa",
        "valor": 540000,
        "grupo": "Boa Vista",
        "categoria": "venda",
        "titulo": "Casa no Boa Vista",
        "preco": "R$ 540.000,00",
        "obs_preco": "Aceita troca",
        "condominio": "—",
        "localizacao": "Próximo ao Hospital Santa Casa, Bezerra de Menezes, padarias, mercados, farmácias, escolas, posto de saúde e restaurantes.",
        "descricao_curta": "270 m² de terreno • 152 m² construídos • 3 quartos (1 suíte), 3 banheiros, área gourmet e garagem para 2 carros.",
        "destaques": ["270 m² terreno", "152 m² construídos", "3 quartos", "2 vagas"],
        "itens": [
            "Sala", "Cozinha", "Três banheiros", "Três quartos, sendo uma suíte",
            "Lavanderia", "Vaga de garagem para dois carros", "Área gourmet", "Churrasqueira",
            "Todo em porcelanato e pedra São Gabriel", "Cerca elétrica", "Portão eletrônico",
        ],
        "imagens": fotos("casa-boa-vista", 19),
    },
    {
        "id": "chacara-rio-preto",
        "tipo": "chacara",
        "valor": 630000,
        "grupo": "Chácara",
        "categoria": "venda",
        "titulo": "Chácara entre Rio Preto e Engenheiro Schmidt",
        "preco": "R$ 630.000,00",
        "obs_preco": "",
        "condominio": "—",
        "localizacao": "Entre São José do Rio Preto e Engenheiro Schmidt.",
        "descricao_curta": "Terreno de 1.000 m² com piscina, varanda ampla com churrasqueira e fogão a lenha, pomar e segurança completa.",
        "destaques": ["1.000 m² terreno", "2 dormitórios", "Piscina", "8 câmeras"],
        "itens": [
            "Casa com 2 dormitórios, sendo 1 suíte com banheira",
            "Sacada e armários embutidos", "2 banheiros, sala e cozinha",
            "Varanda ampla com churrasqueira e fogão a lenha",
            "Mesa de jantar grande de madeira", "Varanda dos fundos com mesa de sinuca",
            "Piscina", "Janelas e portas todas de madeira",
            "Pomar grande com diversos pés de frutas e flores",
            "2 galinheiros e 2 quartinhos de despensa",
            "Toda cercada, portão eletrônico, muros altos e cerca elétrica",
            "Sistema com 8 câmeras de vigilância",
        ],
        "imagens": fotos("chacara-rio-preto", 26),
    },
    {
        "id": "unique-felicita-9andar",
        "tipo": "apartamento",
        "valor": 300000,
        "grupo": "Unique Felicità",
        "categoria": "venda",
        "titulo": "Apartamento no Unique Felicità • 9º andar",
        "preco": "R$ 300.000,00",
        "obs_preco": "",
        "condominio": "—",
        "localizacao": "Região dos Dahmas, represa, mercado Oba, próximo ao Mc Donald e ao Carrefour.",
        "descricao_curta": "9º andar com vista para a represa • 2 quartos, cozinha e banheiro com planejados, varanda e lazer completo.",
        "destaques": ["9º andar", "2 quartos", "1 vaga", "Lazer completo"],
        "itens": [
            "9º andar", "Sala", "Cozinha com planejados", "Banheiro com planejados",
            "Dois quartos", "Lavanderia", "Varanda", "Vaga de garagem e vaga de visitantes",
            "Piscinas, churrasqueiras e playground", "Bicicletário, quadra de basquete e petplace",
            "Três elevadores e mercadinho Stok", "Segurança 24h",
        ],
        "imagens": fotos("unique-felicita-9andar", 27),
    },
]

TIPOS = {"casa": "Casa", "chacara": "Chácara", "apartamento": "Apartamento"}
FAIXAS_PRECO = [  # (valor máximo, rótulo)
    (350000, "Até R$ 350 mil"),
    (600000, "Até R$ 600 mil"),
    (1000000, "Até R$ 1 milhão"),
]


def sem_acento(txt):
    return "".join(c for c in unicodedata.normalize("NFD", txt.lower()) if unicodedata.category(c) != "Mn")


def filtrar_imoveis(itens, q="", cat="", tipo="", preco_max=""):
    q = sem_acento((q or "").strip())
    cat = (cat or "").strip().lower()
    tipo = (tipo or "").strip().lower()
    try:
        preco_max = int(preco_max)
    except (TypeError, ValueError):
        preco_max = 0

    def casa_match(i):
        texto = sem_acento(" ".join([i["titulo"], i["grupo"], i["localizacao"], i["descricao_curta"], " ".join(i["itens"])]))
        ok_q = (q in texto) if q else True
        ok_cat = (i["categoria"] == cat) if cat in {"venda", "aluguel"} else True
        ok_tipo = (i["tipo"] == tipo) if tipo in TIPOS else True
        ok_preco = (i["valor"] <= preco_max) if preco_max else True
        return ok_q and ok_cat and ok_tipo and ok_preco
    return [i for i in itens if casa_match(i)]


@app.route("/")
def imoveis_home():
    wa_base = f"https://api.whatsapp.com/send?phone={WHATSAPP_PHONE}&text="
    filtros = {k: request.args.get(k, "") for k in ("q", "cat", "tipo", "preco_max")}
    filtrados = filtrar_imoveis(IMOVEIS, **filtros)
    total_venda = len([i for i in IMOVEIS if i["categoria"] == "venda"])
    total_aluguel = len([i for i in IMOVEIS if i["categoria"] == "aluguel"])
    # só oferece no buscador os tipos que existem no catálogo
    tipos_disponiveis = [(k, v, sum(1 for i in IMOVEIS if i["tipo"] == k)) for k, v in TIPOS.items()]
    tipos_disponiveis = [t for t in tipos_disponiveis if t[2]]
    return render_template(
        "index.html",
        marca=MARCA_IMOVEIS,
        whatsapp_exibicao=WHATSAPP_EXIBICAO,
        imoveis=filtrados,
        wa_base=wa_base,
        mensagem_base=MENSAGEM_BASE_IMOVEIS,
        total_imoveis=len(IMOVEIS),
        total_venda=total_venda,
        total_aluguel=total_aluguel,
        tipos=tipos_disponiveis,
        tipos_nomes=TIPOS,
        faixas=FAIXAS_PRECO,
        filtros=filtros,
        filtrando=any(filtros.values()),
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
