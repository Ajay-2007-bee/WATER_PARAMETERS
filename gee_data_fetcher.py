unique_locations = df.drop_duplicates(subset=['pond_coordinates'])

def get_gee_timeseries_for_location(row):
    try:
        point = ee.Geometry.Point(row['long'], row['lat'])
        start_date = '2019-01-01'
        end_date = '2025-10-11'

        s2_image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')\
            .filterBounds(point)\
            .filterDate(start_date, end_date)\
            .sort('CLOUDY_PIXEL_PERCENTAGE')\
            .first()

        if s2_image is None: return None, None

        ndwi = s2_image.normalizedDifference(['B3','B8']).rename('ndwi')
        ndvi = s2_image.normalizedDifference(['B8','B4']).rename('ndvi')

        s2_features = ndwi.addBands(ndvi).reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10
        ).getInfo()

        era5_daily = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')\
            .filterDate(start_date, end_date)\
            .select('temperature_2m')

        def extract_values(image):
            mean_temp = image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=11132
            ).get('temperature_2m')

            return ee.Feature(None,{
                'date': image.date().format('YYYY-MM-dd'),
                'avg_temp_celsius': mean_temp
            })

        weather_info = era5_daily.map(extract_values).getInfo()

        dates = [f['properties']['date'] for f in weather_info['features']]
        temps = [f['properties']['avg_temp_celsius'] for f in weather_info['features']]

        temps_celsius = [t-273.15 if t is not None else None for t in temps]

        weather_df = pd.DataFrame({
            'date_str': dates,
            'avg_temp_celsius': temps_celsius
        })

        weather_df['date_only'] = pd.to_datetime(weather_df['date_str']).dt.date

        return s2_features, weather_df[['date_only','avg_temp_celsius']]

    except:
        return None, None
