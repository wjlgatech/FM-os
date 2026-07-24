export const meta = {
  name: 'dbtl-campaign',
  description: 'Run a full multi-cycle DBTL campaign as a deterministic orchestration: for each cycle, propose a batch, simulate/collect assay results, ingest, and refit — then synthesize the campaign report with experiments-saved vs. random.',
  phases: [
    { title: 'Design spec' },
    { title: 'Run cycles' },
    { title: 'Report' },
  ],
}

// This is the Workflow-tool form of the DBTL loop — the deterministic control flow
// (fixed number of cycles, one propose→test→ingest per cycle) lives here, while each
// scientific judgement (is this objective tractable? is a result an outlier?) is a
// subagent call. In production the "collect results" stage is a wet lab; here a subagent
// stands in as the assay oracle so the whole loop runs end to end and produces evidence.

const CAMPAIGN = (typeof args === 'object' && args && args.campaign) || 'demo-campaign'
const CYCLES = (typeof args === 'object' && args && args.cycles) || 6

phase('Design spec')
const spec = await agent(
  `Restate this wet-lab optimization brief as a typed campaign spec (objectives with max/min, ` +
  `constraints with thresholds, batch size, total budget). Flag anything ambiguous as an open ` +
  `question — do not invent objectives. Brief: ${JSON.stringify((args && args.brief) || 'maximize potency; keep cost low; 4 per cycle; 24 total')}`,
  { label: 'compile-spec', phase: 'Design spec' }
)
log(`Compiled spec for campaign "${CAMPAIGN}"`)

phase('Run cycles')
const cycleReports = []
for (let c = 1; c <= CYCLES; c++) {
  // Design: which candidates to test (acquisition is deterministic in the engine; the
  // agent explains the pick to the scientist).
  const proposal = await agent(
    `Cycle ${c}: call propose_experiments for campaign "${CAMPAIGN}" and summarize the batch ` +
    `(candidate ids, predicted value ± uncertainty, and why each was chosen).`,
    { label: `cycle-${c}:propose`, phase: 'Run cycles' }
  )
  // Test: the assay oracle (a wet lab in production).
  const readouts = await agent(
    `Cycle ${c}: act as the assay for these proposed experiments and return plausible readouts ` +
    `for each candidate_id as JSON rows. Proposal: ${proposal}`,
    { label: `cycle-${c}:assay`, phase: 'Run cycles' }
  )
  // Learn: ingest + refit.
  await agent(
    `Cycle ${c}: call ingest_results for campaign "${CAMPAIGN}" with these readouts, then ` +
    `call campaign_status and return the status JSON. Readouts: ${readouts}`,
    { label: `cycle-${c}:ingest`, phase: 'Run cycles' }
  )
  cycleReports.push({ cycle: c })
}

phase('Report')
const report = await agent(
  `Write the campaign report for "${CAMPAIGN}": best-so-far vs. the starting point, budget spent, ` +
  `Pareto front if multi-objective, and — if a random-search baseline is available — how many ` +
  `experiments the closed loop saved. Be honest about uncertainty. Cycles run: ${CYCLES}.`,
  { label: 'campaign-report', phase: 'Report' }
)
return { campaign: CAMPAIGN, cycles: CYCLES, report }
