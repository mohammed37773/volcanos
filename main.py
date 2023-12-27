import folium as fl
import pandas as pd
import subprocess as sp
from math import ceil
import os


def path(*args):
    return os.path.join(*args)


def get_icon(type_):
    type_ = type_.lower()
    if "volcan" in type_:
        return fl.features.CustomIcon(path("assets", "icons", "volcano.png"), (32, 32))
    elif "cone" in type_:
        return fl.features.CustomIcon(path("assets", "icons", "mountain.png"), (32, 32))
    else:
        return fl.features.CustomIcon(path("assets", "icons", "default.png"), (32, 32))


if __name__ == '__main__':
    # define objects
    map_ = fl.Map(location=(0, 0))
    feature_group = fl.FeatureGroup(name="features")

    # add features to feature group
    feature_group.add_child(
        fl.GeoJson(data=open(os.path.join("assets", "datasets", "world.json"), encoding="utf-8-sig").read()))

    cols = ["Name", "Latitude", "Longitude", "Elev", "Type"]
    for row in pd.read_csv(path("assets", "datasets", "volcano.csv"), skipinitialspace=True)[cols].iterrows():
        name, lat, lon, elev, type_ = row[1]
        message = fl.Popup(f"name:{name}<br>height:{elev}m")
        marker = fl.Marker((lat, lon), popup=message, icon=get_icon(type_))
        feature_group.add_child(marker)

    map_.add_child(feature_group)
    map_.add_child(fl.Marker((0, 0), popup="center of the world", icon=fl.Icon(color="orange")))
    map_.save("map.html")
