"""
app.py — Namibian Car-Import Landed-Cost Calculator.

One function: a Namibian types a car price + a few specs, the app returns
the full landed-cost breakdown in NAD. Every line cites its source and a
confidence flag. That honesty is the wedge over AutoLended.

RUN LOCALLY:
    pip install flask
    python app.py
    open http://localhost:5000

DEPLOY ON AWS EC2 (t2.micro, the hackathon requirement):
    sudo apt update && sudo apt install -y python3-pip
    pip3 install flask
    # copy this app/ folder to the instance
    python3 app.py              # runs on port 5000
    # open EC2 security group inbound TCP 5000 from 0.0.0.0/0
    # then: http://<EC2-PUBLIC-IP>:5000

    To run on port 80 (nicer URL) -> sudo python3 app.py
    Or set PORT env var: PORT=80 python3 app.py

Silvio owns this file + rates.py. Anselmo owns templates/ and static/.
"""

import os
from flask import Flask, render_template, request

import rates as R

app = Flask(__name__)


def calc_landed_cost(form):
    """Run the landed-cost calc from form inputs. Returns (lines, total, meta).
    Each line = (key, label, amount_nad, source, flag)."""
    try:
        fob_usd       = float(form.get("fob_usd", 0))
        fx            = float(form.get("fx", R.FX_USD_NAD["value"]))
        freight_usd   = float(form.get("freight_usd", R.FREIGHT_USD["value"]))
        duty_pct      = float(form.get("duty_pct", R.DUTY_PCT["value"]))
        env_levy_nad  = float(form.get("env_levy_nad", R.ENV_LEVY_NAD["value"]))
        port_nad      = float(form.get("port_nad", R.PORT_NAD["value"]))
        clearing_usd  = float(form.get("clearing_usd", R.CLEARING_USD["value"]))
        transport_nad = float(form.get("transport_nad", R.TRANSPORT_NAD["value"]))
        natis_nad     = float(form.get("natis_nad", R.NATIS_NAD["value"]))
    except ValueError:
        return None, 0, {"error": "Please enter valid numbers."}

    fob_nad      = fob_usd * fx
    freight_nad  = freight_usd * fx
    insurance_nad = (fob_nad + freight_nad) * (R.INSURANCE_PCT["value"] / 100.0)
    cif_nad      = fob_nad + freight_nad + insurance_nad

    duty_nad   = cif_nad * (duty_pct / 100.0)
    # Ad valorem excise: A proxied as CIF. Formula floored at 0%, capped 30%.
    excise_pct = R.ad_valorem_excise_pct(cif_nad)
    excise_nad = cif_nad * (excise_pct / 100.0)
    # VAT base: (CIF x 1.10 + duty) per WalvisLink.
    vat_base   = cif_nad * 1.10 + duty_nad
    vat_nad    = vat_base * (R.VAT_PCT["value"] / 100.0)

    clearing_nad = clearing_usd * fx

    lines = {
        "fob":        fob_nad,
        "freight":    freight_nad,
        "insurance":  insurance_nad,
        "cif":        cif_nad,
        "duty":       duty_nad,
        "excise":     excise_nad,
        "vat":        vat_nad,
        "env_levy":   env_levy_nad,
        "port":       port_nad,
        "clearing":   clearing_nad,
        "transport":  transport_nad,
        "natis":      natis_nad,
    }

    # Landed cost = everything from CIF onward (FOB+freight+insurance are IN CIF,
    # so we sum CIF + the post-CIF charges to avoid double counting).
    landed = cif_nad + duty_nad + excise_nad + vat_nad + env_levy_nad + port_nad \
        + clearing_nad + transport_nad + natis_nad
    lines["landed"] = landed

    # Build the display list in the order rates.py defines.
    display = []
    for key, label, source, flag in R.LANDED_COST_LINES:
        display.append({
            "key": key,
            "label": label,
            "amount": lines[key],
            "source": source,
            "flag": flag,
        })

    meta = {
        "fob_usd": fob_usd,
        "fx": fx,
        "duty_pct": duty_pct,
        "excise_pct": round(excise_pct, 3),
        "cif_nad": cif_nad,
        "fob_nad": fob_nad,
    }
    return display, landed, meta


@app.route("/", methods=["GET"])
def form():
    """The input form. Pre-filled with the defaults from rates.py so a demo
    works with one click (press Calculate)."""
    return render_template(
        "form.html",
        fx=R.FX_USD_NAD["value"],
        freight_usd=R.FREIGHT_USD["value"],
        duty_pct=R.DUTY_PCT["value"],
        duty_min=R.DUTY_PCT["min"],
        duty_max=R.DUTY_PCT["max"],
        env_levy_nad=R.ENV_LEVY_NAD["value"],
        port_nad=R.PORT_NAD["value"],
        clearing_usd=R.CLEARING_USD["value"],
        transport_nad=R.TRANSPORT_NAD["value"],
        natis_nad=R.NATIS_NAD["value"],
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    display, total, meta = calc_landed_cost(request.form)
    if display is None:
        return render_template("form.html", error=meta["error"])
    return render_template("result.html", lines=display, total=total, meta=meta)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)