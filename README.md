# caknak-supa

This repository automates the retrieval and storage of ransomware victim data for ASEAN countries using the [Ransomware.live API](https://ransomware.live/). It is curated specifically to support analysis and visualization of regional cybersecurity trends.

## What This Does

- Fetches the latest ransomware victim data from `https://api.ransomware.live/v2`
- Filters results to only ASEAN countries:
  `Malaysia, Singapore, Indonesia, Thailand, Philippines, Vietnam, Brunei, Myanmar, Cambodia, Laos`
- Cleans and formats the data
- Uploads it to a [Supabase](https://supabase.com) PostgreSQL database
- Automatically runs daily using GitHub Actions

## 🗂Repo Structure

- `sync_asean_ransomware.py` — the main sync script
- `requirements.txt` — packages used
- `.github/workflows/sync.yml` — GitHub Action for scheduled syncing

## Sync Frequency

This project is set to **automatically sync once per day** at 1AM UTC. You can also manually trigger it via GitHub Actions.

## Technologies

- Python 3.11
- Supabase Python Client
- GitHub Actions (CI/CD)
- Pandas + Requests

## Disclaimer

This tool is for **educational and analytical purposes only**. It does not exfiltrate, store, or distribute any private or malicious content. Data is sourced from publicly available disclosures on Ransomware.live.
