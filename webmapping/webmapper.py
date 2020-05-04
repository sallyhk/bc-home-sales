import folium
import pandas
from webmapping.functions import color_producer, make_html, calc_thresholds


def run(filepath="scraping/rew_data.csv"):
    try:
        data = pandas.read_csv(filepath)
        data.drop("Unnamed: 0", axis=1, inplace=True)
        data = data.dropna()
    except FileNotFoundError:
        raise

    map = folium.Map(location=[data["Latitude"][0], data["Longitude"][0]], zoom_start=11, tiles="Stamen Terrain")
    fgv = folium.FeatureGroup(name="On Sale")

    l1, l2 = calc_thresholds(data["$/sq"])

    for _, row in data.iterrows():
        html = make_html(row)
        color_fn = color_producer(row["$/sq"], l1, l2)
        iframe = folium.IFrame(html=html, width=180, height=90)
        fgv.add_child(folium.CircleMarker(location=[row["Latitude"], row["Longitude"]], popup=folium.Popup(iframe),
                                          radius=2, fill_color=color_fn, color=color_fn, fill_opacity=1))

    map.add_child(fgv)
    map.save("Properties.html")
