"""
test_calc.py — locks the landed-cost math so a wrong number is caught before
the demo, not on stage.

The seam is one function: calc_landed_cost(form). It takes a plain dict (the
form values, as strings, the way a browser posts them) and returns
(display, total, meta). No HTTP, no Flask, no templates. Just the math.

The expected numbers below are HAND-COMPUTED from the spec formula and the
default inputs, not copied from the code. That is on purpose. If the calc
ever drifts from the spec, these tests fail. I fix the calc. I do not change
the test to make it pass. The test is the truth.

Run:
    cd <this folder>
    pip3 install pytest flask      # one time, if not installed
    pytest -v
"""

import app


# ---- the default form, the demo numbers ----------------------------------
# These mirror the pre-filled defaults in form.html + rates.py. Values are
# strings because a real browser posts strings; the calc floats them.
def default_form(**overrides):
    form = {
        "fob_usd": "4000",
        "fx": "18.5",
        "freight_usd": "1150",
        "duty_pct": "20.0",
        "env_levy_nad": "0",
        "port_nad": "0",
        "clearing_usd": "270",
        "transport_nad": "3500",
        "natis_nad": "1200",
    }
    form.update({k: str(v) for k, v in overrides.items()})
    return form


def amounts(display):
    """Turn the display list into a {key: amount} dict for easy lookup."""
    return {line["key"]: line["amount"] for line in display}


# ---- the worked example (duty 20%, the demo default) ---------------------
# Hand-computed, independent of the code:
#   fob_nad      = 4000 * 18.5            = 74000.0
#   freight_nad  = 1150 * 18.5           = 21275.0
#   insurance    = (74000 + 21275) * 1.5% = 1429.125
#   cif          = 74000 + 21275 + 1429.125 = 96704.125
#   duty         = 96704.125 * 20%       = 19340.825
#   vat          = (96704.125 * 1.10 + 19340.825) * 15% = 18857.304375
#   landed       = cif + duty + excise + vat + clearing + transport + natis
#               = 146677.479875
def test_default_breakdown_matches_the_worked_example():
    display, total, meta = app.calc_landed_cost(default_form())
    assert display is not None, "calc returned no display for valid input"

    a = amounts(display)
    assert abs(a["fob"] - 74000.0) < 0.01
    assert abs(a["freight"] - 21275.0) < 0.01
    assert abs(a["insurance"] - 1429.125) < 0.01
    assert abs(a["cif"] - 96704.125) < 0.01
    assert abs(a["duty"] - 19340.825) < 0.01
    assert abs(a["vat"] - 18857.304375) < 0.01
    assert abs(a["clearing"] - 4995.0) < 0.01
    assert abs(a["transport"] - 3500.0) < 0.01
    assert abs(a["natis"] - 1200.0) < 0.01
    assert abs(total - 146677.479875) < 0.01


# ---- the load-bearing invariant: import tax / CIF lands in 38 to 48% ------
# This is the documented range from the R&D doc, not the code's own formula.
# import tax = duty + excise + vat. CIF is the denominator. Checked at both
# ends of the duty band (18% and 25%) because the duty rate is the one number
# sources conflict on, so the invariant must hold across the whole band.
def _import_tax_ratio(form):
    display, _total, _meta = app.calc_landed_cost(form)
    a = amounts(display)
    import_tax = a["duty"] + a["excise"] + a["vat"]
    return import_tax / a["cif"]


def test_invariant_holds_at_duty_18_percent():
    ratio = _import_tax_ratio(default_form(duty_pct="18.0"))
    assert 0.38 <= ratio <= 0.48, f"import tax / CIF out of range at 18%: {ratio}"


def test_invariant_holds_at_duty_25_percent():
    ratio = _import_tax_ratio(default_form(duty_pct="25.0"))
    assert 0.38 <= ratio <= 0.48, f"import tax / CIF out of range at 25%: {ratio}"


# ---- the floor: zero fees, no crash, no negatives ------------------------
# A user who clears every fee field should still get a sane answer: the calc
# does not crash, no line is negative, and landed is at least CIF.
def test_zero_fees_floor_case():
    form = default_form(
        freight_usd="0",
        clearing_usd="0",
        transport_nad="0",
        natis_nad="0",
        env_levy_nad="0",
        port_nad="0",
    )
    display, total, meta = app.calc_landed_cost(form)
    assert display is not None, "calc crashed on all-zero fees"

    a = amounts(display)
    for key, amount in a.items():
        assert amount >= 0, f"negative amount on line {key}: {amount}"
    assert total >= a["cif"], "landed cost below CIF even with zero fees"


# ---- the error path: non-numeric input is caught, not silently wrong -----
# A user who types "abc" as the price must get a clear error, never a silent
# wrong total. The calc returns (None, 0, {"error": ...}).
def test_non_numeric_input_returns_an_error_not_a_wrong_number():
    display, total, meta = app.calc_landed_cost(default_form(fob_usd="abc"))
    assert display is None, "calc returned a number for non-numeric input"
    assert "error" in meta, "no error message for bad input"
    assert total == 0