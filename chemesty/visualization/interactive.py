"""
Interactive molecular visualization with web-based controls.

This module provides interactive visualization capabilities using matplotlib widgets
and optional web-based interfaces for enhanced user interaction.
"""

from typing import Dict, List, Tuple, Optional, Union, Any, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import matplotlib.patches as patches
from chemesty.molecules.molecule import Molecule
from chemesty.molecules.file_formats import MolecularStructure, Atom, Bond
from chemesty.visualization.molecular_visualizer import MolecularVisualizer
from chemesty.visualization.structure_2d import Structure2DRenderer
from chemesty.visualization.structure_3d import Structure3DRenderer


class InteractiveMoleculeViewer:
    """
    Interactive molecular visualization with controls.
    
    This class provides an interactive interface for exploring molecular structures
    with real-time controls for visualization parameters.
    """
    
    def __init__(self, figsize: Tuple[float, float] = (12, 8)):
        """
        Initialize the interactive viewer.
        
        Args:
            figsize: Figure size (width, height)
        """
        self.figsize = figsize
        self.current_structure = None
        self.current_style = 'ball_and_stick'
        self.show_labels = True
        self.show_bonds = True
        self.show_hydrogens = True
        self.alpha = 0.8
        self.rotation_angle = 45
        self.elevation_angle = 20
        
        # Renderers
        self.visualizer = MolecularVisualizer()
        self.renderer_2d = Structure2DRenderer()
        self.renderer_3d = Structure3DRenderer()
        
        # Widget references
        self.widgets = {}
        self.fig = None
        self.ax_main = None
        self.ax_controls = None
    
    def create_interactive_viewer(self, structure: MolecularStructure) -> Figure:
        """
        Create an interactive viewer for a molecular structure.
        
        Args:
            structure: MolecularStructure to visualize
            
        Returns:
            Matplotlib Figure with interactive controls
        """
        self.current_structure = structure
        
        # Create figure with subplots
        self.fig = plt.figure(figsize=self.figsize)
        
        # Main visualization area (70% of width)
        self.ax_main = plt.subplot2grid((4, 10), (0, 0), colspan=7, rowspan=4, projection='3d')
        
        # Control panel area (30% of width)
        self._create_control_panel()
        
        # Initial render
        self._update_visualization()
        
        # Connect events
        self._connect_events()
        
        plt.tight_layout()
        return self.fig
    
    def _create_control_panel(self) -> None:
        """Create the control panel with widgets."""
        # Style selection
        ax_style = plt.subplot2grid((4, 10), (0, 7), colspan=3, rowspan=1)
        ax_style.set_title('Rendering Style')
        self.widgets['style'] = RadioButtons(
            ax_style, 
            ('ball_and_stick', 'space_filling', 'wireframe', 'stick'),
            active=0
        )
        self.widgets['style'].on_clicked(self._on_style_change)
        
        # Display options
        ax_options = plt.subplot2grid((4, 10), (1, 7), colspan=3, rowspan=1)
        ax_options.set_title('Display Options')
        self.widgets['options'] = CheckButtons(
            ax_options,
            ('Show Labels', 'Show Bonds', 'Show Hydrogens'),
            (self.show_labels, self.show_bonds, self.show_hydrogens)
        )
        self.widgets['options'].on_clicked(self._on_option_change)
        
        # Transparency slider
        ax_alpha = plt.subplot2grid((4, 10), (2, 7), colspan=3, rowspan=1)
        ax_alpha.set_title('Transparency')
        self.widgets['alpha'] = Slider(
            ax_alpha, 'Alpha', 0.1, 1.0, valinit=self.alpha, valfmt='%.2f'
        )
        self.widgets['alpha'].on_changed(self._on_alpha_change)
        
        # Rotation controls
        ax_rotation = plt.subplot2grid((4, 10), (3, 7), colspan=1.5, rowspan=1)
        ax_elevation = plt.subplot2grid((4, 10), (3, 8.5), colspan=1.5, rowspan=1)
        
        self.widgets['rotation'] = Slider(
            ax_rotation, 'Azim', 0, 360, valinit=self.rotation_angle, valfmt='%.0f°'
        )
        self.widgets['elevation'] = Slider(
            ax_elevation, 'Elev', -90, 90, valinit=self.elevation_angle, valfmt='%.0f°'
        )
        
        self.widgets['rotation'].on_changed(self._on_rotation_change)
        self.widgets['elevation'].on_changed(self._on_elevation_change)
    
    def _connect_events(self) -> None:
        """Connect additional events for interactivity."""
        # Mouse events for rotation (if not using sliders)
        self.fig.canvas.mpl_connect('button_press_event', self._on_mouse_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_mouse_motion)
        self.fig.canvas.mpl_connect('button_release_event', self._on_mouse_release)
        
        # Keyboard events
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
        
        self.mouse_pressed = False
        self.last_mouse_pos = None
    
    def _update_visualization(self) -> None:
        """Update the main visualization based on current settings."""
        if not self.current_structure:
            return
        
        # Clear the main axis
        self.ax_main.clear()
        
        # Set up the 3D renderer with current style
        self.renderer_3d.style = self.current_style
        
        # Get coordinates
        coords = self.renderer_3d._get_coordinates(self.current_structure)
        
        # Render based on style
        if self.current_style == 'ball_and_stick':
            self.renderer_3d._render_ball_and_stick(
                self.ax_main, self.current_structure, coords, 
                self.show_labels, self.show_bonds, self.alpha
            )
        elif self.current_style == 'space_filling':
            self.renderer_3d._render_space_filling(
                self.ax_main, self.current_structure, coords, 
                self.show_labels, self.alpha
            )
        elif self.current_style == 'wireframe':
            self.renderer_3d._render_wireframe(
                self.ax_main, self.current_structure, coords, self.show_labels
            )
        elif self.current_style == 'stick':
            self.renderer_3d._render_stick(
                self.ax_main, self.current_structure, coords, self.show_labels
            )
        
        # Set up the plot
        self.renderer_3d._setup_3d_plot(self.ax_main, coords, self.current_structure.title)
        
        # Apply current viewing angles
        self.ax_main.view_init(elev=self.elevation_angle, azim=self.rotation_angle)
        
        # Refresh the display
        self.fig.canvas.draw()
    
    def _on_style_change(self, label: str) -> None:
        """Handle style change event."""
        self.current_style = label
        self._update_visualization()
    
    def _on_option_change(self, label: str) -> None:
        """Handle display option change event."""
        if label == 'Show Labels':
            self.show_labels = not self.show_labels
        elif label == 'Show Bonds':
            self.show_bonds = not self.show_bonds
        elif label == 'Show Hydrogens':
            self.show_hydrogens = not self.show_hydrogens
        
        self._update_visualization()
    
    def _on_alpha_change(self, val: float) -> None:
        """Handle transparency change event."""
        self.alpha = val
        self._update_visualization()
    
    def _on_rotation_change(self, val: float) -> None:
        """Handle rotation change event."""
        self.rotation_angle = val
        self.ax_main.view_init(elev=self.elevation_angle, azim=self.rotation_angle)
        self.fig.canvas.draw()
    
    def _on_elevation_change(self, val: float) -> None:
        """Handle elevation change event."""
        self.elevation_angle = val
        self.ax_main.view_init(elev=self.elevation_angle, azim=self.rotation_angle)
        self.fig.canvas.draw()
    
    def _on_mouse_press(self, event) -> None:
        """Handle mouse press event."""
        if event.inaxes == self.ax_main:
            self.mouse_pressed = True
            self.last_mouse_pos = (event.xdata, event.ydata)
    
    def _on_mouse_motion(self, event) -> None:
        """Handle mouse motion event for rotation."""
        if self.mouse_pressed and event.inaxes == self.ax_main and self.last_mouse_pos:
            if event.xdata and event.ydata:
                dx = event.xdata - self.last_mouse_pos[0]
                dy = event.ydata - self.last_mouse_pos[1]
                
                # Update rotation based on mouse movement
                self.rotation_angle += dx * 2
                self.elevation_angle += dy * 2
                
                # Clamp elevation
                self.elevation_angle = max(-90, min(90, self.elevation_angle))
                
                # Update view
                self.ax_main.view_init(elev=self.elevation_angle, azim=self.rotation_angle)
                
                # Update sliders
                self.widgets['rotation'].set_val(self.rotation_angle % 360)
                self.widgets['elevation'].set_val(self.elevation_angle)
                
                self.fig.canvas.draw()
                self.last_mouse_pos = (event.xdata, event.ydata)
    
    def _on_mouse_release(self, event) -> None:
        """Handle mouse release event."""
        self.mouse_pressed = False
        self.last_mouse_pos = None
    
    def _on_key_press(self, event) -> None:
        """Handle keyboard events."""
        if event.key == 'r':
            # Reset view
            self.rotation_angle = 45
            self.elevation_angle = 20
            self.widgets['rotation'].set_val(self.rotation_angle)
            self.widgets['elevation'].set_val(self.elevation_angle)
            self._update_visualization()
        elif event.key == 's':
            # Save current view
            self.save_current_view()
        elif event.key == '1':
            self.widgets['style'].set_active(0)  # ball_and_stick
        elif event.key == '2':
            self.widgets['style'].set_active(1)  # space_filling
        elif event.key == '3':
            self.widgets['style'].set_active(2)  # wireframe
        elif event.key == '4':
            self.widgets['style'].set_active(3)  # stick
    
    def save_current_view(self, filename: Optional[str] = None) -> None:
        """Save the current view to a file."""
        if not filename:
            filename = f"molecule_view_{self.current_style}.png"
        
        self.fig.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"View saved as {filename}")
    
    def create_comparison_viewer(self, structures: List[MolecularStructure],
                                titles: Optional[List[str]] = None) -> Figure:
        """
        Create an interactive viewer for comparing multiple structures.
        
        Args:
            structures: List of MolecularStructure objects to compare
            titles: Optional titles for each structure
            
        Returns:
            Matplotlib Figure with comparison interface
        """
        n_structures = len(structures)
        if n_structures == 0:
            raise ValueError("At least one structure is required")
        
        # Create figure with subplots for each structure
        fig, axes = plt.subplots(1, n_structures, figsize=(4*n_structures, 6),
                                subplot_kw={'projection': '3d'})
        
        if n_structures == 1:
            axes = [axes]
        
        # Render each structure
        for i, (structure, ax) in enumerate(zip(structures, axes)):
            renderer = Structure3DRenderer(style='ball_and_stick')
            coords = renderer._get_coordinates(structure)
            
            renderer._render_ball_and_stick(ax, structure, coords, True, True, 0.8)
            renderer._setup_3d_plot(ax, coords, structure.title)
            
            title = titles[i] if titles and i < len(titles) else f'Structure {i+1}'
            ax.set_title(title)
        
        plt.tight_layout()
        return fig
    
    def create_animation_controls(self, structure: MolecularStructure) -> Figure:
        """
        Create an interface with animation controls.
        
        Args:
            structure: MolecularStructure to animate
            
        Returns:
            Matplotlib Figure with animation controls
        """
        self.current_structure = structure
        
        # Create figure
        fig = plt.figure(figsize=(12, 8))
        
        # Main plot area
        ax_main = plt.subplot2grid((5, 10), (0, 0), colspan=8, rowspan=4, projection='3d')
        
        # Animation controls
        ax_play = plt.subplot2grid((5, 10), (4, 0), colspan=1, rowspan=1)
        ax_pause = plt.subplot2grid((5, 10), (4, 1), colspan=1, rowspan=1)
        ax_reset = plt.subplot2grid((5, 10), (4, 2), colspan=1, rowspan=1)
        ax_speed = plt.subplot2grid((5, 10), (4, 3), colspan=3, rowspan=1)
        
        # Create buttons
        btn_play = Button(ax_play, 'Play')
        btn_pause = Button(ax_pause, 'Pause')
        btn_reset = Button(ax_reset, 'Reset')
        slider_speed = Slider(ax_speed, 'Speed', 0.1, 5.0, valinit=1.0)
        
        # Animation state
        self.animation_running = False
        self.animation_frame = 0
        self.animation_speed = 1.0
        
        def start_animation(event):
            self.animation_running = True
            animate()
        
        def pause_animation(event):
            self.animation_running = False
        
        def reset_animation(event):
            self.animation_running = False
            self.animation_frame = 0
            update_frame()
        
        def set_speed(val):
            self.animation_speed = val
        
        def animate():
            if self.animation_running:
                self.animation_frame += self.animation_speed
                update_frame()
                fig.canvas.draw()
                fig.canvas.start_event_loop(0.05)  # 20 FPS
                animate()
        
        def update_frame():
            ax_main.clear()
            
            # Render structure with current rotation
            renderer = Structure3DRenderer(style='ball_and_stick')
            coords = renderer._get_coordinates(structure)
            
            renderer._render_ball_and_stick(ax_main, structure, coords, True, True, 0.8)
            renderer._setup_3d_plot(ax_main, coords, structure.title)
            
            # Set rotation based on frame
            angle = (self.animation_frame * 2) % 360
            ax_main.view_init(elev=20, azim=angle)
        
        # Connect events
        btn_play.on_clicked(start_animation)
        btn_pause.on_clicked(pause_animation)
        btn_reset.on_clicked(reset_animation)
        slider_speed.on_changed(set_speed)
        
        # Initial render
        update_frame()
        
        plt.tight_layout()
        return fig
    
    def export_interactive_html(self, structure: MolecularStructure, 
                               filename: str = "molecule_viewer.html") -> None:
        """
        Export an interactive HTML viewer using Plotly for 3D molecular visualization.
        
        Args:
            structure: MolecularStructure to export
            filename: Output HTML filename
        """
        try:
            import plotly.graph_objects as go
            import plotly.offline as pyo
            from plotly.subplots import make_subplots
        except ImportError:
            # Fallback to basic HTML if Plotly is not available
            self._export_basic_html(structure, filename)
            return
        
        # Get 3D coordinates
        renderer = Structure3DRenderer()
        coords = renderer._get_coordinates(structure)
        
        if not coords:
            coords = renderer._generate_3d_layout(structure)
        
        # Prepare data for Plotly
        x_coords = [coord[0] for coord in coords]
        y_coords = [coord[1] for coord in coords]
        z_coords = [coord[2] for coord in coords]
        
        # Get atom colors and sizes
        atom_colors = []
        atom_sizes = []
        atom_labels = []
        
        for atom in structure.atoms:
            color = renderer.atom_colors.get(atom.element, '#808080')
            size = renderer.atom_sizes.get(atom.element, 1.0) * 20  # Scale for Plotly
            atom_colors.append(color)
            atom_sizes.append(size)
            atom_labels.append(f"{atom.element}{atom.id}")
        
        # Create 3D scatter plot for atoms
        atoms_trace = go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='markers+text',
            marker=dict(
                size=atom_sizes,
                color=atom_colors,
                opacity=0.8,
                line=dict(width=2, color='black')
            ),
            text=atom_labels,
            textposition="middle center",
            name="Atoms",
            hovertemplate="<b>%{text}</b><br>" +
                         "X: %{x:.2f}<br>" +
                         "Y: %{y:.2f}<br>" +
                         "Z: %{z:.2f}<br>" +
                         "<extra></extra>"
        )
        
        # Create bond traces
        bond_traces = []
        for bond in structure.bonds:
            atom1_idx = next(i for i, atom in enumerate(structure.atoms) if atom.id == bond.atom1_id)
            atom2_idx = next(i for i, atom in enumerate(structure.atoms) if atom.id == bond.atom2_id)
            
            bond_trace = go.Scatter3d(
                x=[x_coords[atom1_idx], x_coords[atom2_idx], None],
                y=[y_coords[atom1_idx], y_coords[atom2_idx], None],
                z=[z_coords[atom1_idx], z_coords[atom2_idx], None],
                mode='lines',
                line=dict(
                    color='gray',
                    width=6 if bond.order == 1 else 8 if bond.order == 2 else 10
                ),
                name=f"Bond {bond.atom1_id}-{bond.atom2_id}",
                showlegend=False,
                hoverinfo='skip'
            )
            bond_traces.append(bond_trace)
        
        # Create the figure
        fig = go.Figure(data=[atoms_trace] + bond_traces)
        
        # Update layout for better 3D visualization
        fig.update_layout(
            title=dict(
                text=f"Interactive 3D Molecular Viewer: {structure.title or 'Unknown Molecule'}",
                x=0.5,
                font=dict(size=20)
            ),
            scene=dict(
                xaxis_title="X (Å)",
                yaxis_title="Y (Å)",
                zaxis_title="Z (Å)",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                aspectmode='cube'
            ),
            width=1000,
            height=700,
            margin=dict(l=0, r=0, b=0, t=50),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Add annotations with molecule information
        annotations = [
            dict(
                text=f"Atoms: {len(structure.atoms)} | Bonds: {len(structure.bonds)}",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                xanchor="left", yanchor="top",
                font=dict(size=12, color="black"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="black",
                borderwidth=1
            )
        ]
        
        fig.update_layout(annotations=annotations)
        
        # Export to HTML with full interactivity
        config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToAdd': ['resetCameraDefault3d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'molecule_{structure.title or "unknown"}',
                'height': 700,
                'width': 1000,
                'scale': 2
            }
        }
        
        pyo.plot(fig, filename=filename, auto_open=False, config=config)
        
        print(f"Interactive 3D HTML viewer saved as {filename}")
        print("Features: Rotate, zoom, pan, hover for details, save as image")
    
    def _export_basic_html(self, structure: MolecularStructure, filename: str) -> None:
        """Fallback method for basic HTML export when Plotly is not available."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Molecular Viewer - {structure.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .viewer {{ text-align: center; }}
                .info {{ margin: 20px 0; padding: 15px; background: #f0f0f0; border-radius: 5px; }}
                .warning {{ color: #d63384; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="viewer">
                <h1>Molecular Viewer: {structure.title or 'Unknown'}</h1>
                <div class="info">
                    <p class="warning">Interactive 3D viewer requires Plotly library</p>
                    <p>Install with: pip install plotly</p>
                </div>
                <div class="info">
                    <p><strong>Molecule Information:</strong></p>
                    <p>Number of atoms: {len(structure.atoms)}</p>
                    <p>Number of bonds: {len(structure.bonds)}</p>
                    <p>Atoms: {', '.join(set(atom.element for atom in structure.atoms))}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"Basic HTML viewer saved as {filename}")
        print("Note: Install Plotly for full 3D interactive capabilities.")


def create_quick_viewer(structure: MolecularStructure, 
                       interactive: bool = True) -> Figure:
    """
    Quick function to create a molecular viewer.
    
    Args:
        structure: MolecularStructure to visualize
        interactive: Whether to create interactive controls
        
    Returns:
        Matplotlib Figure
    """
    if interactive:
        viewer = InteractiveMoleculeViewer()
        return viewer.create_interactive_viewer(structure)
    else:
        # Simple static view
        renderer = Structure3DRenderer()
        return renderer.render(structure)


def compare_molecules(structures: List[MolecularStructure],
                     titles: Optional[List[str]] = None,
                     interactive: bool = False) -> Figure:
    """
    Quick function to compare multiple molecular structures.
    
    Args:
        structures: List of MolecularStructure objects
        titles: Optional titles for each structure
        interactive: Whether to create interactive controls
        
    Returns:
        Matplotlib Figure with comparison
    """
    if interactive:
        viewer = InteractiveMoleculeViewer()
        return viewer.create_comparison_viewer(structures, titles)
    else:
        # Simple static comparison
        visualizer = MolecularVisualizer()
        return visualizer.create_comparison_plot(structures, titles)