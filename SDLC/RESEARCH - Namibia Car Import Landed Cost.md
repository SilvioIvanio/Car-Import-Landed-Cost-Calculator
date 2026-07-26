---
tags: [hackathon, aws, harambee-hub, research, r-and-d, namibia, car-import, landed-cost]
created: 2026-07-25
description: Research and development document for the Namibian car-import landed-cost calculator. The real FOB to CIF to landed-cost breakdown with cited rates, the competitor check (AutoLanded exists but is indicative-only), the MVP spec, and the pitch. Founder-lived problem. For the AWS For The People hackathon.
---

# Namibia Car-Import Landed-Cost Calculator: Research & Development

A research and development document for the AWS "For The People" Hackathon, 25 July 2026. Harambee Hub team.

Every number here is cited. Where sources disagree, or where I could not reach an official source, I say so plainly instead of guessing. That honesty is the method, not a weakness. I work based on data, based on facts, not assumptions.

---

## 1. The problem (I lived it)

I tried checking car importation once. I went to a Japanese auction site and saw a price that looked cheap. I thought, wow, this is the price. It is not.

That number was **FOB** (Free On Board). The car at the ship in Japan. Before shipping, before insurance, before any Namibian tax. The advertised number. The one that hooks you.

Then I found **CIF** (Cost + Insurance + Freight). FOB plus the ocean shipping and the marine insurance to Walvis Bay. So the price I saw was already incomplete.

Then I found out you still pay more on top of CIF. Customs duty. 15% VAT. Port charges. A clearing agent. Registration. I never got to the real total. Nobody shows you the real total before the car lands. You find out after you are already committed.

That gap is the problem. And I am not the only one who hits it. Every Namibian who has looked at importing a car lives this.

The evidence is not just me:

- **BE Forward**, one of the biggest used-car exporters to Namibia, has a "Total Price Calculator" that stops at CIF to Walvis Bay and tells buyers to *"consult a customs broker"* for everything after [1]. The biggest platform in the space gives up at the border.
- **SBT Japan's FAQ** says it plain: *"the FOB price does not include these fees, it's only the unit cost"* [2]. The price Namibians see is, by definition, not the price they pay.
- **Easyship's duty calculator** covers Namibia but has no vehicle category at all [3]. General duty tools skip cars.
- No Namibian news outlet publishes a worked example. The secondary guides, WalvisLink and AutoLanded, both carry a disclaimer: *"planning only, not a customs quotation"* [4][5].

The pain is real and repeated. No major player solves it end to end. That is the opening.

## 2. FOB, CIF, and landed cost (the three prices, in plain words)

Judges are not car importers. Here are the three prices a Namibian buyer actually meets.

**FOB (Free On Board).** The price of the car, loaded onto the ship in Japan. Nothing else. No shipping, no insurance, no tax. When you see a "cheap" Japanese auction car online, this is almost always the number you are looking at. [2][6]

**CIF (Cost + Insurance + Freight).** FOB plus the ocean shipping and the marine insurance to Walvis Bay. Under CIF the seller pays freight and insurance and hands you three documents at loading: the bill of lading (the shipping receipt), the insurance policy, and the commercial invoice. The risk passes to you the moment the car crosses the ship's rail in Japan. [7][8]

**Landed cost.** CIF plus everything Namibian that happens after the ship docks at Walvis Bay. Unloading. Customs duty. VAT. Excise. Environmental levy. Clearing agent. The truck to Windhoek. NaTIS (the National Traffic Information System) registration and licensing. This is the number no free tool computes for Namibia. It is the gap that burns buyers.

The structure, step by step:

```
FOB  (car at the ship in Japan)
 + freight + marine insurance
 = CIF  (car delivered to Walvis Bay port)
 + port handling + customs duty + VAT + excise + environmental levy
 + clearing agent + inland transport to Windhoek
 + NaTIS registration + licensing + number plates
 = LANDED COST  (car legally on the road in Windhoek)
```

## 3. The real Namibian landed-cost breakdown

Every component of the landed cost for a used passenger car imported from Japan (outside SACU) and brought to Windhoek. Each row carries a confidence flag.

- **verified**: confirmed by at least one primary or authoritative source.
- **conflict**: sources disagree. I show the range and both values.
- **confirm-with-agent**: I could not verify it from a reachable official source. The app must label this field and have it checked by a real Walvis Bay clearing agent before the document goes in front of a judge.

| #   | Component                                                         | Rate / rule                                                                                                | How it is calculated                                                                                                                                                                                                                                                                                                 | Source                                                                                                                                              | Confidence                                                                                                                             |
| --- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **FOB price**                                                     | The auction/vehicle price                                                                                  | User input                                                                                                                                                                                                                                                                                                           | SBT Japan FAQ [2]                                                                                                                                   | verified                                                                                                                               |
| 2   | **Ocean freight, Japan to Walvis Bay**                            | ~US$1,063 to 1,250 for a midsize car (RoRo); ~US$3,000 to 3,400 for a 40ft container shared by 2 to 3 cars | Added to FOB. RoRo (Roll-on/Roll-off, the ship the car drives onto) is cheaper per car                                                                                                                                                                                                                               | AutoLanded [5]                                                                                                                                      | confirm-with-agent (single source; get a live quote)                                                                                   |
| 3   | **Marine insurance**                                              | ~1 to 3% of CIF typically; bundled under CIF                                                               | Included in the CIF figure                                                                                                                                                                                                                                                                                           | SBT Japan support [8]                                                                                                                               | confirm-with-agent                                                                                                                     |
| 4   | **CIF value**                                                     | FOB + freight + insurance                                                                                  | The import value declared at customs                                                                                                                                                                                                                                                                                 | Wikipedia FOB/CIF [6][7]                                                                                                                            | verified                                                                                                                               |
| 5   | **Customs duty (SACU common external tariff, HS 8703)**           | **~18 to 25% depending on engine capacity and fuel**, see conflict note                                    | % of CIF. Set by the SACU (Southern African Customs Union) common external tariff, not a Namibia-only rate. Subheading-dependent: 8703.21 to .33 by engine cc and petrol/diesel                                                                                                                                      | customs-compliance.ai gives 18.0% as the heading average [9]; WalvisLink uses 25% for passenger cars [4]; SARS/NamRA subheading table not reachable | **conflict**. Quote as a range. Confirm the exact HS 8703.xx rate in NamRA eTariff (etariff.namra.org.na) before publishing one number |
| 6   | **Ad valorem excise / customs duty**                              | Formula: **(0.00003 x A minus 0.75)%, max 30%**, where A = recommended retail price excl. VAT              | Layered on top of customs duty. **Floors at 0%** for cheap used imports (at A = NAD 10,000, you get 0.3 minus 0.75 = negative, so 0%). Only bites on expensive vehicles (at A = NAD 500,000, it is 14.25%)                                                                                                           | PwC Tax Summaries, Namibia [10]                                                                                                                     | verified (single authoritative source)                                                                                                 |
| 7   | **Import VAT**                                                    | **15%**                                                                                                    | Charged on the duty-paid value. PwC states the base is *"the greater of the FOB value plus 10% or the market value"* [10]; WalvisLink uses (CIF x 1.10 + duty) x 15% [4]. SACU convention stacks duty into the VAT base. The "16.5%" some guides quote is **not** a different rate. It is 15% applied to a 110% base | PwC [10]; Wikipedia Taxation in Namibia [11]; WalvisLink [4]                                                                                        | verified rate; base medium-confidence, confirm with NamRA                                                                              |
| 8   | **Environmental levy on vehicle CO2 emissions + pneumatic tyres** | A real import line item (amounts not retrieved)                                                            | Applied at customs on imported vehicles and tyres                                                                                                                                                                                                                                                                    | PwC Tax Summaries [10]                                                                                                                              | confirm-with-agent (rate exists; amount unverified)                                                                                    |
| 9   | **Walvis Bay port charges (wharfage, handling, storage)**         | Per-vehicle amount published in the Namport tariff booklet                                                 | Namport publishes a tariff booklet; the deep-link returned 404 this session                                                                                                                                                                                                                                          | Namport [12]; customercare@namport.com.na / +264 64 208 2111                                                                                        | confirm-with-agent. Do not invent a figure                                                                                             |
| 10  | **Clearing agent fee**                                            | ~US$190 to 350+ per vehicle                                                                                | Service fees, disbursements, amendment charges                                                                                                                                                                                                                                                                       | WalvisLink importing guide [13]                                                                                                                     | confirm-with-agent (single-source indicative; quote 2 to 3 agents)                                                                     |
| 11  | **Inland transport, Walvis Bay to Windhoek**                      | Market rate (~400 km by road, B2)                                                                          | Truck transport; ~95% of overland cargo moves by truck in Namibia                                                                                                                                                                                                                                                    | Wikipedia Walvis Bay [14]                                                                                                                           | confirm-with-agent                                                                                                                     |
| 12  | **NaTIS vehicle registration and licensing + number plates**      | Statutory fees (amounts not retrieved)                                                                     | Paid at a NaTIS (National Traffic Information System) office; requires registration, licence disc, roadworthiness, plates                                                                                                                                                                                            | Roads Authority [15]                                                                                                                                | confirm-with-agent. roadsauthority.org.na did not resolve this session                                                                 |

**Two items I deliberately excluded**, with the debunking, so a judge can see the team did the homework:

- **"NAMCOR levy."** NAMCOR (the National Petroleum Corporation of Namibia) collects a per-litre levy on fuel. It is not a charge at vehicle customs. It is a fuel-price component, not an import line item [10][16]. Including it would be a factual error.
- **"MVA Fund levy."** The Motor Vehicle Accident Fund is funded the same way, through the fuel levy, not a separate customs charge [10][17].

**Sanity check on the combined tax.** Take a typical used car with a CIF value of US$10,000. At a 25% duty: US$2,500 duty + US$2,025 VAT (on (10,000 + 2,500) x 15%) = US$4,525, about **45% of CIF**. At an 18% duty: US$1,800 + US$1,920 = US$3,720, about **37% of CIF**. Both land inside the **~38 to 48% of CIF** range AutoLanded and WalvisLink quote [4][5]. The figure holds even with the duty-rate uncertainty, so it is safe to quote a judge as a range.

## 4. The import process, Japan to Walvis Bay to Windhoek

The real flow, cited. This is what the calculator models.

1. **Buy at auction in Japan.** Cars come through 200+ auction groups (JAA, JU, TAA, USS, ZIP). The buyer pays the **FOB price** [18][2].
2. **De-register and certify.** Before export the car is de-registered. An **export certificate** and a **mileage certificate** are issued. The car is biosecurity-cleaned [18].
3. **Ship to Walvis Bay.** By RoRo (the car drives onto the ship) or in a container. The carrier issues a **bill of lading**, which is the receipt, the contract of carriage, and the title document in one [7]. Under CIF you effectively buy three documents: bill of lading + marine insurance + commercial invoice [8]. Transit is about 25 to 32 days [5]. SBT Japan quotes a wider 45 to 60 days from payment to arrival [8].
4. **Arrive at Walvis Bay.** Namibia's only natural deep-water harbour and primary port. A new container terminal (opened August 2019) lifted capacity to 750,000 containers a year [14]. Walvis Bay connects to Windhoek by the B2 road and the TransNamib railway. About 95% of overland cargo moves by truck [14].
5. **Clear customs at Walvis Bay.** Namibia is a SACU member (with Botswana, Eswatini, Lesotho, South Africa) and applies the **SACU common external tariff** on imports from outside the bloc [19]. At this step customs duty (HS 8703, about 18 to 25%), ad valorem excise (floors at 0% for cheap cars), 15% VAT, the environmental levy, and Namport port charges all come due. A clearing agent handles it for a fee [4][13].
6. **Import restrictions (verified, official).** The Namibia Trade Portal (.gov.na) confirms: left-hand-drive vehicles are **prohibited** (diplomats excepted); vehicles older than **12 years** are prohibited; since **1 March 2023** NamRA requires all second-hand cars to enter on a **car-carrier trailer**; the import permit needs the invoice, de/registration or export certificate (English sworn translation if needed), bill of lading, ID/passport, company docs, and proof of payment [20].
7. **Truck to Windhoek.** By road (about 400 km on the B2) or rail. Road dominates [14].
8. **Register and license at NaTIS.** Registration, licence disc, roadworthiness, and number plates at a NaTIS office [15]. The car is now legally on the road. That is the **landed cost**.

## 5. Competitors (the validation)

This is the make-or-break section. The honest answer: a free Namibia-specific vehicle landed-cost calculator does exist. But it is indicative-only, not authoritative. The idea survives, but only if I stop claiming "nothing exists" and start claiming "nothing *authoritative* exists."

**Direct competitor (weak):**

- **AutoLanded, autolanded.com/namibia/** [5]. Free. Namibia-branded ("Vehicle Import Calculator for Africa"). Vehicle-specific: takes price, age, engine size, fuel type. Outputs a line-by-line landed cost: import taxes (duty + excise + VAT, about 38 to 48% of CIF), RoRo/container freight to Walvis Bay, local clearance. Tax data dated 2026-06-12. **The caveats that leave a wedge:** it publishes indicative *ranges* only, explicitly labelled *"planning only, not a customs quotation."* It does not itemise authoritative NamRA subheading duty rates. It does not break out NaTIS, Roads Authority, or Namport with real figures. It omits the environmental levy.

**Partial competitors (CIF stops here):**

- **BE Forward Total Price Calculator** [1]. Free, covers Namibia, outputs **CIF to Walvis Bay** = FOB + shipping + optional insurance/inspection/certificate/warranty. **Explicitly excludes** Namibian customs duty, VAT, import levies, and destination port handling. The help text says to *"consult a customs broker."* This is exactly the gap I lived.
- **WalvisLink Duty Estimator** [4]. Free, Namibia. Uses 25% duty, VAT = (CIF x 1.10 + duty) x 15%, Bank of Namibia weekly FX. Explicitly *"planning only, final customs value determined by NamRA, not your invoice."* **Excludes** port charges, clearing fees, transport, NaTIS. A general duty estimator, not a full landed-cost stack. Weaker than AutoLanded.

**Checked and ruled out:**

- **Easyship Duties & Taxes Calculator** [3]. Covers Namibia but has **no vehicle category**. Cannot do car landed cost.
- **CargoSphere** [21]. Ocean-freight-rate-management software for carriers and forwarders. Not a duty calculator. No Namibia or vehicle focus.
- **Veroot** [22]. US logistics compliance (CTPAT/TSA). Not a duty calculator. No Namibia coverage.
- **SimplyDuty** [23]. Freemium (5 free calcs a day). Claims "hundreds of destinations" but no public country list and no vehicle category visible. Namibia coverage unverified.
- **DutyCalculator.com** [24]. Returned HTTP 500 on every attempt this session. Unverifiable.
- **SBT Japan** [2]. Its Namibia country pages 404. No calculator.
- **Namport / NamRA** [12][25]. They publish tariffs and rates but no self-service calculator.

**Verdict: weak-competitor.** The idea is **not killed**. AutoLanded is the only thing close, and it is explicitly indicative-ranges-only. The wedge is the **authoritative, Namibian-validated version**: real NamRA subheading duty rates, Namport, NaTIS, the environmental levy, live clearing-agent quotes. Not "nothing like this exists." If I cannot source numbers better than AutoLanded's, a judge who finds AutoLanded first will undercut the pitch. I have to retire the blue-ocean thesis.

## 6. The MVP (what we build)

One function. A Namibian types a vehicle price and a few specs. The app returns the full landed-cost breakdown in NAD (Namibian dollars).

**The single screen.**

- **Inputs:** FOB price (or vehicle value), currency, vehicle age, engine capacity (cc), fuel type (petrol/diesel), origin (Japan or South Africa). Optional: freight quote, clearing-agent quote.
- **Output:** a line-by-line breakdown. FOB, freight, insurance, CIF, customs duty, ad valorem excise, VAT, environmental levy, port charges, clearing agent, inland transport, NaTIS registration, **landed cost total in NAD**. Each line shows its source and a confidence flag (verified, range, confirm-with-agent). A Bank of Namibia weekly FX rate converts USD/JPY to NAD.
- **Format:** a **printable HTML quote**, not a live PDF. PDFs are a landmine at demo time. A broken PDF export wastes minutes you do not have. A clean printable HTML page (Ctrl+P, Save as PDF if the judge wants) avoids the risk entirely.

**The tech (2 students, about 10 hours, no AWS experience):**

- A **static site** (HTML + a small JS calculation file) or a **Flask + SQLite** app. Either works. SQLite stores the rate table (duty by HS subheading, VAT, levy, fee schedule) so rates are editable without touching code.
- Deploy on **AWS EC2** (a `t2.micro` free-tier instance). One `app.py`, one `rates.db`, one `index.html`. A single `systemd` unit keeps it running. Nothing fancy.
- No accounts, no live APIs, no scraping. Rates are seeded from the cited sources into the rate table. Each row carries its source URL and confidence flag. A "verify with NamRA" banner sits above the result.

**The split (2 people):**

- **Anselmo:** the form screen and the result screen. Clean inputs, the breakdown table, the confidence flags, the printable layout, the look and feel. One HTML page, one stylesheet.
- **Me (Silvio):** the calculation engine and the EC2 deploy. The rate table schema, the duty/VAT/excise/levy formulas from section 3, the FX lookup, the `app.py` routes, the EC2 and `systemd` setup. I keep the numbers honest.

**Explicitly out of scope:** user accounts, saving quotes, live freight APIs, scraping auction sites, multi-currency wallets, mobile-native builds. One screen, one function, one honest number.

## 7. The 4-minute pitch

1. **Problem (30s).** "I looked at a cheap car on a Japanese auction site. The price looked great. It was FOB, the car at the ship, before anything else. Then I learned about CIF. Then duty. Then VAT. Then port fees. Then NaTIS. I never knew the real total until the car landed. Every Namibian importing a car lives this."
2. **The FOB shock (30s).** Show a real auction listing with a low FOB price. Show BE Forward's calculator stopping at "CIF to Walvis Bay" and literally saying "consult a customs broker." That is the gap.
3. **The app (90s).** Type a price. Select a car. See the full landed-cost breakdown in NAD. Every line, every source, every confidence flag. One honest number.
4. **Live demo (60s).** Run the calculation live on stage. Show the difference between FOB and landed cost. The gap that burned me, made visible.
5. **Close (30s).** "For every Namibian who got burned importing a car. Built by two students in a weekend. Running on AWS. Every number cited, every uncertain number flagged. This is what transparency looks like."

## 8. Honest risks

**Where the numbers are uncertain:**

- The **customs duty rate** is the single biggest credibility risk. Sources genuinely conflict, 18% heading average versus 25% on some petrol subheadings, and the subheading-level table could not be retrieved (SARS 404, NamRA eTariff is a JavaScript app with no static content). The app has to quote it as a **range, about 18 to 25% depending on engine capacity and fuel**, and link to NamRA eTariff. Stating one fixed percentage would be guessing, and a judge would catch it.
- **Namport port charges**, **NaTIS registration/licensing**, **clearing-agent fees**, and the **environmental levy amount** could not be verified from reachable primary sources this session. They are flagged **confirm-with-agent**. Before the document goes in front of a judge they should come from a real Walvis Bay clearing agent and the Namport tariff booklet.
- The **VAT base** (FOB + 10% versus CIF + 10%, and whether duty is stacked in) is medium-confidence. The 15% rate is rock solid, two independent sources. The exact base should be confirmed with NamRA.

**Build risks:**

- A 2-person, 10-hour build has no slack for a wrong rate discovered at demo time. Seed the rate table early, cite each row, and show the confidence flags on screen. A judge who sees "confirm with NamRA" respects the honesty more than a fake number.
- AutoLanded already exists. If we cannot source numbers better than AutoLanded's, the pitch is undercut. The wedge is *authority*, not novelty.

**The one validation I would do with more time:**

Before writing a line of code, call one Walvis Bay clearing agent and confirm four things: the exact HS 8703.xx customs duty rate for a typical used Japanese passenger car, the Namport per-vehicle port charge, the NaTIS registration/licensing fee, and the environmental levy amount. One real phone call turns three "confirm-with-agent" rows into verified numbers and makes the whole document judge-safe. There is no time before this event, so the on-screen flags carry the honesty instead. That is not a workaround. It is the wedge.

---

## Sources

1. **BE Forward stocklist, Namibia.** https://www.beforward.jp/stocklist/namibia. Confirmed BE Forward's Total Price Calculator stops at CIF to Walvis Bay and excludes duty/VAT/levies/port handling. Tells buyers to "consult a customs broker."
2. **SBT Japan FAQ.** https://www.sbtjapan.com/faq. Confirmed FOB price "does not include these fees, it's only the unit cost."
3. **Easyship Duties & Taxes Calculator, Namibia.** https://www.easyship.com/duties-and-taxes-calculator/namibia. Confirmed Easyship covers Namibia but has no vehicle/automobile category.
4. **WalvisLink, Namibia Import Duty Calculator.** https://walvislink.com/resources/namibia-import-duty-calculator. Free Namibia duty estimator. Uses 25% duty and VAT = (CIF x 1.10 + duty) x 15%. "Planning only."
5. **AutoLanded, Namibia.** https://autolanded.com/namibia/. Free Namibia vehicle landed-cost calculator. Indicative ranges only. "Planning only, not a customs quotation." The weak direct competitor.
6. **Wikipedia, FOB (shipping).** https://en.wikipedia.org/wiki/FOB_(shipping). Definition of FOB.
7. **Wikipedia, Bill of Lading.** https://en.wikipedia.org/wiki/Bill_of_lading. Bill of lading as receipt + contract of carriage + document of title. The three CIF documents.
8. **SBT Japan, Shipping Support.** https://www.sbtjapan.com/support/shipping. CIF documents (B/L + insurance + invoice). 45 to 60 day delivery window.
9. **customs-compliance.ai, HS 8703.** https://customs-compliance.ai/duty/hs/8703-motor-cars-and-vehicles-for-transport-of-persons. 18.0% MFN heading average for SACU. 25.0% baseline on some subheadings. Source of the duty-rate conflict.
10. **PwC Tax Summaries, Namibia (Other Taxes).** https://taxsummaries.pwc.com/republic-of-namibia/corporate/other-taxes. 15% VAT. Ad valorem formula (0.00003 x A minus 0.75%, max 30%). Environmental levy on vehicle CO2 and tyres. Confirms NAMCOR/MVA levies are per-litre fuel levies, not import charges.
11. **Wikipedia, Taxation in Namibia.** https://en.wikipedia.org/wiki/Taxation_in_Namibia. Independent confirmation of 15% standard VAT.
12. **Namport, Port Tariffs.** https://www.namport.com.na/port-tariffs/. Walvis Bay port tariff booklet exists. Deep-link returned 404 this session. Contact customercare@namport.com.na / +264 64 208 2111.
13. **WalvisLink, Importing a Car to Namibia.** https://walvislink.com/resources/importing-car-to-namibia. Clearing-agent fee range ~US$190 to 350 per vehicle (indicative).
14. **Wikipedia, Walvis Bay.** https://en.wikipedia.org/wiki/Walvis_Bay. Walvis Bay as Namibia's primary deep-water port. 750,000-container capacity. B2 road and TransNamib railway to Windhoek. ~95% truck modal share.
15. **Roads Authority (NaTIS).** https://www.roadsauthority.org.na. NaTIS registration and licensing. Site did not resolve this session, fees unverified.
16. **NAMCOR.** https://www.namcor.com.na. National Petroleum Corporation of Namibia. Confirmed the NAMCOR levy is a per-litre fuel levy, not a vehicle-import charge.
17. **MVA Fund.** https://www.mvafund.com.na. Motor Vehicle Accident Fund. Funded through the fuel levy, not a separate import charge.
18. **Wikipedia, Japanese Used Vehicle Exporting.** https://en.wikipedia.org/wiki/Japanese_used_vehicle_exporting. 200+ auction groups. De-registration, export certificate, mileage certificate, biosecurity cleaning before export.
19. **Wikipedia, Southern African Customs Union.** https://en.wikipedia.org/wiki/Southern_African_Customs_Union. SACU common external tariff. Namibia is a member with Botswana, Eswatini, Lesotho, South Africa.
20. **Namibia Trade Portal (.gov.na), Motor Vehicles Imported Abroad.** https://namibiatradeportal.gov.na/general-trade-information/exemption-motor-vehicles-imported-abroad. Official restrictions: LHD prohibited, max age 12 years, car-carrier trailer required since 1 March 2023, import permit document list. Authoritative.
21. **CargoSphere.** https://www.cargosphere.com. Ocean-freight-rate-management software. Not a duty/landed-cost calculator. Not a competitor.
22. **Veroot.** https://www.veroot.com. US logistics-compliance automation (CTPAT/TSA). Not a duty calculator. Not a competitor.
23. **SimplyDuty.** https://www.simplyduty.com/import-calculator/. Freemium duty calculator. Namibia/vehicle coverage unverified.
24. **DutyCalculator.com.** https://www.dutycalculator.com. Returned HTTP 500. Unverifiable.
25. **NamRA (Namibia Revenue Agency).** https://www.namra.org.na. NamRA customs. eTariff portal at etariff.namra.org.na is a JS app returning no static content this session.