from datetime import datetime
from zoneinfo import ZoneInfo

from providers.weather import get_weather


# --------------------------------------------------
# SUB-REGIONAL FREQUENCIES
# --------------------------------------------------

SUBREGIONAL_FREQUENCIES = {

    "Alto Minho": {"freq": "123.930", "municipalities": ["Arcos de Valdevez","Caminha","Melgaço","Monção","Paredes de Coura","Ponte da Barca","Ponte de Lima","Valença","Viana do Castelo","Vila Nova de Cerveira"]},

    "Cávado": {"freq": "123.655", "municipalities": ["Amares","Barcelos","Braga","Esposende","Terras de Bouro","Vila Verde"]},

    "Ave": {"freq": "124.955", "municipalities": ["Cabeceiras de Basto","Fafe","Guimarães","Mondim de Basto","Póvoa de Lanhoso","Vieira do Minho","Vila Nova de Famalicão","Vizela"]},

    "Alto Tâmega e Barroso": {"freq": "125.355", "municipalities": ["Boticas","Chaves","Montalegre","Ribeira de Pena","Valpaços","Vila Pouca de Aguiar"]},

    "Terras de Trás-os-Montes": {"freq": "123.160", "municipalities": ["Alfândega da Fé","Bragança","Macedo de Cavaleiros","Mirandela","Mogadouro","Vila Flor","Vimioso","Vinhais"]},

    "Área Metropolitana do Porto": {"freq": "129.690", "municipalities": ["Arouca","Espinho","Gondomar","Maia","Matosinhos","Oliveira de Azeméis","Paredes","Porto","Póvoa de Varzim","Santa Maria da Feira","Santo Tirso","São João da Madeira","Trofa","Vale de Cambra","Valongo","Vila do Conde","Vila Nova de Gaia"]},

    "Tâmega e Sousa": {"freq": "122.830", "municipalities": ["Amarante","Baião","Castelo de Paiva","Celorico de Basto","Felgueiras","Lousada","Marco de Canaveses","Paços de Ferreira","Paredes","Penafiel","Resende","Felgueiras"]},    "Tâmega e Sousa": {"freq": "122.830", "municipalities": ["Amarante","Baião","Felgueiras","Lousada","Marco de Canaveses","Paços de Ferreira","Paredes","Penafiel"]},

    "Douro": {"freq": "120.940", "municipalities": ["Alijó","Armamar","Carrazeda de Ansiães","Freixo de Espada à Cinta","Lamego","Mesão Frio","Moimenta da Beira","Murça","Penedono","Peso da Régua","Sabrosa","Santa Marta de Penaguião","São João da Pesqueira","Sernancelhe","Tabuaço","Torre de Moncorvo","Vila Nova de Foz Côa","Vila Real"]},

    "Região de Aveiro": {"freq": "126.155", "municipalities": ["Águeda","Albergaria-a-Velha","Anadia","Aveiro","Estarreja","Ílhavo","Mealhada","Murtosa","Oliveira do Bairro","Ovar","Sever do Vouga","Vagos"]},

    "Viseu Dão e Lafões": {"freq": "125.805", "municipalities": ["Aguiar da Beira","Carregal do Sal","Castro Daire","Mangualde","Nelas","Oliveira de Frades","Penalva do Castelo","São Pedro do Sul","Sátão","Tondela","Vila Nova de Paiva","Viseu","Vouzela"]},

    "Beiras e Serra da Estrela": {"freq": "123.930", "municipalities": ["Almeida","Belmonte","Celorico da Beira","Covilhã","Figueira de Castelo Rodrigo","Fornos de Algodres","Fundão","Gouveia","Guarda","Manteigas","Mêda","Pinhel","Sabugal","Seia","Trancoso"]},

    "Região de Coimbra": {"freq": "129.805", "municipalities": ["Arganil","Cantanhede","Coimbra","Condeixa-a-Nova","Figueira da Foz","Figueiró dos Vinhos","Góis","Lousã","Mira","Miranda do Corvo","Montemor-o-Velho","Mortágua","Oliveira do Hospital","Penacova","Penela","Soure","Tábua","Vila Nova de Poiares"]},

    "Região de Leiria": {"freq": "124.705", "municipalities": ["Alcobaça","Batalha","Leiria","Marinha Grande","Nazaré","Óbidos","Pombal","Porto de Mós"]},

    "Beira Baixa": {"freq": "123.655", "municipalities": ["Belmonte","Castelo Branco","Covilhã","Fundão","Idanha-a-Nova","Oleiros","Penamacor","Proença-a-Nova","Sertã","Vila de Rei","Vila Velha de Ródão"]},

    "Médio Tejo": {"freq": "123.160", "municipalities": ["Abrantes","Alcanena","Constância","Entroncamento","Ferreira do Zêzere","Mação","Ourém","Sardoal","Tomar","Torres Novas","Vila Nova da Barquinha"]},

    "Oeste": {"freq": "124.955", "municipalities": ["Alcobaça","Alenquer","Arruda dos Vinhos","Bombarral","Cadaval","Caldas da Rainha","Lourinhã","Nazaré","Óbidos","Peniche","Sobral de Monte Agraço","Torres Vedras"]},

    "Lezíria do Tejo": {"freq": "120.940", "municipalities": ["Almeirim","Alpiarça","Azambuja","Benavente","Cartaxo","Chamusca","Coruche","Golegã","Rio Maior","Salvaterra de Magos","Santarém"]},

    "Grande Lisboa": {"freq": "125.805", "municipalities": ["Amadora","Cascais","Lisboa","Loures","Mafra","Odivelas","Oeiras","Sintra","Vila Franca de Xira"]},

    "Península de Setúbal": {"freq": "122.830", "municipalities": ["Alcochete","Almada","Barreiro","Moita","Montijo","Palmela","Seixal","Sesimbra","Setúbal"]},

    "Alentejo Central": {"freq": "125.355", "municipalities": ["Alandroal","Arraiolos","Borba","Estremoz","Évora","Montemor-o-Novo","Mora","Mourão","Portel","Redondo","Reguengos de Monsaraz","Vendas Novas","Viana do Alentejo","Vila Viçosa"]},

    "Alentejo Litoral": {"freq": "129.690", "municipalities": ["Alcácer do Sal","Grândola","Odemira","Santiago do Cacém","Sines"]},

    "Baixo Alentejo": {"freq": "124.705", "municipalities": ["Aljustrel","Almodôvar","Alvito","Barrancos","Beja","Castro Verde","Cuba","Ferreira do Alentejo","Mértola","Moura","Ourique","Serpa","Vidigueira"]},

    "Alto Alentejo": {"freq": "126.155", "municipalities": ["Alter do Chão","Arronches","Avis","Campo Maior","Castelo de Vide","Crato","Elvas","Fronteira","Gavião","Marvão","Monforte","Nisa","Ponte de Sor","Portalegre"]},

    "Algarve": {"freq": "129.805", "municipalities": ["Albufeira","Alcoutim","Aljezur","Castro Marim","Faro","Lagoa","Lagos","Loulé","Monchique","Olhão","Portimão","São Brás de Alportel","Silves","Tavira","Vila do Bispo","Vila Real de Santo António"]},
}


# --------------------------------------------------
# FIRE STATE
# --------------------------------------------------

def get_fire_state(f):

    code = int(f.get("status_code", 0))

    return {
        1: "FALSE ALARM",
        2: "FALSE ALERT",
        3: "DISPATCHED",
        4: "INITIAL",
        5: "ACTIVE",
        6: "ARRIVAL T.O.",
        7: "RESOLUTION",
        8: "CONCLUSION",
        9: "SURVEILLANCE"
    }.get(code, "UNKNOWN")


# --------------------------------------------------
# STYLE
# --------------------------------------------------

def get_style_id(state):

    return {
        "FALSE ALARM": "grey",
        "FALSE ALERT": "grey",
        "CLOSED": "green",
        "DISPATCHED": "orange",
        "INITIAL": "orange",
        "ARRIVAL T.O.": "red",
        "ACTIVE": "red",
        "RESOLUTION": "blue",
        "CONCLUSION": "grey",
        "SURVEILLANCE": "blue",
    }.get(state, "grey")


# --------------------------------------------------
# NORMALIZE
# --------------------------------------------------

def normalize(text: str):

    if not text:
        return ""

    return (
        text.lower()
        .replace("-", " ")
        .split("(")[0]
        .split(",")[0]
        .strip()
    )


# --------------------------------------------------
# SUBREGIONAL FREQUENCY
# --------------------------------------------------

def get_subregional_frequency(municipality):

    if not municipality:
        return "CMD SUB-REGIONAL DESCONHECIDO"

    m = normalize(municipality)

    for region, data in SUBREGIONAL_FREQUENCIES.items():
        for mun in data["municipalities"]:
            if normalize(mun) == m:
                return f"CMD SUB-REGIONAL {region.upper()} - {data['freq']}"

    return "CMD SUB-REGIONAL DESCONHECIDO"


# --------------------------------------------------
# CLEAN PARISH
# --------------------------------------------------

def clean_freguesia(name: str):

    if not name:
        return "Sem freguesia"

    return (
        name
        .split(" Sem informação do número de meios neste momento.")[0]
        .split(" Informação recolhida via Fogos.pt")[0]
        .strip()
    )


# --------------------------------------------------
# BUILD KML
# --------------------------------------------------

def build_kml(occurrences):

    local_time = datetime.now(
        ZoneInfo("Europe/Lisbon")
    ).strftime("%H:%M")

    styles = """
    <Style id="red"><IconStyle><color>ff0000ff</color><scale>1.3</scale></IconStyle></Style>
    <Style id="orange"><IconStyle><color>ff00a5ff</color><scale>1.2</scale></IconStyle></Style>
    <Style id="green"><IconStyle><color>ff00ff00</color><scale>1.1</scale></IconStyle></Style>
    <Style id="blue"><IconStyle><color>ffff0000</color><scale>1.1</scale></IconStyle></Style>
    <Style id="grey"><IconStyle><color>ff808080</color><scale>1.0</scale></IconStyle></Style>
    """

    placemarks = ""

    for f in occurrences:

        name = clean_freguesia(f.get("parish") or "Sem freguesia")
        municipality = f.get("municipality", "")

        lon = f.get("lon")
        lat = f.get("lat")

        if lon is None or lat is None:
            continue

        state = get_fire_state(f)
        style_id = get_style_id(state)

        aerial = f.get("aerial", 0)
        ground = f.get("ground", 0)
        operatives = f.get("operatives", 0)

        wx = get_weather(lat, lon) or {}

        cmd_frequency = get_subregional_frequency(municipality)

        # -----------------------------
        # STARTED_AT (UTC -> Lisboa)
        # -----------------------------

        started_at_raw = f.get("started_at")
        started_at_local = "N/A"

        if started_at_raw:
            try:
                started_dt = datetime.fromisoformat(
                    started_at_raw.replace("Z", "+00:00")
                )
                started_at_local = started_dt.astimezone(
                    ZoneInfo("Europe/Lisbon")
                ).strftime("%d-%m-%y %H:%M") + "L"
            except Exception:
                started_at_local = "N/A"

        description = f"""
<![CDATA[
<b>Estado:</b> {state} | Updated @ {local_time}<br/>
<b>Início:</b> {started_at_local}<br/>
<b>Tipo:</b> {f.get('nature_desc', '')}<br/>
<br/>

<b>Meios Aéreos:</b> {aerial}<br/>
<b>Meios Terrestres:</b> {ground}<br/>
<b>Operacionais:</b> {operatives}<br/>
<br/>

<b>{cmd_frequency}</b><br/>
<br/>

<b>Open-Meteo Forecast<br/>
<b>🌬 Vento:</b> {wx.get('wind_speed', 'N/A')} kt<br/>
<b>🧭 Direção:</b> {wx.get('wind_dir', 'N/A')}°<br/>
<b>🌡 Temperatura:</b> {wx.get('temp', 'N/A')} °C<br/>
<b>📊 QNH:</b> {wx.get('qnh', 'N/A')} hPa<br/>
<br/>

<b>Distrito:</b> {f.get('district', '')}<br/>
<b>Concelho:</b> {municipality}<br/>
<b>Freguesia:</b> {name}<br/>

]]>
"""

        placemarks += f"""
<Placemark>
    <name>{name}</name>
    <styleUrl>#{style_id}</styleUrl>
    <description>{description}</description>
    <Point>
        <coordinates>{lon},{lat},0</coordinates>
    </Point>
</Placemark>
"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
{styles}
{placemarks}
</Document>
</kml>
"""