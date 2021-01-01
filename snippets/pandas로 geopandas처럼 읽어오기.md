```python
if 'shapely' not in sys.modules:
        try:
            from shapely.geometry import shape
        except ImportError:
            ! pip install shapely
            from shapely.geometry import shape

# geojson reader : works exactly the same as geopandas with vanilla pandas
def geojson_read(file,enc="utf-8"):
    
    df = None
    
    with open(file,encoding=enc) as f:
        json_file = json.loads(f.read())

    file =[]
    for dic in json_file['features']:
        tmp = dic['properties']
        tmp.update({'geometry':shape(dic['geometry'])})
        file.append(tmp)

    df = pd.DataFrame(file)
    
    return df
```



- 중간에 딕서너리 정보를 모양(?)객체로 만들어줘야 해서 shapely.geometry.shape 필요
  - 셀 그대로 복사해서 실행시키면 알아서 설치되고 import 됨
- 함수명 geojson_read

> usage

```python
어린이교통사고_격자 = geojson_read(파일경로+'2.오산시_어린이교통사고_격자.geojson')
```

> out

|      |        gid | accident_cnt |                                          geometry |
| ---: | ---------: | -----------: | ------------------------------------------------: |
|    0 | 다사551085 |            0 | (POLYGON ((126.9942156468143 37.17418235770403... |
|    1 | 다사551086 |            0 | (POLYGON ((126.9942096381632 37.17508373885349... |
|    2 | 다사551087 |            0 | (POLYGON ((126.9942036292448 37.17598511986466... |