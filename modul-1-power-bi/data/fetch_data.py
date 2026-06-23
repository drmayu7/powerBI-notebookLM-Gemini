"""Download and pin the open datasets used by Modul 1 to local CSV.

Source: data.gov.my (MOH) and DOSM open data. Run from anywhere:
    python modul-1-power-bi/data/fetch_data.py
"""
from pathlib import Path
import duckdb

OUT = Path(__file__).parent
SOURCES = {
    "covid_deaths_linelist":
        "https://storage.data.gov.my/healthcare/covid_deaths_linelist.parquet",
    "covid_cases":
        "https://storage.data.gov.my/healthcare/covid_cases.parquet",
}
POP_URL = "https://storage.dosm.gov.my/population/population_state.parquet"


def main() -> None:
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")

    for name, url in SOURCES.items():
        dest = OUT / f"{name}.csv"
        con.execute(f"COPY (SELECT * FROM read_parquet('{url}')) "
                    f"TO '{dest.as_posix()}' (HEADER, DELIMITER ',')")
        n = con.execute(f"SELECT count(*) FROM read_parquet('{url}')").fetchone()[0]
        print(f"{name}: {n} rows -> {dest.name}")

    # Population: pre-filter to the 'overall' state totals (one row per state-year).
    pop_dest = OUT / "population_state.csv"
    con.execute(f"""
        COPY (
            SELECT state, date, population
            FROM read_parquet('{POP_URL}')
            WHERE sex = 'both' AND age = 'overall' AND ethnicity = 'overall'
            ORDER BY date, state
        ) TO '{pop_dest.as_posix()}' (HEADER, DELIMITER ',')
    """)
    n = con.execute(f"""
        SELECT count(*) FROM read_parquet('{POP_URL}')
        WHERE sex='both' AND age='overall' AND ethnicity='overall'
    """).fetchone()[0]
    print(f"population_state (filtered): {n} rows -> {pop_dest.name}")


if __name__ == "__main__":
    main()
