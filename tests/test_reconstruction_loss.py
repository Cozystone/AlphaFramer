# -*- coding: utf-8 -*-
"""Semantic-bottleneck audit: rebuild a scene from the context schema alone and measure what
survived. The decoder is deterministic on purpose; the loss is topology, not pixels; the dropped
attributes are the measured curriculum."""
import alphaframer.spatial_memory as sm
from alphaframer.reconstruction_loss import cycle_audit, topology_score


def test_identical_scene_scores_perfect():
    t = [{"label": "물병", "x": 0.2, "y": 0.6, "depth": 0.3},
         {"label": "컵", "x": 0.7, "y": 0.4, "depth": 0.6}]
    s = topology_score(t, [dict(o) for o in t])
    assert s["set_f1"] == 1.0 and s["relation"] == 1.0 and s["total"] == 1.0


def test_mirrored_layout_breaks_relation_not_set():
    t = [{"label": "물병", "x": 0.2, "y": 0.5, "depth": 0.5},
         {"label": "컵", "x": 0.8, "y": 0.5, "depth": 0.5}]
    mirrored = [{**o, "x": 1 - o["x"]} for o in t]          # left/right swapped
    s = topology_score(t, mirrored)
    assert s["set_f1"] == 1.0 and s["relation"] < 1.0       # same objects, broken order


def test_missing_object_breaks_set():
    t = [{"label": "물병", "x": 0.2, "y": 0.5}, {"label": "컵", "x": 0.8, "y": 0.5}]
    s = topology_score(t, t[:1])
    assert s["set_f1"] < 1.0


def test_capacity_names_dropped_attributes():
    t = [{"label": "물병", "x": 0.2, "y": 0.5, "size": 0.05}]
    s = topology_score(t, [{"label": "물병", "x": 0.2, "y": 0.5}])   # probe has no size
    assert "size" in s["capacity"]["dropped"]


def test_cycle_audit_pipe_is_lossless_on_topology():
    r = cycle_audit()
    assert r["set_f1"] == 1.0 and r["relation"] == 1.0 and r["position"] >= 0.99
    assert "size" in r["capacity"]["preserved"]              # the lesson we taught
    assert r["next_lessons"] == ["hue"]                      # the lesson still owed
    assert "deterministic" in r["decoder"]                   # generative decoders barred


def test_snapshot_carries_size_and_scales_rebuild(tmp_path):
    sm._LEDGER = tmp_path / "spatial.jsonl"
    sm.record_snapshot([{"label": "노트북", "x": 0.5, "y": 0.5, "depth": 0.2, "size": 0.2},
                        {"label": "컵", "x": 0.3, "y": 0.6, "depth": 0.2, "size": 0.01}], place="책상")
    scene = sm.reconstruct_scene(sm.recall_snapshot())
    big = next(o for o in scene["objects"] if o["label"] == "노트북")
    small = next(o for o in scene["objects"] if o["label"] == "컵")
    assert big["size"] == 0.2 and big["scale"] > small["scale"]   # remembered big rebuilds bigger
    assert big["shape"]["form"]                                    # replay carries silhouettes too


def test_snapshot_without_size_stays_honest(tmp_path):
    sm._LEDGER = tmp_path / "spatial.jsonl"
    sm.record_snapshot([{"label": "컵", "x": 0.5, "y": 0.5}])
    o = sm.recall_snapshot()["objects"][0]
    assert "size" not in o                                   # absent stays absent — never fabricated
