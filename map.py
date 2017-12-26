import folium
import pandas
import fileinput

##Function to choose marker color according to volcano height
def color_producer(elevation):
    if elevation < 1000:
      return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

##Create base map
map=folium.Map(location=[38.53,-99.09],zoom_start=2,tiles='Mapbox Bright')

##Read volcanoes data
data = pandas.read_csv("resources/Volcanoes_USA.txt")

##Retrieve list of latitude, longitude, volcano name and elevation
lat = list(data["LAT"])
lon = list(data["LON"])
vol_name = list(data["NAME"])
vol_el = list(data["ELEV"])

##Create FeatureGroup for volcanoes
fgv=folium.FeatureGroup(name="volcanoes")

for lt, ln, nm, el in zip(lat,lon,vol_name,vol_el):
    ##Add CircleMarker for every volcano in FeatureGroup
    fgv.add_child(folium.CircleMarker(location=[lt,ln],popup=folium.Popup(str(nm)+" ("+str(el)+" m)",parse_html=True),
    fill_color=color_producer(el),color='grey',fill=True,fill_opacity=1,radius=10))

##Read the world.json to get world Population
file=open("resources/world.json",'r',encoding='utf-8-sig')

##Create FeatureGroup for Population
fgp=folium.FeatureGroup(name="Population")

##Add GeoJson polygon to FeatureGroup
fgp.add_child(folium.GeoJson(data=file.read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

##Add FeatureGroupto Map
map.add_child(fgv)
map.add_child(fgp)

##Add the LayerControl to display/hide population and volcano
map.add_child(folium.LayerControl())

##Save map to file Map1.html
map.save("Map1.html")
