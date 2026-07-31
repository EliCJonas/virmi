# <p align="center">virmi</p>

<p align="center">
  <img src="https://img.shields.io/badge/Available_for-Auro-4c1" alt="Available for Auro" />
  <a href="https://vibescale.github.io/#4">
    <img src="https://vibescale.github.io/badge-bar/4.svg" alt="4/6 LGTM Copilot | Vibescale" />
  </a>
</p>

<p align="center">
  <i>A simple self-hosted web frontend for the VirusTotal API.</i>
</p>

---

## Features
- Look up files by MD5, SHA-1, or SHA-256 hash
- Upload files for scanning (with upload progress)
- Check URLs for threats

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- A free [VirusTotal API key](https://www.virustotal.com/gui/join-us)

## Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/EliCJonas/virmi.git
   cd virmi
   ```

2. Create a `.env` file with your API key:
   ```bash
   echo "VT_API_KEY=your_api_key_here" > .env
   ```

3. Build and run:
   ```bash
   docker compose up --build
   ```

4. Open http://localhost:5000 in your browser.
