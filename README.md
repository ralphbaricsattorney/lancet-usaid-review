# lancet-usaid-review

This is the data and code underlying the reproduction analysis written up [here](https://goflaw.substack.com/p/i-tried-reproducing-that-lancet-study?r=41a8s8).

## Data Assembly

`pip` install the polars requirement inside a fresh conda environment

`pip install -r requirements.txt`

The intermediate data problems are already checked in in `data`. To recreate the mortality data run

`python make_gbd_mortality.py` and to create the USAID disbursement and exposure data run

`python make_usaid_disbursements.py`

and then run `python join.py` to join them together into the flat files in `/data/flattened_files`

## Regressions

Each regression model variant is instantiated as a method in `regressions.R`. You can load up whatever
flattened data file you want and call the desired regression method to analyze it. 