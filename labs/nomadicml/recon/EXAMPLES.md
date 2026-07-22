# NomadicML / Nomadic AI — Public Example Demos (recovered 2026-07-21)

## Sources & method (no fabrication)
All data below was extracted from **embedded state in the sites' own JS bundles** (both sites are Vite SPAs; plain HTML is empty):

- `https://www.nomadicai.com/assets/index-nTEEhlCy.js` (1.95 MB) — contains the **full hard-coded examples array** (`pZ`) that renders `www.nomadicai.com/examples`: every example's id, vertical, title, query, event list with timestamps, batch reasoning, reasoning-trace steps, video/artifact paths, and deep links into the live demo app.
- `https://app.nomadicml.com/assets/Examples-DKxP86F9.js` (23 KB, lazy chunk of `index-CYsiV9YY.js`) — contains the **full card data** for `app.nomadicml.com/live-demo/examples`: 17 curated example cards + 7 public-dataset showcase cards with stats and event counts.
- `https://www.nomadicai.com/sitemap.xml`, `robots.txt`, and `llms.txt` — page inventory, customer list, positioning.
- Marketing copy strings extracted from the same main-site bundle (homepage hero, problem statements).

Confidence: **high** — these are literal string constants from the shipped production bundles, not inference. What was NOT recovered: the actual video files' content (only paths/descriptions), and any behind-the-scenes API responses (the live-demo batch views load per-batch data at runtime; only their URLs are captured here).

---

## 1. Marketing frame (what the examples are meant to prove)

**Positioning:** "Nomadic AI — The Understanding Layer for Physical AI" / "Make Physical AI Work in the Real World."

**Core pitch (homepage meta/hero):** "Nomadic is the understanding layer for Physical AI. Find the failures and edge cases hidden in your operational data, diagnose them with evidence, and turn them into targeted training data. Trusted by Fortune 500s and the most exciting robotics and AV developers."

**From llms.txt:** "Nomadic is the Physical AI understanding platform for autonomous vehicles and robotics. We provide an understanding layer that sits on top of existing perception stacks, transforming multi-sensor video (RGB + lidar + telemetry) into searchable behavior."

**Problem statements the demos answer (homepage section headings):**
- "Most footage and sensor data are never analyzed"
- "Failures are found late, and no one can say why"
- "The feedback loop between failures and training is broken"
- (Case-study copy) "NATIX captures footage across thousands of cameras, but manual review at that scale was impossible. Most data sat on servers, never analyzed, never used."

**Examples page meta description:** "See how Nomadic turns raw video datasets into curated edge cases, from automotive dashcam footage to robotic arm pick-and-place actions."

**Named customers (llms.txt):** Zoox, Mitsubishi Electric Automotive America, Zendar, NATIX Network. Case-study blog posts: `/blog/natix-case-study`, `/blog/zendar-case-study`. Funding: $8.4M seed (TechCrunch, 2026-03-31: "Nomadic raises $8.4M to wrangle the data pouring off AVs").

**Demo pattern each example follows:** natural-language query → batch of videos analyzed → events found with timestamps → per-event "Reasoning Trace" (Event Validation steps written in first person, e.g. "I tracked 9 pedestrians… I concluded the crossing is a valid jaywalking encounter") → "Evidence Supporting Validation" artifacts (annotated/segmentation overlay video, trajectory & motion plots, stills, maps). The point being proved: agentic, evidence-backed video search + validation at fleet scale, not just detection.

---

## 2. www.nomadicai.com/examples — 20 interactive examples (full data)

All from the embedded `pZ` array. Each links to a live batch at `app.nomadicml.com/live-demo/use-cases/rapid-review/batch-view/<id>`.

### AUTOMOTIVE (input: dashcam / ego-vehicle & surround-camera driving footage)

**1. Driving Violations** (`example-driving-violations`)
- Query: "Find driving violations and cite their relevant DMV code."
- Output: 2/2 events approved. Batch reasoning: "We found 2 critical violations in this clip: an unsafe following distance behind a white Lexus, and a rolling stop at a marked STOP intersection…"
  - Event 1/2 [00:00–00:07] Unsafe Following Distance (CVC 21703)
  - Event 2/2 [00:07–00:11] Rolling Stop Violation (CVC 22450(a))

**2. Behavior Recognition** (`example-a`)
- Query: "Find lane merge instances."
- Output: "We found 15 instances across 11 videos where another vehicle merged into the ego-vehicle's lane…" Featured event: [00:02–00:04] "Red Prius merged into ego lane from the left."

**3. Multi-View Understanding** (`example-multi-view`)
- Input: synchronized surround-camera (multi-view) footage.
- Query: "Ego vehicle overtaking pedestrians."
- Output: 3/3 events ([00:00–00:08], [00:11–00:16], [00:17–00:58]), each validated across views, e.g. "Rear-facing camera shows pedestrians receding near a crosswalk, confirming the ego vehicle has overtaken them" — subtitle "(supported by multiple views)".

**4. GPS Location Identification** (`example-gps-location`)
- Query: "Find individual potholes show their GPS locations."
- Output: 5/5 potholes on US-97 pinned to GPS via dashcam telemetry, shown on an interactive map. Events: Pothole cluster in oncoming lane [00:02–00:05]; Potholes spanning both lanes [00:05–00:08]; Pothole chain along centerline [00:08–00:11]; Pothole in left wheel path [00:12–00:14]; Pothole cluster in ego lane [00:16–00:20]. "…so every defect can be located on the map for repair dispatch."

**5. Multi-Query (fleet roadside-hazard review)** (`example-roadside-hazard`)
- Query: "Determine whether a stopped, disabled, or roadside vehicle creates a hazard for the ego vehicle — close enough to the travel lane to narrow the path, require a lane shift or move-over, or create a close-pass risk."
- Output: "Across 85 fleet clips this multi-query review surfaced 59 events — 26 matching the roadside-hazard query." 8 parallel queries with per-scene validations:
  - q0 Hard Brake / Forced Slowdown — scene-0071 [00:08–00:19]: ego brakes to a stop at 'ROAD CLOSED' sign + CAT 950K loader
  - q1 Road Debris / Obstacle — scene-0018 [00:00–00:09]: cones/barriers in travel lane around an excavator
  - q2 Stopped / Roadside Hazard — 6 scenes (0099, 0002, 0010, 0051, 0048, 0092): stopped van/pickup/UPS truck near work zone; flatbed with workers; FedEx truck partly in lane; etc.
  - q3 Erratic / Illegal Maneuver — scene-0068 [00:04–00:13]: seafood delivery truck pulls out without yielding
  - q4 Closed Roads — scene-0045 [00:10–00:22]: lowered boom barrier, ego stops at gate
  - q5 Jaywalker Encounters — scene-0024 [00:07–00:16]: "I tracked 9 pedestrians… mid-block crossing, no marked crosswalk"
  - q6 Yielding/Stopping for Pedestrians — scene-0067 [00:11–00:18]
  - q7 Double-Parked Maneuvers — scene-0006 [00:04–00:12]: lane change around utility truck behind a cone
- Evidence artifacts per scene: segmentation-overlay clips, lane–object interaction plots, camera-trajectory plots.

### ROBOTICS — Humanoid (input: egocentric / head-mounted human video)

**6. Egocentric Annotation** (`example-humanoid-egocentric-action-seg`)
- Query: "Segment all human actions, especially hand movements."
- Output: 10 events over a 12 s chef/cooking clip: Pour liquid into pan [00:00–00:01]; Move pan to station; Pick up spoon; Add ingredient to pan; Add ingredients and drop spoon; Move pan to stove; Place pan on stove; Grab pan handle; Pull pan back; Reach for bowl [00:11–00:12].

**7. Egocentric Action Search** (`example-humanoid-action-seg`)
- Query: "Find each time the human puts a plate on the counter."
- Output: 2 events ([00:01–00:02], [00:24–00:25]) "Place a plate on the counter", with hand/plate/counter interaction validated.

### ROBOTICS — Industrial (input: fixed-camera robot-arm workcell video + gripper/joint telemetry)

**8. Micro-Action Segmentation** (`example-robot-action-segmentation`)
- Query: "Segment every robot arm micro-action." (Franka arm, NIST-style task board reassembly)
- Output: "37 AI annotated events" at **millisecond precision** over 03:57.750 — alternating Remove:/Place: for D-SUB, ethernet, square pegs 1–4, round pegs 1–4, USB, waterproof connector, BNC, bolt 4, large/medium/small gears, bracketed by Idle. Includes an **interactive 3D robot trajectory viewer** (20 Hz sampling, 237.75 s window, `/data/action-segmentation-reassemble-trajectory.json`).

**9. Discrete Pick and Place** (`example-pick-place`)
- Query: "Find all discrete pick and drop actions."
- Output (ms precision): Pick — watermelon slice toy [00:03.474–00:04.394]; Drop — watermelon slice toy onto counter [00:04.640–00:04.725]; Pick — green pear toy [00:06.065–00:06.592]; Drop — green pear toy onto counter [00:06.820–00:06.953]. Artifacts: gripper/object segmentation video with a 9-class motion legend (lift, lift+, lower, lower+, ±x, ±y, diag), End-Effector Position & Gripper Opening plots; validation cites "gripper sensor data and visual evidence".

**10. Failures and Edge Cases** (`example-find-edge-cases`)
- Query: "Find failures that occur during placement or just before release."
- Output: 1 event [00:02.000–00:03.800] "Placement failure during release" with segmentation-overlay + original workspace clips; event-clustering UI.

**11. Manipulation Failures** (`example-safety-edge`)
- Query: "Segment actions and spot failed grasps."
- Output: 3 events: Box Pick Up [00:01–00:03] ("arm grasps a merged unit… carrying 2 boxes"), Box Drop Down [00:03–00:05], Picking Failure [00:07–00:09] (knocked box fails to reach the conveyor).

**12. Action Segmentation** (`example-robot-segment-actions`)
- Query: "Segment robot actions." (robot arm servicing a 3D printer)
- Output: 6 events: Approaching and Grasping Hood; Opening Hood; Approaching Build Platform; Grasping and Unlatching Handle; Extracting and Moving Platform; Inserting into Washer [00:14–00:16].

### ROBOTICS — Other Industries (input: warehouse AMR/forklift camera footage)

**13. Forklift Speed Adjustment** (`example-amr-forklift-speed`)
- Query: "Find moments when the forklift adjusts speed to avoid a collision."
- Output: 1 event [00:01–00:09] "Adjusting speed and path to avoid a crossing forklift" + trajectory & speed plot through the intersection.

**14. Navigation Failures** (`example-amr-stuck`)
- Query: "Identify moments when an AMR is blocked."
- Output: 1 event [00:03–00:11] "Forklift Stops Near Busy Workstation" (6–7 workers) + processed trajectory / speed & motion events chart.

### INFRASTRUCTURE — Aerial (input: drone / high-angle surveillance video)

**15. Safety Violations** (`example-safety-violations`)
- Query: "Find safety violations." (construction/container-terminal aerial view)
- Output: Worker Missing Safety Helmet [00:00–00:02]; Worker Missing High-Visibility Vest [00:02–00:05]; evidence frame: worker on elevated ledge in hi-vis vest without helmet, phone to ear.

**16. Aerial Multi-Query** (`example-virat-aerial-multi-query`)
- Input: VIRAT (DARPA) aerial surveillance footage.
- Query: "Find people running and people who stop to interact with the ground in aerial footage."
- Output: "Across 25 VIRAT aerial videos… 25 approved activity events: 4 people-running events and 21 ground-interaction events." Sample events: People Running on Dirt Road; Person Running Through Intersection; Person Bent Over Open SUV Hood; People Pick Up and Carry Object; Person Places Ground Markers [00:14–00:30]. Artifacts: annotated aerial clips + motion/trajectory plots.

### INFRASTRUCTURE — Construction (input: fixed-camera + egocentric heavy-equipment video, joint telemetry)

**17. Action Segmentation (excavator)** (`example-excavator-action-segmentation`)
- Query: "Segment every excavator micro-action."
- Output: **93 events over 03:00** (34 shown), compound micro-actions like "Raise + Dig (Curl-In) + Extend Arm + Swing Cab", "Extend Arm + Dump (Curl-Out) + Lower", "Hold / Near-Static" — "segmented directly from the excavator's turret, boom, stick, and bucket joint-angle trajectory." Includes 3D trajectory viewer (10 Hz, 180 s window).

**18. Construction Operations** (`example-excavator-dump-loading`)
- Query: "Find events where an excavator is loading a dump truck."
- Output: 1 event [00:11–00:22] "Excavator Loading Dump Truck" with a phase-by-phase description (lift bucket 00:11–00:15, swing over truck by 00:16, release dirt 00:17–00:22).

**19. Egocentric Action Search (excavator cycles)** (`example-construction-cycle-segmentation`)
- Query: "Show the excavator dump, loading, and swing full phases."
- Output: events 27–29 of 52: Dump [00:00–00:03], Loading [00:06–00:15], Swing full [00:15–00:17], with per-phase camera-trajectory graphs.

**20. Ego-Centric Action Segmentation** (`example-construction-egocentric-action-seg`)
- Query: "Segment all ego-centric construction actions, especially hand movements."
- Output: 8 events [00:00–00:10] (Pour liquid into pan, Move pan to station, Pick up spoon, Add ingredient to pan, Return spoon, Move pan to stove, Place pan on stove, Grab pan handle — same kitchen-egocentric clip reused under the construction ego-centric heading). Note: its `description` field in the bundle oddly reads "NVIDIA's autonomous-driving dataset: 1,700+ hours of camera, LiDAR, and radar driving across 25 countries" — likely a copy/paste bug in their data or a nearby dataset blurb; flagged as-is.

---

## 3. app.nomadicml.com/live-demo/examples — 17 example cards + 7 dataset showcases

From `Examples-DKxP86F9.js`. Each card links to a public batch view (`/live-demo/use-cases/rapid-review/batch-view/<id>`), filterable by vertical (All / Automotive / Robotics / Construction / Infrastructure).

### Curated example cards (title — description — stats)
**Automotive**
1. **Search Complex Actions** — "Search massive video datasets to detect complex driving actions and extract trajectories." [Semantic Search, Trajectory Extraction, Agentic Validation] — 24 videos analyzed, 7 events found
2. **Batch Driving Analysis** — "Process thousands of driving videos to track motion, interactions, and behavior at scale." — 100 videos, 5 events
3. **Mine Critical Driving Events** — "Detect rare, safety-critical events like pedestrian intrusions and cyclist cut-ins at scale." — 336 videos, 9 events
4. **Analyze Driving Behavior** — "Break down vehicle decisions, timing, and multi-agent interactions across traffic." — 500 videos, 11 events
5. **Detect Turning Maneuvers** — "Find and classify ego-vehicle turns… including protected and unprotected turns." — 100 videos, 20 events

**Construction**
6. **Detect Safety Risks** — "Surface unsafe worker behavior, equipment hazards, and proximity risks in real time." — 4 videos, 2 events
7. **Catch Critical Failures** — "Detect catastrophic failures and high-impact incidents across job sites." (thumb: "Stuck in Mud") — 5 videos, 7 events
8. **Monitor Jobsite Activity** — "Track workers, equipment, and active zones across large-scale construction sites." — 4 videos, 12 events
9. **Analyze Equipment Operations** — "Understand how machines operate, move, and interact across workflows." — 5 videos, 18 events
10. **Segment Construction Workflows** — "Break down construction workflows into structured, step-by-step task sequences." (thumb: Bricklaying) — 4 videos, 8 events
11. **Detect Equipment Attachments** — "Identify tools and attachments used by machines…" (thumb: "Which Part") — 5 videos, 11 events

**Robotics**
12. **Create Structured Robot Step Traces** — "Turn robot task videos into step-by-step action traces and capture failure modes like missed grasps, collisions, and incomplete executions." — 4 videos, 8 events
13. **Segment 3D Robotic Actions** — "Break robot tasks into precise action primitives like grasp, move, and place." — 1 video, **109 events**
14. **Robot Environment Interactions** — "…query for episodes where an AMR is blocked, causes congestion, or introduces delay and risk." — 9 videos, 2 events
15. **Understand Task Behavior** — "Analyze action sequences, timing, and task execution across robot workflows." — 5 videos, 5 events
16. **Diagnose Robot Failures** — "Identify when, how, and why failures occur to improve model performance." — 9 videos, 6 events
17. **Build Training-Ready Datasets** — "Generate structured, high-quality datasets from robot actions for training and evaluation." — 9 videos, 16 events

### Public-dataset showcase cards (org — dataset — Nomadic's run + event taxonomy w/ counts)
1. **Motional — nuReasoning** ("long-tail AV dataset, Apache 2.0"): 85 videos → 59 events: Stopped/roadside vehicle hazard 26, Jaywalker encounters 11, Double parked vehicle maneuvers 8, Road debris/obstacle 5, Closed roads 3, Yielding/stopping for pedestrians 3, Hard brake/forced slowdown 2, Erratic/illegal maneuver 1. *(This is the same batch behind the site's "Multi-Query" example.)*
2. **Torc Robotics — TruckDrive** ("Level 4, Class 8 highway benchmark, 475K synchronized samples"): 24 videos → 5 events: Road Debris/Obstacle 3, Unsecured/Oversized Load 1, VRU/Worker Near Lane 1 (7 more queries with 0 hits listed).
3. **Amazon Robotics — ArmBench** ("warehouse-robotics benchmark of 235K+ activities"): 200 videos → 130 events: Move-to-destination fail 82, Nominal 70, Package opened 65, Package deconstruction 65, Wait-state fail 31, Approach-place fail 11, plus object-type counts (Books 35, Boxes 25, Bags 5, Other 5) and Approach-grasp fail 3, Move-source fail 3.
4. **DROID — Manipulation Dataset** ("in-the-wild robot-manipulation: 76K demos, 564 scenes"): 75 videos → 120 events: Pick 61, Place 55, Pick Red Marker 4.
5. **NATIX — Street Imagery Dataset** ("world's largest decentralized dashcam network"): 240 multi-view videos → 69 events: Tailgating/Close Following 21, Road Debris/Obstacle 12, Merge onto highway 12, General Edge Case 10, Erratic/Illegal Maneuver 6, Double Parked Maneuvers 6, Rolling Stops 2.
6. **Berkeley DeepDrive — BDD100K** ("100K 40-second driving clips"): 500 videos → **1,969 events**: Traffic signs 1716, Road Debris/Obstacle 58, Adverse Visibility 58, Pedestrian Violations 56, Double Parked Maneuvers 31, Merge onto highway 23, Hard Brake 8, Unprotected Left Turn 5, Stopped/Roadside Hazard 5, Rolling Stops 2, Lane Change 2, Erratic Maneuver 2, General Edge Case 2, Traffic Incidents 1.
7. **VIRAT — Video Dataset** ("DARPA surveillance benchmark, ~29 hours outdoor video"): 25 videos → 25 events: People who stop and interact with the ground 21, People running 4.

An additional embedded query panel in the main-site bundle (likely a fleet-scale showcase) lists: Ego Critical Violations (DMV) 140, Stopped/Disabled Vehicle Hazard 75, Object in Path 73, Lane Change Around Parked Vehicle 56, Adjacent Lane Change 35, Pedestrian Crosswalk Yield 33, Traffic Violation/Lane Departure 24, Erratic Maneuver 21, Vehicle Merge Into Ego Lane 21, Degraded Visibility 19, Rolling Stop at Stop Sign 10 — and a humanoid garment-manipulation panel: Grasp & pick up 90, Fold garment 78, Align & square 73, Insert/assemble 60, Lift & transfer 46, Reposition 45, Withdraw/reset 43, Release 36, Unfold & spread 33, Place & stack 27, Stabilize 13, Wipe/clean 7 (+ 3D trajectory & left/right gripper trajectory views).

---

## 4. Related public pages (sitemap)
Products: /products/our-product, /products/dataset-curation, /products/vla-annotation, /products/find, /products/monitor, /products/curate, /products/our-sdks. Solutions: automotive, robotics, construction, aerial, maritime. Blog (evidence/benchmark posts): nomadic-vlm-robotic-action-classifier (2026-07-14), action-segmentation-benchmark (2026-07-08), excavator-motion-dataset (2026-07-03), natix-case-study, zendar-case-study, av-motion-eval, efficiently-curating-driving-video-datasets. App API base: `https://api-prod.nomadicml.com/api` (auth-gated; not probed beyond identification). Docs: `https://docs.nomadicml.com`.
