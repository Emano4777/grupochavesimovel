import os
import json
import unicodedata
from datetime import date
from flask import Flask, render_template, request, abort, Response

# Pastas
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# =========================
# PÁGINA DE IMÓVEIS (/)
# =========================
MARCA_IMOVEIS = "Grupo Chaves Imóveis"
SITE_URL = "https://www.grupochavesbrasil.com.br"
CIDADE = "São José do Rio Preto"
WHATSAPP_PHONE = "+5517981359872"
WHATSAPP_EXIBICAO = "(17) 98135-9872"
CRECI = "331483-F"
MENSAGEM_BASE_IMOVEIS = "Olá! Vi o anúncio no site do Grupo Chaves Imóveis e tenho interesse"
ATUALIZADO_EM = "2026-10-21"  # data de atualização dos anúncios (sitemap)

# IDs de rastreamento: configurar nas variáveis de ambiente do Vercel quando as contas existirem.
RASTREIO = {
    "ga4_id": os.environ.get("GA4_ID", ""),                          # Google Analytics 4 (G-XXXXXXX)
    "google_ads_id": os.environ.get("GOOGLE_ADS_ID", ""),            # Google Ads (AW-XXXXXXXXX)
    "google_ads_conv": os.environ.get("GOOGLE_ADS_CONV_LABEL", ""),  # rótulo da conversão "clique no WhatsApp"
    "meta_pixel_id": os.environ.get("META_PIXEL_ID", ""),            # Pixel da Meta (Facebook/Instagram)
    "google_verificacao": os.environ.get("GOOGLE_SITE_VERIFICATION", "").strip("﻿ \t\r\n"),  # Search Console (meta tag)
}


def fotos(slug, total):
    """Fotos tratadas (com marca d'água) em static/imoveis/<slug>/01.jpg ... NN.jpg"""
    return [f"/static/imoveis/{slug}/{i:02d}.jpg" for i in range(1, total + 1)]


IMOVEIS = [
    {
        "id": "casa-boa-vista",
        "tipo": "casa",
        "valor": 540000,
        "grupo": "Boa Vista",
        "bairro": "Boa Vista",
        "categoria": "venda",
        "titulo": "Casa no Boa Vista",
        "seo_titulo": "Casa à venda no Boa Vista, São José do Rio Preto – 3 quartos, R$ 540 mil",
        "seo_descricao": "Casa à venda no bairro Boa Vista em São José do Rio Preto, perto da Santa Casa: 270 m² de terreno, 152 m² construídos, 3 quartos (1 suíte) e área gourmet. R$ 540 mil, aceita troca e financiamento.",
        "preco": "R$ 540.000,00",
        "obs_preco": "Aceita troca e financiamento",
        "condominio": "—",
        "localizacao": "Próximo ao Hospital Santa Casa, Bezerra de Menezes, padarias, mercados, farmácias, escolas, posto de saúde e restaurantes.",
        "descricao_curta": "270 m² de terreno • 152 m² construídos • 3 quartos (1 suíte), 3 banheiros, área gourmet e garagem para 2 carros.",
        "destaques": ["270 m² terreno", "152 m² construídos", "3 quartos", "2 vagas"],
        "quartos": 3, "banheiros": 3, "area_m2": 152, "terreno_m2": 270,
        "itens": [
            "Sala", "Cozinha", "Três banheiros", "Três quartos, sendo uma suíte",
            "Lavanderia", "Vaga de garagem para dois carros", "Área gourmet", "Churrasqueira",
            "Todo em porcelanato e pedra São Gabriel", "Cerca elétrica", "Portão eletrônico",
            "Aceita financiamento e troca",
        ],
        "imagens": fotos("casa-boa-vista", 19),
    },
    {
        "id": "chacara-rio-preto",
        "tipo": "chacara",
        "valor": 630000,
        "grupo": "Chácara",
        "bairro": "Engenheiro Schmidt",
        "categoria": "venda",
        "titulo": "Chácara entre Rio Preto e Engenheiro Schmidt",
        "seo_titulo": "Chácara à venda em Rio Preto / Engenheiro Schmidt – 1.000 m² com piscina, R$ 630 mil",
        "seo_descricao": "Chácara à venda entre São José do Rio Preto e Engenheiro Schmidt: 1.000 m², piscina, varanda com churrasqueira e fogão a lenha, suíte com banheira e pomar. R$ 630 mil, aceita financiamento.",
        "preco": "R$ 630.000,00",
        "obs_preco": "Aceita financiamento",
        "condominio": "—",
        "localizacao": "Entre São José do Rio Preto e Engenheiro Schmidt.",
        "descricao_curta": "Terreno de 1.000 m² com piscina, varanda ampla com churrasqueira e fogão a lenha, pomar e segurança completa.",
        "destaques": ["1.000 m² terreno", "2 dormitórios", "Piscina", "8 câmeras"],
        "quartos": 2, "banheiros": 2, "area_m2": None, "terreno_m2": 1000,
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
            "Aceita financiamento",
        ],
        "imagens": fotos("chacara-rio-preto", 26),
    },
    {
        "id": "unique-felicita-9andar",
        "tipo": "apartamento",
        "valor": 300000,
        "grupo": "Unique Felicità",
        "bairro": "Região do Damha",
        "categoria": "venda",
        "titulo": "Apartamento no Unique Felicità • 9º andar",
        "seo_titulo": "Apartamento à venda no Unique Felicità, Rio Preto – 9º andar, 2 quartos, R$ 300 mil",
        "seo_descricao": "Apartamento à venda no Unique Felicità em São José do Rio Preto (região do Damha e da represa): 9º andar com vista, 2 quartos, planejados, lazer completo. R$ 300 mil, condomínio R$ 400. Aceita financiamento.",
        "preco": "R$ 300.000,00",
        "obs_preco": "Aceita financiamento",
        "condominio": "R$ 400,00",
        "iptu": "aprox. R$ 450,00/ano",
        "localizacao": "Região dos Dahmas, represa, mercado Oba, próximo ao Mc Donald e ao Carrefour.",
        "descricao_curta": "9º andar com vista para a represa • 2 quartos, cozinha e banheiro com planejados, varanda e lazer completo.",
        "destaques": ["9º andar", "2 quartos", "1 vaga", "Lazer completo"],
        "quartos": 2, "banheiros": 1, "area_m2": None, "terreno_m2": None,
        "itens": [
            "9º andar", "Sala", "Cozinha com planejados", "Banheiro com planejados",
            "Dois quartos", "Lavanderia", "Varanda", "Vaga de garagem e vaga de visitantes",
            "Piscinas, churrasqueiras e playground", "Bicicletário, quadra de basquete e petplace",
            "Três elevadores e mercadinho Stok", "Segurança 24h",
            "Condomínio R$ 400,00 • IPTU aprox. R$ 450,00/ano", "Aceita financiamento",
        ],
        "imagens": fotos("unique-felicita-9andar", 27),
    },
    {
        "id": "cobertura-duplex-unique",
        "tipo": "apartamento",
        "valor": 450000,
        "grupo": "Unique Felicità",
        "bairro": "Região do Damha",
        "categoria": "venda",
        "titulo": "Cobertura Duplex no Unique Felicità • 17º e 18º andar",
        "seo_titulo": "Cobertura duplex à venda no Unique Felicità, Rio Preto – área gourmet e vista, R$ 450 mil",
        "seo_descricao": "Cobertura duplex à venda no Unique Felicità em São José do Rio Preto (região do Damha): 17º e 18º andar, 2 quartos e 2 banheiros com planejados, área gourmet com churrasqueira e vista para a represa. R$ 450 mil, condomínio R$ 350. Aceita financiamento.",
        "preco": "R$ 450.000,00",
        "obs_preco": "Aceita financiamento",
        "condominio": "R$ 350,00",
        "localizacao": "Região dos Dahmas, represa, mercado Oba, próximo ao Mc Donald e ao Carrefour.",
        "descricao_curta": "Duplex no 17º e 18º andar com vista para a represa • 2 quartos e 2 banheiros com planejados e cobertura com área gourmet e churrasqueira.",
        "destaques": ["Duplex 17º/18º andar", "2 quartos", "2 banheiros", "Área gourmet privativa"],
        "quartos": 2, "banheiros": 2, "area_m2": None, "terreno_m2": None,
        "itens": [
            "17º e 18º andar (duplex)", "Duas salas com planejados", "Cozinha com armários planejados",
            "Dois banheiros com planejados", "Dois quartos com armários planejados",
            "Cobertura com área gourmet e churrasqueira", "Lavanderia", "Varanda",
            "Vaga de garagem e vaga de visitantes", "Piscinas adulto e infantil, churrasqueiras e playground",
            "Bicicletário, quadra de basquete e petplace", "Três elevadores e mercadinho Stok", "Segurança 24h",
            "Condomínio R$ 350,00", "Aceita financiamento",
        ],
        "imagens": fotos("cobertura-duplex-unique", 19),
    },
    {
        "id": "unique-felicita-14andar",
        "tipo": "apartamento",
        "valor": 260000,
        "grupo": "Unique Felicità",
        "bairro": "Região do Damha",
        "categoria": "venda",
        "titulo": "Apartamento no Unique Felicità • 14º andar",
        "seo_titulo": "Apartamento à venda no Unique Felicità, Rio Preto – 14º andar, 2 quartos, R$ 260 mil",
        "seo_descricao": "Apartamento à venda no Unique Felicità em São José do Rio Preto (região do Damha e da represa): 14º andar, 2 quartos, varanda, vaga e lazer completo com duas piscinas e segurança 24h. R$ 260 mil, condomínio R$ 350. Aceita financiamento.",
        "preco": "R$ 260.000,00",
        "obs_preco": "Aceita financiamento",
        "condominio": "R$ 350,00",
        "localizacao": "Região dos Dahmas, represa, mercado Oba, próximo ao Mc Donald e ao Carrefour.",
        "descricao_curta": "14º andar com varanda • 2 quartos, sala, cozinha, banheiro, vaga e lazer completo. As últimas fotos mostram as áreas comuns do condomínio.",
        "destaques": ["14º andar", "2 quartos", "1 vaga", "Lazer completo"],
        "quartos": 2, "banheiros": 1, "area_m2": None, "terreno_m2": None,
        "itens": [
            "14º andar", "Sala", "Cozinha", "Banheiro", "Dois quartos", "Lavanderia", "Varanda",
            "Vaga de garagem e vaga de visitantes", "Duas piscinas, churrasqueiras e playground",
            "Bicicletário, quadra de basquete e petplace", "Três elevadores e mercadinho Stok", "Segurança 24h",
            "Condomínio R$ 350,00", "Aceita financiamento",
        ],
        "imagens": fotos("unique-felicita-14andar", 11),
    },
    {'id': 'unique-felicita-14andar-planejados',
     'tipo': 'apartamento',
     'valor': 350000,
     'grupo': 'Unique Felicità',
     'bairro': 'Região do Damha',
     'categoria': 'venda',
     'titulo': 'Apartamento com planejados no Unique Felicità • 14º andar',
     'seo_titulo': 'Apartamento com planejados à venda no Unique Felicità, Rio Preto – 14º andar, R$ '
                   '350 mil',
     'seo_descricao': 'Apartamento no Unique Felicità, em São José do Rio Preto: 14º andar, 2 quartos, '
                      'sala, cozinha e banheiro com planejados, varanda, vaga e lazer completo. Venda '
                      'por R$ 350 mil.',
     'preco': 'R$ 350.000,00',
     'obs_preco': '',
     'condominio': '—',
     'localizacao': "Região dos Dahmas e da represa, perto do mercado Oba, McDonald's e Carrefour.",
     'descricao_curta': '14º andar • 2 quartos, sala, cozinha e banheiro com planejados, lavanderia, '
                        'varanda, vaga de garagem e lazer completo.',
     'destaques': ['14º andar', '2 quartos com planejados', '1 vaga', 'Lazer completo'],
     'quartos': 2,
     'banheiros': 1,
     'area_m2': None,
     'terreno_m2': None,
     'itens': ['14º andar',
               'Sala com planejados',
               'Cozinha com planejados',
               'Banheiro com planejados',
               'Dois quartos com planejados',
               'Lavanderia',
               'Varanda',
               'Vaga de garagem',
               'Vaga de visitantes',
               'Piscinas',
               'Churrasqueiras',
               'Playground',
               'Bicicletário',
               'Quadra de basquete',
               'Petplace',
               'Três elevadores',
               'Mercadinho Stok',
               'Segurança 24h'],
     'imagens': ['/static/imoveis/unique-felicita-14andar-planejados/01.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/02.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/03.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/04.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/05.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/06.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/07.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/08.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/09.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/10.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/11.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/12.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/13.jpg',
                 '/static/imoveis/unique-felicita-14andar-planejados/14.jpg']},
    {'id': 'chacara-jockey-club',
     'tipo': 'chacara',
     'valor': 250000,
     'grupo': 'Chácara Jockey Club',
     'bairro': 'Chácara Jockey Club (Zona Rural)',
     'categoria': 'venda',
     'titulo': 'Chácara de 1.500 m² no Jockey Club',
     'seo_titulo': 'Chácara de 1.500 m² à venda no Jockey Club, São José do Rio Preto – R$ 250 mil',
     'seo_descricao': 'Chácara de 1.500 m² no Jockey Club, São José do Rio Preto, toda alambrada, com '
                      'portão, água de poço artesiano e árvores frutíferas produzindo. Rua Katsumi '
                      'Ohno, 201. R$ 250 mil.',
     'preco': 'R$ 250.000,00',
     'obs_preco': '',
     'condominio': '—',
     'localizacao': 'Rua Katsumi Ohno, 201 – Chácara Jockey Club (Zona Rural), São José do Rio Preto – '
                    'SP, CEP 15062-003.',
     'endereco_completo': True,
     'mapa_endereco': '-20.8327484,-49.3441582',
     'imagem_localizacao': '/static/imoveis/chacara-jockey-club/05-localizacao.svg',
     'descricao_curta': 'Chácara de 1.500 m², toda alambrada e com portão, água de poço artesiano e '
                        'árvores frutíferas produzindo, em ótima localização.',
     'destaques': ['1.500 m² de terreno', 'Toda alambrada', 'Poço artesiano', 'Frutíferas produzindo'],
     'quartos': None,
     'banheiros': None,
     'area_m2': None,
     'terreno_m2': 1500,
     'itens': ['Terreno com área informada de 1.500 m²',
               'Toda alambrada',
               'Portão',
               'Água de poço artesiano',
               'Árvores frutíferas produzindo',
               'Ótima localização no Jockey Club'],
     'imagens': ['/static/imoveis/chacara-jockey-club/01.jpg',
                 '/static/imoveis/chacara-jockey-club/02.jpg',
                 '/static/imoveis/chacara-jockey-club/03.jpg',
                 '/static/imoveis/chacara-jockey-club/04.jpg',
                 '/static/imoveis/chacara-jockey-club/05-localizacao.svg']},
]
IMOVEIS_POR_ID = {i["id"]: i for i in IMOVEIS}

TIPOS = {"casa": "Casa", "chacara": "Chácara", "apartamento": "Apartamento"}
TIPOS_SCHEMA = {"casa": "SingleFamilyResidence", "chacara": "House", "apartamento": "Apartment"}
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
        texto = sem_acento(" ".join([i["titulo"], i["grupo"], i["bairro"], i["localizacao"], i["descricao_curta"], " ".join(i["itens"])]))
        ok_q = (q in texto) if q else True
        ok_cat = (i["categoria"] == cat) if cat in {"venda", "aluguel"} else True
        ok_tipo = (i["tipo"] == tipo) if tipo in TIPOS else True
        ok_preco = (i["valor"] <= preco_max) if preco_max else True
        return ok_q and ok_cat and ok_tipo and ok_preco
    return [i for i in itens if casa_match(i)]


def schema_empresa():
    return {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": MARCA_IMOVEIS,
        "url": SITE_URL,
        "logo": f"{SITE_URL}/static/logo.png",
        "image": f"{SITE_URL}/static/og-image.jpg",
        "telephone": WHATSAPP_PHONE,
        "identifier": {"@type": "PropertyValue", "propertyID": "CRECI", "value": CRECI},
        "address": {"@type": "PostalAddress", "addressLocality": CIDADE, "addressRegion": "SP", "addressCountry": "BR"},
        "areaServed": [{"@type": "City", "name": c} for c in (CIDADE, "Mirassol", "Bady Bassitt", "Cedral", "Engenheiro Schmidt")],
    }


def schema_imovel(i):
    imovel = {
        "@type": TIPOS_SCHEMA.get(i["tipo"], "House"),
        "name": i["titulo"],
        "address": {"@type": "PostalAddress", "addressLocality": CIDADE, "addressRegion": "SP", "addressCountry": "BR"},
        "numberOfRooms": i.get("quartos"),
        "numberOfBathroomsTotal": i.get("banheiros"),
    }
    if i.get("area_m2"):
        imovel["floorSize"] = {"@type": "QuantitativeValue", "value": i["area_m2"], "unitCode": "MTK"}
    return {
        "@context": "https://schema.org",
        "@type": "RealEstateListing",
        "name": i["seo_titulo"],
        "description": i["seo_descricao"],
        "url": f"{SITE_URL}/imovel/{i['id']}",
        "image": [SITE_URL + u for u in i["imagens"][:6]],
        "datePosted": ATUALIZADO_EM,
        "offers": {
            "@type": "Offer",
            "price": i["valor"],
            "priceCurrency": "BRL",
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "RealEstateAgent", "name": MARCA_IMOVEIS, "telephone": WHATSAPP_PHONE},
        },
        "about": imovel,
    }


@app.context_processor
def contexto_global():
    return {
        "marca": MARCA_IMOVEIS,
        "site_url": SITE_URL,
        "whatsapp_exibicao": WHATSAPP_EXIBICAO,
        "creci": CRECI,
        "wa_base": "https://wa.me/" + "".join(filter(str.isdigit, WHATSAPP_PHONE)) + "?text=",
        "mensagem_base": MENSAGEM_BASE_IMOVEIS,
        "rastreio": RASTREIO,
        "tipos_nomes": TIPOS,
        "ano": date.today().year,
    }


@app.route("/")
def imoveis_home():
    filtros = {k: request.args.get(k, "") for k in ("q", "cat", "tipo", "preco_max")}
    filtrados = filtrar_imoveis(IMOVEIS, **filtros)
    total_venda = len([i for i in IMOVEIS if i["categoria"] == "venda"])
    total_aluguel = len([i for i in IMOVEIS if i["categoria"] == "aluguel"])
    # só oferece no buscador os tipos que existem no catálogo
    tipos_disponiveis = [(k, v, sum(1 for i in IMOVEIS if i["tipo"] == k)) for k, v in TIPOS.items()]
    tipos_disponiveis = [t for t in tipos_disponiveis if t[2]]
    jsonld = [schema_empresa()] + [schema_imovel(i) for i in IMOVEIS]
    return render_template(
        "index.html",
        imoveis=filtrados,
        total_imoveis=len(IMOVEIS),
        total_venda=total_venda,
        total_aluguel=total_aluguel,
        tipos=tipos_disponiveis,
        faixas=FAIXAS_PRECO,
        filtros=filtros,
        filtrando=any(filtros.values()),
        jsonld=json.dumps(jsonld, ensure_ascii=False),
    )


@app.route("/imovel/<id_imovel>")
def imovel_detalhe(id_imovel):
    imovel = IMOVEIS_POR_ID.get(id_imovel)
    if not imovel:
        abort(404)
    outros = [i for i in IMOVEIS if i["id"] != id_imovel]
    jsonld = [schema_empresa(), schema_imovel(imovel), {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Imóveis", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": imovel["titulo"], "item": f"{SITE_URL}/imovel/{imovel['id']}"},
        ],
    }]
    return render_template("imovel.html", imovel=imovel, outros=outros, jsonld=json.dumps(jsonld, ensure_ascii=False))


@app.route("/robots.txt")
def robots():
    txt = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    return Response(txt, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    urls = [(SITE_URL + "/", "1.0")] + [(f"{SITE_URL}/imovel/{i['id']}", "0.9") for i in IMOVEIS]
    corpo = "".join(
        f"<url><loc>{u}</loc><lastmod>{ATUALIZADO_EM}</lastmod><priority>{p}</priority></url>" for u, p in urls
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{corpo}</urlset>'
    return Response(xml, mimetype="application/xml")


@app.errorhandler(404)
def nao_encontrado(e):
    return render_template("404.html"), 404

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
