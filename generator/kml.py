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

    "Terras de Trás-os-Montes": {"freq": "123.160", "municipalities": ["Bragança","Mirandela","Macedo de Cavaleiros","Vinhais"]},

    "Área Metropolitana do Porto": {"freq": "129.690", "municipalities": ["Porto","Maia","Matosinhos","Vila Nova de Gaia","Gondomar","Valongo","Póvoa de Varzim","Vila do Conde"]},

    "Tâmega e Sousa": {"freq": "122.830", "municipalities": ["Amarante","Baião","Felgueiras","Lousada","Marco de Canaveses","Paços de Ferreira","Paredes","Penafiel"]},

    "Douro": {"freq": "120.940", "municipalities": ["Alijó","Lamego","Peso da Régua","Sabrosa","Tabuaço"]},

    "Região de Aveiro": {"freq": "126.155", "municipalities": ["Aveiro","Águeda","Ílhavo","Ovar","Vagos"]},

    "Viseu Dão e Lafões": {"freq": "125.805", "municipalities": ["Viseu","Mangualde","Nelas","Tondela","Vouzela"]},

    "Beiras e Serra da Estrela": {"freq": "123.930", "municipalities": ["Covilhã","Fundão","Guarda","Seia"]},

    "Região de Coimbra": {"freq": "129.805", "municipalities": ["Coimbra","Arganil","Figueira da Foz","Lousã"]},

    "Região de Leiria": {"freq": "124.705", "municipalities": ["Leiria","Pombal","Batalha","Marinha Grande"]},

    "Beira Baixa": {"freq": "123.655", "municipalities": ["Castelo Branco","Oleiros","Sertã","Vila de Rei"]},

    "Médio Tejo": {"freq": "123.160", "municipalities": ["Abrantes","Tomar","Torres Novas","Ourém"]},

    "Oeste": {"freq": "124.955", "municipalities": ["Torres Vedras","Peniche","Nazaré","Caldas da Rainha"]},

    "Lezíria do Tejo": {"freq": "120.940", "municipalities": ["Benavente","Coruche","Santarém","Rio Maior","Chamusca","Almeirim","Alpiarça","Cartaxo","Golegã","Salvaterra de Magos","Azambuja"]},

    "Grande Lisboa": {"freq": "125.805", "municipalities": ["Lisboa","Sintra","Loures","Cascais","Oeiras"]},

    "Península de Setúbal": {"freq": "122.830", "municipalities": ["Setúbal","Palmela","Sesimbra","Seixal","Almada"]},

    "Alto Alentejo": {"freq": "126.155", "municipalities": ["Portalegre","Elvas","Ponte de Sor","Campo Maior"]},

    "Alentejo Central": {"freq": "125.355", "municipalities": ["Évora","Montemor-o-Novo","Arraiolos","Vendas Novas"]},

    "Alentejo Litoral": {"freq": "129.690", "municipalities": ["Sines","Grândola","Odemira","Santiago do Cacém"]},

    "Baixo Alentejo": {"freq": "124.705", "municipalities": ["Beja","Moura","Mértola","Ourique"]},

    "Algarve": {"freq": "129.805", "municipalities": ["Faro","Portimão","Loulé","Tavira","Lagos"]}
}


# --------------------------------------------------
# NORMALIZATION (CRITICAL FIX)
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
# FIRE STATE
# --------------------------------------------------

def get_fire_state(f):

    code = int(f.get("status_code", 0))

    return {
        1: "FALSE ALARM",
        2: "FALSE ALERT",
        3: "CLOSED",
        4: "INITIAL",
        5: "ACTIVE",
        6: "ACTIVE",
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
        "INITIAL": "orange",
        "ACTIVE": "red",
        "RESOLUTION": "blue",
        "CONCLUSION": "grey",
        "SURVEILLANCE": "blue"
    }.get(state, "grey")


# --------------------------------------------------
# FREQUENCY LOOKUP (ROBUST)
# --------------------------------------------------

def get_subregional_frequency(municipality):

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

    local_time = datetime.now(ZoneInfo("Europe/Lisbon")).strftime("%H:%M")

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

        wx = get_weather(lat, lon) or {}

        cmd_frequency = get_subregional_frequency(municipality)

        placemarks += f"""
        <Placemark>
            <name>{name}</name>
            <styleUrl>#{style_id}</styleUrl>
            <description><![CDATA[
                <b>Estado:</b> {state} | Updated @ {local_time}<br/><br/>
                <b>{cmd_frequency}</b><br/><br/>
                <b>Wind:</b> {wx.get('wind_speed','')} kt<br/>
                <b>Temp:</b> {wx.get('temp','')} °C<br/>
                <b>Concelho:</b> {municipality}<br/>
            ]]></description>
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