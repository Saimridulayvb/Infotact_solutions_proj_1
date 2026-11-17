"""
End-to-end integration tests for AtmoGraph pipeline and CLI execution.
"""

import subprocess
import sys
from pathlib import Path
import pandas as pd

def test_pipeline_integration(tmp_path: Path):
    from atmograph.loaders.dataset_bundle import load_dataset_bundle
    from atmograph.preprocessors.pipeline import PreprocessingPipeline
    from atmograph.graph.csv_exporter import GraphCSVExporter

    raw_dir = Path(__file__).parent.parent / "data" / "raw"
    bundle = load_dataset_bundle(raw_dir)

    pipeline = PreprocessingPipeline(top_n=10)
    out_dir = tmp_path / "processed"
    processed = pipeline.run_and_save(bundle, out_dir)

    assert len(processed.selected_companies) == 10
    assert (out_dir / "selected_companies.csv").exists()
    assert (out_dir / "selected_relationships.csv").exists()

    graph_dir = tmp_path / "graph"
    GraphCSVExporter.export(
        processed.selected_companies,
        processed.selected_relationships,
        processed.goes_into_relationships,
        processed.is_type_of_relationships,
        graph_dir
    )
    assert (graph_dir / "companies_nodes.csv").exists()
    assert (graph_dir / "supplies_edges.csv").exists()

def test_cli_execution():
    root = Path(__file__).parent.parent
    cmd = [sys.executable, str(root / "scripts" / "run_pipeline.py"), "preprocess"]
    res = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert res.returncode == 0
    assert "Preprocessed datasets" in res.stdout
