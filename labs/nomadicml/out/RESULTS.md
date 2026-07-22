# nomadic_mini — reproduction of NomadicML public examples

Verbatim queries from nomadicai.com/examples, run on our own
CC-licensed clips (data/SOURCES.txt) through the clean-room pipeline.

## drive_city_34s.mp4

### driving-violations — query: 'Find driving violations and cite their relevant DMV code.'

> The video depicts a routine drive on a multi-lane highway under partly cloudy conditions. Traffic flow appears moderate and orderly. Throughout the recording, no clear instances of driving violations, such as illegal lane changes, unsafe speed (as speed limits are not visible), improper turns, or other reckless maneuvers, were observed by the ego vehicle or any other vehicles. Consequently, no driving violations requiring specific DMV codes were identified.

- (no events detected)

### lane-merges — query: 'Find lane merge instances.'

> The video captures several instances of vehicles performing lane changes and merges on a multi-lane highway. Two specific events involve vehicles merging onto the highway from an on-ramp, interacting with the existing traffic flow.

- [00:20–00:23] **Silver car merges onto highway** (Lane Change Detection, low, conf 0.95) — A silver car merges smoothly from an on-ramp onto the rightmost lane of the highway. The car maintains a safe distance and speed relative to the ego vehicle.
- [00:25–00:29] **White SUV merges onto highway** (Lane Change Detection, low, conf 0.95) — A white SUV merges from an on-ramp onto the rightmost lane of the highway, following the silver car. The maneuver is executed without incident, integrating into traffic ahead of the ego vehicle.

### roadside-hazard — query: 'Determine whether a stopped, disabled, or roadside vehicle creates a hazard for the ego vehicle — close enough to the travel lane to narrow the path, require a lane shift or move-over, or create a close-pass risk.'

> The ego vehicle drives on a multi-lane highway with moderate traffic. A significant event occurs when the ego vehicle passes a large semi-truck stopped on the right shoulder, which is very close to the travel lane.

- [00:30–00:33] **Roadside semi-truck close to travel lane** (Edge Case, medium, conf 0.95) — The ego vehicle passes a large white semi-truck (ECOSHIELD TRANSPORT) parked on the right shoulder. The truck is positioned very close to the travel lane, and orange cones are visible in front of it, indicating a potential work zone or disabled vehicle. This proximity creates a roadside hazard for the ego vehicle.

## drive_highway_51s.mp4

### driving-violations — query: 'Find driving violations and cite their relevant DMV code.'

> The video shows the ego vehicle approaching and stopping at a red traffic light, waiting for it to turn green, and then proceeding. No driving violations were observed by the ego vehicle or other vehicles in the frame.

- (no events detected)

### lane-merges — query: 'Find lane merge instances.'

> The video shows a dashboard view of a vehicle stopped in traffic at an intersection with multiple parallel lanes. No instances of lanes physically merging (e.g., two lanes becoming one or an on-ramp merging) are observed in the road geometry or by other vehicles.

- (no events detected)

### roadside-hazard — query: 'Determine whether a stopped, disabled, or roadside vehicle creates a hazard for the ego vehicle — close enough to the travel lane to narrow the path, require a lane shift or move-over, or create a close-pass risk.'

> The ego vehicle is traveling in congested traffic when it encounters a disabled U-Haul truck with its ramp down, blocking the rightmost travel lane ahead. This obstruction significantly impacts traffic flow and creates a hazardous situation, though the ego vehicle itself is in an adjacent lane and merely stops as part of the overall traffic queue.

- [00:07–00:50] **Disabled U-Haul truck obstructing right lane** (Edge Case, medium, conf 0.90) — A U-Haul truck, likely disabled or in the process of loading/unloading with its ramp down, is stopped in the rightmost travel lane. This creates a significant obstruction for vehicles in that lane, causing a traffic bottleneck. While the ego vehicle is in the adjacent lane and not directly forced to take evasive action, the blocked lane creates an indirect hazard by causing congestion and the potential for other vehicles to merge into the ego vehicle's path.

## search: 'vehicle merging into ego lane'
summary: 4 event(s) matched 'vehicle merging into ego lane'
- sim 0.805 · vid-894822d079 · event 0 — A silver car merges smoothly from an on-ramp onto the rightmost lane of the highway. The car maintains a safe 
- sim 0.800 · vid-894822d079 · event 1 — A white SUV merges from an on-ramp onto the rightmost lane of the highway, following the silver car. The maneu
- sim 0.717 · vid-0cc817fbfa · event 0 — A U-Haul truck, likely disabled or in the process of loading/unloading with its ramp down, is stopped in the r

## search: 'stop sign or traffic violation'
summary: 4 event(s) matched 'stop sign or traffic violation'
- sim 0.616 · vid-0cc817fbfa · event 0 — A U-Haul truck, likely disabled or in the process of loading/unloading with its ramp down, is stopped in the r
- sim 0.592 · vid-894822d079 · event 0 — The ego vehicle passes a large white semi-truck (ECOSHIELD TRANSPORT) parked on the right shoulder. The truck 
- sim 0.549 · vid-894822d079 · event 0 — A silver car merges smoothly from an on-ramp onto the rightmost lane of the highway. The car maintains a safe 

## search: 'hazard requiring a lane shift'
summary: 4 event(s) matched 'hazard requiring a lane shift'
- sim 0.736 · vid-0cc817fbfa · event 0 — A U-Haul truck, likely disabled or in the process of loading/unloading with its ramp down, is stopped in the r
- sim 0.724 · vid-894822d079 · event 0 — A silver car merges smoothly from an on-ramp onto the rightmost lane of the highway. The car maintains a safe 
- sim 0.718 · vid-894822d079 · event 0 — The ego vehicle passes a large white semi-truck (ECOSHIELD TRANSPORT) parked on the right shoulder. The truck 
