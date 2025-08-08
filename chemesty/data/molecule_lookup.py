"""
Module for looking up molecules in the dataset.

This module provides functions for looking up molecules in the dataset
using various search criteria such as formula, name, molecular weight,
and substructure.
"""

import os
from typing import List, Dict, Optional, Tuple, Any, Union

from chemesty.data.database import MoleculeDatabase
from chemesty.data.download import download_chembl_dataset
from chemesty.molecules.molecule import Molecule

class MoleculeLookup:
    """
    Class for looking up molecules in the dataset.

    This class provides methods for looking up molecules in the dataset
    using various search criteria such as formula, name, molecular weight,
    and substructure.
    """

    def __init__(self, db_path: str = None):
        """
        Initialize with path to SQLite database.

        Args:
            db_path: Path to the SQLite database file. If None, uses the default path.
        """
        # Check if the database exists, and if not, download it
        if db_path is None:
            # Use default path in the package data directory
            package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(package_dir, 'data', 'molecules.db')

        # If the database doesn't exist, download it
        if not os.path.exists(db_path):
            print(f"Database not found at {db_path}. Downloading...")
            download_chembl_dataset()

        # Initialize the database connection
        self.db = MoleculeDatabase(db_path)

    def lookup_by_formula(self, formula: str) -> List[Molecule]:
        """
        Look up molecules by formula.

        Args:
            formula: The molecular formula to search for

        Returns:
            List of Molecule objects matching the formula
        """
        results = self.db.search_by_formula(formula)
        return [self._create_molecule(row['smiles']) for row in results]

    def lookup_by_name(self, name_pattern: str) -> List[Molecule]:
        """
        Look up molecules by name pattern.

        Args:
            name_pattern: The name pattern to search for

        Returns:
            List of Molecule objects matching the name pattern
        """
        results = self.db.search_by_name(name_pattern)
        return [self._create_molecule(row['smiles']) for row in results]

    def lookup_by_molecular_weight(self, target_mw: float, tolerance: float = 0.1) -> List[Molecule]:
        """
        Look up molecules by molecular weight within a tolerance.

        Args:
            target_mw: The target molecular weight
            tolerance: The tolerance range (±) in atomic mass units

        Returns:
            List of Molecule objects matching the molecular weight
        """
        results = self.db.search_by_molecular_weight(target_mw, tolerance)
        return [self._create_molecule(row['smiles']) for row in results]

    def lookup_by_volume(self, target_volume: float, tolerance_percent: float = 10.0) -> List[Molecule]:
        """
        Look up molecules by volume within a percentage tolerance.

        Args:
            target_volume: The target volume in cubic angstroms (Å³)
            tolerance_percent: The tolerance range as a percentage of the target value

        Returns:
            List of Molecule objects matching the volume
        """
        results = self.db.search_by_volume(target_volume, tolerance_percent)
        return [self._create_molecule(row['smiles']) for row in results]

    def lookup_by_density(self, target_density: float, tolerance_percent: float = 10.0) -> List[Molecule]:
        """
        Look up molecules by density within a percentage tolerance.

        Args:
            target_density: The target density in g/cm³
            tolerance_percent: The tolerance range as a percentage of the target value

        Returns:
            List of Molecule objects matching the density
        """
        results = self.db.search_by_density(target_density, tolerance_percent)
        return [self._create_molecule(row['smiles']) for row in results]

    def lookup_by_molar_volume(self, target_molar_volume: float, tolerance_percent: float = 10.0) -> List[Molecule]:
        """
        Look up molecules by molar volume within a percentage tolerance.

        Args:
            target_molar_volume: The target molar volume in cm³/mol
            tolerance_percent: The tolerance range as a percentage of the target value

        Returns:
            List of Molecule objects matching the molar volume
        """
        results = self.db.search_by_molar_volume(target_molar_volume, tolerance_percent)
        return [self._create_molecule(row['smiles']) for row in results]

    def lookup_by_substructure(self, smarts_pattern: str, limit: int = 100) -> List[Molecule]:
        """
        Look up molecules containing a substructure.

        Args:
            smarts_pattern: SMARTS pattern for the substructure
            limit: Maximum number of results to return

        Returns:
            List of Molecule objects containing the substructure
        """
        results = self.db.search_by_substructure(smarts_pattern, limit)
        return [self._create_molecule(row['smiles']) for row in results]

    def lookup_similar_molecules(self, smiles: str, threshold: float = 0.7, limit: int = 100) -> List[Tuple[Molecule, float]]:
        """
        Look up molecules similar to a reference molecule.

        Args:
            smiles: SMILES string of the reference molecule
            threshold: Similarity threshold (0.0 to 1.0)
            limit: Maximum number of results to return

        Returns:
            List of tuples (Molecule, similarity) sorted by similarity
        """
        results = self.db.get_similar_molecules(smiles, threshold, limit)
        return [(self._create_molecule(row['smiles']), similarity) for row, similarity in results]

    def find_molecule(self, query: str) -> List[Molecule]:
        """
        Find molecules using a tiered lookup strategy.

        This method tries different lookup strategies in order of increasing
        computational cost until it finds matching molecules.

        Args:
            query: The query string (could be formula, name, SMILES, etc.)

        Returns:
            List of matching Molecule objects
        """
        # Try exact formula match first (fastest)
        results = self.lookup_by_formula(query)
        if results:
            return results

        # Try name search next
        results = self.lookup_by_name(query)
        if results:
            return results

        # Try molecular weight, volume, density, or molar volume if it looks like a number
        try:
            value = float(query)

            # Try molecular weight first (most common)
            results = self.lookup_by_molecular_weight(value, tolerance=0.1)
            if results:
                return results

            # Try volume next
            results = self.lookup_by_volume(value, tolerance_percent=10.0)
            if results:
                return results

            # Try density next
            if 0.5 <= value <= 20.0:  # Typical range for molecular density in g/cm³
                results = self.lookup_by_density(value, tolerance_percent=10.0)
                if results:
                    return results

            # Try molar volume last
            results = self.lookup_by_molar_volume(value, tolerance_percent=10.0)
            if results:
                return results
        except ValueError:
            pass

        # Try SMILES if it looks like a SMILES string
        if '(' in query or '=' in query:
            try:
                similar_results = self.lookup_similar_molecules(query)
                return [molecule for molecule, _ in similar_results]
            except Exception:
                pass

        # As a last resort, try substructure search
        try:
            results = self.lookup_by_substructure(query)
            return results
        except Exception:
            pass

        return []

    def _create_molecule(self, smiles: str) -> Molecule:
        """
        Create a Molecule object from a SMILES string.

        Args:
            smiles: SMILES string

        Returns:
            Molecule object
        """
        return Molecule(smiles=smiles)

    def close(self):
        """Close the database connection."""
        self.db.close()

    def __enter__(self):
        """Support for context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager protocol."""
        self.close()


def lookup_molecule(query: str, db_path: str = None) -> List[Molecule]:
    """
    Convenience function for looking up molecules.

    Args:
        query: The query string (could be formula, name, SMILES, etc.)
        db_path: Path to the SQLite database file. If None, uses the default path.

    Returns:
        List of matching Molecule objects
    """
    with MoleculeLookup(db_path) as lookup:
        return lookup.find_molecule(query)
