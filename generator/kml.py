from datetime import datetime
from zoneinfo import ZoneInfo

from providers.weather import get_weather


# --------------------------------------------------
# SUB-REGIONAL FREQUENCIES
# --------------------------------------------------

SUBREGIONAL_FREQUENCIES = {

    "Alto Minho": {
        "freq": "123.930",
        "municipalities": [
            "Arcos De Valdevez",
            "Caminha",
            "Melgaço",
            "Monção",
            "Paredes De Coura",
            "Ponte Da Barca",
            "Ponte De Lima",
            "Valença",
            "Viana Do Castelo",
            "Vila Nova De Cerveira"
        ]
    },

    "Cávado": {
        "freq": "123.655",
        "municipalities": [
            "Amares",
            "Barcelos",
            "Braga",
            "Esposende",
            "Terras De Bouro",
            "Vila Verde"
        ]
    },

    "Ave": {
        "freq": "124.955",
        "municipalities": [
            "Cabeceiras De Basto",
            "Fafe",
            "Guimarães",
            "Mondim De Basto",
            "Póvoa De Lanhoso",
            "Vieira Do Minho",
            "Vila Nova De Famalicão",
            "Vizela"
        ]
    },

    "Alto Tâmega e Barroso": {
        "freq": "125.355",
        "municipalities": [
            "Boticas",
            "Chaves",
            "Montalegre",
            "Ribeira De Pena",
            "Valpaços",
            "Vila Pouca De Aguiar"
        ]
    },

    "Terras de Trás-os-Montes": {
        "freq": "123.160",
        "municipalities": [
            "Bragança",
            "Mirandela",
            "Macedo De Cavaleiros",
            "Vinhais"
        ]
    },

    "Área Metropolitana do Porto": {
        "freq": "129.690",
        "municipalities": [
            "Porto",
            "Maia",
            "Matosinhos",
            "Vila Nova De Gaia",
            "Gondomar",
            "Valongo",
            "Póvoa De Varzim",
            "Vila Do Conde"
        ]
    },

    "Tâmega e Sousa": {
        "freq": "122.830",
        "municipalities": [
            "Amarante",
            "Baião",
            "Felgueiras",
            "Lousada",
            "Marco De Canaveses",
            "Paços De Ferreira",
            "Paredes",
            "Penafiel"
        ]
    },

    "Douro": {
        "freq": "120.940",
        "municipalities": [
            "Alijó",
            "Lamego",
            "Peso Da Régua",
            "Sabrosa",
            "Tabuaço"
        ]
    },

    "Região de Aveiro": {
        "freq": "126.155",
        "municipalities": [
            "Aveiro",
            "Águeda",
            "Ílhavo",
            "Ovar",
            "Vagos"
        ]
    },

    "Viseu Dão e Lafões": {
        "freq": "125.805",
        "municipalities": [
            "Viseu",
            "Mangualde",
            "Nelas",
            "Tondela",
            "Vouzela"
        ]
    },

    "Beiras e Serra da Estrela": {
        "freq": "123.930",
        "municipalities": [
            "Covilhã",
            "Fundão",
            "Guarda",
            "Seia"
        ]
    },

    "Região de Coimbra": {
        "freq": "129.805",
        "municipalities": [
            "Coimbra",
            "Arganil",
            "Figueira Da Foz",
            "Lousã"
        ]
    },

    "Região de Leiria": {
        "freq": "124.705",
        "municipalities": [
            "Leiria",
            "Pombal",
            "Batalha",
            "Marinha Grande"
        ]
    },

    "Beira Baixa": {
        "freq": "123.655",
        "municipalities": [
            "Castelo Branco",
            "Oleiros",
            "Sertã",
            "Vila De Rei"
        ]
    },

    "Médio Tejo": {
        "freq": "123.160",
        "municipalities": [
            "Abrantes",
            "Tomar",
            "Torres Novas",
            "Ourém"
        ]
    },

    "Oeste": {
        "freq": "124.955",
        "municipalities": [
            "Torres Vedras",
            "Peniche",
            "Nazaré",
            "Caldas Da Rainha"
        ]
    },

    "Lezíria do Tejo": {
        "freq": "120.940",
        "municipalities": [
            "Benavente",
            "Coruche",
            "Santarém",
            "Rio Maior"
        ]
    },

    "Grande Lisboa": {
        "freq": "125.805",
        "municipalities": [
            "Lisboa",
            "Sintra",
            "Loures",
            "Cascais",
            "Oeiras"
        ]
    },

    "Península de Setúbal": {
        "freq": "122.830",
        "municipalities": [
            "Setúbal",
            "Palmela",
            "Sesimbra",
            "Seixal",
            "Almada"
        ]
    },

    "Alto Alentejo": {
        "freq": "126.155",
        "municipalities": [
            "Portalegre",
            "Elvas",
            "Ponte De Sor",
            "Campo Maior"
        ]
    },

    "Alentejo Central": {
        "freq": "125.355",
        "municipalities": [
            "Évora",
            "Montemor-O-Novo",
            "Arraiolos",
            "Vendas Novas"
        ]
    },

    "Alentejo Litoral": {
        "freq": "129.690",
        "municipalities": [
            "Sines",
            "Grândola",
            "Odemira",
            "Santiago Do Cacém"
        ]
    },

    "Baixo Alentejo": {
        "freq": "124.705",
        "municipalities": [
            "Beja",
            "Moura",
            "Mértola",
            "Ourique"
        ]
    },

    "Algarve": {
        "freq": "129.805",
        "municipalities": [
            "Faro",
            "Portimão",
            "Loulé",
            "Tavira",
            "Lagos"
        ]
    }
}


# --------------------------------------------------
# FIRE STATE
# --------------------------------------------------

def get_fire_state(f):

    code = int(f.get("status_code", 0))

    if code == 1:
        return "FALSE ALARM"
    if code == 2:
        return "FALSE ALERT"
    if code == 3:
        return "CLOSED"
    if code == 4:
        return "INITIAL"
    if code in (5, 6):
        return "ACTIVE"
    if code == 7:
        return "RESOLUTION"
    if code == 8:
        return "CONCLUSION"
    if code == 9:
        return "SURVEILLANCE"

    return "UNKNOWN"


# --------------------------------------------------
# PIN COLORS
# --------------------------------------------------

def get_style_id(state):

    if state in ("FALSE ALARM", "FALSE ALERT"):
        return "grey"
    if state == "CLOSED":
        return "green"
    if state == "INITIAL":
        return "orange"
    if state == "ACTIVE":
        return "red"
    if state == "RESOLUTION":
        return "blue"
    if state == "CONCLUSION":
        return "grey"
    if state == "SURVEILLANCE":
        return "blue"

    return "grey"


# --------------------------------------------------
# CLEAN PARISH
# --------------------------------------------------

def clean_freguesia(name: str):

    if not name:
        return "Sem freguesia"

    name = name.split(" Sem informação do número de meios neste momento.")[0]
    name = name.split(" Informação recolhida via Fogos.pt")[0]

    return name.strip()


# --------------------------------------------------
# SUBREGIONAL FREQUENCY
# --------------------------------------------------

def get_subregional_frequency(municipality):

    if not municipality:
        return "CMD SUB-REGIONAL DESCONHECIDO"

    municipality = municipality.split("(")[0].strip().title()

    for region_name, data in SUBREGIONAL_FREQUENCIES.items():
        if municipality in data["municipalities"]:
            return f"CMD SUB-REGIONAL {region_name.upper()} - {data['freq']}"

    return "CMD SUB-REGIONAL DESCONHECIDO"


# --------------------------------------------------
# BUILD KML
# --------------------------------------------------

def build_kml(occurrences):

    local_time = datetime.now(
        ZoneInfo("Europe/Lisbon")
    ).strftime("%H:%M")

    styles = """
    <Style id="red">
        <IconStyle><color>ff0000ff</color><scale>1.3</scale></IconStyle>
    </Style>

    <Style id="orange">
        <IconStyle><color>ff00a5ff</color><scale>1.2</scale></IconStyle>
    </Style>

    <Style id="green">
        <IconStyle><color>ff00ff00</color><scale>1.1</scale></IconStyle>
    </Style>

    <Style id="blue">
        <IconStyle><color>ffff0000</color><scale>1.1</scale></IconStyle>
    </Style>

    <Style id="grey">
        <IconStyle><color>ff808080</color><scale>1.0</scale></IconStyle>
    </Style>
    """

    placemarks = ""

    for f in occurrences:

        raw_name = f.get("parish") or "Sem freguesia"
        name = clean_freguesia(raw_name)

        municipality = f.get("municipality", "")

        lon = f.get("lon")
        lat = f.get("lat")

        if lon is None or lat is None:
            continue

        state = get_fire_state(f)
        style_id = get_style_id(state)

        wx = get_weather(lat, lon) or {}

        cmd_frequency = get_subregional_frequency(municipality)

        description = f"""
        <![CDATA[
        <b>Estado:</b> {state} | Updated @ {local_time}<br/>
        <br/>

        <b>{cmd_frequency}</b><br/>
        <br/>

        <b>🌬 Vento:</b> {wx.get('wind_speed', 'N/A')} kt<br/>
        <b>🧭 Direção:</b> {wx.get('wind_dir', 'N/A')}°<br/>
        <b>🌡 Temperatura:</b> {wx.get('temp', 'N/A')} °C<br/>
        <b>📊 QNH:</b> {wx.get('qnh', 'N/A')} hPa<br/>
        <br/>

        <b>Distrito:</b> {f.get('district', '')}<br/>
        <b>Concelho:</b> {municipality}<br/>
        <b>Freguesia:</b> {name}<br/>
        <b>Tipo:</b> {f.get('nature_desc', '')}<br/>
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