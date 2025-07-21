import polars as pl


def main() -> pl.DataFrame:
    data = pl.read_csv("data/mortality_data/IHME-GBD_2021_DATA-a7aeb2d1-1.csv")
    data = data.unique()
    data = data.select(["location_name", "year", "val"])
    data.columns = ["location_name", "year", "all_cause_deaths"]
    data = data.with_columns(pl.col("all_cause_deaths").cast(pl.Int64))

    # Sourced from the world bank
    # https://www.jspn.or.jp/uploads/uploads/files/english/119th_World_Bank_list_of_economies.pdf#:~:text=This%20table%20classifies%20all%20World,IDA
    incomes = pl.read_csv("data/other_data/incomes.csv", truncate_ragged_lines=True)
    data = data.join(incomes, on="location_name")
    data.write_csv("data/mortality_data/all_cause_deaths_by_year_by_country.csv")
    return data

if __name__ == "__main__":
    main()
