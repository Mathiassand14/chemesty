"""
Main command-line interface for Chemesty.

Provides a comprehensive CLI for common chemistry operations including
element lookup, molecule analysis, database queries, and ML predictions.
"""

import argparse
import sys
import json
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

try:
    from chemesty.elements.element_factory import ElementFactory
    from chemesty.molecules.molecule import Molecule
    from chemesty.data.database import ChemicalDatabase
    from chemesty.ml.property_predictor import PropertyPredictor
    from chemesty.ml.descriptors import MolecularDescriptors
    from chemesty.data.download import download_dataset
except ImportError as e:
    logger.error(f"Failed to import Chemesty modules: {e}")
    sys.exit(1)


class ChemestyCLI:
    """Main CLI class for Chemesty operations."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.element_factory = ElementFactory()
        self.descriptor_calculator = MolecularDescriptors()
        self.database = None
        self.ml_predictor = None
    
    def setup_database(self, db_path: Optional[str] = None):
        """Set up database connection."""
        try:
            self.database = ChemicalDatabase(db_path)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
    
    def setup_ml_predictor(self, model_dir: Optional[str] = None):
        """Set up ML predictor."""
        try:
            self.ml_predictor = PropertyPredictor(model_dir)
            logger.info("ML predictor initialized")
        except Exception as e:
            logger.error(f"Failed to initialize ML predictor: {e}")


def element_command(args):
    """Handle element lookup commands."""
    cli = ChemestyCLI()
    
    try:
        element = cli.element_factory.get_element(args.symbol)
        
        if args.output_format == 'json':
            element_data = {
                'symbol': element.symbol,
                'name': element.name,
                'atomic_number': element.atomic_number,
                'atomic_mass': element.atomic_mass,
                'group': getattr(element, 'group', None),
                'period': getattr(element, 'period', None),
                'is_metal': element.is_metal(),
                'is_nonmetal': element.is_nonmetal(),
                'is_metalloid': element.is_metalloid()
            }
            print(json.dumps(element_data, indent=2))
        else:
            print(f"Element: {element.name} ({element.symbol})")
            print(f"Atomic Number: {element.atomic_number}")
            print(f"Atomic Mass: {element.atomic_mass:.4f} u")
            if hasattr(element, 'group'):
                print(f"Group: {element.group}")
            if hasattr(element, 'period'):
                print(f"Period: {element.period}")
            print(f"Type: {'Metal' if element.is_metal() else 'Non-metal' if element.is_nonmetal() else 'Metalloid'}")
            
    except Exception as e:
        logger.error(f"Error looking up element {args.symbol}: {e}")
        sys.exit(1)


def molecule_command(args):
    """Handle molecule analysis commands."""
    cli = ChemestyCLI()
    
    try:
        if args.smiles:
            # Create molecule from SMILES
            molecule = Molecule.from_smiles(args.smiles)
        elif args.formula:
            # Create molecule from formula
            molecule = Molecule.from_formula(args.formula)
        elif args.file:
            # Load molecule from file
            molecule = Molecule.from_file(args.file)
        else:
            logger.error("Must specify either --smiles, --formula, or --file")
            sys.exit(1)
        
        # Calculate descriptors
        descriptors = cli.descriptor_calculator.calculate_all_descriptors(molecule)
        
        if args.output_format == 'json':
            print(json.dumps(descriptors, indent=2))
        else:
            print(f"Molecule Analysis:")
            print(f"Molecular Weight: {descriptors.get('molecular_weight', 'N/A'):.4f} g/mol")
            print(f"Number of Atoms: {descriptors.get('num_atoms', 'N/A')}")
            print(f"Number of Heavy Atoms: {descriptors.get('num_heavy_atoms', 'N/A')}")
            print(f"Number of Bonds: {descriptors.get('num_bonds', 'N/A')}")
            print(f"LogP: {descriptors.get('logp', 'N/A'):.2f}")
            print(f"TPSA: {descriptors.get('tpsa', 'N/A'):.2f} Ų")
            print(f"H-bond Donors: {descriptors.get('num_h_donors', 'N/A')}")
            print(f"H-bond Acceptors: {descriptors.get('num_h_acceptors', 'N/A')}")
            
    except Exception as e:
        logger.error(f"Error analyzing molecule: {e}")
        sys.exit(1)


def predict_command(args):
    """Handle ML prediction commands."""
    cli = ChemestyCLI()
    cli.setup_ml_predictor(args.model_dir)
    
    if not cli.ml_predictor:
        logger.error("ML predictor not available")
        sys.exit(1)
    
    try:
        if args.smiles:
            molecule = Molecule.from_smiles(args.smiles)
        elif args.formula:
            molecule = Molecule.from_formula(args.formula)
        elif args.file:
            molecule = Molecule.from_file(args.file)
        else:
            logger.error("Must specify either --smiles, --formula, or --file")
            sys.exit(1)
        
        if args.property:
            # Predict specific property
            try:
                prediction = cli.ml_predictor.predict_property(molecule, args.property)
                if args.output_format == 'json':
                    print(json.dumps({args.property: prediction}, indent=2))
                else:
                    print(f"Predicted {args.property}: {prediction:.4f}")
            except ValueError as e:
                logger.error(f"Property prediction failed: {e}")
                available = cli.ml_predictor.list_available_properties()
                if available:
                    logger.info(f"Available properties: {', '.join(available)}")
                sys.exit(1)
        else:
            # Predict all available properties
            predictions = cli.ml_predictor.predict_multiple_properties(molecule)
            if args.output_format == 'json':
                print(json.dumps(predictions, indent=2))
            else:
                print("Property Predictions:")
                for prop, value in predictions.items():
                    if value is not None:
                        print(f"  {prop}: {value:.4f}")
                    else:
                        print(f"  {prop}: N/A")
                        
    except Exception as e:
        logger.error(f"Error making predictions: {e}")
        sys.exit(1)


def database_command(args):
    """Handle database operations."""
    cli = ChemestyCLI()
    cli.setup_database(args.database)
    
    if not cli.database:
        logger.error("Database not available")
        sys.exit(1)
    
    try:
        if args.action == 'search':
            if not args.query:
                logger.error("Search query required")
                sys.exit(1)
            
            results = cli.database.search_molecules(args.query, limit=args.limit)
            
            if args.output_format == 'json':
                print(json.dumps(results, indent=2))
            else:
                print(f"Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result.get('name', 'Unknown')} - {result.get('formula', 'N/A')}")
        
        elif args.action == 'info':
            info = cli.database.get_database_info()
            if args.output_format == 'json':
                print(json.dumps(info, indent=2))
            else:
                print("Database Information:")
                for key, value in info.items():
                    print(f"  {key}: {value}")
                    
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        sys.exit(1)


def download_command(args):
    """Handle dataset download commands."""
    try:
        download_dataset(
            source=args.source,
            output_dir=args.output_dir,
            limit=args.limit,
            force=args.force
        )
        logger.info(f"Dataset download completed to {args.output_dir}")
    except Exception as e:
        logger.error(f"Download failed: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Chemesty - Chemistry Library Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  chemesty element H                    # Look up hydrogen
  chemesty molecule --smiles "CCO"      # Analyze ethanol
  chemesty predict --smiles "CCO" --property logp  # Predict LogP
  chemesty database search --query "caffeine"      # Search database
  chemesty download --source chembl --limit 1000   # Download data
        """
    )
    
    parser.add_argument('--version', action='version', version='Chemesty 1.0.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Element command
    element_parser = subparsers.add_parser('element', help='Look up element information')
    element_parser.add_argument('symbol', help='Element symbol (e.g., H, He, Li)')
    element_parser.set_defaults(func=element_command)
    
    # Molecule command
    molecule_parser = subparsers.add_parser('molecule', help='Analyze molecules')
    molecule_group = molecule_parser.add_mutually_exclusive_group(required=True)
    molecule_group.add_argument('--smiles', help='SMILES string')
    molecule_group.add_argument('--formula', help='Molecular formula')
    molecule_group.add_argument('--file', help='Molecule file path')
    molecule_parser.set_defaults(func=molecule_command)
    
    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Predict molecular properties')
    predict_group = predict_parser.add_mutually_exclusive_group(required=True)
    predict_group.add_argument('--smiles', help='SMILES string')
    predict_group.add_argument('--formula', help='Molecular formula')
    predict_group.add_argument('--file', help='Molecule file path')
    predict_parser.add_argument('--property', help='Specific property to predict')
    predict_parser.add_argument('--model-dir', help='Directory containing ML models')
    predict_parser.set_defaults(func=predict_command)
    
    # Database command
    db_parser = subparsers.add_parser('database', help='Database operations')
    db_parser.add_argument('action', choices=['search', 'info'], help='Database action')
    db_parser.add_argument('--query', help='Search query')
    db_parser.add_argument('--limit', type=int, default=10, help='Result limit')
    db_parser.add_argument('--database', help='Database file path')
    db_parser.set_defaults(func=database_command)
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download chemical datasets')
    download_parser.add_argument('--source', choices=['chembl', 'pubchem'], 
                                default='chembl', help='Data source')
    download_parser.add_argument('--output-dir', default='./data', 
                                help='Output directory')
    download_parser.add_argument('--limit', type=int, help='Limit number of compounds')
    download_parser.add_argument('--force', action='store_true', 
                                help='Force re-download')
    download_parser.set_defaults(func=download_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Execute command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()