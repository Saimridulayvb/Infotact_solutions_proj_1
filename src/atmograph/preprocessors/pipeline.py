"""
End-to-end preprocessing pipeline orchestrator.
Produces all standard processed datasets.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union
import pandas as pd

from atmograph.loaders.dataset_bundle import DatasetBundle, load_dataset_bundle
from .company_selector import CompanySelector
from .relationship_extractor import RelationshipExtractor
from .stage_resolver import StageResolver
from .sequence_processor import SequenceProcessor
from .deduplicator import RelationshipDeduplicator
from .cleaner import StringSanitizer

@dataclass
class ProcessedBundle:
    selected_companies: pd.DataFrame
    selected_relationships: pd.DataFrame
    goes_into_relationships: pd.DataFrame
    is_type_of_relationships: pd.DataFrame

class PreprocessingPipeline:
    """Orchestrates data cleaning, company ranking, relationship filtering, and file export."""

    def __init__(self, top_n: int = 20):
        self.top_n = top_n
        self.company_selector = CompanySelector()
        self.stage_resolver = StageResolver()
        self.seq_processor = SequenceProcessor()
        self.deduplicator = RelationshipDeduplicator()

    def run(self, bundle: DatasetBundle) -> ProcessedBundle:
        # 1. Sanitize raw text
        providers = StringSanitizer.sanitize_dataframe(bundle.providers)
        provision = StringSanitizer.sanitize_dataframe(bundle.provision)
        inputs = StringSanitizer.sanitize_dataframe(bundle.inputs)
        sequence = StringSanitizer.sanitize_dataframe(bundle.sequence)

        # 2. Resolve missing stages in inputs
        resolved_inputs = self.stage_resolver.resolve_stages(inputs, sequence)

        # 3. Select top companies
        selected_companies = self.company_selector.select_top_companies(
            providers, provision, top_n=self.top_n
        )

        # 4. Extract relationships and deduplicate
        raw_relationships = RelationshipExtractor.extract_relationships(
            selected_companies, provision, resolved_inputs
        )
        selected_relationships = self.deduplicator.deduplicate(raw_relationships)

        # 5. Process sequence edges
        goes_into, is_type_of = self.seq_processor.process(sequence)

        return ProcessedBundle(
            selected_companies=selected_companies,
            selected_relationships=selected_relationships,
            goes_into_relationships=goes_into,
            is_type_of_relationships=is_type_of
        )

    def run_and_save(self, bundle: DatasetBundle, output_dir: Union[str, Path] = "data/processed") -> ProcessedBundle:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        processed = self.run(bundle)
        processed.selected_companies.to_csv(out_path / "selected_companies.csv", index=False)
        processed.selected_relationships.to_csv(out_path / "selected_relationships.csv", index=False)
        processed.goes_into_relationships.to_csv(out_path / "goes_into_relationships.csv", index=False)
        processed.is_type_of_relationships.to_csv(out_path / "is_type_of_relationships.csv", index=False)

        return processed
