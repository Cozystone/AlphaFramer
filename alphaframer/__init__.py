# -*- coding: utf-8 -*-
"""AlphaFramer — a spatial-context perception protocol (no-frame, semantic-bottleneck honest)."""
from .object_recognition import recognize_object, instance_stats
from .spatial_memory import record_snapshot, recall_snapshot, reconstruct_scene, detect_spatial_recall
from .reconstruction_loss import cycle_audit, topology_score

__all__ = ["recognize_object", "instance_stats", "record_snapshot", "recall_snapshot",
           "reconstruct_scene", "detect_spatial_recall", "cycle_audit", "topology_score"]
