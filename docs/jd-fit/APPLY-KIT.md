# Apply kit — 8 roles, 8 tailored resumes, and the one thing I cannot do for you

**Blocker, stated first: I could not submit these.** All 8 applications live behind an
authenticated account — Google Careers requires a signed-in Google account
(`accounts.google.com` appears on the apply path), and NVIDIA's Workday requires one too.
I do not have your credentials, and the automation browser deliberately uses an isolated
profile rather than attaching to your logged-in daily browser. So every step up to the
sign-in wall is done and verified; the submit click is yours.

That is the playbook's own rule for auth-walled surfaces — *feasibility-probe the wall
first, and if it is walled, push auth into the user's own browser* — applied honestly
instead of pretending a headless agent can be you.

## What IS ready

8 role-tailored resumes, generated from ONE verified fact base
(`data/resume_facts.yml`) so no two documents disagree about the same work:

```bash
python3 scripts/build_resume.py --pdf        # regenerate all, md + html + pdf
python3 scripts/build_resume.py --slug gdm-humanoids --pdf
```

| # | Role | Company | Fit | Resume PDF |
|---|---|---|:--:|---|
| 1 | Research Engineer, **Human Understanding** | Google DeepMind | **95** | `resumes/gdm-human-understanding.pdf` |
| 2 | Research Engineer, **SSI / self-improving agents** | Google DeepMind | 92 | `resumes/gdm-ssi-self-improving-agents.pdf` |
| 3 | Research SWE, **Multimodal AI** | Google | 100 | `resumes/google-research-swe-multimodal.pdf` |
| 4 | RE, **Multimodal Reasoning / Information Literacy** | Google DeepMind | 100 | `resumes/gdm-multimodal-information-literacy.pdf` |
| 5 | RE, **Humanoids** | Google DeepMind | 94 | `resumes/gdm-humanoids.pdf` |
| 6 | RE, **Winslow** | Google DeepMind | 100 | `resumes/gdm-winslow.pdf` |
| 7 | RE, **AGI Safety & Alignment** | Google DeepMind | 92 | `resumes/gdm-agi-safety-alignment.pdf` |
| 8 | Sr RS, **Human-AI Perception & Interaction** | NVIDIA | 95 | `resumes/nvidia-human-ai-perception.pdf` |

Each one leads with the proof blocks that role actually turns on, and each ends with a
section called **"The edge I'd be learning, not teaching"** naming its real weak spot —
JAX/Flax for Human Understanding, distributed data infra for SSI, interpretability
tooling for AGI Safety, lab-scale human-subjects work for NVIDIA. That section is the
reason the rest of the document is believable; it is generated, not optional (the builder
refuses a role without one).

## The role your search never showed you

You searched *"Research Engineer, Human Understanding, DeepMind"*. LinkedIn returned a
posting titled "Research Engineer, DeepMind" whose body is Science & Strategic Initiatives
— a different role. **The actual Human Understanding role exists on Google Careers and was
not among the 10 LinkedIn ids.** It scores 95/100 over 11 caps and is now target #1.

Lesson worth keeping: search the **employer's own board**, not only the aggregator.

## Verified apply URLs

Confirmed by fetching each page (HTTP 200, title matched):

| Role | Apply URL |
|---|---|
| Human Understanding | `google.com/about/careers/applications/jobs/results/107269257477137094-research-engineer-human-understanding-deepmind` |
| Humanoids | `…/105870811830592198-research-engineer-humanoids-deepmind` |
| AGI Safety & Alignment | `…/102552346151527110-research-engineer-agi-safety-and-alignment-deepmind` |

**Not yet resolved to a Google Careers id** (SSI, Multimodal AI, Information Literacy,
Winslow): the LinkedIn posting does not expose the external apply link without auth, and
I did not want to guess an id — a wrong id applies you to the wrong job. Resolve each by
searching its exact title on Google Careers, or open the LinkedIn posting while signed in
and follow its Apply button.

NVIDIA: `nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite` (Workday, account required).

## Answers vault — the fields every one of these forms asks

Reused verbatim so no two applications disagree:

| Field | Answer |
|---|---|
| Name | Paul Jialiang Wu |
| Email | wjlgatech@gmail.com |
| Phone | 650-656-3046 |
| Location | Mountain View, CA |
| Work authorization | No visa sponsorship required |
| LinkedIn | linkedin.com/in/paul-jialiang-wu-phd |
| GitHub | github.com/wjlgatech |
| Portfolio | agentic-portfolio-lovat.vercel.app |
| Highest degree | PhD, Bioinformatics — Georgia Tech |
| Demographic questions | decline to self-identify |

## Your 5-minute path per role

1. Open the apply URL **in your normal signed-in browser**.
2. Upload `docs/jd-fit/resumes/<slug>.pdf` — the one matching that role, not a generic copy.
3. Fields autofill from your Google profile; check them against the vault above.
4. Before submitting, verify every field renders (the Stage 7.5 rule: verify-gate each
   field, because a silently-empty phone or resume chip is the common failure).
5. Screenshot the confirmation, then log it in the campaign's Outcome log.

If you would rather I drive it: run `/anyagent` again from a session where you have
already signed in to Google Careers in the automation Chrome profile
(`~/.browser-harness-chrome`, CDP 9223) and say so — then the auth wall is gone and I can
fill and verify each form field-by-field, stopping at the final submit for your click.
