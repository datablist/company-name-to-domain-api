# Company Name to Domain API — Python examples

These are short learning examples. Start with the basic script for your preferred
HTTP library; the CSV version imports its `find_domains` function.

## Setup

Use Python 3.12 or newer. From this `python` folder:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
```

Create your key on the [Datablist API page](https://app.datablist.com/account/api).
Keep it out of source files and version control. These examples make real calls
that can consume credits; see the current
[pricing and limits](https://platform.datablist.com/docs/enrichments/tools/company-name-to-domain#credits-and-limits).

## Basic examples

**Synchronous, using requests:**

```sh
python sync_requests.py
```

**Asynchronous, using HTTPX:**

```sh
python async_httpx.py
```

Edit the `companies` list at the bottom of either script. Each prints the full
result objects, including status, outputs, credits used, and any per-row error.

Both scripts submit a background task, poll every three seconds, and read all
result pages. The requests version waits using blocking calls. The HTTPX version
uses `await` and `asyncio.sleep`. Neither runs multiple tasks concurrently.

Each basic script submits **one task, with at most 10,000 company names**.
For larger files, use a CSV example.

## CSV examples

The included [sample CSV](examples/companies.csv) has a `company_name` column
and additional columns that are preserved in the output.

```sh
python csv_sync_requests.py
python csv_async_httpx.py
```

These create `companies_sync_enriched.csv` and `companies_async_enriched.csv`.
Edit the paths at the bottom of each script to use your own files. For a
different company column, pass its name:

```python
process_csv("input.csv", "output_enriched.csv", api_key, company_column="Company")
```

In async code, use `await process_csv(...)`.

The scripts read UTF-8 CSV files with an optional BOM, submit up to 10,000 rows
at a time, and finish one batch before starting the next. Provide nonblank
company names. The API also enforces request-size limits; see the reference.

Original columns, row order, and duplicate company names are preserved. Results
are matched by `inputId` within each task. These columns are appended:

- `datablist_company_domain`
- `datablist_company_url`
- `datablist_domain_confidence`
- `datablist_status`
- `datablist_credits_used`
- `datablist_error_code`
- `datablist_error_message`

Existing output files are never overwritten. Choose a new output filename to
run the example again.

## When something fails

HTTP errors raise the library's normal exception. Failed or stopped tasks raise
an exception showing their task ID. A completed task can still contain per-row
errors or no matches; review the result statuses.

The examples do not retry requests or resume interrupted work. CSV batches
already written remain in the output, but that file may be incomplete. Stopping
a script does not cancel a submitted backend task. Before rerunning after an
interruption or lost response, inspect your
[task history](https://platform.datablist.com/docs/enrichments/tasks) to avoid
repeating paid work.
