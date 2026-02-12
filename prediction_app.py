print("\n" + "="*50)
print(" " * 8 + "PHASE 3: PREDICTION APPLICATION")
print("="*50)

try:
    predictor_ph = CatBoostRegressor().load_model(os.path.join(BASE_PATH, "final_pond_ph_predictor.cbm"))
    predictor_ammonia = CatBoostRegressor().load_model(os.path.join(BASE_PATH, "final_pond_ammonia_predictor.cbm"))
    predictor_do = CatBoostRegressor().load_model(os.path.join(BASE_PATH, "final_pond_dissolved_oxygen_predictor.cbm"))
    predictor_chlorophyll = CatBoostRegressor().load_model(os.path.join(BASE_PATH, "final_pond_chlorophyll_predictor.cbm"))
    print("\n✅ All prediction models loaded successfully.")
except Exception as e:
    assert False, f"Could not load saved models. Error: {e}"

print("\nPlease provide the following for a new prediction:")

try:
    lat_input = float(input("Enter Latitude (e.g., 16.6224): "))
    lon_input = float(input("Enter Longitude (e.g., 81.0819): "))
    date_input = input("Enter Date and Time (e.g., '2024-05-15 10:00'): ")

    input_timestamp = pd.to_datetime(date_input)
    input_date_only = input_timestamp.date()

    print("\nFetching satellite and weather data for your input location...")

    s2_data, weather_timeseries = get_gee_timeseries_for_location({
        'lat': lat_input,
        'long': lon_input,
        'pond_coordinates': 'new_prediction_point'
    })

    if s2_data and weather_timeseries is not None:

        temp_for_date_row = weather_timeseries[
            weather_timeseries['date_only'] == input_date_only
        ]

        if not temp_for_date_row.empty:

            avg_temp = temp_for_date_row['avg_temp_celsius'].iloc[0]

            input_coord_string = f"{lat_input},{lon_input}"

            new_data = {
                'lat': lat_input,
                'long': lon_input,
                'month': input_timestamp.month,
                'day_of_year': input_timestamp.dayofyear,
                'pond_coordinates': input_coord_string,
                'ndwi': s2_data.get('ndwi'),
                'ndvi': s2_data.get('ndvi'),
                'avg_temp_celsius': avg_temp
            }

            prediction_df = pd.DataFrame([new_data])

            predicted_ph = predictor_ph.predict(prediction_df)[0]
            predicted_ammonia = predictor_ammonia.predict(prediction_df)[0]
            predicted_do = predictor_do.predict(prediction_df)[0]
            predicted_chlorophyll = predictor_chlorophyll.predict(prediction_df)[0]

            print("\n" + "="*40)
            print("      WATER QUALITY PREDICTION REPORT")
            print("="*40)
            print(f"For coordinates: ({lat_input}, {lon_input})")
            print(f"On Date:         {date_input}")
            print("-"*40)
            print("PREDICTED VALUES:")
            print(f"  pH:               {predicted_ph:.4f}")
            print(f"  Ammonia:          {predicted_ammonia:.4f} mg/L")
            print(f"  Chlorophyll:      {predicted_chlorophyll:.4f} µg/L (est.)")
            print(f"  Dissolved Oxygen: {predicted_do:.4f} mg/L")
            print("="*40)

        else:
            print(f"❌ Prediction failed. Weather data was not available for the specific date: {input_date_only}")

    else:
        print("❌ Prediction failed. Could not retrieve satellite/weather data for the given location.")

except ValueError:
    print("\n❌ Invalid input. Please ensure coordinates are numbers and date is in a valid format.")

except Exception as e:
    print(f"\nAn error occurred during prediction: {e}")
