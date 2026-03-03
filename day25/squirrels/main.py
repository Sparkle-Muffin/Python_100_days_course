from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
squirrels_data_path = BASE_DIR / "2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv"
squirrel_count_path = BASE_DIR / "squirrel_count.csv"

squirrels_data = pd.read_csv(squirrels_data_path)

black_squirrels_num = len(squirrels_data[squirrels_data["Primary Fur Color"] == "Black"])
gray_squirrels_num = len(squirrels_data[squirrels_data["Primary Fur Color"] == "Gray"])
cinnamon_squirrels_num = len(squirrels_data[squirrels_data["Primary Fur Color"] == "Cinnamon"])

squirrels_num_data = {
    "Color": ["Black", "Gray", "Cinnamon"],
    "Count": [black_squirrels_num, gray_squirrels_num, cinnamon_squirrels_num]
}

squirrels_num_df = pd.DataFrame(squirrels_num_data)
squirrels_num_df.to_csv(squirrel_count_path)
