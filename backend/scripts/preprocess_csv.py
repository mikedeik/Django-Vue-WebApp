import csv 
import pandas as pd
import os
import geopandas
from shapely import wkt
from EcoQuest.models import Category, Nomos, Perifereia
from decimal import Decimal

def find_category(filename):
    category = ""
    if filename == "AisthitikaDash.csv":
        category = "Αισθητικά Δάση"
    elif filename == "NaturaKaiProstateuomenes.csv":
        category = "Δίκτυο Natura 2000 και προστατευόμενες περιοχές"
    elif filename == "LimnesElladas.csv":
        category = "Λίμνες Ελλάδας"
    elif filename == "EthnikaParka.csv":
        category = "Εθνικά Πάρκα"
    elif filename == "EthnikoiDrumoi.csv":
        category = "Εθνικοί Δρυμοί"
    elif filename == "KatafugiaAgriasZwhs.csv":
        category = "Καταφύγια Άγριας ζωής"
    elif filename == "AktesMeGalaziaShmaia.csv":
        category = "Ακτές με γαλάζια σημαία"
    return category

def find_column(columns, literal):
    if literal.upper() in columns:
        return literal.upper()
    for col in columns:
        temp = col
        temp = temp.lower()
        if literal.lower() in temp:
            return col
    return None

def process_point_coordinate(point):
    point = str(point)
    point = point[7:len(point)-1]
    point = point.split(" ")
    return point

#creates the final dataframe that will be inserted intto the POI model
def create_final_dataframe(df, category_obj):
    category = [category_obj.CategoryId for i in range(len(df))]
    new_df = df.copy()
    print(new_df)

    nomosID = []
    perifereiaID = []
    column_names = [col for col in df.columns]
    for i in range(len(df)):
        if "nomos" in column_names:
            cell = df.iloc[i]['nomos']
            nomos_obj, created = Nomos.objects.get_or_create(Name=cell)
            nomosID.append(nomos_obj.NomosId)
        else:
            nomosID.append(None)
        if "perifereia" in column_names:
            cell = df.iloc[i]['perifereia']
            perifereia_obj, created = Perifereia.objects.get_or_create(Name=cell)
            perifereiaID.append(perifereia_obj.PerifereiaId)
        else:
            perifereiaID.append(None)

    #add category column
    new_df['category'] = category
    new_df['nomos'] = nomosID
    new_df['perifereia'] = perifereiaID
    #rearrange order of columns
    new_df = new_df[['name', 'category', 'perifereia', 'nomos', 'longitude', 'latitude']]

    # remove_duplicates(new_df)
    # print(new_df)
    return new_df

def preprocess(file):
    print("Hello this is your script!")

    #check if path to directory of data is given
    print(file)

    #find the category corresponding to this file and save it to the database
    category = find_category(file)
    category_obj, created = Category.objects.get_or_create(Name=category)

    #convert csv to dataframe
    df = pd.read_csv(file)
    print(df.head(3))

    column_names = [col for col in df.columns]

    #find the column that has the name of each data point
    name_col = find_column(column_names, "name")
    if name_col == None:
        print("No column name. Abort.")
        exit(127)

    #find the column that has the periphery of each data point
    periphery_col = find_column(column_names, "periphery")
    if periphery_col == None:
        print("No periphery column. Abort.")
    # print(periphery_col)

    #find the column that has the prefecture of each data point
    if "NOMOS" in column_names:
        prefecture_col = "NOMOS"
    else:
        prefecture_col = find_column(column_names, "prefecture")
    if prefecture_col == None:
        print("No prefecture column. Abort.")
    # print(prefecture_col)

    #convert to another dataframe only with the needed data
    if periphery_col == None:
        if prefecture_col == None:
            new_df = df[[name_col, 'the_geom']].copy()
            new_df.rename(columns={name_col: 'name'}, inplace=True)
        else:
            new_df = df[[name_col, prefecture_col, 'the_geom']].copy()
            new_df.rename(columns={name_col: 'name', prefecture_col: 'nomos'}, inplace=True)
    else:
        if prefecture_col != None:
            new_df = df[[name_col, periphery_col, prefecture_col, 'the_geom']].copy()
            new_df.rename(columns={name_col: 'name', periphery_col: 'perifereia', prefecture_col: 'nomos'}, inplace=True)
        else:
            new_df = df[[name_col, periphery_col, 'the_geom']].copy()
            new_df.rename(columns={name_col: 'name', periphery_col: 'perifereia'}, inplace=True)

    print(new_df.head(2))
    new_df['the_geom'] = geopandas.GeoSeries.from_wkt(new_df["the_geom"])
    gdf = geopandas.GeoDataFrame(new_df, geometry="the_geom")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(gdf.head(2))
    
    ######################################
    
    gdf = gdf.set_crs(epsg=2100)   #UTM zone 34 (previously 32634)

    # find what kind of geospatial data we have (POINT, POLYGON/MULTIPOLYGON)
    cell = df.iloc[0]['the_geom']
    flag=False
    if "POINT" in cell: 
        gdf['the_geom'] = gdf['the_geom'].to_crs(epsg=4326)    
        flag=True
    else:   # if the_geom contains POLYGON / MULTIPOLYGON find its center
        gdf['centroid'] = gdf.centroid
        gdf['centroid'] = gdf['centroid'].to_crs(epsg=4326) # ESPG: 4326 for longitude and latitude              

    print(gdf.head(2))
    
    #convert geodataframe to dataframe
    df = pd.DataFrame(gdf)

    #extract longitude and latitude from the_geom/centroid colunmn
    longitude = []
    latitude = []
    if flag == False:
        for i in range(len(df)):
            point = process_point_coordinate(df.iloc[i]['centroid'])
            longitude.append(Decimal(point[0]))
            latitude.append(Decimal(point[1]))
        df = df.drop('centroid', axis=1)
    else:
        for i in range(len(df)):
            point = process_point_coordinate(df.iloc[i]['the_geom'])
            longitude.append(Decimal(point[0]))
            latitude.append(Decimal(point[1]))
    df = df.drop('the_geom', axis=1)

    df['longitude'] = longitude
    df['latitude'] = latitude
    print('---------------------------------------------')
    print(df.head(3))

    #create dataframe consisting of object ids (where appropriate)
    final_df = create_final_dataframe(df, category_obj)
    print("------------------------END------------------")
    return final_df
            
    
