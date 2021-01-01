```python
if 'shapely' not in sys.modules:
    from copy import deepcopy
    try:
        from shapely.geometry import shape
    except ImportError:
        ! pip install shapely
        from shapely.geometry import shape

# geojson reader : json 파일로부터 dictionary 반환 => folium.Geojson() 에 활용
def geojson_read(file,enc="utf-8"):

    df = None
    with open(file,encoding=enc) as f:
        json_file = json.loads(f.read())
    
    return json_file

# geojson to df : geopandas 로 불러왔을때랑 같은 모양의 데이터프레임 반환 => 일반적인 분석에 활용
def geojson_to_df(json_file):
    
    file =[]
    for dic in json_file['features']:
        tmp = deepcopy(dic['properties'])
        tmp.update({'geometry':shape(dic['geometry'])})
        file.append(tmp)

    df = pd.DataFrame(file)
    return df
```



- 중간에 딕서너리 정보를 모양(?)객체로 만들어줘야 해서 shapely.geometry.shape 필요
  - 셀 그대로 복사해서 실행시키면 알아서 설치되고 import 됨
- 함수명 geojson_read , geojson_to_df

> usage : __geojson_read__ 

```python
어린이교통사고_격자 = geojson_read(파일경로+'2.오산시_어린이교통사고_격자.geojson')
```

> out

```python
{'type': 'FeatureCollection',
 'name': '오산시_어린이교통사고_격자',
 'crs': {'type': 'name',
  'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}},
 'features': [{'type': 'Feature',
   'properties': {'gid': '다사551085', 'accident_cnt': 0},
   'geometry': {'type': 'MultiPolygon',
    'coordinates': [[[[126.99421564681425, 37.17418235770403],
       [126.99420963816323, 37.17508373885349],
       [126.99533608014656, 37.175088541741566],
       [126.99534207541716, 37.174187160436155],
       [126.99421564681425, 37.17418235770403]]]]}},
  {'type': 'Feature',
   'properties': {'gid': '다사551086', 'accident_cnt': 0},
   'geometry': {'type': 'MultiPolygon',
    'coordinates': [[[[126.9942096381632 ...
```

> reference

```python
center =[37.15222, 127.07056]
zoom =13
m = folium.Map(location=center, zoom_start=zoom)

folium.GeoJson(
    어린이교통사고_격자,
    style_function=lambda feature: {
        'color': '#8b00ff',
        'weight': 3,
        'dashArray': '1,2,1'
    }
).add_to(m)
```

---

> usage : __geojson_to_df__ 

```python
어린이교통사고_격자_df = geojson_to_df(어린이교통사고_격자)
```

> out

|      |        gid | accident_cnt |                                          geometry |
| ---: | ---------: | -----------: | ------------------------------------------------: |
|    0 | 다사551085 |            0 | (POLYGON ((126.9942156468143 37.17418235770403... |
|    1 | 다사551086 |            0 | (POLYGON ((126.9942096381632 37.17508373885349... |
|    2 | 다사551087 |            0 | (POLYGON ((126.9942036292448 37.17598511986466... |

> refernece

```python
IN : len(어린이교통사고_격자_df[어린이교통사고_격자_df.accident_cnt>3])
```

```python
OUT : 19
```