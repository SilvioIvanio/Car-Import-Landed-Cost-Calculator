# Namibia Car-Import Landed-Cost Calculator

**Harambee Hub. AWS "For The People" Hackathon, 25 July 2026.**

One function: a Namibian types a car price + a few specs, the app returns the full landed-cost breakdown in NAD. Every line cites its source and a confidence flag. That honesty is the wedge over AutoLanded (which gives indicative ranges with no sources).

## Run locally

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

## Deploy on AWS EC2 (the hackathon requirement)

```bash
# on the EC2 instance (Ubuntu):
sudo apt update && sudo apt install -y python3-pip
pip3 install -r requirements.txt

# copy this app/ folder to the instance (scp or git)
python3 app.py              # serves on port 5000
```

Open the EC2 **security group** inbound: TCP **5000** from `0.0.0.0/0`.
Then: `http://<EC2-PUBLIC-IP>:5000`

Nicer URL (port 80): `sudo PORT=80 python3 app.py`

### Keep it running after you close SSH (optional, but judges like it)

```bash
sudo tee /etc/systemd/system/carcalc.service >/dev/null <<'EOF'
[Unit]
Description=Namibia Car-Import Landed-Cost Calculator
After=network.target

[Service]
WorkingDirectory=/home/ubuntu/app
ExecStart=/usr/bin/python3 app.py
Restart=always
Environment=PORT=5000
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now carcalc
# check: sudo systemctl status carcalc
```

## Who owns what

- **Silvio**: `app.py` (calc engine + routes), `rates.py` (the rate table: every number, its source, its confidence flag). Keeps the numbers honest.
- **Anselmo**: `templates/form.html`, `templates/result.html`, `static/style.css`. The look and feel. Make it clean and beautiful.

## The honest method (read before the pitch)

The duty rate is a **range (18–25%)** because sources conflict. The user picks inside it. Every other uncertain line is flagged `confirm-with-agent` on screen with its source. **Do not fake-precise a number.** A judge who sees "confirm with NamRA" respects the honesty more than a fake-precise figure. That flag IS the wedge over AutoLanded.

See `../RESEARCH - Namibia Car Import Landed Cost.md` for the full cited R&D document (show this to the judge).

## Out of scope (roadmap slide, not build)

User accounts, saving quotes, live freight APIs, scraping auction sites, multi-currency wallets, mobile-native. One screen, one function, one honest number.