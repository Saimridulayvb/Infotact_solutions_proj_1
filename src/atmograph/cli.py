"""
Unified command line interface for AtmoGraph.
"""

import argparse
import sys
from pathlib import Path
from atmograph.loaders.dataset_bundle import load_dataset_bundle
from atmograph.validators.pipeline_validator import PipelineValidator
from atmograph.preprocessors.pipeline import PreprocessingPipeline
from atmograph.graph.csv_exporter import GraphCSVExporter
from atmograph.logger import get_logger

logger = get_logger("atmograph.cli")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AtmoGraph Supply Chain Pipeline CLI")
    parser.add_argument("--version", action="version", version="AtmoGraph 0.2.0")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # validate
    val_p = subparsers.add_parser("validate", help="Validate raw dataset quality")
    val_p.add_argument("--data-dir", default="data/raw", help="Path to raw data directory")

    # preprocess
    prep_p = subparsers.add_parser("preprocess", help="Run data cleaning and company selection")
    prep_p.add_argument("--data-dir", default="data/raw", help="Raw data directory")
    prep_p.add_argument("--output-dir", default="data/processed", help="Processed output directory")
    prep_p.add_argument("--top-n", type=int, default=20, help="Number of top companies to select")

    # export-graph
    exp_p = subparsers.add_parser("export-graph", help="Export graph nodes and edges for Neo4j")
    exp_p.add_argument("--processed-dir", default="data/processed", help="Processed data directory")
    exp_p.add_argument("--graph-dir", default="data/processed/graph", help="Graph export directory")

    # run-all
    subparsers.add_parser("run-all", help="Execute complete pipeline end-to-end")

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command or args.command == "run-all":
        logger.info("Executing AtmoGraph full pipeline end-to-end...")
        bundle = load_dataset_bundle("data/raw")
        validator = PipelineValidator()
        report = validator.run_all(bundle)
        logger.info("Data Validation: %s issues detected. Valid: %s", report.total_issues, report.is_valid)

        pipeline = PreprocessingPipeline(top_n=20)
        processed = pipeline.run_and_save(bundle, "data/processed")
        logger.info("Preprocessing complete: %d companies selected.", len(processed.selected_companies))

        GraphCSVExporter.export(
            processed.selected_companies,
            processed.selected_relationships,
            processed.goes_into_relationships,
            processed.is_type_of_relationships,
            "data/processed/graph"
        )
        logger.info("Graph export complete at data/processed/graph/")
        return 0

    if args.command == "validate":
        bundle = load_dataset_bundle(args.data_dir)
        report = PipelineValidator().run_all(bundle)
        print(f"Validation Report: {report.summary()}")
        return 0

    if args.command == "preprocess":
        bundle = load_dataset_bundle(args.data_dir)
        pipeline = PreprocessingPipeline(top_n=args.top_n)
        pipeline.run_and_save(bundle, args.output_dir)
        print(f"Preprocessed datasets saved to {args.output_dir}")
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())
