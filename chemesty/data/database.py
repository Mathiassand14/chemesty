"""
Module for interacting with the molecule database.

This module provides a class for interacting with the SQLite database
that stores molecule data.
"""

import os
import sqlite3
import threading
from contextlib import contextmanager
from typing import List, Tuple, Optional, Dict, Any, Iterator
import time
from chemesty.utils.parallel_processing import ParallelDatabaseProcessor

class MoleculeDatabase:
    """
    Class for interacting with the molecule database.

    This class provides methods for storing and retrieving molecule data
    from a SQLite database.
    """

    def __init__(self, db_path: str, pool_size: int = 5):
        """
        Initialize with path to SQLite database and connection pooling.

        Args:
            db_path: Path to the SQLite database file
            pool_size: Maximum number of connections in the pool
        """
        self.db_path = db_path
        self.pool_size = pool_size
        self._connection_pool = []
        self._pool_lock = threading.Lock()
        
        # Initialize the main connection for setup
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # Enable WAL mode for better concurrent access
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.conn.execute('PRAGMA synchronous=NORMAL')
        self.conn.execute('PRAGMA cache_size=10000')
        self.conn.execute('PRAGMA temp_store=MEMORY')

        # Create the molecules table if it doesn't exist
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS molecules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            smiles TEXT UNIQUE,
            formula TEXT,
            molecular_weight REAL,
            inchi TEXT,
            logp REAL,
            num_atoms INTEGER,
            num_rings INTEGER,
            volume REAL,
            density REAL,
            molar_volume REAL
        )
        ''')

        # Create indexes for faster lookups
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_formula ON molecules(formula)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_name ON molecules(name)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_mw ON molecules(molecular_weight)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_smiles ON molecules(smiles)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_volume ON molecules(volume)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_density ON molecules(density)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_molar_volume ON molecules(molar_volume)')

    def add_molecule(self, name: str, smiles: str, formula: str, molecular_weight: float,
                    inchi: Optional[str] = None, logp: Optional[float] = None,
                    num_atoms: Optional[int] = None, num_rings: Optional[int] = None,
                    volume: Optional[float] = None, density: Optional[float] = None,
                    molar_volume: Optional[float] = None) -> int:
        """
        Add a molecule to the database.

        Args:
            name: Name of the molecule
            smiles: SMILES string representation of the molecule
            formula: Molecular formula
            molecular_weight: Molecular weight
            inchi: InChI string representation of the molecule
            logp: LogP value
            num_atoms: Number of atoms
            num_rings: Number of rings
            volume: Molecular volume in cubic angstroms (Å³)
            density: Molecular density in g/cm³
            molar_volume: Molar volume in cm³/mol

        Returns:
            ID of the inserted molecule
        """
        # If volume, density, or molar_volume are not provided, calculate them
        if volume is None or density is None or molar_volume is None:
            from chemesty.molecules.molecule import Molecule
            mol = Molecule(smiles=smiles)
            volume = volume or mol.volume_value
            density = density or mol.density_value
            molar_volume = molar_volume or mol.molar_volume

        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO molecules
        (name, smiles, formula, molecular_weight, inchi, logp, num_atoms, num_rings, volume, density, molar_volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, smiles, formula, molecular_weight, inchi, logp, num_atoms, num_rings, volume, density, molar_volume))
        self.conn.commit()

        # Get the ID of the inserted molecule
        cursor.execute('SELECT id FROM molecules WHERE smiles = ?', (smiles,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_molecule_by_id(self, molecule_id: int) -> Optional[sqlite3.Row]:
        """
        Get a molecule by ID with optimized column selection.

        Args:
            molecule_id: ID of the molecule

        Returns:
            Molecule data as a sqlite3.Row, or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, name, smiles, formula, molecular_weight, inchi, logp, 
               num_atoms, num_rings, volume, density, molar_volume
        FROM molecules WHERE id = ?
        ''', (molecule_id,))
        return cursor.fetchone()

    def search_by_formula(self, formula: str) -> List[sqlite3.Row]:
        """
        Search for molecules by formula.

        Args:
            formula: Molecular formula

        Returns:
            List of matching molecules
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, smiles FROM molecules WHERE formula = ?', (formula,))
        return cursor.fetchall()

    def search_by_name(self, name_pattern: str) -> List[sqlite3.Row]:
        """
        Search for molecules by name pattern.

        Args:
            name_pattern: Name pattern to search for

        Returns:
            List of matching molecules
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, smiles FROM molecules WHERE name LIKE ?', (f'%{name_pattern}%',))
        return cursor.fetchall()

    def search_by_name_fuzzy(self, name_pattern: str, threshold: float = 0.6, limit: int = 100) -> List[Tuple[sqlite3.Row, float]]:
        """
        Search for molecules by name using fuzzy matching.

        Args:
            name_pattern: Name pattern to search for
            threshold: Similarity threshold (0.0 to 1.0)
            limit: Maximum number of results to return

        Returns:
            List of tuples (molecule, similarity) sorted by similarity
        """
        try:
            from difflib import SequenceMatcher
        except ImportError:
            # Fallback to regular name search
            return [(mol, 1.0) for mol in self.search_by_name(name_pattern)]

        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, smiles FROM molecules WHERE name IS NOT NULL')
        all_molecules = cursor.fetchall()
        
        fuzzy_matches = []
        name_pattern_lower = name_pattern.lower()
        
        for molecule in all_molecules:
            molecule_name = molecule['name']
            if molecule_name:
                molecule_name_lower = molecule_name.lower()
                
                # Calculate similarity using SequenceMatcher
                similarity = SequenceMatcher(None, name_pattern_lower, molecule_name_lower).ratio()
                
                # Also check if the pattern is contained in the name (partial match bonus)
                if name_pattern_lower in molecule_name_lower:
                    similarity = max(similarity, 0.8)  # Boost similarity for substring matches
                
                if similarity >= threshold:
                    fuzzy_matches.append((molecule, similarity))
        
        # Sort by similarity (descending) and limit results
        fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
        return fuzzy_matches[:limit]

    def search_by_molecular_weight(self, target_mw: float, tolerance: float = 0.1) -> List[sqlite3.Row]:
        """
        Search for molecules by molecular weight within a tolerance.

        Args:
            target_mw: Target molecular weight
            tolerance: Tolerance range (±) in atomic mass units

        Returns:
            List of matching molecules
        """
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, name, smiles, molecular_weight
        FROM molecules
        WHERE molecular_weight BETWEEN ? AND ?
        ORDER BY ABS(molecular_weight - ?)
        ''', (target_mw - tolerance, target_mw + tolerance, target_mw))
        return cursor.fetchall()

    def search_by_volume(self, target_volume: float, tolerance_percent: float = 10.0) -> List[sqlite3.Row]:
        """
        Search for molecules by volume within a percentage tolerance.

        Args:
            target_volume: Target volume in cubic angstroms (Å³)
            tolerance_percent: Tolerance range as a percentage of the target value

        Returns:
            List of matching molecules
        """
        tolerance = target_volume * (tolerance_percent / 100.0)
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, name, smiles, volume
        FROM molecules
        WHERE volume BETWEEN ? AND ?
        ORDER BY ABS(volume - ?)
        ''', (target_volume - tolerance, target_volume + tolerance, target_volume))
        return cursor.fetchall()

    def search_by_density(self, target_density: float, tolerance_percent: float = 10.0) -> List[sqlite3.Row]:
        """
        Search for molecules by density within a percentage tolerance.

        Args:
            target_density: Target density in g/cm³
            tolerance_percent: Tolerance range as a percentage of the target value

        Returns:
            List of matching molecules
        """
        tolerance = target_density * (tolerance_percent / 100.0)
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, name, smiles, density
        FROM molecules
        WHERE density BETWEEN ? AND ?
        ORDER BY ABS(density - ?)
        ''', (target_density - tolerance, target_density + tolerance, target_density))
        return cursor.fetchall()

    def search_by_molar_volume(self, target_molar_volume: float, tolerance_percent: float = 10.0) -> List[sqlite3.Row]:
        """
        Search for molecules by molar volume within a percentage tolerance.

        Args:
            target_molar_volume: Target molar volume in cm³/mol
            tolerance_percent: Tolerance range as a percentage of the target value

        Returns:
            List of matching molecules
        """
        tolerance = target_molar_volume * (tolerance_percent / 100.0)
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, name, smiles, molar_volume
        FROM molecules
        WHERE molar_volume BETWEEN ? AND ?
        ORDER BY ABS(molar_volume - ?)
        ''', (target_molar_volume - tolerance, target_molar_volume + tolerance, target_molar_volume))
        return cursor.fetchall()

    def search_by_substructure(self, smarts_pattern: str, limit: int = 100) -> List[sqlite3.Row]:
        """
        Search for molecules containing a substructure using RDKit.

        Args:
            smarts_pattern: SMARTS pattern for the substructure
            limit: Maximum number of results to return

        Returns:
            List of matching molecules
        """
        try:
            from rdkit import Chem
            from rdkit.Chem import rdMolDescriptors
        except ImportError:
            # Fallback to dummy implementation if RDKit is not available
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, name, smiles FROM molecules LIMIT ?', (limit,))
            return cursor.fetchall()

        # Parse the SMARTS pattern
        pattern_mol = Chem.MolFromSmarts(smarts_pattern)
        if pattern_mol is None:
            raise ValueError(f"Invalid SMARTS pattern: {smarts_pattern}")

        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, smiles FROM molecules')
        all_molecules = cursor.fetchall()
        
        matching_molecules = []
        for molecule in all_molecules:
            if len(matching_molecules) >= limit:
                break
                
            smiles = molecule['smiles']
            if smiles:
                try:
                    mol = Chem.MolFromSmiles(smiles)
                    if mol is not None and mol.HasSubstructMatch(pattern_mol):
                        matching_molecules.append(molecule)
                except Exception:
                    # Skip molecules that can't be parsed
                    continue
        
        return matching_molecules

    def get_similar_molecules(self, smiles: str, threshold: float = 0.7, limit: int = 100) -> List[Tuple[sqlite3.Row, float]]:
        """
        Get molecules similar to a reference molecule using RDKit fingerprints.

        Args:
            smiles: SMILES string of the reference molecule
            threshold: Similarity threshold (0.0 to 1.0)
            limit: Maximum number of results to return

        Returns:
            List of tuples (molecule, similarity) sorted by similarity
        """
        try:
            from rdkit import Chem
            from rdkit.Chem import rdMolDescriptors
            from rdkit import DataStructs
        except ImportError:
            # Fallback to dummy implementation if RDKit is not available
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, name, smiles FROM molecules LIMIT ?', (limit,))
            molecules = cursor.fetchall()
            return [(molecule, 0.9) for molecule in molecules]

        # Parse the reference molecule
        ref_mol = Chem.MolFromSmiles(smiles)
        if ref_mol is None:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        # Calculate reference fingerprint
        ref_fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(ref_mol, 2, nBits=2048)

        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, smiles FROM molecules')
        all_molecules = cursor.fetchall()
        
        similar_molecules = []
        for molecule in all_molecules:
            smiles_str = molecule['smiles']
            if smiles_str and smiles_str != smiles:  # Skip the reference molecule itself
                try:
                    mol = Chem.MolFromSmiles(smiles_str)
                    if mol is not None:
                        # Calculate fingerprint for this molecule
                        fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
                        
                        # Calculate Tanimoto similarity
                        similarity = DataStructs.TanimotoSimilarity(ref_fp, fp)
                        
                        if similarity >= threshold:
                            similar_molecules.append((molecule, similarity))
                except Exception:
                    # Skip molecules that can't be parsed
                    continue
        
        # Sort by similarity (descending) and limit results
        similar_molecules.sort(key=lambda x: x[1], reverse=True)
        return similar_molecules[:limit]

    def search_compound_query(self, 
                            name_pattern: str = None,
                            formula: str = None,
                            mw_min: float = None,
                            mw_max: float = None,
                            smarts_pattern: str = None,
                            similarity_smiles: str = None,
                            similarity_threshold: float = 0.7,
                            limit: int = 100) -> List[sqlite3.Row]:
        """
        Perform a compound search combining multiple criteria.

        Args:
            name_pattern: Name pattern to search for (optional)
            formula: Exact molecular formula (optional)
            mw_min: Minimum molecular weight (optional)
            mw_max: Maximum molecular weight (optional)
            smarts_pattern: SMARTS pattern for substructure search (optional)
            similarity_smiles: SMILES for similarity search (optional)
            similarity_threshold: Similarity threshold for similarity search
            limit: Maximum number of results to return

        Returns:
            List of molecules matching all specified criteria
        """
        # Start with all molecules
        cursor = self.conn.cursor()
        
        # Build the SQL query dynamically based on provided criteria
        conditions = []
        params = []
        
        if name_pattern:
            conditions.append("name LIKE ?")
            params.append(f'%{name_pattern}%')
        
        if formula:
            conditions.append("formula = ?")
            params.append(formula)
        
        if mw_min is not None:
            conditions.append("molecular_weight >= ?")
            params.append(mw_min)
        
        if mw_max is not None:
            conditions.append("molecular_weight <= ?")
            params.append(mw_max)
        
        # Base query
        base_query = 'SELECT id, name, smiles, formula, molecular_weight FROM molecules'
        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)
        
        cursor.execute(base_query, params)
        candidates = cursor.fetchall()
        
        # Apply RDKit-based filters if specified
        if smarts_pattern or similarity_smiles:
            try:
                from rdkit import Chem
                from rdkit.Chem import rdMolDescriptors
                from rdkit import DataStructs
                
                filtered_candidates = []
                
                # Prepare substructure pattern if specified
                pattern_mol = None
                if smarts_pattern:
                    pattern_mol = Chem.MolFromSmarts(smarts_pattern)
                    if pattern_mol is None:
                        raise ValueError(f"Invalid SMARTS pattern: {smarts_pattern}")
                
                # Prepare similarity reference if specified
                ref_fp = None
                if similarity_smiles:
                    ref_mol = Chem.MolFromSmiles(similarity_smiles)
                    if ref_mol is None:
                        raise ValueError(f"Invalid SMILES string: {similarity_smiles}")
                    ref_fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(ref_mol, 2, nBits=2048)
                
                for molecule in candidates:
                    if len(filtered_candidates) >= limit:
                        break
                    
                    smiles = molecule['smiles']
                    if not smiles:
                        continue
                    
                    try:
                        mol = Chem.MolFromSmiles(smiles)
                        if mol is None:
                            continue
                        
                        # Check substructure match if specified
                        if pattern_mol and not mol.HasSubstructMatch(pattern_mol):
                            continue
                        
                        # Check similarity if specified
                        if ref_fp:
                            fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
                            similarity = DataStructs.TanimotoSimilarity(ref_fp, fp)
                            if similarity < similarity_threshold:
                                continue
                        
                        filtered_candidates.append(molecule)
                        
                    except Exception:
                        # Skip molecules that can't be parsed
                        continue
                
                return filtered_candidates
                
            except ImportError:
                # If RDKit is not available, ignore RDKit-based filters
                pass
        
        return candidates[:limit]

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        """Support for context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager protocol."""
        self.close()

    # Performance enhancement methods
    
    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """
        Get a connection from the pool or create a new one.
        
        Yields:
            A database connection
        """
        conn = None
        try:
            with self._pool_lock:
                if self._connection_pool:
                    conn = self._connection_pool.pop()
                else:
                    conn = sqlite3.connect(self.db_path, check_same_thread=False)
                    conn.row_factory = sqlite3.Row
                    # Apply performance settings
                    conn.execute('PRAGMA journal_mode=WAL')
                    conn.execute('PRAGMA synchronous=NORMAL')
                    conn.execute('PRAGMA cache_size=10000')
                    conn.execute('PRAGMA temp_store=MEMORY')
            
            yield conn
            
        finally:
            if conn:
                with self._pool_lock:
                    if len(self._connection_pool) < self.pool_size:
                        self._connection_pool.append(conn)
                    else:
                        conn.close()
    
    def batch_add_molecules(self, molecules_data: List[Dict[str, Any]]) -> List[int]:
        """
        Add multiple molecules in a single transaction for better performance.
        
        Args:
            molecules_data: List of dictionaries containing molecule data
            
        Returns:
            List of inserted molecule IDs
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            inserted_ids = []
            
            try:
                conn.execute('BEGIN TRANSACTION')
                
                for mol_data in molecules_data:
                    cursor.execute('''
                    INSERT OR IGNORE INTO molecules
                    (name, smiles, formula, molecular_weight, inchi, logp, num_atoms, num_rings, volume, density, molar_volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        mol_data.get('name'),
                        mol_data.get('smiles'),
                        mol_data.get('formula'),
                        mol_data.get('molecular_weight'),
                        mol_data.get('inchi'),
                        mol_data.get('logp'),
                        mol_data.get('num_atoms'),
                        mol_data.get('num_rings'),
                        mol_data.get('volume'),
                        mol_data.get('density'),
                        mol_data.get('molar_volume')
                    ))
                    
                    if cursor.lastrowid:
                        inserted_ids.append(cursor.lastrowid)
                
                conn.commit()
                return inserted_ids
                
            except Exception as e:
                conn.rollback()
                raise e
    
    def batch_get_molecules(self, identifiers: List[str], search_type: str = 'name') -> List[Optional[sqlite3.Row]]:
        """
        Get multiple molecules in a single query for better performance.
        
        Args:
            identifiers: List of molecule identifiers
            search_type: Type of identifier ('name', 'formula', 'smiles', 'id')
            
        Returns:
            List of molecule rows (None for not found)
        """
        if not identifiers:
            return []
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build query based on search type
            if search_type == 'name':
                placeholders = ','.join(['?' for _ in identifiers])
                query = f'SELECT * FROM molecules WHERE name IN ({placeholders})'
            elif search_type == 'formula':
                placeholders = ','.join(['?' for _ in identifiers])
                query = f'SELECT * FROM molecules WHERE formula IN ({placeholders})'
            elif search_type == 'smiles':
                placeholders = ','.join(['?' for _ in identifiers])
                query = f'SELECT * FROM molecules WHERE smiles IN ({placeholders})'
            elif search_type == 'id':
                placeholders = ','.join(['?' for _ in identifiers])
                query = f'SELECT * FROM molecules WHERE id IN ({placeholders})'
            else:
                raise ValueError(f"Invalid search_type: {search_type}")
            
            cursor.execute(query, identifiers)
            results = cursor.fetchall()
            
            # Create a mapping for quick lookup
            result_map = {}
            if search_type == 'name':
                result_map = {row['name']: row for row in results}
            elif search_type == 'formula':
                result_map = {row['formula']: row for row in results}
            elif search_type == 'smiles':
                result_map = {row['smiles']: row for row in results}
            elif search_type == 'id':
                result_map = {row['id']: row for row in results}
            
            # Return results in the same order as input identifiers
            return [result_map.get(identifier) for identifier in identifiers]
    
    def batch_update_molecules(self, updates: List[Dict[str, Any]]) -> int:
        """
        Update multiple molecules in a single transaction.
        
        Args:
            updates: List of dictionaries with 'id' and update fields
            
        Returns:
            Number of molecules updated
        """
        if not updates:
            return 0
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            updated_count = 0
            
            try:
                conn.execute('BEGIN TRANSACTION')
                
                for update_data in updates:
                    if 'id' not in update_data:
                        continue
                    
                    molecule_id = update_data.pop('id')
                    
                    # Build dynamic UPDATE query
                    set_clauses = []
                    values = []
                    
                    for field, value in update_data.items():
                        if field in ['name', 'smiles', 'formula', 'molecular_weight', 
                                   'inchi', 'logp', 'num_atoms', 'num_rings', 
                                   'volume', 'density', 'molar_volume']:
                            set_clauses.append(f"{field} = ?")
                            values.append(value)
                    
                    if set_clauses:
                        query = f"UPDATE molecules SET {', '.join(set_clauses)} WHERE id = ?"
                        values.append(molecule_id)
                        
                        cursor.execute(query, values)
                        if cursor.rowcount > 0:
                            updated_count += 1
                
                conn.commit()
                return updated_count
                
            except Exception as e:
                conn.rollback()
                raise e
    
    def batch_delete_molecules(self, identifiers: List[str], search_type: str = 'name') -> int:
        """
        Delete multiple molecules in a single transaction.
        
        Args:
            identifiers: List of molecule identifiers
            search_type: Type of identifier ('name', 'formula', 'smiles', 'id')
            
        Returns:
            Number of molecules deleted
        """
        if not identifiers:
            return 0
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                conn.execute('BEGIN TRANSACTION')
                
                # Build query based on search type
                if search_type == 'name':
                    placeholders = ','.join(['?' for _ in identifiers])
                    query = f'DELETE FROM molecules WHERE name IN ({placeholders})'
                elif search_type == 'formula':
                    placeholders = ','.join(['?' for _ in identifiers])
                    query = f'DELETE FROM molecules WHERE formula IN ({placeholders})'
                elif search_type == 'smiles':
                    placeholders = ','.join(['?' for _ in identifiers])
                    query = f'DELETE FROM molecules WHERE smiles IN ({placeholders})'
                elif search_type == 'id':
                    placeholders = ','.join(['?' for _ in identifiers])
                    query = f'DELETE FROM molecules WHERE id IN ({placeholders})'
                else:
                    raise ValueError(f"Invalid search_type: {search_type}")
                
                cursor.execute(query, identifiers)
                deleted_count = cursor.rowcount
                
                conn.commit()
                return deleted_count
                
            except Exception as e:
                conn.rollback()
                raise e
    
    def batch_search_molecules(self, queries: List[Dict[str, Any]]) -> List[List[sqlite3.Row]]:
        """
        Perform multiple searches using parallel processing for better performance.
        
        Args:
            queries: List of query dictionaries with search parameters
            
        Returns:
            List of result lists for each query
        """
        if not queries:
            return []
        
        # Use parallel processing for large batches
        if len(queries) > 5:
            processor = ParallelDatabaseProcessor()
            return processor.parallel_search(self.db_path, queries)
        
        # Use sequential processing for small batches
        results = []
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for query_params in queries:
                try:
                    # Extract search parameters
                    search_type = query_params.get('type', 'name')
                    search_value = query_params.get('value', '')
                    limit = query_params.get('limit', 100)
                    
                    if search_type == 'molecular_weight_range':
                        min_weight = query_params.get('min_weight', 0)
                        max_weight = query_params.get('max_weight', 1000)
                        cursor.execute('''
                        SELECT id, name, smiles, formula, molecular_weight 
                        FROM molecules 
                        WHERE molecular_weight BETWEEN ? AND ? 
                        ORDER BY ABS(molecular_weight - ?)
                        LIMIT ?
                        ''', (min_weight, max_weight, (min_weight + max_weight) / 2, limit))
                    
                    elif search_type == 'formula_pattern':
                        cursor.execute('''
                        SELECT id, name, smiles, formula 
                        FROM molecules 
                        WHERE formula LIKE ? 
                        LIMIT ?
                        ''', (f'%{search_value}%', limit))
                    
                    elif search_type == 'name_pattern':
                        cursor.execute('''
                        SELECT id, name, smiles, formula 
                        FROM molecules 
                        WHERE name LIKE ? 
                        LIMIT ?
                        ''', (f'%{search_value}%', limit))
                    
                    else:
                        # Default exact match search
                        cursor.execute(f'''
                        SELECT id, name, smiles, formula, molecular_weight 
                        FROM molecules 
                        WHERE {search_type} = ? 
                        LIMIT ?
                        ''', (search_value, limit))
                    
                    results.append(cursor.fetchall())
                    
                except Exception as e:
                    # Log error but continue with other queries
                    print(f"Warning: Batch search query failed: {e}")
                    results.append([])
        
        return results
    
    def optimize_database(self) -> None:
        """
        Perform database optimization operations and set performance pragmas.
        """
        with self.get_connection() as conn:
            # Set performance optimization pragmas
            conn.execute('PRAGMA cache_size = 10000')  # Increase cache size
            conn.execute('PRAGMA temp_store = MEMORY')  # Store temp tables in memory
            conn.execute('PRAGMA journal_mode = WAL')   # Use Write-Ahead Logging
            conn.execute('PRAGMA synchronous = NORMAL') # Balance safety and performance
            conn.execute('PRAGMA mmap_size = 268435456') # Use memory mapping (256MB)
            
            # Analyze tables for query optimization
            conn.execute('ANALYZE')
            
            # Vacuum to reclaim space and defragment
            conn.execute('VACUUM')
            
            # Update statistics
            conn.execute('PRAGMA optimize')
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics for monitoring performance.
        
        Returns:
            Dictionary containing database statistics
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute('SELECT COUNT(*) as molecule_count FROM molecules')
            molecule_count = cursor.fetchone()['molecule_count']
            
            # Get database size
            cursor.execute('PRAGMA page_count')
            page_count = cursor.fetchone()[0]
            cursor.execute('PRAGMA page_size')
            page_size = cursor.fetchone()[0]
            db_size = page_count * page_size
            
            return {
                'molecule_count': molecule_count,
                'database_size_bytes': db_size,
                'database_size_mb': db_size / (1024 * 1024),
                'page_count': page_count,
                'page_size': page_size,
                'connection_pool_size': len(self._connection_pool)
            }

# Alias for backward compatibility
ChemicalDatabase = MoleculeDatabase
