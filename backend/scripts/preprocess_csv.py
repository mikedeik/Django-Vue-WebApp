import csv 
import pandas as pd
import os
import geopandas
from shapely import wkt
from EcoQuest.models import Category, Nomos, Perifereia
from decimal import Decimal
from io import StringIO

#this will probably be deleted
def find_category(filename):
    categories = []
    if filename == "AisthitikaDash.csv":
        categories.append("Αισθητικά Δάση")
        categories.append("Δάση")
    elif filename == "NaturaKaiProstateuomenes.csv":
        categories.append("Δίκτυο Natura 2000")
        categories.append("Προστατευόμενες περιοχές")
    elif filename == "LimnesElladas.csv":
        categories.append("Λίμνες Ελλάδας")
    elif filename == "EthnikaParka.csv":
        categories.append("Εθνικά Πάρκα")
    elif filename == "EthnikoiDrumoi.csv":
        categories.append("Εθνικοί Δρυμοί")
    elif filename == "KatafugiaAgriasZwhs.csv":
        categories.append("Καταφύγια Άγριας ζωής")
    elif filename == "AktesMeGalaziaShmaia.csv":
        categories.append("Ακτές με γαλάζια σημαία")
        categories.append("Ακτές")
    print(categories)
    return categories

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

#checks if coordinates are within the distance threshold
def within_distance_threshold(coords1, coords2):
    distance_threshold = 0.05
    point1 = wkt.loads(coords1)
    point2 = wkt.loads(coords2)
    distance = point1.distance(point2)
    return distance <= distance_threshold

#remvoves duplicate data entries based on the difference of longitude and latitude
def remove_duplicates(gdf, type):

    gdf['coords'] = gdf[type].astype(str)

    # Iterate over the GeoDataFrame to find and remove duplicate entries
    to_remove = []
    for i, row in gdf.iterrows():
        if i not in to_remove:
            for j, other_row in gdf.iterrows():
                if j != i and j not in to_remove:
                    if within_distance_threshold(row['coords'], other_row['coords']):
                        to_remove.append(j)

    #create a new GeoDataFrame without the duplicate entries
    gdf_unique = gdf.drop(to_remove)

    #remove the temporary 'coords' column
    gdf_unique = gdf_unique.drop('coords', axis=1)
    return gdf_unique

#creates the final dataframe that will be inserted intto the POI model
def create_final_dataframe(df, categoryIDs):

    categories = [categoryIDs for i in range(len(df))]
    new_df = df.copy()

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
    new_df['categories'] = categories
    new_df['nomos'] = nomosID
    new_df['perifereia'] = perifereiaID
    #rearrange order of columns
    new_df = new_df[['name', 'categories', 'perifereia', 'nomos', 'longitude', 'latitude']]

    return new_df

def preprocess(file, filename):

    #find the category corresponding to this file and save it to the database
    #TO BE CHANGED IN ALL PROBABILITY
    categories = find_category(filename)
    categoryIDs = []
    for category in categories:
        category_obj, created = Category.objects.get_or_create(Name=category)
        print(category_obj)
        categoryIDs.append(category_obj.CategoryId)
    #convert csv to dataframe
    df = pd.read_csv(file)

    column_names = [col for col in df.columns]

    #find the column that has the name of each data point
    name_col = find_column(column_names, "name")
    if name_col == None:
        print("No column name. Abort.")
        exit(127)

    #find the column that has the periphery of each data point
    periphery_col = find_column(column_names, "periphery")

    #find the column that has the prefecture of each data point
    if "NOMOS" in column_names:
        prefecture_col = "NOMOS"
    else:
        prefecture_col = find_column(column_names, "prefecture")


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

    new_df['the_geom'] = geopandas.GeoSeries.from_wkt(new_df["the_geom"])
    gdf = geopandas.GeoDataFrame(new_df, geometry="the_geom")
    
    ######################################
    
    gdf = gdf.set_crs(epsg=2100)   # Greek grid EPSG for geospatial data 

    # find what kind of geospatial data we have (POINT, POLYGON/MULTIPOLYGON)
    cell = df.iloc[0]['the_geom']
    flag=False
    type = "the_geom"
    if "POINT" in cell: 
        gdf['the_geom'] = gdf['the_geom'].to_crs(epsg=4326)    
        flag=True
    else:   # if the_geom contains POLYGON / MULTIPOLYGON find its center
        gdf['centroid'] = gdf.centroid
        gdf['centroid'] = gdf['centroid'].to_crs(epsg=4326) # ESPG: 4326 for longitude and latitude              
        type = "centroid"
    print(gdf.head(2))
    
    #######################
    gdf = remove_duplicates(gdf, type)

    #convert geodataframe to dataframe
    df = pd.DataFrame(gdf)

    #extract longitude and latitude columns from the_geom/centroid colunmn
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

    #create dataframe consisting of object ids (where appropriate)
    final_df = create_final_dataframe(df, categoryIDs)
    final_df.reset_index(drop=True, inplace=True)
    return final_df
            
    
