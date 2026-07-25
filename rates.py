"""
rates.py — the rate table for the Namibian car-import landed-cost calculator.

This is the SOURCE OF TRUTH for every number the app uses. Each rate carries:
  - value       : the number (or default) used in the calc
  - source      : where it came from (matches the R&D doc source list)
  - flag        : "verified" | "range" | "confirm-with-agent"
  - note        : one line for the screen / the pitch

Silvio owns this file. Anselmo never touches it.
If a number is wrong, fix it HERE — the app reads from this table.

Honesty is the wedge: AutoLanded gives indicative ranges with no sources.
We give the SAME ranges PLUS a source PLUS a confidence flag on every line.
That is the whole pitch. Do not fake-precise a number. If it is unverified,
flag it "confirm-with-agent" and let the flag show on screen.
"""

# Bank of Namambia weekly FX. Pegged 1:1 to ZAR; USD/ZAR ~ 18.5.
# Editable on the form. Flagged.
FX_USD_NAD = {
    "value": 18.5,
    "source": "Bank of Namibia weekly rate (indicative default)",
    "flag": "confirm-with-agent",
    "note": "Edit to today's BoN rate. USD->NAD.",
}

# Customs duty — THE big uncertainty. SACU common external tariff, HS 8703.
# Sources CONFLICT: 18.0% heading average (customs-compliance.ai) vs 25% (WalvisLink).
# So we let the USER pick inside the range on the form. Default 20%.
DUTY_PCT = {
    "value": 20.0,          # default, user-selectable
    "min": 18.0,
    "max": 25.0,
    "source": "customs-compliance.ai (18% heading avg) / WalvisLink (25%)",
    "flag": "range",
    "note": "SACU HS 8703. Confirm exact subheading at etariff.namra.org.na.",
}

# Ad valorem excise — PwC formula: (0.00003 * A - 0.75)%, max 30%.
# A = recommended retail price excl VAT. Floors at 0% for cheap cars.
# For the MVP we proxy A = CIF (flag it). Real definition needs NamRA.
def ad_valorem_excise_pct(A):
    """A = recommended retail price excl VAT (NAD). Returns excise % (floored at 0, capped 30)."""
    pct = 0.00003 * A - 0.75
    return max(0.0, min(30.0, pct))

EXCISE = {
    "source": "PwC Tax Summaries - Namibia",
    "flag": "range",
    "note": "Formula (0.00003 x A - 0.75)%, A = retail excl VAT. A proxied as CIF - confirm with NamRA.",
}

# Import VAT — 15% is rock solid (two independent sources).
# Base: WalvisLink uses (CIF x 1.10 + duty) x 15%. We follow that.
VAT_PCT = {
    "value": 15.0,
    "source": "PwC Tax Summaries / Wikipedia Taxation in Namibia / WalvisLink",
    "flag": "verified",
    "note": "15% on (CIF x 1.10 + duty). The '16.5%' some quote is just 15% on a 110% base.",
}

# Marine insurance — typically 1-3% of CIF, bundled under CIF. We use 1.5%.
INSURANCE_PCT = {
    "value": 1.5,
    "source": "SBT Japan shipping support (typical range 1-3%)",
    "flag": "confirm-with-agent",
    "note": "Usually bundled in CIF. 1.5% indicative.",
}

# Freight Japan -> Walvis Bay (RoRo, midsize car). AutoLanded ~US$1,063-1,250.
FREIGHT_USD = {
    "value": 1150,           # midpoint
    "source": "AutoLanded (RoRo midsize ~US$1,063-1,250)",
    "flag": "confirm-with-agent",
    "note": "RoRo per car. Container is different. Get a live quote.",
}

# Environmental levy on vehicle CO2 + tyres. Real line item, amount unverified.
ENV_LEVY_NAD = {
    "value": 0,              # unknown -> 0 placeholder, FLAG IT
    "source": "PwC Tax Summaries - Namibia (levy exists, amount not retrieved)",
    "flag": "confirm-with-agent",
    "note": "Real import line item. Amount must be confirmed with NamRA / agent.",
}

# Walvis Bay port charges (wharfage/handling/storage). Namport tariff booklet.
PORT_NAD = {
    "value": 0,              # unknown -> 0 placeholder, FLAG IT
    "source": "Namport tariff booklet (deep-link 404 this session)",
    "flag": "confirm-with-agent",
    "note": "customercare@namport.com.na / +264 64 208 2111.",
}

# Clearing agent fee. WalvisLink ~US$190-350. Midpoint ~270 USD -> NAD.
CLEARING_USD = {
    "value": 270,
    "source": "WalvisLink importing guide (~US$190-350 per vehicle)",
    "flag": "confirm-with-agent",
    "note": "Indicative. Quote 2-3 agents.",
}

# Inland transport Walvis Bay -> Windhoek (~400 km, B2). Market rate.
TRANSPORT_NAD = {
    "value": 3500,
    "source": "Market estimate (~400 km by road)",
    "flag": "confirm-with-agent",
    "note": "~95% of overland cargo moves by truck. Confirm with a transporter.",
}

# NaTIS registration + licensing + number plates. Statutory, unverified.
NATIS_NAD = {
    "value": 1200,
    "source": "Roads Authority / NaTIS (site did not resolve, fees unverified)",
    "flag": "confirm-with-agent",
    "note": "Registration + licence disc + roadworthiness + plates. Confirm at NaTIS.",
}

# The ordered list of lines, for the result screen + the calc.
# Each: key, label, source, flag. The calc fills in the amount.
LANDED_COST_LINES = [
    ("fob",          "FOB price (vehicle at the ship, Japan)",        "User input",                                   "verified"),
    ("freight",      "Ocean freight, origin -> Walvis Bay (RoRo)",    FREIGHT_USD["source"],                          FREIGHT_USD["flag"]),
    ("insurance",    "Marine insurance",                              INSURANCE_PCT["source"],                        INSURANCE_PCT["flag"]),
    ("cif",          "CIF value (FOB + freight + insurance)",        "Wikipedia FOB/CIF",                            "verified"),
    ("duty",         "Customs duty (SACU HS 8703)",                  DUTY_PCT["source"],                             DUTY_PCT["flag"]),
    ("excise",       "Ad valorem excise (PwC formula)",              EXCISE["source"],                               EXCISE["flag"]),
    ("vat",          "Import VAT (15%)",                             VAT_PCT["source"],                              VAT_PCT["flag"]),
    ("env_levy",    "Environmental levy (CO2 + tyres)",              ENV_LEVY_NAD["source"],                         ENV_LEVY_NAD["flag"]),
    ("port",        "Walvis Bay port charges",                       PORT_NAD["source"],                             PORT_NAD["flag"]),
    ("clearing",    "Clearing agent fee",                            CLEARING_USD["source"],                         CLEARING_USD["flag"]),
    ("transport",   "Inland transport, Walvis Bay -> Windhoek",      TRANSPORT_NAD["source"],                        TRANSPORT_NAD["flag"]),
    ("natis",       "NaTIS registration + licensing + plates",       NATIS_NAD["source"],                            NATIS_NAD["flag"]),
    ("landed",      "LANDED COST (car legally on the road, Windhoek)", "Sum of the above",                          "verified"),
]