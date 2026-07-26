---
tags: [hackathon, aws, harambee-hub, spec, prd, namibia, car-import, landed-cost, ready-for-agent]
created: 2026-07-25
description: Spec (PRD) for the Namibian Car-Import Landed-Cost Calculator. Problem, solution, user stories, implementation decisions, the single testing seam, out of scope. Status ready-for-agent. No project issue tracker exists, so this file is the published spec.
status: ready-for-agent
---

# Spec: Namibia Car-Import Landed-Cost Calculator

---

## Problem Statement

A Namibian looking at a used car on a Japanese auction site sees a low **FOB** price (Free On Board), the car at the ship in Japan, before shipping, insurance, taxes, or any Namibian charge. That number looks cheap, so it is the number buyers anchor on. Then they discover **CIF** (Cost + Insurance + Freight), FOB plus ocean shipping and marine insurance to Walvis Bay. Then, after the car lands, they still pay customs duty, 15% VAT, an environmental levy, port charges, a clearing agent, inland transport, and NaTIS registration. They never knew the real total until the car was on their doorstep. No free tool computes the true landed cost for Namibia end to end. BE Forward's calculator stops at CIF and says *"consult a customs broker."* AutoLanded gives indicative ranges with no sources and no NamRA subheading rates. The buyer gets burned by a gap nobody makes visible before the commitment.

I lived this. I saw a cheap FOB price, learned about CIF, then learned there was still more to pay, and never reached the real number. That lived pain is what the idea is built on.

## Solution

A single-screen web app. A Namibian types a vehicle price (FOB) and a few specs, and the app returns the full landed-cost breakdown in NAD, line by line, from FOB to CIF to every Namibian tax and fee to the real total. Every line cites its source and carries a confidence flag (verified, range, or confirm-with-agent). The honesty is the product. Where a number is uncertain, the customs duty rate, which sources report as 18 to 25%, the app shows it as a user-selectable range and flags it instead of faking precision. A "planning estimate, not a NamRA quotation" banner sits above the result. The result is a printable HTML quote (print, then save as PDF), not a live-generated PDF, so a render failure cannot kill the demo. It deploys on AWS EC2, the hackathon requirement. It does one thing: turn the FOB price a buyer saw into the real number they will pay.

## User Stories

1. As a Namibian car buyer, I want to type the FOB price I saw on a Japanese auction site, so that I can see what that car actually costs me on the road in Windhoek.
2. As a Namibian car buyer, I want the result in NAD, so that I can compare it to what I actually pay locally.
3. As a Namibian car buyer, I want to set the USD to NAD exchange rate myself, so that the estimate uses today's Bank of Namibia rate, not a stale default.
4. As a Namibian car buyer, I want ocean freight shown as a separate line, so that I can see how much of the gap is just getting the car here.
5. As a Namibian car buyer, I want marine insurance shown as a separate line, so that the CIF total is transparent, not buried in a lump sum.
6. As a Namibian car buyer, I want the CIF value called out clearly, so that I understand the midpoint between the auction price and the real landed cost.
7. As a Namibian car buyer, I want customs duty shown as a range I can adjust (18 to 25%), so that I am not lied to with one fake-precise percentage.
8. As a Namibian car buyer, I want ad valorem excise computed and shown, so that I see the full statutory tax stack, not just duty and VAT.
9. As a Namibian car buyer, I want the 15% VAT shown with the base it is calculated on, so that I understand why the total is what it is.
10. As a Namibian car buyer, I want the environmental levy, port charges, clearing agent, inland transport, and NaTIS registration each on their own line, so that nothing is hidden in one "fees" bucket.
11. As a Namibian car buyer, I want every line to show its source, so that I can trust or verify the number rather than take the app's word.
12. As a Namibian car buyer, I want every uncertain line to show a confidence flag (confirm-with-agent), so that I know which numbers I still have to check with a clearing agent before I commit.
13. As a Namibian car buyer, I want a clear "planning estimate, not a NamRA quotation" banner, so that I do not mistake the app for an official customs bill.
14. As a Namibian car buyer, I want a print or save-as-PDF button on the result, so that I can take the quote to a clearing agent or a family member.
15. As a Namibian car buyer, I want to see the gap between the FOB price I saw and the real landed cost, so that the hidden cost is made visible. This is the core payoff.
16. As a Namibian car buyer, I want the form pre-filled with sensible defaults, so that I can see a full worked example with one click before I enter my own numbers.
17. As a Namibian car buyer, I want a clear warning if I enter something that is not a number, so that the app does not silently produce a wrong total.
18. As a second-hand car importer, I want to edit the freight, clearing, transport, and fee fields, so that I can plug in quotes I have actually received and get a more accurate landed cost.
19. As a second-hand car importer, I want the duty rate adjustable inside the 18 to 25% band, so that I can model different vehicle classes the SACU tariff treats differently.
20. As a Walvis Bay clearing agent, I want the app to cite its sources per line, so that I can see which figures the buyer is using and correct the wrong ones for a specific vehicle.
21. As a hackathon judge, I want a clean, professional UI, so that the product feels real and considered, not a thrown-together demo.
22. As a hackathon judge, I want the confidence flags visible on every line, so that I can see the team was honest about what it knew and what it did not. That is the wedge over the indicative-only competitor.
23. As a hackathon judge, I want the app deployed and reachable on AWS EC2, so that the Deployment Strategy category is satisfied with a live URL, not a localhost screenshot.
24. As a hackathon judge, I want the gap between FOB and landed cost obvious on the result page, so that the problem is felt in one glance.
25. As Silvio (backend, deploy, pitch), I want the rate table separated from the calc logic, so that I can correct a number in one place without touching the engine or the UI.
26. As Silvio, I want the calc function callable with a plain dictionary of inputs, so that I can test the math directly without spinning up the web server.
27. As Silvio, I want a single deploy command and a systemd unit documented, so that I can get a skeleton live on EC2 before styling is finished.
28. As Anselmo (frontend), I want the form and result as separate templates with a dedicated stylesheet, so that I can make the look right without touching the calculation code.
29. As Anselmo, I want each result line to carry its key, label, amount, source, and flag, so that I can render the breakdown table consistently.
30. As Anselmo, I want a print stylesheet that hides the navigation and actions and keeps the breakdown, so that the saved PDF is a clean quote.
31. As a future maintainer, I want the rate table to be the single source of truth for every number, source, and flag, so that updating a rate does not require hunting across files.
32. As a future maintainer, I want the landed-cost line order defined once, so that the form, the calc, and the result all agree on what comes after what.

## Implementation Decisions

- **One function, one screen.** The product is one calc: inputs to landed-cost breakdown in NAD. No accounts, no saved quotes, no multi-step wizard.
- **Three-layer separation.** A rate-table module (the single source of truth for every number, source, and flag), a calc-engine function that reads that table and the form inputs, and two templates plus one stylesheet for presentation. The backend owner edits the first two. The frontend owner edits the last three. They never edit each other's files.
- **The rate table is the contract.** Each rate is a record with `value`, `source`, `flag` (verified, range, or confirm-with-agent), and a one-line `note`. The ordered list of landed-cost lines (key to label to source to flag) is defined once in the rate table. The calc fills in the amounts, the result renders them. This keeps form, calc, and result in agreement on line order. From the working prototype.
- **The calc formula (the decision-rich core, from the prototype):**
  - `FOB_nad = fob_usd * fx`
  - `freight_nad = freight_usd * fx`
  - `insurance_nad = (fob_nad + freight_nad) * insurance_pct%`
  - `cif_nad = fob_nad + freight_nad + insurance_nad`
  - `duty_nad = cif_nad * duty_pct%` (duty_pct user-selectable, default 20, range 18 to 25)
  - `excise_pct = clamp(0.00003 * A - 0.75, 0, 30)`, with `A` proxied as CIF (flagged; the real definition is retail excl. VAT, confirm with NamRA). `excise_nad = cif_nad * excise_pct%`
  - `vat_nad = (cif_nad * 1.10 + duty_nad) * 15%` (WalvisLink base; 15% rate verified by two sources)
  - `clearing_nad = clearing_usd * fx`
  - `landed_nad = cif_nad + duty_nad + excise_nad + vat_nad + env_levy + port + clearing_nad + transport + natis`
  - **Invariant:** import tax divided by `cif_nad` (duty + excise + vat) lands in **38 to 48%**, the documented range. Smoke-tested at 41.7% with the demo defaults.
- **Honesty over precision.** Unknown amounts (environmental levy, port charges, NaTIS) default to a placeholder and are flagged `confirm-with-agent` on screen with their source. The duty rate is a user-adjustable range, not a fixed figure. A verify-with-NamRA banner sits above the result. This is the explicit wedge over AutoLanded's source-less indicative ranges.
- **Printable HTML, not live PDF.** The result is a clean HTML page with a print stylesheet. The user prints and saves as PDF. No server-side PDF render, so a fresh-EC2 font or library problem cannot kill the demo.
- **Currency.** FOB, freight, and clearing are entered in USD. Everything converts to NAD through a user-editable FX field (default Bank of Namibia indicative rate). The result is NAD throughout.
- **Inputs.** FOB (USD), FX, freight (USD), duty %, environmental levy (NAD), port (NAD), clearing (USD), transport (NAD), NaTIS (NAD). All pre-filled with defaults so the demo works on one click. Vehicle age, engine cc, and fuel type are accepted on the form as context but do not change the calc in v1. The duty band is the proxy for vehicle class. Those are roadmap inputs.
- **Deployment.** Flask on an EC2 free-tier instance, port 5000 (security group open to 0.0.0.0/0), optional systemd unit for persistence, optional port 80. No database, no external APIs, no scraping. The rate table is in-process.
- **Error handling.** Non-numeric input re-renders the form with a clear message. No silent wrong totals.

## Testing Decisions

- **One seam, the highest possible: the calc engine.** `calc_landed_cost(form)` accepts a plain dict (it calls `form.get(...)`), so it is testable directly without the web server, HTTP, or Flask plumbing. This is the only place real logic lives. The templates are presentation. The routes are wiring. Testing the routes would be testing implementation details.
- **What a good test checks here:** the external behavior of the calc. Given a dict of inputs, the returned line amounts and the total are correct, and the documented invariant (import tax divided by CIF lands in 38 to 48%) holds across the duty band at 18% and 25%. Tests do not assert internal variable names or structure, only the returned numbers.
- **Modules tested:** the calc engine, fed by the rate table. The rate table itself is data. It is exercised through the calc.
- **Prior art and test shape:** a plain `pytest` (or stdlib `unittest`) test that builds a default-input dict, calls `calc_landed_cost`, and asserts CIF equals FOB + freight + insurance, duty equals CIF times duty%, the total equals the documented sum, and the import-tax ratio is within 38 to 48% at both duty 18% and duty 25%. A second case with all-zero fees confirms the floor. This mirrors the smoke check already run by hand against the prototype.
- **A second seam is deliberately not added** for the 3-hour build. An HTTP smoke test (form 200, /calculate 200) would test Flask wiring, not behavior, and costs time the build window does not have. Recorded here so the decision is visible.

## Out of Scope

- User accounts, authentication, or saved quote history.
- Live freight, FX, or auction-site APIs. Web scraping.
- Server-side PDF generation (printable HTML only).
- Vehicle-class-specific duty lookup by engine cc, age, or fuel (the duty band is the v1 proxy).
- Multi-currency wallets, mobile-native builds, or an offline/PWA mode.
- A clearing-agent marketplace, booking, or payment integration.
- Backoffice analytics or admin tooling.
- The "call a clearing agent" pre-build validation step. No time before the event. The on-screen flags carry the honesty wedge instead.

## Further Notes

- **Founder-fit is the foundation.** The pitch rests on my own experience of the FOB to CIF to landed-cost gap. The result page's gap line is the emotional core, and Anselmo should style toward it being the line that hits hardest.
- **Competitor posture.** This is a weak-competitor, wedge play, not a blue-ocean play. AutoLanded exists and is free. The differentiator is *authority* (per-line sources plus NamRA-flagged confidence), not novelty. The pitch must not claim "nothing like this exists." It must claim "nothing authoritative exists."
- **Cited backing.** The full rate table, sources, the import flow, the competitor landscape, and the 4-minute pitch arc live in the companion R&D document (`RESEARCH - Namibia Car Import Landed Cost.md`), which is judge-presentable and should be shown alongside the demo.
- **Pitch arc (30/30/90/60/30s):** Problem. The FOB shock (BE Forward stopping at CIF). The app. Live demo (type a price, see the real number). Close on "for every Namibian who got burned importing a car."
- **Deploy first.** A deployed skeleton on EC2, even unstyled, scores on Deployment Strategy before any polish is done. Ship the skeleton, then style.