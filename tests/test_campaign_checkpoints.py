"""Dated checkpoints must be WOOP-complete, and a past-due one must FAIL the build.

Three consecutive report cards recorded the same growth miss (F3 — no dated checkpoint).
Each time the open partials were named with a leverage score, which reads like a plan and
is only a ranking. The fix is not another reminder: it is a test that turns an overdue
checkpoint into a red build, because that is the one form of memory that does not depend
on anyone remembering.
"""

import datetime
import pathlib

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = yaml.safe_load((ROOT / "data" / "campaign_checkpoints.yml").read_text())
ITEMS = DATA["checkpoints"]
VALID_STATUS = {"open", "done", "wont-build"}


def test_there_is_at_least_one_checkpoint():
    """An empty file would satisfy every other test in here."""
    assert ITEMS, "no checkpoints recorded — the F3 miss is back"


@pytest.mark.parametrize("item", ITEMS, ids=[i["id"] for i in ITEMS])
class TestEachCheckpointIsWoopComplete:
    def test_has_an_id_and_a_description(self, item):
        assert item.get("id") and len(item.get("what", "")) > 40

    def test_has_a_real_date(self, item):
        """`by` must parse as a date — 'soon' is how the miss happened."""
        datetime.date.fromisoformat(str(item["by"]))

    def test_has_a_metric_that_states_what_will_be_true(self, item):
        assert len(item.get("metric", "")) > 40, f"{item['id']}: metric too vague"

    def test_has_an_if_then_plan_not_just_a_hope(self, item):
        """Mental contrasting: an obstacle WITH a matching if-then. A checkpoint with no
        if_missed is a fantasy, which the growth rubric says backfires."""
        assert len(item.get("if_missed", "")) > 40, f"{item['id']}: no if-then"

    def test_status_is_from_the_closed_set(self, item):
        assert item.get("status") in VALID_STATUS


def test_no_checkpoint_is_past_due_while_still_open():
    """THE GATE. An overdue open checkpoint fails the build, naming itself.

    'wont-build' counts as closed on purpose: an honestly declined item is a decision,
    and the point of this file is to forbid silent drift, not to forbid saying no.
    """
    today = datetime.date.today()
    overdue = [i for i in ITEMS
               if i["status"] == "open" and datetime.date.fromisoformat(str(i["by"])) < today]
    assert not overdue, (
        "past-due checkpoint(s) still open — resolve or explicitly decline them: "
        + "; ".join(f"{i['id']} (due {i['by']}): {i['if_missed'][:70]}" for i in overdue))


def test_every_open_item_names_a_specific_next_action():
    """Guards against a checkpoint that is technically complete but unactionable."""
    for i in ITEMS:
        if i["status"] == "open":
            assert any(w in i["if_missed"].lower()
                       for w in ("resolve", "split", "escalate", "state", "do not")), \
                f"{i['id']}: if_missed does not name an action"
