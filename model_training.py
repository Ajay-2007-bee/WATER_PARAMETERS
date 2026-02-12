df_final = pd.read_csv(OUTPUT_PATH)

features_to_use = [
    'lat','long','month','day_of_year',
    'pond_coordinates','ndwi','ndvi','avg_temp_celsius'
]

categorical_features = ['pond_coordinates']

targets = ['ph','ammonia','dissolved_oxygen','chlorophyll']

for target in targets:

    X = df_final[features_to_use]
    y = df_final[target]

    X_train,X_test,y_train,y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    model = CatBoostRegressor(
        iterations=1500,
        learning_rate=0.05,
        depth=8,
        verbose=500,
        random_seed=42,
        cat_features=categorical_features,
        allow_writing_files=False
    )

    model.fit(X_train,y_train)

    predictions = model.predict(X_test)

    r2 = r2_score(y_test,predictions)

    print(target,"R2:",r2)

    model_path = os.path.join(
        BASE_PATH,
        f"final_pond_{target}_predictor.cbm"
    )

    model.save_model(model_path)

print("Training complete")
