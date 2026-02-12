final_df_list = []

for index,row in unique_locations.iterrows():

    s2_data, weather_timeseries = get_gee_timeseries_for_location(row)

    if s2_data and weather_timeseries is not None and not weather_timeseries.empty:

        location_subset_df = df[df['pond_coordinates']==row['pond_coordinates']].copy()

        location_subset_df['ndwi'] = s2_data.get('ndwi')
        location_subset_df['ndvi'] = s2_data.get('ndvi')

        merged_df = pd.merge(
            location_subset_df,
            weather_timeseries,
            on='date_only',
            how='left'
        )

        final_df_list.append(merged_df)

df_final = pd.concat(final_df_list)
df_final.dropna(inplace=True)

OUTPUT_PATH = os.path.join(BASE_PATH,"final_pond_gee_dataset_EFFICIENT.csv")

df_final.to_csv(OUTPUT_PATH,index=False)

print("Saved fused dataset:", OUTPUT_PATH)
