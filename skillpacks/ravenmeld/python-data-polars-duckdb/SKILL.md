---
name: python-data-polars-duckdb
description: |
  Practical data engineering workflows with Polars + DuckDB: fast local analytics, Parquet, and repeatable ETL patterns.
---

# Python Data: Polars + DuckDB

## Use When

- You want fast local analytics without spinning up a database.
- You work with Parquet/CSV/JSON and need reliable transforms.
- You want a repeatable ETL pattern that scales from laptop to server.

## Workflow

1. Use Polars for dataframe transforms (fast + memory-efficient).
2. Use DuckDB for SQL over files (Parquet/CSV) and joins/aggregations.
3. Persist intermediate results to Parquet (columnar, compressible, portable).
4. Validate with small invariants (row counts, null rates, schema checks).

## Install

```bash
python -m pip install -U polars duckdb pyarrow
```

## Example: Polars Read + Write Parquet

```python
import polars as pl

df = pl.read_csv("input.csv")
df = df.with_columns(pl.col("amount").cast(pl.Float64))
df.write_parquet("output.parquet")
```

## Example: DuckDB SQL Over Parquet

```python
import duckdb

con = duckdb.connect()
rows = con.execute(
    "select country, count(*) as n from 'output.parquet' group by country order by n desc"
).fetchall()
print(rows[:10])
```

## Example: Hybrid Pattern (Polars -> DuckDB)

```python
import polars as pl
import duckdb

df = pl.read_parquet("output.parquet")
con = duckdb.connect()
con.register("t", df.to_arrow())
print(con.execute("select avg(amount) from t").fetchone())
```

## Tips

- Prefer Parquet for intermediate storage (faster + smaller than CSV).
- Use explicit schema casts early to avoid silent type drift.
- Always log a small summary (row count, column list, key stats) for debugging.

