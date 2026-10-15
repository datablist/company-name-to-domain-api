"""Add company website domains to a CSV using the async HTTPX API example.

Read company names from a UTF-8 CSV, submit up to 10,000 rows per task, and
write the results alongside the original columns. Await each batch before
starting the next. CSV file reading and writing use ordinary synchronous I/O.

Set DATABLIST_API_KEY and run: python csv_async_httpx.py
Edit the input/output paths at the bottom; the default company column is
company_name. The output must be a new file. Calls can consume credits, and a
failure leaves an incomplete output containing the batches already saved.
"""

import asyncio
import csv
import os
from itertools import batched

from async_httpx import find_domains


async def process_csv(
    input_path: str,
    output_path: str,
    api_key: str,
    company_column: str = "company_name",
) -> None:
    """Keep the original columns and await each batch before starting the next."""
    result_columns = [
        "datablist_company_domain",
        "datablist_company_url",
        "datablist_domain_confidence",
        "datablist_status",
        "datablist_credits_used",
        "datablist_error_code",
        "datablist_error_message",
    ]

    with open(input_path, encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        source_columns = reader.fieldnames or []
        if company_column not in source_columns:
            raise ValueError(f"Missing CSV column: {company_column}")
        if set(source_columns).intersection(result_columns):
            raise ValueError("The CSV already contains enrichment result columns.")

        # 'x' creates a new file and refuses to overwrite an existing one.
        with open(output_path, "x", encoding="utf-8", newline="") as output:
            output_columns = source_columns + result_columns
            writer = csv.DictWriter(output, fieldnames=output_columns)
            writer.writeheader()

            batches = batched(reader, 10_000)
            for batch in batches:
                companies = [row[company_column] for row in batch]
                results = await find_domains(companies, api_key)
                results_by_input_id = {result["inputId"]: result for result in results}

                for index, row in enumerate(batch, start=1):
                    input_id = f"row-{index}"
                    result = results_by_input_id[input_id]
                    outputs = result["outputs"]
                    error = result.get("error") or {}
                    enriched_row = {
                        **row,
                        "datablist_company_domain": outputs.get("companyDomain", ""),
                        "datablist_company_url": outputs.get("companyUrl", ""),
                        "datablist_domain_confidence": outputs.get("domainConfidence", ""),
                        "datablist_status": result["status"],
                        "datablist_credits_used": result["creditsUsed"],
                        "datablist_error_code": error.get("code", ""),
                        "datablist_error_message": error.get("message", ""),
                    }
                    writer.writerow(enriched_row)
                output.flush()
                print(f"Saved {len(batch)} rows to {output_path}")


async def main() -> None:
    api_key = os.environ["DATABLIST_API_KEY"]
    input_path = "examples/companies.csv"
    output_path = "companies_async_enriched.csv"

    await process_csv(input_path, output_path, api_key)


if __name__ == "__main__":
    asyncio.run(main())
