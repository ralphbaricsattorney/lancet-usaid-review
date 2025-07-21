import polars as pl


def overall_bin_spends(
    data: pl.DataFrame,
    exclude_high_incomes: bool = False,
    exclude_upper_middle_incomes: bool = False
) -> pl.DataFrame:
    if exclude_high_incomes:
        data = data.filter(pl.col("income_group") != "High income")
    if exclude_upper_middle_incomes:
        data = data.filter(pl.col("income_group") != "Upper middle income")
    q1 = data.select(pl.col("per_capita_spend").quantile(0.25)).item()
    q2 = data.select(pl.col("per_capita_spend").quantile(0.50)).item()
    q3 = data.select(pl.col("per_capita_spend").quantile(0.75)).item()

    # Create a spend_quartile column using these thresholds
    data = data.with_columns([
        pl.when(pl.col("per_capita_spend") <= q1).then(1)
        .when(pl.col("per_capita_spend") <= q2).then(2)
        .when(pl.col("per_capita_spend") <= q3).then(3)
        .otherwise(4)
        .alias("spend_quartile_overall")
    ])

    # Add dummy variables for each quartile
    data = data.with_columns([
        (pl.col("spend_quartile_overall") == 1).alias("is_q1_overall"),
        (pl.col("spend_quartile_overall") == 2).alias("is_q2_overall"),
        (pl.col("spend_quartile_overall") == 3).alias("is_q3_overall"),
        (pl.col("spend_quartile_overall") == 4).alias("is_q4_overall")
    ])
    return data

def by_year_bin_spends(
    data: pl.DataFrame,
    exclude_high_incomes: bool = False,
    exclude_upper_middle_incomes: bool = False
) -> pl.DataFrame:
    if exclude_high_incomes:
        data = data.filter(pl.col("income_group") != "High income")
    if exclude_upper_middle_incomes:
        data = data.filter(pl.col("income_group") != "Upper middle income")
    data = data.with_columns([
        pl.when(
            pl.col("per_capita_spend") <= pl.col("per_capita_spend")
            .quantile(0.25)
            .over("year")
        ).then(1)
        .when(
            pl.col("per_capita_spend") <= pl.col("per_capita_spend")
            .quantile(0.50)
            .over("year")
        ).then(2)
        .when(
            pl.col("per_capita_spend") <= pl.col("per_capita_spend")
            .quantile(0.75)
            .over("year")
        ).then(3)
        .otherwise(4)
        .alias("spend_quartile")
    ])

    # dummies
    data = data.with_columns([
        (pl.col("spend_quartile") == 1).alias("is_q1_by_year"),
        (pl.col("spend_quartile") == 2).alias("is_q2_by_year"),
        (pl.col("spend_quartile") == 3).alias("is_q3_by_year"),
        (pl.col("spend_quartile") == 4).alias("is_q4_by_year")
    ])
    return data


def main() -> None:
    mortality = pl.read_csv("data/mortality_data/all_cause_deaths_by_year_by_country.csv")
    exposures = pl.read_csv("data/exposure_data/usaid_disbursements.csv")
    bridge = pl.read_csv("data/other_data/exposure_mortality_country_bridge.csv")
    data = mortality.join(
        bridge,
        left_on="location_name",
        right_on="mortality_country_name"
    ).join(
        exposures,
        left_on=["year", "exposure_country_name"],
        right_on=["Fiscal Year", "Country Name"]
    )
    overall_bin_spends(
        by_year_bin_spends(data)
    ).write_csv("data/flattened_data/all_income_flattened_data.csv")

    overall_bin_spends(
        by_year_bin_spends(
        data,
        exclude_high_incomes=True
    ), exclude_high_incomes=True
    ).write_csv("data/flattened_data/non_high_income_data.csv")

    overall_bin_spends(
        by_year_bin_spends(
            data,
            exclude_upper_middle_incomes=True,
            exclude_high_incomes=True
        ),
        exclude_upper_middle_incomes=True,
        exclude_high_incomes=True
    ).write_csv("data/flattened_data/low_income_data.csv")
    return
    
    
if __name__ == "__main__":
    main()