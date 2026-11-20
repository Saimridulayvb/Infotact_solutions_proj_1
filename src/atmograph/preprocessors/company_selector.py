"""
Company connectivity ranker and selector.
"""

import pandas as pd
from typing import Optional, List
from .entity_filter import EntityFilter

class CompanySelector:
    """Ranks organizations by unique input connections and selects top entities."""

    def __init__(self, entity_filter: Optional[EntityFilter] = None):
        self.entity_filter = entity_filter or EntityFilter()

    def select_top_companies(
        self,
        providers_df: pd.DataFrame,
        provision_df: pd.DataFrame,
        top_n: int = 20,
        min_connections: int = 1
    ) -> pd.DataFrame:
        # Filter organizations only
        orgs = providers_df[providers_df["provider_type"] == "organization"].copy()

        # Count unique provided_ids per provider
        counts = (
            provision_df.groupby("provider_id")["provided_id"]
            .nunique()
            .reset_index(name="connected_inputs")
        )

        # Merge with organization metadata
        merged = counts.merge(
            orgs[["provider_id", "provider_name", "country"]],
            on="provider_id",
            how="inner"
        )

        # Apply entity filter
        filtered = self.entity_filter.filter_providers(merged)

        # Deduplicate provider IDs
        deduped = filtered.drop_duplicates(subset="provider_id")

        # Filter by min connections
        qualified = deduped[deduped["connected_inputs"] >= min_connections]

        # Sort descending by connected_inputs, secondary by provider_name
        sorted_companies = qualified.sort_values(
            by=["connected_inputs", "provider_name"],
            ascending=[False, True]
        ).reset_index(drop=True)

        return sorted_companies.head(top_n).copy()


    def get_top_n_limit(self) -> int:
        """Return the maximum number of organizations configured for extraction."""
        return self.top_n


    def has_company(self, company_id: str, selected_df: pd.DataFrame) -> bool:
        """Check whether a specific provider ID is included in selected companies subset."""
        return company_id in selected_df["provider_id"].values if "provider_id" in selected_df.columns else False
