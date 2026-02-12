df = pd.read_csv(TABULAR_DATA_PATH)

df.columns = df.columns.str.strip().str.lower()

def parse_coords(coord_str):
    if not isinstance(coord_str, str): return None, None
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", coord_str)
    if len(numbers) == 2: return float(numbers[0]), float(numbers[1])
    return None, None

df[['lat','long']] = df['pond_coordinates'].apply(lambda x: pd.Series(parse_coords(x)))

df['timestamp'] = pd.to_datetime(df['date'], errors='coerce')
df['date_only'] = df['timestamp'].dt.date
df['month'] = df['timestamp'].dt.month
df['day_of_year'] = df['timestamp'].dt.dayofyear
df['hour'] = 0

numeric_cols = ['ph','ammonia','dissolved_oxygen','chlorophyll','lat','long']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(subset=['timestamp','lat','long','ph','ammonia','dissolved_oxygen','chlorophyll'], inplace=True)

print("Cleaned rows:", len(df))
