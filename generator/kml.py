
from providers.weather import get_weather


def get_fire_state(f):

    code = f.get("status_code")

    if code == 9:
        return "SURVAILANCE"

    if code == 8:
        return "CONCLUSION"

    if code == 7:
        return "RESOLUTION"

    if code == 6:
        return "ACTIVE"

    if code == 5:
        return "INITIAL"

    return "UNKNOWN"


def get_style_id(state):

    if state == "SURVAILANCE":
        return "green"

    if state == "CONCLUSION":
        return "grey"

    if state == "RESOLUTION":
        return "green"

    if state == "ACTIVE":
        return "red"

    if state == "INITIAL":
        return "orange"

    return "blue"


def build_kml(occurrences):

    styles = """
    <Style id="red">
        <IconStyle>
            <color>ff0000ff</color>
            <scale>1.3</scale>
        </IconStyle>
    </Style>

    <Style id="orange">
        <IconStyle>
            <color>ff00a5ff</color>
            <scale>1.2</scale>
        </IconStyle>
    </Style>

    <Style id="green">
        <IconStyle>
            <color>ff00ff00</color>
            <scale>1.1</scale>
        </IconStyle>
    </Style>

    <Style id="grey">
        <IconStyle>
            <color>ff808080</color>
            <scale>1.0</scale>
        </IconStyle>
    </Style>

    <Style id="blue">
        <IconStyle>
            <color>ffffa500</color>
            <scale>1.0</scale>
        </IconStyle>
    </Style>
    """

    placemarks = ""

    for f in occurrences:

        name = f.get("parish") or "Sem freguesia"

        lon = f.get("lon")
        lat = f.get("lat")

        if lon is None or lat is None:
            continue

        state = get_fire_state(f)
        style_id = get_style_id(state)

        # 🔥 WEATHER (modelo interpolado)
        wx = get_weather(lat, lon)

        aerial = f.get("aerial", 0)
        ground = f.get("ground", 0)
        operatives = f.get("operatives", 0)

        description = f"""
        <![CDATA[
        <b>Estado:</b> {state}<br/>
        <br/>

        <b>🌬 Vento:</b> {wx['wind_speed']} kt<br/>
        <b>🧭 Direção:</b> {wx['wind_dir']}°<br/>
        <b>🌡 Temperatura:</b> {wx['temp']} °C<br/>
        <b>📊 QNH:</b> {wx['qnh']} hPa<br/>
        <br/>

        <b>Aeronaves:</b> {aerial}<br/>
        <b>Viaturas:</b> {ground}<br/>
        <b>Operacionais:</b> {operatives}<br/>
        <br/>

        <b>Distrito:</b> {f.get('district', '')}<br/>
        <b>Concelho:</b> {f.get('municipality', '')}<br/>
        <b>Freguesia:</b> {f.get('parish', '')}<br/>
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
