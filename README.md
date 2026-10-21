# Company Name to Domain API

Find a company's website domain from its name with the
[Datablist](https://www.datablist.com/) Company Name to Domain API.

Send company names as JSON and get matching domains, website URLs, and confidence
levels when available. Use the results to add websites to CRM records, enrich
company lists, or prepare domains for contact-finding workflows.

The default workflow searches a company dataset first, then uses Google search
for names it could not match. You can also choose dataset-only or Google-only
lookups in the [API settings](https://platform.datablist.com/docs/enrichments/tools/company-name-to-domain#settings).

- **Bulk company name to domain lookup:** send up to 10,000 company names per task,
  within the API's request-size limits.
- **Match confidence:** use the returned confidence level to decide which
  company websites need a manual review.
- **Standalone API:** use the results in your own application without creating
  a Datablist workspace or uploading a spreadsheet to the app.

## Get started

Choose [Python](python/README.md) or [TypeScript](typescript/README.md).
The commands below use Python.

To try the API from your terminal, jump to the [cURL example](#try-with-curl).

1. [Create a Personal API Key](https://app.datablist.com/account/api).
2. With Python 3.12 or newer, run the commands below from this repository's root.
3. Edit the `companies` list in the script to look up your own company names.

```sh
cd python
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
python sync_requests.py
```

See the [Python setup guide](python/README.md#setup) for virtual environment
instructions. Calls can consume account credits; check the
[current pricing](https://platform.datablist.com/docs/enrichments/tools/company-name-to-domain#credits-and-limits)
before running the examples.

## Try with cURL

Create a [Personal API Key](https://app.datablist.com/account/api), then set it
in your terminal:

```sh
export DATABLIST_API_KEY='your-personal-api-key'
```

**1. Submit a company name.**

```sh
curl --request POST 'https://api.datablist.com/v1/enrichments/tasks' \
  --header "X-API-Key: $DATABLIST_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "enrichmentId": "company-name-to-domain",
    "uniqueId": "company-domain-curl-001",
    "settings": {"workflow": "dataset_google"},
    "inputs": [
      {"inputId": "row-1", "data": {"companyName": "Datablist"}}
    ]
  }'
```

The response contains the task ID in `@id`. Copy that value into `TASK_ID` below.
Use a new `uniqueId` when submitting a new task.

**2. Check the task status.**

```sh
TASK_ID='paste-returned-task-id'

curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

Repeat the status command every few seconds until `status` is `completed`,
`failed`, or `stopped`.

**3. Retrieve the results.**

```sh
curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID/results" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

The response contains a `results` array like the [output example](#output-domain-website-url-and-confidence)
below. Failed or stopped tasks can also contain useful results.

## Input and output

### Input: company names

Send a JSON request to the enrichment task endpoint with your API key:

```http
POST https://api.datablist.com/v1/enrichments/tasks
X-API-Key: YOUR_PERSONAL_API_KEY
Content-Type: application/json
```

Request body:

```json
{
  "enrichmentId": "company-name-to-domain",
  "uniqueId": "company-domain-example-001",
  "settings": {
    "workflow": "dataset_google"
  },
  "inputs": [
    {
      "inputId": "row-1",
      "data": {
        "companyName": "Datablist"
      }
    }
  ]
}
```

Use a new `uniqueId` for each new task. Add more objects to `inputs` to look up
several companies; give each one its own `inputId` to match it to the result.

### Output: domain, website URL, and confidence

The POST returns `202 Accepted` with a task ID. Processing runs in the background.
Check `GET /v1/enrichments/tasks/TASK_ID` until the task finishes, then read
`GET /v1/enrichments/tasks/TASK_ID/results`.

Illustrative results response (sample task ID, data, and credit amount):

```json
{
  "taskId": "00000000000040008000000000000001",
  "results": [
    {
      "inputId": "row-1",
      "status": "success",
      "outputs": {
        "companyDomain": "datablist.com",
        "companyUrl": "https://www.datablist.com",
        "domainConfidence": "High"
      },
      "creditsUsed": "1",
      "error": null
    }
  ],
  "nextCursor": null
}
```

`inputId` links the result to the company you sent. A lookup can also return
`no_result`, `error`, or `skipped`. Output fields depend on the settings and data
found; a domain is not guaranteed. Follow `nextCursor` when more result pages
are available.

## Python examples

The examples handle task submission, polling, and result pagination for you.
Each basic file is self-contained and shows the HTTP calls step by step.

| Example | What it shows |
| --- | --- |
| [Synchronous requests](python/sync_requests.py) | Look up a list of company names with blocking HTTP calls. |
| [Asynchronous HTTPX](python/async_httpx.py) | Use `async` and `await` for the same API workflow. |
| [CSV processing with requests](python/csv_sync_requests.py) | Add domains to a CSV in sequential batches of up to 10,000 rows. |
| [CSV processing with async HTTPX](python/csv_async_httpx.py) | Await each batch and write results alongside the original CSV columns. |

See the [Python README](python/README.md) for CSV instructions and customization.

## TypeScript example

Use [the standalone TypeScript example](typescript/example.ts) with Node.js 24.3+;
no packages to install. From the repository root:

```sh
export DATABLIST_API_KEY='your-personal-api-key'
node typescript/example.ts
```

Or run with `tsx`, without installing it globally:

```sh
npx tsx typescript/example.ts
```

See the [TypeScript guide](typescript/README.md) for editable inputs and settings.

## Documentation

- [Company Name to Domain API](https://platform.datablist.com/docs/enrichments/tools/company-name-to-domain)
- [Enrichments API quickstart](https://platform.datablist.com/docs/enrichments/quickstart)
- [Task lifecycle](https://platform.datablist.com/docs/enrichments/tasks)

## Other Datablist API examples

- [Company Name Cleaner API](https://github.com/datablist/company-name-cleaner-api): clean and standardize company names.
- [LinkedIn Profile Finder API](https://github.com/datablist/linkedin-profile-finder-api): find profiles from names and company keywords.
- [Impressum Scraper API](https://github.com/datablist/impressum-scraper-api): extract business details from website Impressum pages.
