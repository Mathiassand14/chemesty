"""
Module for storing and retrieving chemical reactions from a database.

This module provides a ReactionDatabase class for storing chemical reactions
in a SQLite database and retrieving them based on various criteria.
"""

import os
import sqlite3
import threading
from contextlib import contextmanager
from typing import List, Dict, Optional, Any, Union, Tuple

from chemesty.reactions.reaction import Reaction, ReactionComponent
from chemesty.molecules.molecule import Molecule


class ReactionDatabase:
    """
    Class for interacting with the reaction database.

    This class provides methods for storing and retrieving chemical reaction data
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

        # Create the reactions table if it doesn't exist
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS reactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            reaction_type TEXT,
            temperature REAL,
            pressure REAL,
            is_balanced INTEGER,
            equation TEXT
        )
        ''')

        # Create the reactants table if it doesn't exist
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS reactants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reaction_id INTEGER,
            formula TEXT,
            coefficient REAL,
            phase TEXT,
            is_catalyst INTEGER,
            FOREIGN KEY (reaction_id) REFERENCES reactions (id) ON DELETE CASCADE
        )
        ''')

        # Create the products table if it doesn't exist
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reaction_id INTEGER,
            formula TEXT,
            coefficient REAL,
            phase TEXT,
            FOREIGN KEY (reaction_id) REFERENCES reactions (id) ON DELETE CASCADE
        )
        ''')

        # Create the conditions table if it doesn't exist
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS conditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reaction_id INTEGER,
            name TEXT,
            value TEXT,
            FOREIGN KEY (reaction_id) REFERENCES reactions (id) ON DELETE CASCADE
        )
        ''')

        # Create indexes for faster lookups
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_reaction_type ON reactions(reaction_type)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_reaction_name ON reactions(name)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_reactant_formula ON reactants(formula)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_product_formula ON products(formula)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_reactant_reaction ON reactants(reaction_id)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_product_reaction ON products(reaction_id)')

    def add_reaction(self, reaction: Reaction) -> int:
        """
        Add a reaction to the database.

        Args:
            reaction: Reaction object to add

        Returns:
            ID of the inserted reaction
        """
        cursor = self.conn.cursor()
        
        # Start a transaction
        self.conn.execute('BEGIN TRANSACTION')
        
        try:
            # Insert the reaction
            cursor.execute('''
            INSERT INTO reactions
            (name, reaction_type, temperature, pressure, is_balanced, equation)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                reaction.name,
                reaction.type,
                reaction.temperature,
                reaction.pressure,
                1 if reaction.is_balanced() else 0,
                str(reaction)
            ))
            
            reaction_id = cursor.lastrowid
            
            # Insert reactants
            for reactant in reaction.reactants:
                cursor.execute('''
                INSERT INTO reactants
                (reaction_id, formula, coefficient, phase, is_catalyst)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    reaction_id,
                    reactant.molecule.molecular_formula,
                    reactant.coefficient,
                    reactant.phase,
                    1 if reactant.is_catalyst else 0
                ))
            
            # Insert products
            for product in reaction.products:
                cursor.execute('''
                INSERT INTO products
                (reaction_id, formula, coefficient, phase)
                VALUES (?, ?, ?, ?)
                ''', (
                    reaction_id,
                    product.molecule.molecular_formula,
                    product.coefficient,
                    product.phase
                ))
            
            # Insert conditions
            for name, value in reaction.conditions.items():
                cursor.execute('''
                INSERT INTO conditions
                (reaction_id, name, value)
                VALUES (?, ?, ?)
                ''', (
                    reaction_id,
                    name,
                    str(value)
                ))
            
            # Commit the transaction
            self.conn.commit()
            
            return reaction_id
            
        except Exception as e:
            # Rollback the transaction in case of error
            self.conn.rollback()
            raise e

    def get_reaction_by_id(self, reaction_id: int) -> Optional[Reaction]:
        """
        Get a reaction by ID.

        Args:
            reaction_id: ID of the reaction

        Returns:
            Reaction object or None if not found
        """
        cursor = self.conn.cursor()
        
        # Get the reaction
        cursor.execute('''
        SELECT * FROM reactions WHERE id = ?
        ''', (reaction_id,))
        
        reaction_row = cursor.fetchone()
        if not reaction_row:
            return None
        
        # Create a new Reaction object
        reaction = Reaction(
            name=reaction_row['name'],
            temperature=reaction_row['temperature'],
            pressure=reaction_row['pressure']
        )
        
        # Get reactants
        cursor.execute('''
        SELECT * FROM reactants WHERE reaction_id = ?
        ''', (reaction_id,))
        
        for reactant_row in cursor.fetchall():
            reaction.add_reactant(
                molecule=reactant_row['formula'],
                coefficient=reactant_row['coefficient'],
                phase=reactant_row['phase'],
                is_catalyst=bool(reactant_row['is_catalyst'])
            )
        
        # Get products
        cursor.execute('''
        SELECT * FROM products WHERE reaction_id = ?
        ''', (reaction_id,))
        
        for product_row in cursor.fetchall():
            reaction.add_product(
                molecule=product_row['formula'],
                coefficient=product_row['coefficient'],
                phase=product_row['phase']
            )
        
        # Get conditions
        cursor.execute('''
        SELECT * FROM conditions WHERE reaction_id = ?
        ''', (reaction_id,))
        
        for condition_row in cursor.fetchall():
            reaction.conditions[condition_row['name']] = condition_row['value']
        
        return reaction

    def search_reactions(self, 
                        reaction_type: Optional[str] = None,
                        reactant_formula: Optional[str] = None,
                        product_formula: Optional[str] = None,
                        name: Optional[str] = None,
                        balanced_only: bool = False,
                        limit: int = 100) -> List[Reaction]:
        """
        Search for reactions based on various criteria.

        Args:
            reaction_type: Type of reaction (combustion, redox, etc.)
            reactant_formula: Formula of a reactant
            product_formula: Formula of a product
            name: Name of the reaction
            balanced_only: Whether to return only balanced reactions
            limit: Maximum number of results to return

        Returns:
            List of matching Reaction objects
        """
        cursor = self.conn.cursor()
        
        # Build the query
        query = "SELECT id FROM reactions WHERE 1=1"
        params = []
        
        if reaction_type:
            query += " AND reaction_type = ?"
            params.append(reaction_type)
        
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        
        if balanced_only:
            query += " AND is_balanced = 1"
        
        if reactant_formula:
            query += " AND id IN (SELECT reaction_id FROM reactants WHERE formula LIKE ?)"
            params.append(f"%{reactant_formula}%")
        
        if product_formula:
            query += " AND id IN (SELECT reaction_id FROM products WHERE formula LIKE ?)"
            params.append(f"%{product_formula}%")
        
        query += " LIMIT ?"
        params.append(limit)
        
        # Execute the query
        cursor.execute(query, params)
        
        # Get the results
        reaction_ids = [row[0] for row in cursor.fetchall()]
        
        # Get the full reaction objects
        reactions = []
        for reaction_id in reaction_ids:
            reaction = self.get_reaction_by_id(reaction_id)
            if reaction:
                reactions.append(reaction)
        
        return reactions

    def get_all_reactions(self, limit: int = 100) -> List[Reaction]:
        """
        Get all reactions in the database.

        Args:
            limit: Maximum number of results to return

        Returns:
            List of Reaction objects
        """
        cursor = self.conn.cursor()
        
        # Get all reaction IDs
        cursor.execute('''
        SELECT id FROM reactions LIMIT ?
        ''', (limit,))
        
        reaction_ids = [row[0] for row in cursor.fetchall()]
        
        # Get the full reaction objects
        reactions = []
        for reaction_id in reaction_ids:
            reaction = self.get_reaction_by_id(reaction_id)
            if reaction:
                reactions.append(reaction)
        
        return reactions

    def update_reaction(self, reaction_id: int, reaction: Reaction) -> bool:
        """
        Update a reaction in the database.

        Args:
            reaction_id: ID of the reaction to update
            reaction: Updated Reaction object

        Returns:
            True if the update was successful, False otherwise
        """
        cursor = self.conn.cursor()
        
        # Start a transaction
        self.conn.execute('BEGIN TRANSACTION')
        
        try:
            # Update the reaction
            cursor.execute('''
            UPDATE reactions
            SET name = ?, reaction_type = ?, temperature = ?, pressure = ?, is_balanced = ?, equation = ?
            WHERE id = ?
            ''', (
                reaction.name,
                reaction.type,
                reaction.temperature,
                reaction.pressure,
                1 if reaction.is_balanced() else 0,
                str(reaction),
                reaction_id
            ))
            
            # Delete existing reactants, products, and conditions
            cursor.execute('DELETE FROM reactants WHERE reaction_id = ?', (reaction_id,))
            cursor.execute('DELETE FROM products WHERE reaction_id = ?', (reaction_id,))
            cursor.execute('DELETE FROM conditions WHERE reaction_id = ?', (reaction_id,))
            
            # Insert new reactants
            for reactant in reaction.reactants:
                cursor.execute('''
                INSERT INTO reactants
                (reaction_id, formula, coefficient, phase, is_catalyst)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    reaction_id,
                    reactant.molecule.molecular_formula,
                    reactant.coefficient,
                    reactant.phase,
                    1 if reactant.is_catalyst else 0
                ))
            
            # Insert new products
            for product in reaction.products:
                cursor.execute('''
                INSERT INTO products
                (reaction_id, formula, coefficient, phase)
                VALUES (?, ?, ?, ?)
                ''', (
                    reaction_id,
                    product.molecule.molecular_formula,
                    product.coefficient,
                    product.phase
                ))
            
            # Insert new conditions
            for name, value in reaction.conditions.items():
                cursor.execute('''
                INSERT INTO conditions
                (reaction_id, name, value)
                VALUES (?, ?, ?)
                ''', (
                    reaction_id,
                    name,
                    str(value)
                ))
            
            # Commit the transaction
            self.conn.commit()
            
            return True
            
        except Exception as e:
            # Rollback the transaction in case of error
            self.conn.rollback()
            print(f"Error updating reaction: {e}")
            return False

    def delete_reaction(self, reaction_id: int) -> bool:
        """
        Delete a reaction from the database.

        Args:
            reaction_id: ID of the reaction to delete

        Returns:
            True if the deletion was successful, False otherwise
        """
        cursor = self.conn.cursor()
        
        try:
            # Delete the reaction (cascade will delete related records)
            cursor.execute('DELETE FROM reactions WHERE id = ?', (reaction_id,))
            self.conn.commit()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error deleting reaction: {e}")
            return False

    def batch_add_reactions(self, reactions: List[Reaction]) -> List[int]:
        """
        Add multiple reactions in a single transaction.

        Args:
            reactions: List of Reaction objects to add

        Returns:
            List of inserted reaction IDs
        """
        cursor = self.conn.cursor()
        
        # Start a transaction
        self.conn.execute('BEGIN TRANSACTION')
        
        try:
            reaction_ids = []
            
            for reaction in reactions:
                # Insert the reaction
                cursor.execute('''
                INSERT INTO reactions
                (name, reaction_type, temperature, pressure, is_balanced, equation)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    reaction.name,
                    reaction.type,
                    reaction.temperature,
                    reaction.pressure,
                    1 if reaction.is_balanced() else 0,
                    str(reaction)
                ))
                
                reaction_id = cursor.lastrowid
                reaction_ids.append(reaction_id)
                
                # Insert reactants
                for reactant in reaction.reactants:
                    cursor.execute('''
                    INSERT INTO reactants
                    (reaction_id, formula, coefficient, phase, is_catalyst)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        reaction_id,
                        reactant.molecule.molecular_formula,
                        reactant.coefficient,
                        reactant.phase,
                        1 if reactant.is_catalyst else 0
                    ))
                
                # Insert products
                for product in reaction.products:
                    cursor.execute('''
                    INSERT INTO products
                    (reaction_id, formula, coefficient, phase)
                    VALUES (?, ?, ?, ?)
                    ''', (
                        reaction_id,
                        product.molecule.molecular_formula,
                        product.coefficient,
                        product.phase
                    ))
                
                # Insert conditions
                for name, value in reaction.conditions.items():
                    cursor.execute('''
                    INSERT INTO conditions
                    (reaction_id, name, value)
                    VALUES (?, ?, ?)
                    ''', (
                        reaction_id,
                        name,
                        str(value)
                    ))
            
            # Commit the transaction
            self.conn.commit()
            
            return reaction_ids
            
        except Exception as e:
            # Rollback the transaction in case of error
            self.conn.rollback()
            raise e

    def get_reaction_types(self) -> List[str]:
        """
        Get a list of all reaction types in the database.

        Returns:
            List of reaction types
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
        SELECT DISTINCT reaction_type FROM reactions
        ''')
        
        return [row[0] for row in cursor.fetchall()]

    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary containing database statistics
        """
        cursor = self.conn.cursor()
        
        # Get reaction count
        cursor.execute('SELECT COUNT(*) FROM reactions')
        reaction_count = cursor.fetchone()[0]
        
        # Get reactant count
        cursor.execute('SELECT COUNT(*) FROM reactants')
        reactant_count = cursor.fetchone()[0]
        
        # Get product count
        cursor.execute('SELECT COUNT(*) FROM products')
        product_count = cursor.fetchone()[0]
        
        # Get reaction type counts
        cursor.execute('''
        SELECT reaction_type, COUNT(*) FROM reactions
        GROUP BY reaction_type
        ''')
        reaction_type_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Get database size
        cursor.execute('PRAGMA page_count')
        page_count = cursor.fetchone()[0]
        cursor.execute('PRAGMA page_size')
        page_size = cursor.fetchone()[0]
        db_size = page_count * page_size
        
        return {
            'reaction_count': reaction_count,
            'reactant_count': reactant_count,
            'product_count': product_count,
            'reaction_type_counts': reaction_type_counts,
            'database_size_bytes': db_size,
            'database_size_mb': db_size / (1024 * 1024)
        }

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            
        # Close any connections in the pool
        with self._pool_lock:
            for conn in self._connection_pool:
                conn.close()
            self._connection_pool = []

    @contextmanager
    def get_connection(self):
        """
        Get a connection from the pool or create a new one.
        
        This is a context manager that can be used with the 'with' statement.
        """
        conn = None
        
        # Try to get a connection from the pool
        with self._pool_lock:
            if self._connection_pool:
                conn = self._connection_pool.pop()
            
        # If no connection was available, create a new one
        if conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
        
        try:
            # Yield the connection to the caller
            yield conn
            
        finally:
            if conn:
                with self._pool_lock:
                    if len(self._connection_pool) < self.pool_size:
                        self._connection_pool.append(conn)
                    else:
                        conn.close()