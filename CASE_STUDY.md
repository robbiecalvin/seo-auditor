# Technical case study: SEO Auditor

## Problem
Manual technical SEO reviews are repetitive and difficult to compare across pages.

## Approach
A Python CLI recursively crawls internal links, captures page status and timing, checks metadata and image alt attributes, identifies duplicate metadata and broken links, and produces CSV and HTML reports. Docker provides a documented execution option.

```mermaid
flowchart LR
 A[Target URL] --> B[Crawler]
 B --> C[Page and link analysis]
 C --> D[CSV and HTML reports]
 D --> E[Optional SMTP delivery]
```

## Reproduction
Use an authorized test site with known metadata and broken links.

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m seo_auditor.cli https://example.com
```

## Evidence
[README](README.md) documents CLI and Docker usage. [Testing](TESTING.md) describes verification and dependency auditing.

## Limitations
A passing dependency audit is not a functional crawler test. No measured SEO ranking improvement, crawl throughput or comprehensive accuracy benchmark is claimed. Keep SMTP credentials out of Git.

## Resume summary
Developed a Python technical SEO crawler with automated metadata checks, structured reporting and containerized execution.

## Verified CI evidence — 2026-11-25

pip-audit reported no known vulnerabilities in the audited requirements. This is not a functional crawler test or a security guarantee.

- [GitHub Actions run](https://github.com/robbiecalvin/seo-auditor/actions/runs/45641459553)
- [Tested revision](https://github.com/robbiecalvin/seo-auditor/commit/7cebd91c0075ce058e13687b19e160d70eb34972)

Results were inspected from completed job logs. They apply to the linked revision and executed checks only.
