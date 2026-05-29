from providers.weather import get_weather


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


def clean_freguesia(name: str):

    if not name:
        return "Sem freguesia"

    # remove lixo conhecido do API
    name = name.split(" Sem informação")[0]
    name = name.split(" Informação")[0]

    return name.strip()


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

    <Style id="blue">
        <IconStyle>
            <color>ffff0000</color>
            <scale>1.1</scale>
        </IconStyle>
    </Style>

    <Style id="grey">
        <IconStyle>
            <color>ff808080</color>
            <scale>1.0</scale>
        </IconStyle>
    </Style>
    """

    placemarks = ""

    for f in occurrences:

        raw_name = f.get("parish") or "Sem freguesia"
        name = clean_freguesia(raw_name)

        lon = f.get("lon")
        lat = f.get("lat")

        if lon is None or lat is None:
            continue

        state = get_fire_state(f)
        style_id = get_style_id(state)

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