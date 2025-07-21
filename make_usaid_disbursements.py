import polars as pl


def main() -> pl.DataFrame:
    # sourced from https://foreignassistance.gov/data
    disbursements = pl.read_csv("data/exposure_data/us_foreign_aid_funding.csv")

    # sourced from https://datahub.io/core/population/r/population.csv
    # slightly modified country names to make the join clean.
    populations = pl.read_csv("data/other_data/population.csv", ignore_errors=True)
    disbursements = disbursements.filter(
        (pl.col("Transaction Type Name") == "Disbursements") &
        (pl.col("Country Name") != "World") &
        (pl.col("Funding Agency Name") == "U.S. Agency for International Development")
    )
    disbursements = disbursements.with_columns(
        pl.col("Country Name")
        .str.to_lowercase()
        .str.contains("region", literal=True)
        .alias("contains_region")
    )
    disbursements = disbursements.filter(pl.col("contains_region") == False)
    disbursements = disbursements.select(
        ["Country Name", "Fiscal Year", "current_amount", "constant_amount"]
    ).group_by(["Country Name", "Fiscal Year"]).sum()
    disbursements = disbursements.filter(pl.col("current_amount") > 0)
    disbursements = disbursements.filter((pl.col("Fiscal Year") < 2024) & (pl.col("Fiscal Year") > 2000))
    disbursements = disbursements.join(
        populations,
        left_on=["Country Name", "Fiscal Year"],
        right_on=["Country Name", "Year"],
    )
    disbursements = disbursements.rename({"Value": "population"})
    disbursements = disbursements.with_columns(
        per_capita_spend=pl.col("current_amount") / pl.col("population")
    )
    disbursements.write_csv("data/exposure_data/usaid_disbursements.csv")
    return disbursements


if __name__ == "__main__":
    main()