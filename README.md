# Namibia Car-Import Landed-Cost Calculator

A Namibian sees a car price online (FOB at the auction, or CIF to Walvis Bay). That price is **not** what the car costs on the road in Windhoek. This app turns that one price into the full landed-cost breakdown in NAD — every Namibian tax and fee on its own line, every line citing its source, every uncertain number flagged.

Built for the AWS "For The People" Hackathon (25 July 2026).

## Run locally

```bash
python3 -m venv .venv          # Windows: py -m venv .venv
source .venv/bin/activate      # Windows (PowerShell): .venv\Scripts\Activate.ps1
python3 -m pip install -r requirements.txt
python3 app.py                 # Windows: py app.py
# open http://localhost:5000
```

If port 5000 is already in use on your machine, run on another port:

```bash
PORT=5005 python3 app.py        # Windows (PowerShell): $env:PORT='5005'; py app.py
```

## How it works

Enter the price you saw (USD), whether it is FOB or CIF, where the car is coming from, and a USD→NAD rate (click *Use today's rate* to pull it live). The app computes the landed cost and shows it line by line — FOB, freight, insurance, customs duty, excise, VAT, environmental levy, port charges, clearing, inland transport, NaTIS registration — each with its source and a confidence flag.

- **Customs duty is a range (18–25%)** because public sources conflict by engine size and fuel type. You pick the value inside the range; the default is 20%. Confirm the exact subheading at etariff.namra.org.na.
- **Every uncertain line is flagged** on screen with its source, instead of being given a false-exact number.

## What this is (and isn't)

This is a **planning estimate**, not a NamRA quotation. You do **not** confirm every line with a clearing agent — only the flagged ones. Most of the breakdown is firm and cited: VAT, the environmental levy, NaTIS registration, port charges, and the ad-valorem excise are known numbers. Only two things actually move: the **customs duty** (a range, because the sources conflict) and a couple of **broker quotes** (freight, the clearing fee). The app flags exactly those.

So you walk into the clearing agent already knowing the structure, the sources, and the ballpark — and you ask them to confirm only the flagged lines, instead of walking in blind and trusting whatever number they hand you. That is the point of this.

## Run on a server

```bash
python3 -m pip install -r requirements.txt
PORT=5000 python3 app.py
```

Open the firewall to TCP 5000 (on AWS EC2: the security group inbound, from `0.0.0.0/0`). Then `http://<server-ip>:5000`. For port 80: `sudo PORT=80 python3 app.py`.

To keep it running after you close SSH (systemd):

```bash
sudo tee /etc/systemd/system/carcalc.service >/dev/null <<'EOF'
[Unit]
Description=Namibia Car-Import Landed-Cost Calculator
After=network.target

[Service]
WorkingDirectory=/home/ubuntu/carcalc
ExecStart=/usr/bin/python3 app.py
Restart=always
Environment=PORT=5000
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now carcalc
sudo systemctl status carcalc
```

## Project structure

```
app.py            Flask app: the landed-cost calc engine + the two routes
rates.py          the rate table — every number, its source, its confidence flag
test_calc.py      pytest suite (7 hand-computed cases)
templates/        form.html, result.html (Jinja2)
static/           style.css, main.js
requirements.txt  Flask 3.0.3
```

## Team

- Silvio Ivanio
- Anselmo Martins