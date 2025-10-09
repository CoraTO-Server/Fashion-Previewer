import tkinter as tk
import colorsys
from tkinter import filedialog, messagebox, Scrollbar, Canvas, ttk
import tkinter.colorchooser as colorchooser
from PIL import Image, ImageDraw, ImageTk
import os
import re
import sys
import time
import json

PALETTE_SIZE = 256

# Fix working directory to the script's location
def fix_working_directory():
    """Change working directory to the script's location to ensure relative paths work"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)

# Character mapping based on the provided list
from icon_handler import IconHandler, CHARACTER_MAPPING

class CustomPreviewDialog:
    def __init__(self, parent, max_frames, start_frame=0, end_frame=None, num_frames=3, use_bmp=False, show_labels=True, initial_frame=None):
        self.parent = parent
        self.result = None
        self.max_frames = max_frames
        self.use_bmp = use_bmp
        self.show_labels = show_labels
        self.initial_frame = initial_frame if initial_frame is not None else 0
        
        # Get parent's export settings if available
        if isinstance(parent, PaletteTool):
            self.use_bmp = parent.use_bmp_export
            self.use_portrait = parent.use_portrait_export
            self.show_labels = parent.show_frame_labels
            self.cute_bg_option = parent.cute_bg_option  # Initialize cute background option from parent
        else:
            self.use_portrait = False
            self.cute_bg_option = "no_cute_bg"  # Default value for non-PaletteTool parents
        
        # Determine the widget parent for the dialog
        widget_parent = parent.master if isinstance(parent, PaletteTool) else parent
        
        # Create dialog window
        self.dialog = tk.Toplevel(widget_parent)
        self.dialog.title("Custom Preview Settings")
        self.dialog.transient(widget_parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Build the dialog content first, then center
        # (centering will be done after content is created)
        
        # Container frame for content and buttons
        container = tk.Frame(self.dialog)
        container.pack(fill="both", expand=True)
        
        # Main frame for content
        main_frame = tk.Frame(container)
        main_frame.pack(fill="both", padx=20, pady=(10,0))
        
        # Title
        title_label = tk.Label(main_frame, text="Custom Frame Settings", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 2))  # Reduced padding
        
        # Total frames info
        total_frames_label = tk.Label(main_frame, text=f"Total Available Frames: {max_frames}", font=("Arial", 10))
        total_frames_label.pack(pady=(0, 5))
        
        # Frame count input
        count_frame = tk.Frame(main_frame)
        count_frame.pack(fill="x", pady=(0,2))  # Reduced padding
        
        tk.Label(count_frame, text="Number of Frames:").pack(side="left")
        
        self.frame_var = tk.StringVar(value=str(num_frames))
        self.frame_entry = tk.Entry(count_frame, textvariable=self.frame_var, width=10)
        self.frame_entry.pack(side="left", padx=(5, 0))
        
        # Frame range inputs
        range_frame = tk.Frame(main_frame)
        range_frame.pack(fill="x", pady=0)
        
        # Start frame
        start_frame_container = tk.Frame(range_frame)
        start_frame_container.pack(fill="x", pady=1)  # Reduced padding
        tk.Label(start_frame_container, text="Start Frame:").pack(side="left")
        # Always use initial_frame (current frame) as the default start frame, convert to 1-based
        initial_start = self.initial_frame
        self.start_var = tk.StringVar(value=str(initial_start + 1))  # Convert to 1-based
        self.start_entry = tk.Entry(start_frame_container, textvariable=self.start_var, width=10)
        self.start_entry.pack(side="left", padx=(5, 0))
        
        # End frame
        end_frame_container = tk.Frame(range_frame)
        end_frame_container.pack(fill="x", pady=1)  # Reduced padding
        tk.Label(end_frame_container, text="End Frame:").pack(side="left")
        # Convert end frame to 1-based
        end_value = end_frame if end_frame is not None else max_frames - 1
        self.end_var = tk.StringVar(value=str(end_value + 1))  # Convert to 1-based
        self.end_entry = tk.Entry(end_frame_container, textvariable=self.end_var, width=10)
        self.end_entry.pack(side="left", padx=(5, 0))
        
        # Create horizontal container for export format boxes
        export_container = tk.Frame(main_frame)
        export_container.pack(fill="x", pady=(2,2), padx=5)
        
        # Left box - Export Format
        format_frame = tk.LabelFrame(export_container, text="Export Format")
        format_frame.pack(side="left", fill="both", expand=True, padx=(0,3))
        
        # Right box - Portrait BG
        bg_frame = tk.LabelFrame(export_container, text="Portrait BG")
        bg_frame.pack(side="right", fill="both", expand=True, padx=(3,0))
        
        # Palette format frame (separate)
        palette_frame = tk.LabelFrame(main_frame, text="Palette Format")
        palette_frame.pack(fill="x", pady=(0,2), padx=5)  # Reduced padding
        
        self.palette_format_var = tk.StringVar(value="png")
        tk.Radiobutton(palette_frame, text="PAL", variable=self.palette_format_var,
                      value="pal").pack(side="left", padx=10, pady=2)
        tk.Radiobutton(palette_frame, text="PNG Grid", variable=self.palette_format_var,
                      value="png").pack(side="left", padx=10, pady=2)
        
        # Add checkbox to control Export Palette button visibility
        # Get initial value from parent if available
        initial_show_button = False
        if isinstance(parent, PaletteTool):
            initial_show_button = parent.show_export_palette_button
        
        self.show_export_button_var = tk.BooleanVar(value=initial_show_button)
        self.show_export_checkbox = tk.Checkbutton(palette_frame, text="Show Button", 
                                                    variable=self.show_export_button_var,
                                                    command=self.toggle_export_button)
        self.show_export_checkbox.pack(side="left", padx=10, pady=2)
        
        # Initialize variables
        self.format_var = tk.BooleanVar(value=self.use_bmp)
        self.portrait_var = tk.BooleanVar(value=self.use_portrait)
        self.cute_bg_var = tk.StringVar(value=self.cute_bg_option)
        
        # Add trace to update parent's export button when format changes
        def on_format_change(*args):
            is_bmp = self.format_var.get()
            if isinstance(parent, PaletteTool):
                parent.use_bmp_export = is_bmp
                parent.update_export_button_text()
                parent.master.update()  # Force update of the main window
            
            # Portrait mode is always enabled
            self.portrait_checkbox.configure(state="normal")
            
            # Update BG Style options based on Portrait mode
            self.update_bg_style_state()
        self.format_var.trace_add("write", on_format_change)
        
        # Left box content - Format options with reduced padding
        tk.Radiobutton(format_frame, text="Transparent PNG", variable=self.format_var, 
                      value=False).pack(anchor="w", padx=5, pady=1)
        tk.Radiobutton(format_frame, text="Background BMP", variable=self.format_var, 
                      value=True).pack(anchor="w", padx=5, pady=1)
        
        # Portrait checkbox with extra padding after BMP option
        self.portrait_checkbox = tk.Checkbutton(format_frame, text="Portrait export (105x105)", 
                                              variable=self.portrait_var,
                                              command=self.update_bg_style_state)
        self.portrait_checkbox.pack(anchor="w", padx=5, pady=(5,1))
        
        # Right box content - Portrait BG options with reduced padding
        self.cute_bg_frame = tk.Frame(bg_frame)
        self.cute_bg_frame.pack(anchor="w", padx=5, pady=1)
        
        # Create radio buttons with initial state based on portrait mode
        initial_state = "normal" if self.portrait_var.get() else "disabled"
        tk.Radiobutton(self.cute_bg_frame, text="No cute BG", variable=self.cute_bg_var,
                      value="no_cute_bg", state=initial_state).pack(side="top", anchor="w", pady=1)
        tk.Radiobutton(self.cute_bg_frame, text="Cute BG", variable=self.cute_bg_var,
                      value="cute_bg", state=initial_state).pack(side="top", anchor="w", pady=1)
        tk.Radiobutton(self.cute_bg_frame, text="Both", variable=self.cute_bg_var,
                      value="both", state=initial_state).pack(side="top", anchor="w", pady=1)
        
        # Update parent's settings when any option changes
        def update_parent_settings(*args):
            if isinstance(self.parent, PaletteTool):
                old_mode = getattr(self.parent, 'live_pal_ui_mode', 'Advanced')
                self.parent.use_bmp_export = self.format_var.get()
                self.parent.use_portrait_export = self.portrait_var.get()
                self.parent.cute_bg_option = self.cute_bg_var.get()
                self.parent.show_frame_labels = self.labels_var.get()
                self.parent.palette_format = self.palette_format_var.get()
                self.parent.use_frame_choice = self.user_choice_var.get()
                new_mode = self.live_pal_ui_var.get()
                self.parent.live_pal_ui_mode = new_mode
                # Update excess colors prompt setting (invert because setting is "dont_show")
                self.parent.dont_show_excess_colors_prompt = not self.show_excess_colors_prompt_var.get()
                
                # If the live editor is open and the mode changed, rebuild the grid
                if (old_mode != new_mode and 
                    hasattr(self.parent, '_live_editor_window') and 
                    self.parent._live_editor_window and 
                    self.parent._live_editor_window.winfo_exists()):
                    self.parent._rebuild_live_palette_grid()
                    
                if self.user_choice_var.get() and hasattr(self, 'frame_choice_var'):
                    try:
                        self.parent.chosen_frame = int(self.frame_choice_var.get())
                    except (ValueError, AttributeError):
                        pass
                
        # Update checkbox states when format changes
        def update_checkbox_states(*args):
            state = "normal" if self.format_var.get() else "disabled"
            self.portrait_checkbox.config(state=state)
            if not self.format_var.get():
                self.portrait_var.set(False)
            update_parent_settings()
        
        # Frame label toggle
        label_frame = tk.Frame(main_frame)
        label_frame.pack(fill="x", pady=1)  # Minimal padding
        
        self.labels_var = tk.BooleanVar(value=self.show_labels)
        tk.Checkbutton(label_frame, text="Show Frame Numbers", variable=self.labels_var).pack(side="left")
        
        # User Choice Frame Export option
        choice_frame = tk.Frame(main_frame)
        choice_frame.pack(fill="x", pady=(1,2))  # Minimal padding
        
        # Initialize with parent's settings if available
        initial_choice = False
        
        if isinstance(self.parent, PaletteTool):
            initial_choice = self.parent.use_frame_choice
            # If frame choice was previously used, use that frame, otherwise use the initial frame
            if self.parent.use_frame_choice:
                initial_frame = self.parent.chosen_frame
            else:
                initial_frame = self.initial_frame
                # Frame choice should be off by default
                initial_choice = False
        
        self.user_choice_var = tk.BooleanVar(value=initial_choice)
        choice_checkbox = tk.Checkbutton(choice_frame, text="User Choice Frame Export", 
                                       variable=self.user_choice_var,
                                       command=self.toggle_frame_choice)
        choice_checkbox.pack(side="left")
        
        # Frame number entry
        self.frame_choice_container = tk.Frame(choice_frame)
        self.frame_choice_container.pack(side="left", padx=(10,0))
        
        tk.Label(self.frame_choice_container, text="Frame:").pack(side="left")
        self.frame_choice_var = tk.StringVar(value=str(initial_frame))  # Already 1-based
        self.frame_choice_entry = tk.Entry(self.frame_choice_container, 
                                        textvariable=self.frame_choice_var,
                                        width=5)
        self.frame_choice_entry.pack(side="left", padx=(5,5))
        
        # Live Pal Editor UI option
        live_pal_frame = tk.LabelFrame(main_frame, text="Live Pal Editor UI")
        live_pal_frame.pack(fill="x", pady=(2,2), padx=5)
        
        # Get parent's live pal editor UI mode if available
        if isinstance(parent, PaletteTool):
            initial_mode = getattr(parent, 'live_pal_ui_mode', 'Advanced')
        else:
            initial_mode = 'Advanced'
        
        self.live_pal_ui_var = tk.StringVar(value=initial_mode)
        self.live_pal_ui_var.trace_add("write", update_parent_settings)
        tk.Radiobutton(live_pal_frame, text="Simple", variable=self.live_pal_ui_var,
                      value="Simple").pack(side="left", padx=10, pady=2)
        tk.Radiobutton(live_pal_frame, text="Advanced", variable=self.live_pal_ui_var,
                      value="Advanced").pack(side="left", padx=10, pady=2)
        
        # Add validation to prevent unexpected changes
        def validate_frame_choice(*args):
            try:
                value = int(self.frame_choice_var.get())
                if isinstance(self.parent, PaletteTool):
                    max_frame = len(self.parent.character_images.get(self.parent.current_character, []))
                    if value < 1:
                        self.frame_choice_var.set("1")
                    elif value > max_frame:
                        self.frame_choice_var.set(str(max_frame))
            except ValueError:
                # If not a valid number, don't change anything
                pass
            
        self.frame_choice_var.trace_add("write", validate_frame_choice)
        
        
        # Show/hide frame choice based on initial state
        if initial_choice:
            self.frame_choice_container.pack(side="left", padx=(10,0))
        else:
            self.frame_choice_container.pack_forget()
        
        # Add traces for immediate updates
        self.format_var.trace_add("write", update_checkbox_states)
        self.portrait_var.trace_add("write", update_parent_settings)
        self.labels_var.trace_add("write", update_parent_settings)
        self.cute_bg_var.trace_add("write", update_parent_settings)
        self.palette_format_var.trace_add("write", update_parent_settings)
        self.user_choice_var.trace_add("write", update_parent_settings)
        
        # Show Dev Buttons checkbox
        dev_buttons_frame = tk.Frame(main_frame)
        dev_buttons_frame.pack(fill="x", pady=(5, 0))
        
        # Get initial value from parent if available
        initial_show_dev = False
        if isinstance(parent, PaletteTool):
            initial_show_dev = parent.show_dev_buttons
        
        self.show_dev_buttons_var = tk.BooleanVar(value=initial_show_dev)
        self.show_dev_buttons_checkbox = tk.Checkbutton(dev_buttons_frame, text="Show Dev Buttons", 
                                                        variable=self.show_dev_buttons_var,
                                                        command=self.toggle_dev_buttons)
        self.show_dev_buttons_checkbox.pack(anchor="center")
        
        # Excess Colors Prompt checkbox
        excess_colors_frame = tk.Frame(main_frame)
        excess_colors_frame.pack(fill="x", pady=(5, 0))
        
        # Get initial value from parent if available
        initial_show_excess_prompt = True  # Default to True (show prompts)
        if isinstance(parent, PaletteTool):
            # Load from settings - note: setting is "dont_show" so we invert it
            dont_show = getattr(parent, 'dont_show_excess_colors_prompt', False)
            initial_show_excess_prompt = not dont_show
        
        self.show_excess_colors_prompt_var = tk.BooleanVar(value=initial_show_excess_prompt)
        self.show_excess_colors_checkbox = tk.Checkbutton(excess_colors_frame, text="Show Excess Colors Prompts", 
                                                         variable=self.show_excess_colors_prompt_var)
        self.show_excess_colors_checkbox.pack(anchor="center")
        
        # Add trace for show_excess_colors_prompt_var after it's created
        self.show_excess_colors_prompt_var.trace_add("write", update_parent_settings)
        
        # Validation message
        self.validation_label = tk.Label(main_frame, text="", fg="red", wraplength=250)
        self.validation_label.pack(pady=5)
        
        # Button frame in the middle
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 40))
        
        # Center container for buttons
        button_container = tk.Frame(button_frame)
        button_container.pack(anchor="center")
        
        # Credits button with the same style as the main UI
        credits_button = tk.Button(button_container, text="Credits ♥", command=self.parent.show_credits,
                                bg="#C8A2C8", fg="white", activebackground="#B695B6", activeforeground="white")
        credits_button.pack(side="left", padx=5)
        
        # OK button (wider)
        self.ok_button = tk.Button(button_container, text="OK", command=self.ok_clicked, width=12)
        self.ok_button.pack(side="left", padx=5)
        
        # Cancel button
        cancel_button = tk.Button(button_container, text="Cancel", command=self.cancel_clicked, width=8)
        cancel_button.pack(side="left", padx=5)
        
        # Bind validation to input changes
        self.frame_var.trace_add("write", lambda *args: self.validate_inputs())
        self.start_var.trace_add("write", lambda *args: self.validate_inputs())
        self.end_var.trace_add("write", lambda *args: self.validate_inputs())
        
        # Center the dialog after all content is created
        self.dialog.update_idletasks()
        self._center_dialog_on_parent()
        
        # Apply initial button visibility based on checkbox states
        self.toggle_export_button()
        self.toggle_dev_buttons()
        
        # Bind Enter key to OK
        self.dialog.bind("<Return>", lambda e: self.ok_clicked())
        self.dialog.bind("<Escape>", lambda e: self.cancel_clicked())
        
        # Focus on entry
        self.frame_entry.focus_set()
        self.frame_entry.select_range(0, tk.END)
        
        # Initial validation (but don't auto-adjust values during initialization)
        self._initializing = True
        self.validate_inputs()
        self._initializing = False
        
    def validate_inputs(self):
        """Validate all inputs and update UI accordingly"""
        try:
            frames = int(self.frame_var.get())
            # Convert from 1-based to 0-based for internal validation
            start_frame = int(self.start_var.get()) - 1
            end_frame = int(self.end_var.get()) - 1
            
            if frames <= 0:
                self.show_validation_error("Number of frames must be greater than 0")
                return False
            if frames > self.max_frames:
                self.show_validation_error(f"Number of frames cannot exceed {self.max_frames}")
                return False
            if start_frame < 0:
                self.show_validation_error("Start frame must be at least 1")
                return False
            if end_frame >= self.max_frames:
                self.show_validation_error(f"End frame cannot exceed {self.max_frames}")
                return False
            if start_frame > end_frame:
                self.show_validation_error("Start frame must be less than or equal to end frame")
                return False
            # If frame count is larger than the range, auto-adjust it (but not during initialization)
            range_size = end_frame - start_frame + 1
            if range_size < frames and not getattr(self, '_initializing', False):
                self.frame_var.set(str(range_size))
                frames = range_size  # Update frames to match range
                return True  # Allow validation to pass with adjusted frame count
                
            self.validation_label.config(text="")
            self.ok_button.config(state="normal")
            return True
            
        except ValueError:
            self.show_validation_error("Please enter valid numbers")
            return False
            
    def show_validation_error(self, message):
        """Display validation error and disable OK button"""
        self.validation_label.config(text=message)
        self.ok_button.config(state="disabled")
    
    def update_bg_style_state(self):
        """Enable/disable BG Style options based on Portrait mode"""
        state = "normal" if self.portrait_var.get() else "disabled"
        for child in self.cute_bg_frame.winfo_children():
            if isinstance(child, tk.Radiobutton):
                child.configure(state=state)
        if not self.portrait_var.get():
            self.cute_bg_var.set("no_cute_bg")  # Reset to default when disabled
    
    def toggle_export_button(self):
        """Toggle visibility of Export Palette button in parent PaletteTool"""
        if isinstance(self.parent, PaletteTool):
            if self.show_export_button_var.get():
                # Insert before Live Edit Palette button to maintain order
                self.parent.export_palette_button.pack(side="left", padx=(0, 5), before=self.parent.live_edit_button)
            else:
                self.parent.export_palette_button.pack_forget()
    
    def toggle_dev_buttons(self):
        """Toggle visibility of dev buttons (Export All Frames, Debug Info) in parent PaletteTool"""
        if isinstance(self.parent, PaletteTool):
            if self.show_dev_buttons_var.get():
                # Show Export All Frames button (insert before Export Palette or Live Edit button)
                self.parent.export_all_frames_button.pack(side="left", padx=(0, 5), before=self.parent.live_edit_button)
                # Show Debug Info button (insert before Statistics button)
                self.parent.debug_info_button.pack(side="left", padx=(0, 5), before=self.parent.statistics_button)
            else:
                self.parent.export_all_frames_button.pack_forget()
                self.parent.debug_info_button.pack_forget()
    
    def toggle_frame_choice(self):
        """Toggle visibility of frame choice entry"""
        if self.user_choice_var.get():
            self.frame_choice_container.pack(side="left", padx=(10,0))
        else:
            self.frame_choice_container.pack_forget()
            
    def ok_clicked(self, close=True):
        try:
            frames = int(self.frame_var.get())
            # Convert from 1-based to 0-based for internal storage
            start_frame = int(self.start_var.get()) - 1
            end_frame = int(self.end_var.get()) - 1
            # Smart mode switching based on frame range settings
            if isinstance(self.parent, PaletteTool):
                current_mode = self.parent.preview_var.get()
                
                # Determine the appropriate mode based on frame settings
                if start_frame == 0 and end_frame == self.max_frames - 1:
                    # Full range (1 to max) - check if should be in all mode
                    if frames == self.max_frames:
                        # Full range with all frames - should be in all mode
                        target_mode = "all"
                    else:
                        # Full range but not all frames - use custom mode
                        target_mode = "custom"
                elif start_frame == 0 and end_frame == 0:
                    # Single frame (1 to 1) - could be single mode
                    if frames == 1:
                        target_mode = "single"
                        # Set the single frame index
                        self.parent.current_image_index = 0
                    else:
                        target_mode = "custom"
                else:
                    # Custom range - always use custom mode
                    target_mode = "custom"
                
                # Apply the mode change if needed
                if current_mode != target_mode:
                    self.parent.preview_var.set(target_mode)
                    # Ensure UI reflects the mode change immediately
                    try:
                        self.parent.on_preview_mode_change()
                    except Exception:
                        pass
            # Validate frame choice if enabled
            if self.user_choice_var.get():
                try:
                    # Get the frame number from user input (1-based)
                    chosen_frame = int(self.frame_choice_var.get())
                    if isinstance(self.parent, PaletteTool):
                        max_frame = len(self.parent.character_images.get(self.parent.current_character, []))
                        if chosen_frame < 1 or chosen_frame > max_frame:
                            messagebox.showerror("Invalid Input", f"Frame number must be between 1 and {max_frame}.")
                            return
                        # Keep as 1-based, don't convert to 0-based
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid frame number.")
                    return
            
            # Validate inputs
            if frames <= 0:
                messagebox.showerror("Invalid Input", "Number of frames must be greater than 0.")
                return
            
            if frames > self.max_frames:
                messagebox.showwarning("Too Many Frames", 
                                     f"You cannot display more than {self.max_frames} frames for lag purposes.\n"
                                     f"The number has been set to {self.max_frames}.")
                frames = self.max_frames
                self.frame_var.set(str(frames))
            
            if start_frame < 0:
                messagebox.showerror("Invalid Input", "Start frame must be greater than or equal to 0")
                return
            if end_frame >= self.max_frames:
                messagebox.showerror("Invalid Input", f"End frame must be less than {self.max_frames}")
                return
            if start_frame > end_frame:
                messagebox.showerror("Invalid Input", "Start frame must be less than or equal to end frame")
                return
            # If frame count is larger than the range, auto-adjust it
            range_size = end_frame - start_frame + 1
            if range_size < frames:
                frames = range_size  # Update frames to match range
                self.frame_var.set(str(frames))  # Update the display
            
            # Check for 50+ frames warning if it's a PaletteTool
            if isinstance(self.parent, PaletteTool) and frames > 50:
                if not self.parent._get_50_frames_warning_preference():
                    # Show warning dialog
                    warning_dialog = FramesWarningDialog(self, frames)
                    result, dont_show_again = warning_dialog.show()
                    
                    # Save the "don't show again" preference if user checked it
                    if dont_show_again:
                        self.parent._save_50_frames_warning_preference(True)
                    
                    if not result:
                        # User chose "Nah I'm good" - highlight fields and return to dialog
                        self._highlight_frame_fields()
                        self.dialog.lift()
                        self.dialog.focus_force()
                        return
                
            # Update parent's settings if it's a PaletteTool
            if isinstance(self.parent, PaletteTool):
                self.parent.use_bmp_export = self.format_var.get()
                self.parent.use_portrait_export = self.portrait_var.get()
                self.parent.cute_bg_option = self.cute_bg_var.get()  # This is handled separately from the result tuple
                self.parent.palette_format = self.palette_format_var.get()  # Update palette format
                self.parent.show_frame_labels = self.labels_var.get()
                self.parent.use_frame_choice = self.user_choice_var.get()
                self.parent.live_pal_ui_mode = self.live_pal_ui_var.get()  # Update live pal editor UI mode
                self.parent.show_export_palette_button = self.show_export_button_var.get()  # Save checkbox state
                self.parent.show_dev_buttons = self.show_dev_buttons_var.get()  # Save checkbox state
                if self.user_choice_var.get():
                    self.parent.chosen_frame = int(self.frame_choice_var.get())  # Keep as 1-based
                # Apply immediate frame settings for custom preview
                self.parent.custom_frame_count = frames
                if not self.user_choice_var.get():
                    self.parent.custom_start_index = start_frame
                
                # Save settings to file (global settings + per-character)
                self.parent._save_settings()
                if self.parent.current_character:
                    self.parent._save_character_settings(self.parent.current_character)
            
            # Include user's frame choice if enabled (keep as 1-based for result tuple)
            chosen_frame = int(self.frame_choice_var.get()) if self.user_choice_var.get() else None
            self.result = (frames, start_frame, end_frame, self.format_var.get(), self.labels_var.get(), 
                         self.portrait_var.get(), self.user_choice_var.get(), chosen_frame,
                         self.palette_format_var.get(), self.cute_bg_var.get(), self.live_pal_ui_var.get(),
                         self.show_export_button_var.get(), self.show_dev_buttons_var.get(), 
                         self.show_excess_colors_prompt_var.get())
            if close:
                self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    def cancel_clicked(self):
        self.dialog.destroy()
    
    def _center_dialog_on_parent(self):
        """Center the dialog on its parent window."""
        widget_parent = self.parent.master if isinstance(self.parent, PaletteTool) else self.parent
        
        # Get actual dialog dimensions after content is rendered
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        if widget_parent and widget_parent.winfo_exists():
            # Center on parent window
            parent_x = widget_parent.winfo_x()
            parent_y = widget_parent.winfo_y()
            parent_width = widget_parent.winfo_width()
            parent_height = widget_parent.winfo_height()
            
            # Calculate center position relative to parent
            x = parent_x + (parent_width - dialog_width) // 2
            y = parent_y + (parent_height - dialog_height) // 2
        else:
            # Center on screen if no parent
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width - dialog_width) // 2
            y = (screen_height - dialog_height) // 2
        
        # Set the dialog position (keep current size)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _highlight_frame_fields(self):
        """Highlight the frame-related input fields to draw attention"""
        # Store original colors
        if not hasattr(self, '_original_colors'):
            self._original_colors = {}
            
        # Highlight start frame entry
        if hasattr(self, 'start_entry'):
            self._original_colors['start'] = self.start_entry.cget('bg')
            self.start_entry.config(bg='#ffcccc')  # Light red
            
        # Highlight end frame entry  
        if hasattr(self, 'end_entry'):
            self._original_colors['end'] = self.end_entry.cget('bg')
            self.end_entry.config(bg='#ffcccc')  # Light red
            
        # Highlight frames entry
        if hasattr(self, 'frame_entry'):
            self._original_colors['frames'] = self.frame_entry.cget('bg')
            self.frame_entry.config(bg='#ffcccc')  # Light red
            
        # Schedule removal of highlighting after 3 seconds
        self.dialog.after(3000, self._remove_highlight)
    
    def _remove_highlight(self):
        """Remove highlighting from frame fields"""
        if hasattr(self, '_original_colors'):
            if hasattr(self, 'start_entry') and 'start' in self._original_colors:
                self.start_entry.config(bg=self._original_colors['start'])
            if hasattr(self, 'end_entry') and 'end' in self._original_colors:
                self.end_entry.config(bg=self._original_colors['end'])
            if hasattr(self, 'frame_entry') and 'frames' in self._original_colors:
                self.frame_entry.config(bg=self._original_colors['frames'])

class PaletteLayer:
    def __init__(self, name, colors, palette_type, active=True):
        self.name = name
        self.colors = colors  # List of (r,g,b)
        self.palette_type = palette_type  # 'hair', 'gloves', 'fashion', etc.
        self.active = active

class Statistics:
    """Class to track and manage program statistics"""
    def __init__(self):
        self.live_palette_files_edited = set()  # Track unique files edited
        self.live_palette_files_saved = set()  # Track unique files saved
        self.palettes_previewed = 0  # Track number of palettes previewed in main UI
        
        self.icons_edited = set()  # Track unique icons edited
        self.icons_saved = set()
        self.frames_previewed = 0
        self.frames_skipped = 0  # Track frames skipped with navigation

        self.start_time = time.time()
        self.character_edits = {}  # Dict to track edits per character/job
        self.exported_frames = 0
        self.exported_backgrounds = 0
        self.exported_palettes = {}  # Dict to track exports by character & type
        self.colors_saved = 0  # Combined from both editors
        
        # New statistics
        self.indexes_changed = 0  # Total number of palette indexes modified
        self.indexes_selected = 0  # Total number of indexes selected
        self.indexes_saved_in_pals = 0  # Number of non-keyed indexes saved in .pal files
        self.colors_saved_in_json = 0  # Number of colors saved in JSON format
        self.preview_indexes_selected = {
            'live_pal': 0,  # Indexes selected in live palette editor
            'live_icon': 0  # Indexes selected in live icon editor
        }
        
    def add_palette_edit(self, char_id: str, job_type: str):
        """Track a palette edit for a character/job"""
        key = f"{char_id}_{job_type}"
        if key not in self.character_edits:
            self.character_edits[key] = {
                'views': 0,
                'edits': 0,
                'palette_saves': 0,
                'exports': 0
            }
        self.character_edits[key]['edits'] += 1
        
    def add_character_view(self, char_id: str, job_type: str):
        """Track when a character/job is viewed"""
        key = f"{char_id}_{job_type}"
        if key not in self.character_edits:
            self.character_edits[key] = {
                'views': 0,
                'edits': 0,
                'palette_saves': 0,
                'exports': 0
            }
        self.character_edits[key]['views'] += 1
        
    def get_most_edited(self):
        """Get the most edited character & job type"""
        if not self.character_edits:
            return None, None, 0
            
        most_edited = max(self.character_edits.items(), 
                         key=lambda x: x[1]['edits'])
        char_id, job_type = most_edited[0].split('_', 1)
        return char_id, job_type, most_edited[1]['edits']
        
    def get_program_time(self):
        """Get total time in program in HH:MM:SS format"""
        total_seconds = int(time.time() - self.start_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
    def to_dict(self):
        """Convert statistics to a dictionary for saving"""
        return {
            'live_palette_files_edited': list(self.live_palette_files_edited),
            'live_palette_files_saved': list(self.live_palette_files_saved),
            'icons_edited': list(self.icons_edited),
            'icons_saved': list(self.icons_saved),
            'frames_previewed': self.frames_previewed,
            'frames_skipped': self.frames_skipped,
            'start_time': self.start_time,
            'character_edits': self.character_edits,
            'exported_frames': self.exported_frames,
            'exported_backgrounds': self.exported_backgrounds,
            'exported_palettes': self.exported_palettes,
            'colors_saved': self.colors_saved,
            'indexes_changed': self.indexes_changed,
            'indexes_selected': self.indexes_selected,
            'indexes_saved_in_pals': self.indexes_saved_in_pals,
            'colors_saved_in_json': self.colors_saved_in_json,
            'preview_indexes_selected': self.preview_indexes_selected,
            'palettes_previewed': self.palettes_previewed
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create a Statistics instance from a dictionary"""
        stats = cls()
        stats.live_palette_files_edited = set(data.get('live_palette_files_edited', []))
        stats.live_palette_files_saved = set(data.get('live_palette_files_saved', []))
        stats.icons_edited = set(data.get('icons_edited', []))
        stats.icons_saved = set(data.get('icons_saved', []))
        stats.frames_previewed = data.get('frames_previewed', 0)
        stats.frames_skipped = data.get('frames_skipped', 0)
        stats.start_time = data.get('start_time', time.time())
        stats.character_edits = data.get('character_edits', {})
        stats.exported_frames = data.get('exported_frames', 0)
        stats.exported_backgrounds = data.get('exported_backgrounds', 0)
        stats.exported_palettes = data.get('exported_palettes', {})
        stats.colors_saved = data.get('colors_saved', 0)
        stats.indexes_changed = data.get('indexes_changed', 0)
        stats.indexes_selected = data.get('indexes_selected', 0)
        stats.indexes_saved_in_pals = data.get('indexes_saved_in_pals', 0)
        stats.colors_saved_in_json = data.get('colors_saved_in_json', 0)
        stats.preview_indexes_selected = data.get('preview_indexes_selected', {
            'live_pal': 0,
            'live_icon': 0
        })
        stats.palettes_previewed = data.get('palettes_previewed', 0)
        return stats

class StatisticsDialog:
    """Dialog to display program statistics"""
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent.master)
        self.dialog.title("Program Statistics")
        self.dialog.transient(parent.master)
        self.dialog.grab_set()
        
        # Set fixed window size
        window_width = 650
        window_height = 450
        
        # Center the window
        x = (self.dialog.winfo_screenwidth() - window_width) // 2
        y = (self.dialog.winfo_screenheight() - window_height) // 2
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.dialog.resizable(False, False)
        
        # Main container with padding
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Local Statistics", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Create two columns
        columns_frame = ttk.Frame(main_frame)
        columns_frame.pack(fill="both", expand=True)
        
        # Configure equal column widths
        columns_frame.grid_columnconfigure(0, weight=1, uniform="column")
        columns_frame.grid_columnconfigure(1, weight=1, uniform="column")
        
        # General Stats Column
        general_frame = ttk.LabelFrame(columns_frame, text="General Statistics", padding="5")
        general_frame.grid(row=0, column=0, sticky="nsew", padx=2)
        
        general_canvas = tk.Canvas(general_frame, width=150)  # Larger base width
        general_scrollbar = ttk.Scrollbar(general_frame, orient="vertical", command=general_canvas.yview)
        general_content = ttk.Frame(general_canvas)
        
        general_canvas.configure(yscrollcommand=general_scrollbar.set)
        general_scrollbar.pack(side="right", fill="y")
        general_canvas.pack(side="left", fill="both", expand=True)
        
        # Character Stats Column
        character_frame = ttk.LabelFrame(columns_frame, text="Character Statistics", padding="5")
        character_frame.grid(row=0, column=1, sticky="nsew", padx=2)
        
        character_canvas = tk.Canvas(character_frame, width=150)  # Larger base width
        character_scrollbar = ttk.Scrollbar(character_frame, orient="vertical", command=character_canvas.yview)
        character_content = ttk.Frame(character_canvas)
        
        character_canvas.configure(yscrollcommand=character_scrollbar.set)
        character_scrollbar.pack(side="right", fill="y")
        character_canvas.pack(side="left", fill="both", expand=True)
        
        # Populate General Statistics first
        stats = parent.statistics
        self._add_stat(general_content, "Time in Program", stats.get_program_time())
        
        # Files and Icons
        self._add_stat(general_content, "Live Palette Files Edited", len(stats.live_palette_files_edited))
        self._add_stat(general_content, "Live Palette Files Saved", len(stats.live_palette_files_saved))
        self._add_stat(general_content, "Palettes Previewed", stats.palettes_previewed)
        self._add_stat(general_content, "Icons Edited", len(stats.icons_edited))
        self._add_stat(general_content, "Icons Saved", len(stats.icons_saved))
        
        # Frames
        self._add_stat(general_content, "Frames Previewed", stats.frames_previewed)
        self._add_stat(general_content, "Frames Skipped", stats.frames_skipped)
        
        # Palette Indexes
        self._add_stat(general_content, "Indexes Changed", stats.indexes_changed)
        self._add_stat(general_content, "Indexes Selected", stats.indexes_selected)
        self._add_stat(general_content, "Indexes Saved in PALs", stats.indexes_saved_in_pals)
        
        # Colors and Selections
        self._add_stat(general_content, "Colors Saved", stats.colors_saved)
        self._add_stat(general_content, "Colors Saved in JSON", stats.colors_saved_in_json)
        self._add_stat(general_content, "Live Palette Indexes Selected", stats.preview_indexes_selected['live_pal'])
        self._add_stat(general_content, "Live Icon Indexes Selected", stats.preview_indexes_selected['live_icon'])
        
        # Export Statistics (moved from separate column)
        self._add_stat(general_content, "Exported Frames", stats.exported_frames)
        self._add_stat(general_content, "Exported Backgrounds", stats.exported_backgrounds)
        
        # Add palette export stats
        if stats.exported_palettes:
            for char_type, count in stats.exported_palettes.items():
                self._add_stat(general_content, f"Exported {char_type} Palettes", count)
        
        # Populate Character Statistics
        char_id, job_type, edit_count = stats.get_most_edited()
        if char_id and job_type:
            char_name = self._get_character_display_name(char_id)
            self._add_stat(character_content, "Most Edited Character", f"{char_name} ({job_type})")
            self._add_stat(character_content, "Edit Count", edit_count)
        
        # Add character-specific stats
        for key, data in sorted(stats.character_edits.items()):
            char_id, job_type = key.split('_', 1)
            char_name = self._get_character_display_name(char_id)
            frame = ttk.LabelFrame(character_content, text=f"{char_name} - {job_type}")
            frame.pack(fill="x", pady=2)
            self._add_stat(frame, "Views", data['views'])
            self._add_stat(frame, "Edits", data['edits'])
            self._add_stat(frame, "Palette Saves", data['palette_saves'])
            self._add_stat(frame, "Exports", data['exports'])
        
        
        # Create windows for the content frames after content is added
        self.dialog.update_idletasks()  # Update to get proper canvas dimensions
        
        general_canvas.create_window((0, 0), window=general_content, anchor="nw")
        character_canvas.create_window((0, 0), window=character_content, anchor="nw")
        
        # Configure scroll regions after adding content
        general_content.update_idletasks()
        character_content.update_idletasks()
        
        general_canvas.configure(scrollregion=general_canvas.bbox("all"))
        character_canvas.configure(scrollregion=character_canvas.bbox("all"))
        
        # Mouse wheel scrolling
        general_content.bind("<MouseWheel>", lambda e: general_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        character_content.bind("<MouseWheel>", lambda e: character_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.dialog.destroy)
        close_button.pack(pady=(10, 0))
        
    def _get_character_display_name(self, char_id):
        """Get the proper display name for a character"""
        from icon_handler import CHARACTER_MAPPING
        if char_id in CHARACTER_MAPPING:
            return CHARACTER_MAPPING[char_id]['name']
        return char_id
    
    def _add_stat(self, parent, label, value):
        """Add a statistic row to the given parent frame"""
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=1, padx=2)
        
        # Create a single label that spans the full width
        full_text = f"{label}: {value}"
        label_widget = ttk.Label(frame, text=full_text)
        label_widget.pack(fill="x", expand=True)

class AllModeWarningDialog:
    """Warning dialog for switching to 'All' mode"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = False
        self.dont_show_again = False
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent.master)
        self.dialog.title("Warning - All Mode")
        self.dialog.geometry("500x200")
        self.dialog.resizable(False, False)
        
        # Make it modal and bring to front
        self.dialog.transient(parent.master)
        self.dialog.grab_set()
        self.dialog.lift()
        self.dialog.focus_force()
        
        # Center the dialog on the parent window
        self._center_dialog()
        
        self._create_ui()
        
    def _center_dialog(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.master.winfo_x()
        parent_y = self.parent.master.winfo_y()
        parent_width = self.parent.master.winfo_width()
        parent_height = self.parent.master.winfo_height()
        
        # Calculate center position
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f"+{x}+{y}")
        
    def _create_ui(self):
        """Create the dialog UI"""
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning message
        message = ("Warning: This may be resource-intensive on even newer machines, continue? "
                  "You can always use Custom Preview Options (the gear icon) to change your view "
                  "to more or less frames.")
        
        msg_label = tk.Label(main_frame, text=message, wraplength=460, justify="left", font=("Arial", 10))
        msg_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Buttons
        ballsy_btn = tk.Button(button_frame, text="Yeah, I'm ballsy!", command=self._on_ballsy, 
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15)
        ballsy_btn.pack(side="left", padx=(0, 10))
        
        good_btn = tk.Button(button_frame, text="No, I'm good", command=self._on_good, 
                            bg="#f44336", fg="white", font=("Arial", 10), width=15)
        good_btn.pack(side="left")
        
        # Don't show again checkbox
        self.dont_show_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(main_frame, text="Don't show warning again", 
                                 variable=self.dont_show_var, font=("Arial", 9))
        checkbox.pack(anchor="w")
        
        # Handle window close event
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_good)
        
    def _on_ballsy(self):
        """User chose to proceed with All mode"""
        self.result = True
        self.dont_show_again = self.dont_show_var.get()
        self.dialog.destroy()
        
    def _on_good(self):
        """User chose not to proceed with All mode"""
        self.result = False
        self.dont_show_again = self.dont_show_var.get()
        self.dialog.destroy()
        
    def show(self):
        """Show the dialog and return the result"""
        self.dialog.wait_window()
        return self.result, self.dont_show_again


class FramesWarningDialog:
    """Warning dialog for displaying 50+ frames in custom preview"""
    
    def __init__(self, parent, frame_count):
        self.parent = parent
        self.frame_count = frame_count
        self.result = False
        self.dont_show_again = False
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent.dialog)
        self.dialog.title("Warning - High Frame Count")
        self.dialog.geometry("500x180")
        self.dialog.resizable(False, False)
        
        # Make it modal and bring to front
        self.dialog.transient(parent.dialog)
        self.dialog.grab_set()
        self.dialog.lift()
        self.dialog.focus_force()
        
        # Center the dialog on the parent dialog
        self._center_dialog()
        
        self._create_ui()
        
    def _center_dialog(self):
        """Center the dialog on the parent dialog"""
        self.dialog.update_idletasks()
        
        # Get parent dialog position and size
        parent_x = self.parent.dialog.winfo_x()
        parent_y = self.parent.dialog.winfo_y()
        parent_width = self.parent.dialog.winfo_width()
        parent_height = self.parent.dialog.winfo_height()
        
        # Calculate center position
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f"+{x}+{y}")
        
    def _create_ui(self):
        """Create the dialog UI"""
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning message
        message = f"WARNING: Over 50 frames displayed ({self.frame_count} frames), this may be very laggy on older computers. Continue?"
        
        msg_label = tk.Label(main_frame, text=message, wraplength=460, justify="left", font=("Arial", 10))
        msg_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Buttons
        ballsy_btn = tk.Button(button_frame, text="Yeah I'm ballsy", command=self._on_ballsy, 
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15)
        ballsy_btn.pack(side="left", padx=(0, 10))
        
        good_btn = tk.Button(button_frame, text="Nah I'm good", command=self._on_good, 
                            bg="#f44336", fg="white", font=("Arial", 10), width=15)
        good_btn.pack(side="left")
        
        # Don't show again checkbox
        self.dont_show_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(main_frame, text="Don't show again", 
                                 variable=self.dont_show_var, font=("Arial", 9))
        checkbox.pack(anchor="w")
        
        # Handle window close event
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_good)
        
    def _on_ballsy(self):
        """User chose to proceed with high frame count"""
        self.result = True
        self.dont_show_again = self.dont_show_var.get()
        self.dialog.destroy()
        
    def _on_good(self):
        """User chose not to proceed with high frame count"""
        self.result = False
        self.dont_show_again = self.dont_show_var.get()
        self.dialog.destroy()
        
    def show(self):
        """Show the dialog and return the result"""
        self.dialog.wait_window()
        return self.result, self.dont_show_again


class PaletteTool:
    def _warn_if_nonimpact(self, palette_type: str) -> bool:
        """Return True to proceed, False to cancel. Warn only for hair or 3rd job base."""
        try:
            pt = str(palette_type or "").strip().lower()
        except Exception:
            pt = str(palette_type).lower() if palette_type is not None else ""
        if pt in ("hair", "3rd_job_base".lower()):
            # Track acknowledgements per editor session so we don't spam
            if not hasattr(self, "_live_warned_types"):
                self._live_warned_types = set()
            if pt in getattr(self, "_live_warned_types", set()):
                return True
            msg = "⚠️ WARNING: Editing this part will not impact in game fashion, are you sure you want to continue?"
            
            # Create custom dialog with red text
            dialog = tk.Toplevel(self.master)
            dialog.title("Heads up")
            dialog.resizable(False, False)
            dialog.transient(self.master)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            width = 400
            height = 150
            x = (dialog.winfo_screenwidth() - width) // 2
            y = (dialog.winfo_screenheight() - height) // 2
            dialog.geometry(f"{width}x{height}+{x}+{y}")
            
            # Warning message in red
            tk.Label(dialog, text=msg, wraplength=350, justify="center", 
                    fg="red", font=("Arial", 11, "bold")).pack(pady=20)
            
            # Button frame
            button_frame = tk.Frame(dialog)
            button_frame.pack(pady=10)
            
            result = {"ok": False}
            
            def on_yes():
                result["ok"] = True
                dialog.destroy()
            
            def on_no():
                result["ok"] = False
                dialog.destroy()
            
            tk.Button(button_frame, text="Yes", command=on_yes, width=10).pack(side="left", padx=5)
            tk.Button(button_frame, text="No", command=on_no, width=10).pack(side="left", padx=5)
            
            # Wait for dialog to close
            dialog.wait_window()
            ok = result["ok"]
            
            if ok:
                try:
                    self._live_warned_types.add(pt)
                except Exception:
                    pass
            return bool(ok)
        return True
        
    def _get_statistics_path(self):
        """Get the path to the statistics file"""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "statistics.json")
    
    def _load_statistics(self):
        """Load statistics from file"""
        try:
            stats_path = self._get_statistics_path()
            with open(stats_path, 'r') as f:
                data = json.load(f)
                self.statistics = Statistics.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            # Keep default statistics if file doesn't exist or is invalid
            pass
            
    def _save_statistics(self):
        """Save statistics to file"""
        try:
            stats_path = self._get_statistics_path()
            with open(stats_path, 'w') as f:
                json.dump(self.statistics.to_dict(), f, indent=4)
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error saving statistics: {e}")
    
    def _get_settings_path(self):
        """Get the path to the settings file"""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
    
    def _load_settings(self):
        """Load settings from file"""
        try:
            settings_path = self._get_settings_path()
            with open(settings_path, 'r') as f:
                data = json.load(f)
                
                # Load global settings
                global_settings = data.get('global', {})
                self.use_bmp_export = global_settings.get('use_bmp_export', True)
                self.use_portrait_export = global_settings.get('use_portrait_export', True)
                self.cute_bg_option = global_settings.get('cute_bg_option', "both")
                self.palette_format = global_settings.get('palette_format', "png")
                self.show_frame_labels = global_settings.get('show_frame_labels', True)
                self.use_right_click = global_settings.get('use_right_click', True)
                self.live_pal_ui_mode = global_settings.get('live_pal_ui_mode', "Simple")
                self.show_export_palette_button = global_settings.get('show_export_palette_button', False)
                self.show_dev_buttons = global_settings.get('show_dev_buttons', False)
                self.use_quick_export = global_settings.get('use_quick_export', False)
                self.zoom_level = global_settings.get('zoom_level', "100%")
                self.dont_show_excess_colors_prompt = global_settings.get('dont_show_excess_colors_prompt', False)
                
                # Initialize session-only settings (cleared when program closes)
                self.session_dont_show_excess_colors_prompt = False
                
                # Load background color (convert list back to tuple)
                bg_color = global_settings.get('background_color', [255, 255, 255])
                self.background_color = tuple(bg_color) if isinstance(bg_color, list) else (255, 255, 255)
                
                # Load session state (last used character, frame, preview)
                self.last_character = global_settings.get('last_character', None)
                self.last_job = global_settings.get('last_job', None)
                self.last_frame = global_settings.get('last_frame', 0)
                self.last_preview_mode = global_settings.get('last_preview_mode', "single")
                
                # Store per-character settings for later use
                self.per_character_settings = data.get('per_character', {})
                
        except (FileNotFoundError, json.JSONDecodeError):
            # Use defaults if file doesn't exist or is invalid
            self.per_character_settings = {}
            self.use_quick_export = False
            # Initialize session state defaults
            self.last_character = None
            self.last_job = None
            self.last_frame = 0
            self.last_preview_mode = "single"
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            settings_path = self._get_settings_path()
            
            # Load existing settings to preserve per-character data
            try:
                with open(settings_path, 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {'global': {}, 'per_character': {}}
            
            # Update global settings (preserve dont_show_excess_colors_prompt if it exists)
            existing_global = data.get('global', {})
            data['global'] = {
                'use_bmp_export': self.use_bmp_export,
                'use_portrait_export': self.use_portrait_export,
                'cute_bg_option': self.cute_bg_option,
                'palette_format': self.palette_format,
                'show_frame_labels': self.show_frame_labels,
                'use_right_click': self.use_right_click,
                'live_pal_ui_mode': self.live_pal_ui_mode,
                'show_export_palette_button': self.show_export_palette_button,
                'show_dev_buttons': self.show_dev_buttons,
                'use_quick_export': self.use_quick_export,
                'zoom_level': self.zoom_var.get() if hasattr(self, 'zoom_var') else "100%",
                'background_color': list(self.background_color),  # Convert tuple to list for JSON
                'dont_show_excess_colors_prompt': getattr(self, 'dont_show_excess_colors_prompt', False),
                'dont_show_all_mode_warning': existing_global.get('dont_show_all_mode_warning', False),
                'dont_show_50_frames_warning': existing_global.get('dont_show_50_frames_warning', False),
                # Session state
                'last_character': self.current_character,
                'last_job': self.current_job,
                'last_frame': self.current_image_index,
                'last_preview_mode': self.preview_var.get() if hasattr(self, 'preview_var') else "single"
            }
            
            # Keep per-character settings
            if not hasattr(self, 'per_character_settings'):
                self.per_character_settings = {}
            data['per_character'] = self.per_character_settings
            
            # Save to file
            with open(settings_path, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error saving settings: {e}")
    
    def _get_all_mode_warning_preference(self):
        """Get the 'don't show all mode warning' preference from settings"""
        try:
            settings_path = self._get_settings_path()
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    return settings.get('global', {}).get('dont_show_all_mode_warning', False)
        except Exception:
            pass
        return False
    
    def _save_all_mode_warning_preference(self, dont_show):
        """Save the 'don't show all mode warning' preference to settings"""
        try:
            settings_path = self._get_settings_path()
            
            # Load existing settings
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                settings = {'global': {}, 'per_character': {}}
            
            # Ensure global key exists
            if 'global' not in settings:
                settings['global'] = {}
            
            # Update the preference
            settings['global']['dont_show_all_mode_warning'] = dont_show
            
            # Save settings
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
                
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error saving all mode warning preference: {e}")
    
    def _show_all_mode_warning(self):
        """Show the all mode warning dialog and return user's choice"""
        dialog = AllModeWarningDialog(self)
        result, dont_show_again = dialog.show()
        
        # Save the "don't show again" preference if user checked it
        if dont_show_again:
            self._save_all_mode_warning_preference(True)
        
        return result
    
    def _get_50_frames_warning_preference(self):
        """Get the 'don't show 50+ frames warning' preference from settings"""
        try:
            settings_path = self._get_settings_path()
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    return settings.get('global', {}).get('dont_show_50_frames_warning', False)
        except Exception:
            pass
        return False
    
    def _save_50_frames_warning_preference(self, dont_show):
        """Save the 'don't show 50+ frames warning' preference to settings"""
        try:
            settings_path = self._get_settings_path()
            
            # Load existing settings
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                settings = {'global': {}, 'per_character': {}}
            
            # Ensure global key exists
            if 'global' not in settings:
                settings['global'] = {}
            
            # Update the preference
            settings['global']['dont_show_50_frames_warning'] = dont_show
            
            # Save settings
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
                
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error saving 50 frames warning preference: {e}")
    
    def _load_character_settings(self, char_id):
        """Load per-character settings for the given character"""
        if not hasattr(self, 'per_character_settings'):
            self.per_character_settings = {}
            
        char_settings = self.per_character_settings.get(char_id, {})
        
        # Only load per-character settings (frame-related)
        self.custom_frame_count = char_settings.get('custom_frame_count', 1)
        self.custom_start_index = char_settings.get('custom_start_index', 0)
        self.use_frame_choice = char_settings.get('use_frame_choice', False)
        self.chosen_frame = char_settings.get('chosen_frame', 1)
    
    def _save_character_settings(self, char_id):
        """Save per-character settings for the given character"""
        if not hasattr(self, 'per_character_settings'):
            self.per_character_settings = {}
        
        # Save per-character settings (frame-related only)
        self.per_character_settings[char_id] = {
            'custom_frame_count': self.custom_frame_count,
            'custom_start_index': self.custom_start_index,
            'use_frame_choice': self.use_frame_choice,
            'chosen_frame': self.chosen_frame
        }
        
        # Save to file
        self._save_settings()


    def __init__(self, master):
        # Initialize statistics first
        self.statistics = Statistics()
        self._load_statistics()
        
        self.master = master
        self.master.title("Fashion Previewer v4.1 - A CoraTO & Kyo Collab")

        # Dictionary to store frame range settings per character/job
        # Format: {char_id: {job: (frame_count, start_frame, end_frame)}}
        self.frame_range_settings = {}

        self.original_image = None
        self.original_palette = [(0, 0, 0)] * PALETTE_SIZE
        self.palette_layers = []
        
        # Character and job selection
        self.current_character = None
        self.current_job = None
        self.current_image_path = None
        self.current_image_index = 0
        
        # Initialize default settings (will be overridden by _load_settings)
        # Custom preview settings
        self.custom_frame_count = 1
        self.custom_start_index = 0
        self.use_bmp_export = True  # False = PNG, True = BMP
        self.use_portrait_export = True  # Portrait mode (100x100)
        self.cute_bg_option = "both"  # Options: "no_cute_bg", "cute_bg", "both"
        self.palette_format = "png"  # Options: "pal", "png"
        self.show_frame_labels = True  # Whether to show frame numbers
        self.use_right_click = True  # True = Right click save (default), False = Left click save
        self.use_frame_choice = False  # Whether to use user-chosen frame for export
        self.chosen_frame = 1  # User's chosen frame for export (1-based)
        self.background_color = (255, 255, 255)  # Default background color (white)
        self.live_pal_ui_mode = "Simple"  # Default to Simple mode for Live Pal Editor UI
        self._current_preview_mode = "single"  # Track current preview mode for intelligent switching
        self.colorpicker_active = False  # Track colorpicker mode for simple palette editor
        
        # UI button visibility settings
        self.show_export_palette_button = False  # Show Button checkbox state
        self.show_dev_buttons = False  # Show Dev Buttons checkbox state
        
        # Load settings from file (will override defaults)
        self._load_settings()
        
        # HSL adjustment settings with defaults
        self._gradient_adjust_hue = True
        self._gradient_adjust_saturation = False
        self._gradient_adjust_value = False
        
        # Get root directory for relative paths
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load base images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        myshop_base_path = os.path.join(script_dir, "nonremovable_assets", "myshop_base.bmp")
        try:
            self.myshop_base = Image.open(myshop_base_path)
        except Exception as e:
            self.myshop_base = None
        
        # Available data
        self.available_characters = []
        self.available_jobs = []
        self.character_images = {}  # chr001 -> [list of image paths]
        self.fashion_palettes = {}  # chr001 -> [list of fashion palette paths]
        self.hair_palettes = {}     # chr001 -> [list of hair palette paths]
        self.third_job_palettes = {} # chr001 -> [list of 3rd job base fashion paths]
        self.custom_pals = {}       # chr001 -> [list of custom palette paths]
        
        # UI variables
        self.character_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.hair_var = tk.StringVar()
        self.third_job_var = tk.StringVar()
        self.zoom_var = tk.StringVar(value=getattr(self, 'zoom_level', "100%"))
        self.fashion_vars = {}  # Track fashion selection variables
        
        # Load all available data
        self.load_all_data()
        
        # Create UI
        self.create_ui()
        
        # Try to restore last session state, otherwise auto-load first character
        restored = False
        if hasattr(self, 'last_character') and self.last_character and hasattr(self, 'last_job') and self.last_job:
            # Try to restore the saved character and job
            if self.last_character in self.available_characters:
                if self.last_character in CHARACTER_MAPPING:
                    char_info = CHARACTER_MAPPING[self.last_character]
                    
                    # Directly set the character and job without triggering on_character_change
                    self.current_character = self.last_character
                    self.current_job = char_info['job']
                    self.character_var.set(char_info['name'])
                    self.job_var.set(char_info['job'])
                    
                    # Set restoration flag to prevent saving during restoration
                    self._is_restoring_session = True
                    
                    # Load character settings and data
                    self._load_character_settings(self.last_character)
                    
                    # Populate frame_range_settings for the restored character/job combo
                    # This is needed for custom preview mode to work properly
                    if self.current_character not in self.frame_range_settings:
                        self.frame_range_settings[self.current_character] = {}
                    
                    # Store the custom frame settings for this character/job
                    self.frame_range_settings[self.current_character][char_info['job']] = (
                        self.custom_frame_count,
                        self.custom_start_index,
                        self.custom_start_index + self.custom_frame_count - 1
                    )
                    
                    # Track character view
                    self.statistics.add_character_view(self.last_character, char_info["job"])
                    self._save_statistics()
                    
                    # Update UI sections
                    self.update_third_job_section()
                    self.update_hair_section()
                    self.update_fashion_section()
                    
                    # Load palettes and update display
                    self.load_palettes()
                    self.update_zoom_combo_state()
                    
                    # Restore the last viewed frame if valid
                    if hasattr(self, 'last_frame') and self.last_frame is not None:
                        # Check if character has images loaded
                        if self.current_character in self.character_images:
                            images = self.character_images[self.current_character]
                            if images and 0 <= self.last_frame < len(images):
                                self.current_image_index = self.last_frame
                                # Load the specific frame
                                self.load_image_from_path(images[self.current_image_index])
                    
                    # Update display to show the restored state
                    self.update_image_display()
                    
                    # Update navigation buttons to enable them
                    self.update_navigation_buttons()
                    
                    # Clear restoration flag - now navigation can save settings
                    self._is_restoring_session = False
                    
                    restored = True
        
        # If restoration failed, auto-load first character if available
        if not restored and self.available_characters:
            first_char = self.available_characters[0]
            if first_char in CHARACTER_MAPPING:
                char_info = CHARACTER_MAPPING[first_char]
                self.character_var.set(char_info['name'])
                self.job_var.set(char_info['job'])
                self.on_character_change()
        
        # Initialize zoom combo state based on preview mode (after character is loaded)
        self.update_zoom_combo_state()
        
        # Final navigation button update after all initialization is complete
        if hasattr(self, 'update_navigation_buttons'):
            self.update_navigation_buttons()
        
        # Set up window close handler to save settings and statistics
        def on_app_close():
            """Save settings and statistics before closing"""
            self._save_settings()
            self._save_statistics()
            self.master.destroy()
        
        self.master.protocol("WM_DELETE_WINDOW", on_app_close)

    # --- Smooth HSV slider: tiny debouncer to prevent jitter ----
    def _hsv_debounced_change(self, *_):
        """Debounce slider/entry changes and call _live_hsv_changed() once per burst. Prevents jitter by avoiding recursion and canceling stale callbacks."""
        # Cancel any prior scheduled call
        try:
            if getattr(self, "_hsv_after_id", None):
                try:
                    self.master.after_cancel(self._hsv_after_id)
                except Exception:
                    pass
        except Exception:
            pass
    
        def _apply():
            # Clear token to avoid future cancels on this one
            self._hsv_after_id = None
            # Guard to avoid re-entrancy if widgets update vars
            if getattr(self, "_hsv_guard", False):
                return
            try:
                self._hsv_guard = True
                if hasattr(self, "_live_hsv_changed"):
                    self._live_hsv_changed()
            finally:
                self._hsv_guard = False
    
        # Schedule a single near-future update (~60 FPS)
        try:
            self._hsv_after_id = self.master.after(16, _apply)
        except Exception:
            _apply()
    
    def _debounced_display_update(self):
        """Debounce main display updates to prevent flickering during live palette editing"""
        # Skip main display updates if live palette editor is open
        if (hasattr(self, '_live_editor_window') and 
            self._live_editor_window and 
            self._live_editor_window.winfo_exists()):
            return
        
        # Skip main display updates if icon palette editor is open
        from icon_handler import IconHandler
        if (IconHandler._icon_editor_instance and 
            IconHandler._icon_editor_instance.window and 
            IconHandler._icon_editor_instance.window.winfo_exists()):
            return
        
        # Cancel any prior scheduled display update
        try:
            if getattr(self, "_display_update_after_id", None):
                try:
                    self.master.after_cancel(self._display_update_after_id)
                except Exception:
                    pass
        except Exception:
            pass
        
        def _update_display():
            try:
                self.update_image_display()
            except Exception as e:
                print(f"Error updating display: {e}")
        
        # Schedule display update with slightly longer delay to reduce flickering
        try:
            self._display_update_after_id = self.master.after(50, _update_display)
        except Exception:
            _update_display()
    
    def _is_keyed_color(self, rgb_color, palette_index=None):
        """Check if an RGB color is a keyed/transparency color that should be avoided"""
        r, g, b = rgb_color
        
        # Universal keying colors
        if self.is_universal_keying_color(rgb_color):
            return True
        
        # Magenta (chroma key)
        if rgb_color == (255, 0, 255):
            return True
        
        # Black is generally allowed ("Never make black transparent")
        # Exception: chr004 specifically treats black as keyed
        if rgb_color == (0, 0, 0):
            if hasattr(self, 'current_character') and self.current_character:
                char_num = self.current_character[3:]  # Extract number from chr###
                if char_num == "004":
                    return True  # Black is keyed for chr004
            # Black is allowed for all other characters
            return False
        
        return False
    
    def _find_nearest_non_keyed_color(self, target_rgb, adjustment_direction='both'):
        """Find the nearest non-keyed color by adjusting RGB values"""
        r, g, b = target_rgb
        
        # If the color is not keyed, return it as-is
        if not self._is_keyed_color(target_rgb):
            return target_rgb
        
        # Try different adjustment strategies
        for offset in range(1, 20):  # Try up to 20 units of adjustment
            candidates = []
            
            if adjustment_direction in ['both', 'up']:
                # Try increasing values
                candidates.extend([
                    (min(255, r + offset), g, b),
                    (r, min(255, g + offset), b),
                    (r, g, min(255, b + offset)),
                    (min(255, r + offset), min(255, g + offset), b),
                    (min(255, r + offset), g, min(255, b + offset)),
                    (r, min(255, g + offset), min(255, b + offset)),
                ])
            
            if adjustment_direction in ['both', 'down']:
                # Try decreasing values
                candidates.extend([
                    (max(0, r - offset), g, b),
                    (r, max(0, g - offset), b),
                    (r, g, max(0, b - offset)),
                    (max(0, r - offset), max(0, g - offset), b),
                    (max(0, r - offset), g, max(0, b - offset)),
                    (r, max(0, g - offset), max(0, b - offset)),
                ])
            
            # Check each candidate
            for candidate in candidates:
                if not self._is_keyed_color(candidate):
                    return candidate
        
        # If we can't find a good alternative, return a safe default
        return (128, 128, 128)  # Gray as fallback
    
    def load_all_data(self):
        """Load all available characters, images, and palettes"""
        # Fix working directory first
        fix_working_directory()
        
        # Load character images from rawbmps folder
        rawbmps_path = "rawbmps"
        if os.path.exists(rawbmps_path):
            for char_folder in os.listdir(rawbmps_path):
                if char_folder.startswith("chr") and os.path.isdir(os.path.join(rawbmps_path, char_folder)):
                    char_path = os.path.join(rawbmps_path, char_folder)
                    images = []
                    for file in os.listdir(char_path):
                        if file.lower().endswith(('.bmp', '.png')):
                            images.append(os.path.join(char_path, file))
                    if images:
                        self.character_images[char_folder] = sorted(images)
                        if char_folder in CHARACTER_MAPPING:
                            self.available_characters.append(char_folder)
        
        # Load fashion palettes from nonremovable_assets/vanilla_pals/fashion folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        fashion_path = os.path.join(script_dir, "nonremovable_assets", "vanilla_pals", "fashion")
        if os.path.exists(fashion_path):
            for file in os.listdir(fashion_path):
                if file.lower().endswith('.pal'):
                    char_match = re.match(r'^chr(\d{3})_w\d+\.pal$', file.lower())
                    if char_match:
                        char_num = char_match.group(1)
                        char_id = f"chr{char_num}"
                        if char_id not in self.fashion_palettes:
                            self.fashion_palettes[char_id] = []
                        
                        # Validate the palette file before adding it
                        palette_path = os.path.join(fashion_path, file)
                        try:
                            with open(palette_path, "rb") as f:
                                data = f.read()
                            
                            if len(data) != PALETTE_SIZE * 3:
                                print(f"CONSOLE ERROR MSG: Invalid fashion palette file {file} - incorrect size: {len(data)} bytes")
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            valid_file = True
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"CONSOLE ERROR MSG: Invalid fashion palette file {file} - invalid byte at position {i}")
                                    valid_file = False
                                    break
                            
                            if valid_file:
                                self.fashion_palettes[char_id].append(palette_path)
                            
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Failed to load fashion palette {file}: {e}")
                            continue
        
        # Load custom fashion palettes from root/exports/custom_pals/fashion AND backwards compatibility
        root_dir = getattr(self, "root_dir", 
                          os.environ.get("FASHION_PREVIEWER_ROOT", 
                                       os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        # Check both new and old paths for custom fashion palettes
        custom_fashion_paths = [
            os.path.join(root_dir, "exports", "custom_pals", "fashion"),
            os.path.join(root_dir, "exports", "custom_fashion_pals")  # backwards compatibility
        ]
        
        for custom_pals_path in custom_fashion_paths:
            path_type = "new" if "custom_pals" in custom_pals_path and "fashion" in custom_pals_path else "legacy"
            
            if not os.path.exists(custom_pals_path):
                if path_type == "new":
                    os.makedirs(custom_pals_path, exist_ok=True)
                continue
            for file in os.listdir(custom_pals_path):
                if file.lower().endswith('.pal'):
                    # Check for fashion palettes (chr###_w#.pal through chr###_w######.pal)
                    fashion_match = re.match(r'^chr(\d{3})_w\d+\.pal$', file.lower())
                    if fashion_match:
                        char_num = fashion_match.group(1)
                        char_id = f"chr{char_num}"
                        if char_id not in self.fashion_palettes:
                            self.fashion_palettes[char_id] = []
                        
                        # Validate the palette file before adding it
                        palette_path = os.path.join(custom_pals_path, file)
                        try:
                            with open(palette_path, "rb") as f:
                                data = f.read()
                            
                            if len(data) != PALETTE_SIZE * 3:
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            valid_file = True
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"CONSOLE ERROR MSG: Invalid custom fashion palette file {file} - invalid byte at position {i}")
                                    valid_file = False
                                    break
                            
                            if valid_file:
                                self.fashion_palettes[char_id].append(palette_path)
                            
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Failed to load custom fashion palette {file}: {e}")
                            continue
        
        # Load hair palettes from nonremovable_assets/vanilla_pals/hair folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        hair_path = os.path.join(script_dir, "nonremovable_assets", "vanilla_pals", "hair")
        if os.path.exists(hair_path):
            for file in os.listdir(hair_path):
                if file.lower().endswith('.pal'):
                    char_match = re.match(r'^chr(\d{3})_\d+\.pal$', file)
                    if char_match:
                        char_num = char_match.group(1)
                        char_id = f"chr{char_num}"
                        if char_id not in self.hair_palettes:
                            self.hair_palettes[char_id] = []
                        
                        # Validate the palette file before adding it
                        palette_path = os.path.join(hair_path, file)
                        try:
                            with open(palette_path, "rb") as f:
                                data = f.read()
                            
                            if len(data) != PALETTE_SIZE * 3:
                                print(f"CONSOLE ERROR MSG: Invalid hair palette file {file} - incorrect size: {len(data)} bytes")
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"CONSOLE ERROR MSG: Invalid hair palette file {file} - invalid byte at position {i}")
                                    continue
                            
                            self.hair_palettes[char_id].append(palette_path)
                            
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Failed to load hair palette {file}: {e}")
                            continue
        
        # Load custom hair palettes from exports/custom_pals/hair folder
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        custom_hair_path = os.path.join(root_dir, "exports", "custom_pals", "hair")
        if os.path.exists(custom_hair_path):
            for file in os.listdir(custom_hair_path):
                if file.lower().endswith('.pal'):
                    # Match pattern: chr###_#.pal (where # can be any number of digits)
                    char_match = re.match(r'^chr(\d{3})_(\d+)\.pal$', file)
                    if char_match:
                        char_num = char_match.group(1)
                        char_id = f"chr{char_num}"
                        if char_id not in self.hair_palettes:
                            self.hair_palettes[char_id] = []
                        
                        # Validate the custom palette file before adding it
                        palette_path = os.path.join(custom_hair_path, file)
                        try:
                            with open(palette_path, "rb") as f:
                                data = f.read()
                            
                            if len(data) != PALETTE_SIZE * 3:
                                print(f"CONSOLE ERROR MSG: Invalid custom hair palette file {file} - incorrect size: {len(data)} bytes")
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"CONSOLE ERROR MSG: Invalid custom hair palette file {file} - invalid byte at position {i}")
                                    continue
                            
                            self.hair_palettes[char_id].append(palette_path)
                            
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Failed to load custom hair palette {file}: {e}")
                            continue
        
        # Load 3rd job base fashion palettes
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        third_job_path = os.path.join(script_dir, "nonremovable_assets", "vanilla_pals", "3rd_default_fashion")
        if os.path.exists(third_job_path):
            for char_folder in os.listdir(third_job_path):
                if char_folder.startswith("chr") and os.path.isdir(os.path.join(third_job_path, char_folder)):
                    char_path = os.path.join(third_job_path, char_folder)
                    palettes = []
                    for file in os.listdir(char_path):
                        if file.lower().endswith('.pal'):
                            # Validate the palette file before adding it
                            palette_path = os.path.join(char_path, file)
                            try:
                                with open(palette_path, "rb") as f:
                                    data = f.read()
                                
                                if len(data) != PALETTE_SIZE * 3:
                                    print(f"CONSOLE ERROR MSG: Invalid 3rd job palette file {file} - incorrect size: {len(data)} bytes")
                                    continue
                                
                                # Validate that all bytes are valid (0-255)
                                for i in range(PALETTE_SIZE * 3):
                                    if not (0 <= data[i] <= 255):
                                        print(f"CONSOLE ERROR MSG: Invalid 3rd job palette file {file} - invalid byte at position {i}")
                                        continue
                                
                                palettes.append(palette_path)
                                
                            except Exception as e:
                                print(f"CONSOLE ERROR MSG: Failed to load 3rd job palette {file}: {e}")
                                continue
                    if palettes:
                        self.third_job_palettes[char_folder] = sorted(palettes)
        
        # Get unique jobs from available characters
        jobs = set()
        for char_id in self.available_characters:
            if char_id in CHARACTER_MAPPING:
                jobs.add(CHARACTER_MAPPING[char_id]["job"])
        self.available_jobs = sorted(list(jobs))
        
        # Print summary of loaded data
    def refresh_data(self):
        """Reloads assets from disk (rawbmps, pals, custom_fashion_pals, 3rd job) and rebuilds the UI without restarting."""
        try:
            # Save current selections & state
            prev_char_name = self.character_var.get() if hasattr(self, "character_var") else None
            prev_job_name = self.job_var.get() if hasattr(self, "job_var") else None
            prev_image_index = getattr(self, "current_image_index", 0)
            prev_preview = self.preview_var.get() if hasattr(self, "preview_var") else "single"
            prev_zoom = self.zoom_var.get() if hasattr(self, "zoom_var") else "100%"
            prev_custom_count = getattr(self, "custom_frame_count", 3)
            prev_custom_start = getattr(self, "custom_start_index", 0)

            saved_hair = self.hair_var.get() if hasattr(self, "hair_var") else "NONE"
            saved_third = self.third_job_var.get() if hasattr(self, "third_job_var") else "NONE"
            saved_fashion = {}
            if hasattr(self, "fashion_vars") and isinstance(self.fashion_vars, dict):
                for k, var in self.fashion_vars.items():
                    try:
                        saved_fashion[k] = var.get()
                    except Exception:
                        pass

            # Reset in-memory databases
            self.available_characters = []
            self.available_jobs = []
            self.character_images = {}
            self.fashion_palettes = {}
            self.hair_palettes = {}
            self.third_job_palettes = {}
            self.fashion_vars = {}

            # Reload from disk
            self.load_all_data()

            # Helper to see if a character+job still exists
            def find_char_id_by_name_job(name, job):
                for cid in self.available_characters:
                    if cid in CHARACTER_MAPPING:
                        info = CHARACTER_MAPPING[cid]
                        if info.get("name") == name and info.get("job") == job:
                            return cid
                return None

            # Restore character/job if possible
            target_char_id = None
            if prev_char_name and prev_job_name:
                target_char_id = find_char_id_by_name_job(prev_char_name, prev_job_name)
            if target_char_id is None and self.available_characters:
                target_char_id = self.available_characters[0]

            # Apply restored selection
            if target_char_id:
                # Set UI vars
                if target_char_id in CHARACTER_MAPPING:
                    self.character_var.set(CHARACTER_MAPPING[target_char_id]["name"])
                    self.job_var.set(CHARACTER_MAPPING[target_char_id]["job"])
                else:
                    self.character_var.set(target_char_id)
                # Build sections + palettes
                self.on_job_change()

                # Try to restore prior palette choices if still present
                try:
                    if saved_third and saved_third != "NONE" and os.path.exists(saved_third):
                        self.third_job_var.set(saved_third)
                except Exception:
                    pass

                try:
                    if saved_hair and saved_hair != "NONE" and os.path.exists(saved_hair):
                        self.hair_var.set(saved_hair)
                except Exception:
                    pass

                # Fashion per-type
                for k, v in saved_fashion.items():
                    if k in self.fashion_vars:
                        try:
                            if v == "NONE" or os.path.exists(v):
                                self.fashion_vars[k].set(v)
                        except Exception:
                            pass

                # Reload layers & image
                self.load_palettes()

                # Restore image index if valid
                if target_char_id in self.character_images:
                    imgs = self.character_images[target_char_id]
                    if imgs:
                        if 0 <= prev_image_index < len(imgs):
                            self.current_image_index = prev_image_index
                        else:
                            self.current_image_index = 0
                        self.load_character_image()

            # Restore preview/zoom/custom state
            try:
                self.preview_var.set(prev_preview)
            except Exception:
                pass
            try:
                self.zoom_var.set(prev_zoom)
            except Exception:
                pass
            self.custom_frame_count = prev_custom_count
            self.custom_start_index = prev_custom_start

            # Refresh display/controls
            self.update_zoom_combo_state()
            self.update_image_display()

            try:
                messagebox.showinfo("Refresh", "Assets reloaded. New palettes and images are now available.")
            except Exception:
                pass

        except Exception as e:
            try:
                messagebox.showerror("Refresh", f"Failed to refresh assets:\\n{e}")
            except Exception:
                pass


    def register_focusable(self, widget, tag=None):
        """Register a widget as focusable and store its tag for quick access"""
        self.focusable_widgets.append(widget)
        if tag:
            if not hasattr(self, 'widget_tags'):
                self.widget_tags = {}
            self.widget_tags[tag] = widget
    
    def navigate_widgets(self, direction):
        """Handle up/down arrow key navigation"""
        current = self.master.focus_get()
        if current in self.focusable_widgets:
            current_idx = self.focusable_widgets.index(current)
            if direction == "up":
                next_idx = (current_idx - 1) % len(self.focusable_widgets)
            else:  # down
                next_idx = (current_idx + 1) % len(self.focusable_widgets)
            self.focusable_widgets[next_idx].focus_set()
    
    def handle_enter(self):
        """Handle Enter key press for selection"""
        current = self.master.focus_get()
        if current:
            if isinstance(current, (tk.Radiobutton, tk.Checkbutton)):
                current.invoke()  # Simulate click
            elif isinstance(current, tk.Button):
                current.invoke()  # Simulate button click
    
    def toggle_view_mode(self):
        """Toggle between single and custom view modes"""
        current_mode = self.preview_var.get()
        if current_mode == "single":
            self.preview_var.set("custom")
        elif current_mode == "custom":
            self.preview_var.set("single")
        self.on_preview_mode_change()
    
    
    def create_ui(self):
        """Create the main UI"""
        # List to store focusable widgets in order
        self.focusable_widgets = []
        self.widget_tags = {}
        
        
        # Bind keyboard shortcuts
        self.master.bind("b", lambda e: self.pick_background_color())
        self.master.bind("e", lambda e: self.export_background_bmp())
        self.master.bind("E", lambda e: self.export_all_frames())  # Shift+E
        self.master.bind("p", lambda e: self.open_live_palette_editor())
        self.master.bind("P", lambda e: self.export_pal())  # Shift+P
        self.master.bind("r", lambda e: self.reset_to_original())
        self.master.bind("d", lambda e: self.debug_info())
        self.master.bind("v", lambda e: self.toggle_view_mode())
        self.master.bind("o", lambda e: self.open_custom_settings())
        
        
        # Set window size and make it resizable
        self.master.geometry("900x650")
        self.master.resizable(True, True)
        self.master.minsize(900, 650)
        
        # Center the window on screen
        self._center_window()
        
        # Main frame
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top section - Character and Job selection
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Character selection
        tk.Label(top_frame, text="Character:").pack(side="left")
        
        # Create unique character names (without job info)
        character_names = []
        # Sort characters numerically by their number
        def sort_char_key(char_id):
            # Extract the number from chr### format
            match = re.match(r'chr(\d+)', char_id)
            if match:
                return int(match.group(1))
            return 0
        
        for char_id in sorted(self.available_characters, key=sort_char_key):
            if char_id in CHARACTER_MAPPING:
                char_info = CHARACTER_MAPPING[char_id]
                if char_info['name'] not in character_names:
                    character_names.append(char_info['name'])
            else:
                if char_id not in character_names:
                    character_names.append(char_id)
        
        self.character_combo = ttk.Combobox(top_frame, textvariable=self.character_var, 
                                          values=character_names, state="readonly", width=15)
        self.character_combo.pack(side="left", padx=(5, 10))
        self.character_combo.bind("<<ComboboxSelected>>", lambda e: self.on_character_change())
        
        # Job selection
        tk.Label(top_frame, text="Job:").pack(side="left")
        self.job_combo = ttk.Combobox(top_frame, textvariable=self.job_var, 
                                    values=self.available_jobs, state="readonly", width=15)
        self.job_combo.pack(side="left", padx=(5, 10))
        self.job_combo.bind("<<ComboboxSelected>>", lambda e: self.on_job_change())
        
        # Zoom selection
        tk.Label(top_frame, text="Zoom:").pack(side="left")

        # Refresh assets (placed between Zoom and Preview)

        self.zoom_combo = ttk.Combobox(top_frame, textvariable=self.zoom_var, 
                                     values=["100%", "200%", "300%", "400%", "500%", "Fit"], state="readonly", width=10)
        self.zoom_combo.pack(side="left", padx=(5, 10))
        # Refresh assets (between Zoom dropdown and Preview)
        self.refresh_btn = tk.Button(top_frame, text="Refresh", command=self.refresh_data)
        try:
            self.refresh_btn.pack(in_=top_frame, side="left", padx=(6, 6), after=self.zoom_combo)
        except Exception:
            self.refresh_btn.pack(side="left", padx=(6, 6))
        self.zoom_combo.bind("<<ComboboxSelected>>", lambda e: self.on_zoom_change())
        
        # Create a spacer frame to push preview section to the right
        spacer_frame = tk.Frame(top_frame)
        spacer_frame.pack(side="left", fill="x", expand=True)
        
        # Preview mode selection (right side)
        preview_frame = tk.Frame(top_frame)
        preview_frame.pack(side="right", padx=(0, 10))
        
        tk.Label(preview_frame, text="Preview:").pack(side="left")
        # Use saved preview mode from settings
        initial_preview_mode = getattr(self, 'last_preview_mode', 'single')
        self.preview_var = tk.StringVar(value=initial_preview_mode)
        tk.Radiobutton(preview_frame, text="Single", variable=self.preview_var, 
                      value="single", command=self.on_preview_mode_change).pack(side="left", padx=(5, 0))
        tk.Radiobutton(preview_frame, text="All", variable=self.preview_var, 
                      value="all", command=self.on_preview_mode_change).pack(side="left", padx=(5, 0))
        
        # Custom preview option with gear button
        custom_frame = tk.Frame(preview_frame)
        custom_frame.pack(side="left", padx=(5, 0))
        
        self.custom_var = tk.StringVar(value="custom")
        custom_radio = tk.Radiobutton(custom_frame, text="Custom", variable=self.preview_var, 
                                     value="custom", command=self.on_preview_mode_change)
        custom_radio.pack(side="left")
        
        # Gear button for custom settings
        self.gear_button = tk.Button(custom_frame, text="⚙", font=("Arial", 10), 
                                   command=self.open_custom_settings, width=2, height=1)
        self.gear_button.pack(side="left", padx=(2, 0))
        
        # Main content area with image on left, controls on right
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Image display area (left side)
        img_frame = tk.Frame(content_frame)
        img_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Scrollable canvas for image with both vertical and horizontal scrollbars
        # Create frame for scrollbars with border to ensure clipping
        scroll_frame = tk.Frame(img_frame, relief="solid", bd=1)
        scroll_frame.pack(fill="both", expand=True)
        
        # Vertical scrollbar only
        self.v_scroll = Scrollbar(scroll_frame, orient="vertical")
        self.v_scroll.pack(side="right", fill="y")
        
        # Canvas with vertical scrollbar only - constrained to container
        self.canvas = Canvas(scroll_frame, 
                           yscrollcommand=self.v_scroll.set,
                           highlightthickness=0,
                           bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Configure scrollbar
        self.v_scroll.config(command=self.canvas.yview)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Add mouse wheel support
        def _on_mousewheel(event):
            if event.state & 0x4:  # Check if Control is pressed
                return  # Don't scroll if Control is pressed (let it handle zoom)
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        self.canvas.bind("<MouseWheel>", _on_mousewheel)  # Windows
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Linux
        
        self.img_id = None
        self.tk_image = None
        
        # Control panel (right side)
        control_frame = tk.Frame(content_frame)
        control_frame.pack(side="right", fill="y", padx=(10, 0))
        
        # Create PanedWindow for resizable sections (hair and fashion only)
        self.paned = tk.PanedWindow(control_frame, orient="vertical", sashwidth=4, sashrelief="raised")
        self.paned.pack(fill="both", expand=True)
        # Set initial sash position
        self.paned.after_idle(lambda: self.paned.sash_place(0, 0, 120))
        
        # 3rd Job Base Fashion section (only for 3rd jobs) - static section below PanedWindow
        self.third_job_frame = tk.LabelFrame(control_frame, text="3rd Job Base Fashion")
        # Initially hidden, will be shown when needed
        self.third_job_frame.configure(width=300)
        
        # Hair section
        self.hair_frame = tk.LabelFrame(self.paned, text="Hair")
        self.hair_frame.configure(width=300)
        self.paned.add(self.hair_frame)

        
        # Create scrollable frame for hair palettes - force very small height
        self.hair_canvas = tk.Canvas(self.hair_frame, height=10)
        self.hair_scrollbar = tk.Scrollbar(self.hair_frame, orient="vertical", command=self.hair_canvas.yview)
        self.hair_scrollable_frame = tk.Frame(self.hair_canvas)
        
        # Configure hair canvas
        self.hair_canvas.configure(yscrollcommand=self.hair_scrollbar.set)
        
        # Update scroll region when frame size changes
        def update_hair_scroll_region(event):
            self.hair_canvas.configure(scrollregion=self.hair_canvas.bbox("all"))
        self.hair_scrollable_frame.bind("<Configure>", update_hair_scroll_region)
        
        # Create window in canvas
        self.hair_canvas.create_window((0, 0), window=self.hair_scrollable_frame, anchor="nw")
        
        # Add mouse wheel support for hair palette
        def _on_hair_mousewheel(event):
            if event.state & 0x4:  # Check if Control is pressed
                return  # Don't scroll if Control is pressed
            # Get the scrollbar position info
            first, last = self.hair_scrollbar.get()
            if first != 0.0 or last != 1.0:  # Only scroll if scrollbar is active
                self.hair_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        # Bind scroll events to both canvas and frame to ensure it works everywhere in the hair section
        self.hair_canvas.bind("<MouseWheel>", _on_hair_mousewheel)
        self.hair_scrollable_frame.bind("<MouseWheel>", _on_hair_mousewheel)
        def _on_hair_linux_scroll(direction):
            first, last = self.hair_scrollbar.get()
            if first != 0.0 or last != 1.0:  # Only scroll if scrollbar is active
                self.hair_canvas.yview_scroll(direction, "units")
        # Bind Linux scroll events to both canvas and frame
        for widget in (self.hair_canvas, self.hair_scrollable_frame):
            widget.bind("<Button-4>", lambda e: _on_hair_linux_scroll(-1))
            widget.bind("<Button-5>", lambda e: _on_hair_linux_scroll(1))
        
        # Pack hair canvas and scrollbar
        self.hair_canvas.pack(side="left", fill="both", expand=True)
        self.hair_scrollbar.pack(side="right", fill="y")
        
        # Fashion section with scrollbar
        self.fashion_frame = tk.LabelFrame(self.paned, text="Fashion")
        self.fashion_frame.configure(height=360, width=300)
        self.paned.add(self.fashion_frame)
        
        # Create scrollable frame for fashion palettes - reduced height
        self.fashion_canvas = tk.Canvas(self.fashion_frame, height=360, width=300)
        self.fashion_scrollbar = tk.Scrollbar(self.fashion_frame, orient="vertical", command=self.fashion_canvas.yview)
        self.fashion_scrollable_frame = tk.Frame(self.fashion_canvas)
        
        def update_scroll_region(event):
            self.fashion_canvas.configure(scrollregion=self.fashion_canvas.bbox("all"))
        
        self.fashion_scrollable_frame.bind("<Configure>", update_scroll_region)
        
        self.fashion_canvas.create_window((0, 0), window=self.fashion_scrollable_frame, anchor="nw")
        self.fashion_canvas.configure(yscrollcommand=self.fashion_scrollbar.set)
        
        # Add mouse wheel support for fashion palette
        def _on_fashion_mousewheel(event):
            if event.state & 0x4:  # Check if Control is pressed
                return  # Don't scroll if Control is pressed
            # Get the scrollbar position info
            first, last = self.fashion_scrollbar.get()
            if first != 0.0 or last != 1.0:  # Only scroll if scrollbar is active
                self.fashion_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        # Bind scroll events to both canvas and frame to ensure it works everywhere in the fashion section
        self.fashion_canvas.bind("<MouseWheel>", _on_fashion_mousewheel)
        self.fashion_scrollable_frame.bind("<MouseWheel>", _on_fashion_mousewheel)
        def _on_fashion_linux_scroll(direction):
            first, last = self.fashion_scrollbar.get()
            if first != 0.0 or last != 1.0:  # Only scroll if scrollbar is active
                self.fashion_canvas.yview_scroll(direction, "units")
        # Bind Linux scroll events to both canvas and frame
        for widget in (self.fashion_canvas, self.fashion_scrollable_frame):
            widget.bind("<Button-4>", lambda e: _on_fashion_linux_scroll(-1))
            widget.bind("<Button-5>", lambda e: _on_fashion_linux_scroll(1))
        
        self.fashion_canvas.pack(side="left", fill="both", expand=True)
        self.fashion_scrollbar.pack(side="right", fill="y")

        # Control buttons at the bottom
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        # Navigation buttons
        nav_frame = tk.Frame(button_frame)
        nav_frame.pack(side="left", padx=(0, 10))
        
        self.prev_btn = tk.Button(nav_frame, text="◀", command=self.prev_image, width=3)
        self.prev_btn.pack(side="left", padx=(0, 2))
        
        self.next_btn = tk.Button(nav_frame, text="▶", command=self.next_image, width=3)
        self.next_btn.pack(side="left")
        
        # Other buttons
        self.export_button = tk.Button(button_frame, text="Export Transparent PNG", command=self.export_transparent_png)
        self.export_button.pack(side="left", padx=(0, 5))
        # Initial button state based on export format
        self.update_export_button_text()
        self.export_all_frames_button = tk.Button(button_frame, text="Export All Frames", command=self.export_all_frames)
        self.export_all_frames_button.pack_forget()  # Hidden by default
        self.export_palette_button = tk.Button(button_frame, text="Export Palette", command=self.export_pal)
        self.export_palette_button.pack_forget()  # Hidden by default
        self.live_edit_button = tk.Button(button_frame, text="Live Edit Palette", command=self.open_live_palette_editor)
        self.live_edit_button.pack(side="left", padx=(0, 5))
        self.icon_editor_button = tk.Button(button_frame, text="Icon Editor", command=self._open_icon_editor)
        self.icon_editor_button.pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Reset to Original", command=self.reset_to_original).pack(side="left", padx=(0, 5))
        self.debug_info_button = tk.Button(button_frame, text="Debug Info", command=self.debug_info)
        self.debug_info_button.pack_forget()  # Hidden by default
        self.statistics_button = tk.Button(button_frame, text="Statistics", command=self.show_statistics)
        self.statistics_button.pack(side="left", padx=(0, 5))
        
        # Background color picker (right side of button bar)
        bg_color_frame = tk.Frame(button_frame)
        bg_color_frame.pack(side="right", padx=(5, 0))
        
        tk.Label(bg_color_frame, text="BG:").pack(side="left")
        self.bg_color_button = tk.Button(bg_color_frame, text="🎨", font=("Arial", 12), 
                                        command=self.pick_background_color, width=3, height=1)
        self.bg_color_button.pack(side="left", padx=(2, 0))
        
        # Initialize background color (default white)
        self.background_color = (255, 255, 255)
        # Set initial button color
        self.bg_color_button.configure(bg="#FFFFFF")
        
        # Bind arrow keys for image navigation
        self.master.bind("<Left>", lambda e: self.prev_image())
        self.master.bind("<Right>", lambda e: self.next_image())

    def on_character_change(self):
        """Handle character selection change"""
        character_name = self.character_var.get()
        if not character_name:
            return
            
        # Find the first character ID for this character name
        char_id = None
        for char_id_key in self.available_characters:
            if char_id_key in CHARACTER_MAPPING:
                char_info = CHARACTER_MAPPING[char_id_key]
                if char_info['name'] == character_name:
                    char_id = char_id_key
                    break
            else:
                if char_id_key == character_name:
                    char_id = char_id_key
                    break
                    
        # Reset custom frame settings when changing character
        if hasattr(self, 'current_character') and self.current_character != char_id:
            # Save per-character settings before switching
            if self.current_character:
                self._save_character_settings(self.current_character)
            
            # Store current settings before changing
            if self.preview_var.get() == "custom" and hasattr(self, 'custom_frame_count'):
                current_job = self.job_var.get() if hasattr(self, 'job_var') else None
                if self.current_character not in self.frame_range_settings:
                    self.frame_range_settings[self.current_character] = {}
                self.frame_range_settings[self.current_character][current_job] = (
                    self.custom_frame_count,
                    getattr(self, 'custom_start_frame', 0),
                    getattr(self, 'custom_end_frame', len(self.character_images.get(self.current_character, [])) - 1)
                )
        
        if char_id and char_id in CHARACTER_MAPPING:
            char_info = CHARACTER_MAPPING[char_id]
            self.current_character = char_id
            self.current_job = char_info["job"]
            self.job_var.set(self.current_job)
            
            # Load per-character settings for this character
            self._load_character_settings(char_id)
            
            # Track character view
            self.statistics.add_character_view(char_id, char_info["job"])
            self._save_statistics()
            
            # Clear current image display first (only if canvas exists)
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                self.canvas.delete("all")
            self.original_image = None
            self.current_image_path = None
            
            # Clear fashion variables before updating UI
            self.fashion_vars.clear()
            
            # Reset palette selections
            self.hair_var.set("NONE")
            self.third_job_var.set("NONE")
            
            # Clear palette layers
            self.palette_layers = []
            
            # Update all UI sections
            self.update_third_job_section()
            self.update_hair_section()
            self.update_fashion_section()
            
            # Reset scroll positions
            self.reset_scroll_positions()
            
            # Load palettes and update display immediately for all characters
            self.load_palettes()
            # Update zoom combo state based on new character's frame count
            self.update_zoom_combo_state()
            self.update_image_display()
            
            # Load first image for this character
            if char_id in self.character_images and self.character_images[char_id]:
                self.current_image_index = 0
                self.load_character_image()
                self.update_navigation_buttons()
            
            # Ensure zoom state is updated after character change
            self.update_zoom_combo_state()

    def prev_image(self):
        """Navigate to previous image"""
        preview_mode = self.preview_var.get()
        
        # Don't allow navigation in "all" mode
        if preview_mode == "all":
            return
        
        if preview_mode == "custom":
            self.prev_custom_frames()
        else:
            if not hasattr(self, 'current_character') or not self.current_character:
                return
                
            char_id = self.current_character
            if char_id not in self.character_images:
                return
                
            images = self.character_images[char_id]
            if len(images) <= 1:
                return
                
            # Wrap around to the last image when at the beginning
            if self.current_image_index > 0:
                self.current_image_index = self.current_image_index - 1
            else:
                self.current_image_index = len(images) - 1
                
            self.load_image_from_path(images[self.current_image_index])
            self.update_navigation_buttons()
            
            # Save current frame position
            self._save_settings()
    
    def prev_custom_frames(self):
        """Navigate to previous set of custom frames"""
        if not hasattr(self, 'current_character') or not self.current_character:
            return
            
        char_id = self.current_character
        if char_id not in self.character_images:
            return
            
        images = self.character_images[char_id]
        max_frames = len(images)
        
        # Get current job
        current_job = self.job_var.get() if hasattr(self, 'job_var') else None
        
        # Get stored settings for this character/job combination
        char_settings = self.frame_range_settings.get(self.current_character, {})
        job_settings = char_settings.get(current_job, None)
        
        if job_settings:
            frame_count, start_frame, end_frame = job_settings
            # Move backward by custom_frame_count frames within the range
            self.custom_start_index -= self.custom_frame_count
            
            # Wrap around within the selected range
            if self.custom_start_index < start_frame:
                # Go to the last complete set of frames within the range
                last_set_start = end_frame - ((end_frame - start_frame) % self.custom_frame_count)
                self.custom_start_index = last_set_start
        else:
            # Move back by custom_frame_count frames
            self.custom_start_index -= self.custom_frame_count
            
            # Wrap around if we go below 0
            if self.custom_start_index < 0:
                # Calculate how many frames we can show from the end
                remaining_frames = abs(self.custom_start_index)
                self.custom_start_index = max(0, max_frames - remaining_frames)
        
        # Update zoom combo state after custom frame navigation
        self.update_zoom_combo_state()
        self.update_image_display()

    def next_image(self):
        """Navigate to next image"""
        preview_mode = self.preview_var.get()
        
        # Don't allow navigation in "all" mode
        if preview_mode == "all":
            return
        
        if preview_mode == "custom":
            self.next_custom_frames()
            # Track frame navigation
            self.statistics.frames_skipped += 1
            self._save_statistics()
        else:
            if not hasattr(self, 'current_character') or not self.current_character:
                return
                
            char_id = self.current_character
            if char_id not in self.character_images:
                return
                
            images = self.character_images[char_id]
            if len(images) <= 1:
                return
                
            # Wrap around to the first image when at the end
            if self.current_image_index < len(images) - 1:
                self.current_image_index = self.current_image_index + 1
            else:
                self.current_image_index = 0
                
            self.load_image_from_path(images[self.current_image_index])
            self.update_navigation_buttons()
            # Track frame navigation
            self.statistics.frames_skipped += 1
            self._save_statistics()
            
            # Save current frame position
            self._save_settings()
    
    def next_custom_frames(self):
        """Navigate to next set of custom frames"""
        if not hasattr(self, 'current_character') or not self.current_character:
            return
            
        char_id = self.current_character
        if char_id not in self.character_images:
            return
            
        images = self.character_images[char_id]
        max_frames = len(images)
        
        # Get current job
        current_job = self.job_var.get() if hasattr(self, 'job_var') else None
        
        # Get stored settings for this character/job combination
        char_settings = self.frame_range_settings.get(self.current_character, {})
        job_settings = char_settings.get(current_job, None)
        
        if job_settings:
            frame_count, start_frame, end_frame = job_settings
            # Move forward by custom_frame_count frames within the range
            self.custom_start_index += self.custom_frame_count
            
            # Wrap around within the selected range
            if self.custom_start_index > end_frame:
                self.custom_start_index = start_frame
        else:
            # Move forward by custom_frame_count frames
            self.custom_start_index += self.custom_frame_count
            
            # Wrap around if we exceed the total number of frames
            if self.custom_start_index >= max_frames:
                self.custom_start_index = 0
        
        # Update zoom combo state after custom frame navigation
        self.update_zoom_combo_state()
        self.update_image_display()

    def update_navigation_buttons(self):
        """Update the state of image navigation buttons"""
        preview_mode = self.preview_var.get()
        
        # Disable navigation buttons in "all" mode
        if preview_mode == "all":
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            return
        
        if not hasattr(self, 'current_character') or not self.current_character:
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            return
            
        char_id = self.current_character
        if char_id not in self.character_images:
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            return
            
        images = self.character_images[char_id]
        
        if preview_mode == "custom":
            # For custom mode, always enable navigation if we have frames
            if len(images) > 0:
                self.prev_btn.config(state="normal")
                self.next_btn.config(state="normal")
            else:
                self.prev_btn.config(state="disabled")
                self.next_btn.config(state="disabled")
        else:
            # For single mode, enable if we have more than one image
            if len(images) > 1:
                # Always enable navigation buttons since we have wrap-around
                self.prev_btn.config(state="normal")
                self.next_btn.config(state="normal")
            else:
                self.prev_btn.config(state="disabled")
                self.next_btn.config(state="disabled")

    def on_job_change(self):
        """Handle job selection change"""
        character_name = self.character_var.get()
        job_name = self.job_var.get()
        
        if not character_name or not job_name:
            return
            
        # Find the character ID for this character name and job
        char_id = None
        
        # Store current frame settings before job change
        if hasattr(self, 'current_character') and self.preview_var.get() == "custom" and hasattr(self, 'custom_frame_count'):
            old_job = getattr(self, 'current_job', None)
            if old_job and old_job != job_name:
                if self.current_character not in self.frame_range_settings:
                    self.frame_range_settings[self.current_character] = {}
                self.frame_range_settings[self.current_character][old_job] = (
                    self.custom_frame_count,
                    getattr(self, 'custom_start_frame', 0),
                    getattr(self, 'custom_end_frame', len(self.character_images.get(self.current_character, [])) - 1)
                )
        
        # For Paula, map job to correct character IDs
        if character_name == "Paula":
            if job_name == "1st Job":
                # Use chr025 for images, chr100 for palettes
                if "chr025" in self.available_characters:
                    char_id = "chr025"
                elif "chr100" in self.available_characters:
                    char_id = "chr100"
            elif job_name == "2nd Job":
                # Use chr026 for images, chr101 for palettes
                if "chr026" in self.available_characters:
                    char_id = "chr026"
                elif "chr101" in self.available_characters:
                    char_id = "chr101"
            elif job_name == "3rd Job":
                # Use chr027 for images, chr102 for palettes
                if "chr027" in self.available_characters:
                    char_id = "chr027"
                elif "chr102" in self.available_characters:
                    char_id = "chr102"
        else:
            # For other characters, use the original logic
            for char_id_key in self.available_characters:
                if char_id_key in CHARACTER_MAPPING:
                    char_info = CHARACTER_MAPPING[char_id_key]
                    if char_info['name'] == character_name and char_info['job'] == job_name:
                        char_id = char_id_key
                        break
        
        if char_id and char_id in CHARACTER_MAPPING:
            self.current_character = char_id
            self.current_job = job_name
            
            # Load per-character settings for this character
            self._load_character_settings(char_id)
            
            # Clear current image display first
            self.canvas.delete("all")
            self.original_image = None
            self.current_image_path = None
            
            # Clear fashion variables before updating UI
            self.fashion_vars.clear()
            
            # Reset palette selections
            self.hair_var.set("NONE")
            self.third_job_var.set("NONE")
            
            # Clear palette layers
            self.palette_layers = []
            
            # Update all UI sections
            self.update_third_job_section()
            self.update_hair_section()
            self.update_fashion_section()
            
            # Reset scroll positions
            self.reset_scroll_positions()
            
            # Load palettes and update display immediately for 3rd job characters
            self.load_palettes()
            # Update zoom combo state based on new character's frame count
            self.update_zoom_combo_state()
            self.update_image_display()
            
            # Load first image for this character
            if char_id in self.character_images and self.character_images[char_id]:
                self.current_image_index = 0
                self.load_character_image()
            
            # Update navigation buttons after job change (always, not just when loading image)
            self.update_navigation_buttons()
            
            # Ensure zoom state is updated after job change
            self.update_zoom_combo_state()

    def update_third_job_section(self):
        """Update the 3rd Job Base Fashion section"""
        # Clear existing widgets
        for widget in self.third_job_frame.winfo_children():
            widget.destroy()
        
        # Hide the third job frame initially
        self.third_job_frame.pack_forget()
        
        if not hasattr(self, 'current_character') or not self.current_character:
            # Reset fashion frame to normal height when no third job
            self._adjust_layout_for_third_job(False)
            return
        
        char_id = self.current_character
        if char_id not in CHARACTER_MAPPING:
            return
        
        char_info = CHARACTER_MAPPING[char_id]
        
        # For 1st and 2nd jobs, hide the 3rd job section entirely
        if char_info["job"] in ["1st Job", "2nd Job"]:
            # Reset fashion frame to normal height when no third job
            self._adjust_layout_for_third_job(False)
            return
        else:
            # Show the 3rd job frame for 3rd jobs - pack it below the PanedWindow
            self.third_job_frame.pack(fill="x", pady=(5, 0))
            # Adjust layout to accommodate third job frame
            self._adjust_layout_for_third_job(True)
        
        # Special handling for Paula characters - they don't have 3rd job base fashion
        if char_id in ["chr025", "chr026", "chr027"]:
            tk.Label(self.third_job_frame, text="Silly, Paula doesn't have multiple 3rd jobs!", 
                    fg="red", font=("Arial", 9, "bold")).pack(anchor="w", padx=5, pady=5)
            return
        
        # Check if this character has 3rd job base fashion palettes
        palette_char_id = self.get_palette_character_id(char_id)
        if palette_char_id in self.third_job_palettes:
            palettes = self.third_job_palettes[palette_char_id]
            
            # Add palette options (no NONE option for 3rd jobs)
            for palette_path in palettes:
                palette_name = os.path.basename(palette_path)
                tk.Radiobutton(self.third_job_frame, text=palette_name, variable=self.third_job_var,
                              value=palette_path, command=self.on_third_job_change).pack(anchor="w", padx=2, pady=0)
            
            # Set default to first palette if available
            if palettes:
                self.third_job_var.set(palettes[0])
            else:
                self.third_job_var.set("NONE")

    def _adjust_layout_for_third_job(self, has_third_job):
        """Adjust the layout to accommodate the third job frame"""
        if has_third_job:
            # Reduce fashion frame height to make room for third job frame
            self.fashion_frame.configure(height=240)
            self.fashion_canvas.configure(height=240)
            # Keep the same minimum window size - just adjust the internal layout
            self.master.minsize(900, 650)
        else:
            # Restore normal fashion frame height
            self.fashion_frame.configure(height=360)
            self.fashion_canvas.configure(height=360)
            # Keep the same minimum window size
            self.master.minsize(900, 650)

    def get_palette_character_id(self, char_id):
        """Get the character ID to use for palettes (handles Paula mapping)"""
        if char_id == "chr025":
            return "chr100"  # Paula 1st Job: chr025 images -> chr100 palettes
        elif char_id == "chr026":
            return "chr101"  # Paula 2nd Job: chr026 images -> chr101 palettes
        elif char_id == "chr027":
            return "chr102"  # Paula 3rd Job: chr027 images -> chr102 palettes
        else:
            return char_id  # For other characters, use the same ID

    def get_fashion_type_name(self, char_id, fashion_type):
        """Get the proper name for a fashion type based on character"""
        # Map Paula's display IDs to their palette IDs
        if char_id == "chr025":
            char_id = "chr100"  # Paula 1st Job
        elif char_id == "chr026":
            char_id = "chr101"  # Paula 2nd Job
        elif char_id == "chr027":
            char_id = "chr102"  # Paula 3rd Job
            
        char_num = char_id[3:] if char_id.startswith("chr") else char_id
        
        # Fashion type mappings for different characters
        fashion_names = {
            "001": {  # chr001
                "fashion_1": "Hoodie",
                "fashion_2": "Gloves", 
                "fashion_3": "Skort",
                "fashion_4": "Backpack",
                "fashion_5": "Shoes"
            },
            "002": {  # chr002
                "fashion_1": "Airshoes",
                "fashion_2": "Turtle Vest",
                "fashion_3": "Sash Belt", 
                "fashion_4": "Warmups",
                "fashion_5": "Wraps",
                "fashion_6": "Hood Tie"
            },
            "004": {  # chr004
                "fashion_1": "Robe",
                "fashion_2": "Shirt",
                "fashion_3": "Jeans",
                "fashion_4": "Monk Shoes", 
                "fashion_5": "Cane"
            },
            "005": {  # chr005
                "fashion_1": "Coat",
                "fashion_2": "Heels",
                "fashion_3": "Slit Skirt",
                "fashion_4": "Tank",
                "fashion_5": "Tote"
            },
            "006": {  # chr006
                "fashion_1": "Jacket",
                "fashion_2": "Shorts",
                "fashion_3": "Trainers",
                "fashion_4": "Open Glove",
                "fashion_5": "T-neck"
            },
            "007": {  # chr007
                "fashion_1": "Ribbon",
                "fashion_2": "Belt",
                "fashion_3": "Halter",
                "fashion_4": "Heels",
                "fashion_5": "Paws",
                "fashion_6": "Skirt"
            },
            "008": {  # chr008
                "fashion_1": "Blazer",
                "fashion_2": "Slacks",
                "fashion_3": "Dress Shoes"
            },
            "009": {  # chr009
                "fashion_1": "Robe",
                "fashion_2": "Boxing Glove",
                "fashion_3": "Shorts",
                "fashion_4": "Gloves",
                "fashion_5": "Boxing Shoes",
                "fashion_6": "Stocking"
            },
            "010": {  # chr010
                "fashion_1": "Fur Collar",
                "fashion_2": "Tunic",
                "fashion_3": "Bolero",
                "fashion_4": "Gauntlet",
                "fashion_5": "Leather Shoes"
            },
            "012": {  # chr012
                "fashion_1": "Shawl",
                "fashion_2": "Beads Necklace",
                "fashion_3": "Robe",
                "fashion_4": "Wrap Skirt",
                "fashion_5": "Ankle Boots"
            },
            "013": {  # chr013
                "fashion_1": "Sports Suit",
                "fashion_2": "Tube Top",
                "fashion_3": "Elbow Wrap",
                "fashion_4": "Mittens",
                "fashion_5": "Walkers"
            },
            "014": {  # chr014
                "fashion_1": "Turtleneck",
                "fashion_2": "Coil Coat",
                "fashion_3": "Utility Belt",
                "fashion_4": "Glove",
                "fashion_5": "Boots"
            },
            "015": {  # chr015
                "fashion_1": "Hippie Shirt",
                "fashion_2": "Studded Belt",
                "fashion_3": "Checkered Skirt",
                "fashion_4": "Checkered Stockings",
                "fashion_5": "Heel Boots"
            },
            "016": {  # chr016
                "fashion_1": "Dress Shirt",
                "fashion_2": "Checkered Suit",
                "fashion_3": "Dress Shoes"
            },
            "100": {  # chr100 (Paula 1st Job)
                "fashion_1": "Stadium Jacket",
                "fashion_2": "Sleeveless Dress",
                "fashion_3": "Knee Socks",
                "fashion_4": "School Loafers",
                "fashion_5": "Ribbon Chou",
                "fashion_6": "Cutie Satchel",
                "fashion_7": "Extra"
            },
            "101": {  # chr101 (Paula 2nd Job)
                "fashion_1": "Pocket One-piece",
                "fashion_2": "Animal Pocket Belt",
                "fashion_3": "Knee-high Boots",
                "fashion_4": "Ribbons",
                "fashion_5": "Arm Cover",
                "fashion_6": "Whip"
            },
            "102": {  # chr102 (Paula 3rd Job)
                "fashion_1": "Blouse",
                "fashion_2": "Trench Dress",
                "fashion_3": "Frilly Socks",
                "fashion_4": "Cutie Buckle Boots",
                "fashion_5": "Ribbon Rubber",
                "fashion_6": "Ribbon Brooch",
                "fashion_7": "Mini Pocket Belt",
                "fashion_8": "Leather Buckle Gloves"
            },
            "003": {  # chr003
                "fashion_1": "Blouse",
                "fashion_2": "Bow",
                "fashion_3": "Frill Dress",
                "fashion_4": "Flats",
                "fashion_5": "Socks",
                "fashion_6": "Spellbook"
            },
            "020": {  # chr020
                "fashion_1": "Wrap",
                "fashion_2": "Hooded Robe",
                "fashion_3": "Overcoat",
                "fashion_4": "Robe",
                "fashion_5": "Leather Boots"
            },
            "017": {  # chr017
                "fashion_1": "Tube Top",
                "fashion_2": "Bolero Jacket",
                "fashion_3": "Gauntlets",
                "fashion_4": "Chord Skirt",
                "fashion_5": "Steel Boots"
            },
            "018": {  # chr018
                "fashion_1": "Asymmetrical Tee",
                "fashion_2": "Protector",
                "fashion_3": "Kilt",
                "fashion_4": "Steel Armlets",
                "fashion_5": "Ankle Shoes"
            },
            "011": {  # chr011
                "fashion_1": "Checkered Dress",
                "fashion_2": "Ribbon",
                "fashion_3": "Minisack",
                "fashion_4": "Gloves",
                "fashion_5": "Ribbon Boots"
            },
            "019": {  # chr019
                "fashion_1": "Flower Ribbon",
                "fashion_2": "Puffy Blouse",
                "fashion_3": "Flower Brooch",
                "fashion_4": "Layered Dress",
                "fashion_5": "Flower Shoes"
            },
            "021": {  # chr021
                "fashion_1": "Zip-up Coat",
                "fashion_2": "Leather Shorts",
                "fashion_3": "Leather Wristlets",
                "fashion_4": "Buckle Boots",
                "fashion_5": "Unknown"
            },
            "022": {  # chr022
                "fashion_1": "Zip-up Jacket",
                "fashion_2": "Long Jacket",
                "fashion_3": "Shorts",
                "fashion_4": "Long Boots",
                "fashion_5": "Unknown"
            },
            "023": {  # chr023
                "fashion_1": "Double Coat",
                "fashion_2": "Shirring Skirt",
                "fashion_3": "Buckle Shoes",
                "fashion_4": "Blouse"
            },
            "024": {  # chr024 (Raccoon 3rd Job)
                "fashion_1": "Dress Shirt",
                "fashion_2": "Opera Cape",
                "fashion_3": "Frock Coat",
                "fashion_4": "Dress Pants",
                "fashion_5": "Full Suit",
                "fashion_6": "Formal Shoes"
            },
            "025": {  # chr025 (Paula 1st Job)
                "fashion_1": "Stadium Jacket",
                "fashion_2": "Sleeveless Dress",
                "fashion_3": "Knee Socks",
                "fashion_4": "School Loafers",
                "fashion_5": "Ribbon Chou",
                "fashion_6": "Cutie Satchel",
                "fashion_7": "Extra"
            },
            "026": {  # chr026 (Paula 2nd Job)
                "fashion_1": "Pocket One-piece",
                "fashion_2": "Animal Pocket Belt",
                "fashion_3": "Knee-high Boots",
                "fashion_4": "Ribbons",
                "fashion_5": "Arm Cover",
                "fashion_6": "Whip"
            },
            "027": {  # chr027 (Paula 3rd Job)
                "fashion_1": "Blouse",
                "fashion_2": "Trench Dress",
                "fashion_3": "Frilly Socks",
                "fashion_4": "Cutie Buckle Boots",
                "fashion_5": "Ribbon Rubber",
                "fashion_6": "Ribbon Brooch",
                "fashion_7": "Mini Pocket Belt",
                "fashion_8": "Leather Buckle Gloves",
                "fashion_8": "Special"
            }
        }
        
        if char_num in fashion_names and fashion_type in fashion_names[char_num]:
            return fashion_names[char_num][fashion_type]
        else:
            return fashion_type  # Return original if no mapping found

    def update_hair_section(self):
        """Update the Hair section"""
        # Clear existing widgets
        for widget in self.hair_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Clear any existing "NONE" option
        for widget in self.hair_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton) and widget.cget("text") == "NONE":
                widget.destroy()
        
        # Add "NONE" option outside the scrollable area
        rb = tk.Radiobutton(self.hair_frame, text="NONE", variable=self.hair_var,
                      value="NONE", command=self.on_hair_change)
        rb.configure(pady=0, bd=0, highlightthickness=0)  # Remove all padding and borders
        rb.pack(anchor="w", padx=3, pady=1, before=self.hair_canvas)
        
        if not hasattr(self, 'current_character') or not self.current_character:
            return
            
        char_id = self.current_character
        palette_char_id = self.get_palette_character_id(char_id)
        
        # Add hair palette options (limit to about 6 lines)
        if palette_char_id in self.hair_palettes:
            # Add hair palette options to the existing scrollable frame
            for palette_path in sorted(self.hair_palettes[palette_char_id]):
                palette_name = os.path.basename(palette_path)
                # Check if this is a custom palette (from custom_pals/hair or custom_pals/fashion)
                root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                custom_hair_pals_path = os.path.join(root_dir, "exports", "custom_pals", "hair")
                custom_fashion_pals_path = os.path.join(root_dir, "exports", "custom_pals", "fashion")
                # Also check old path for backward compatibility
                old_custom_fashion_pals_path = os.path.join(root_dir, "exports", "custom_fashion_pals")
                is_custom_hair = os.path.abspath(palette_path).startswith(os.path.abspath(custom_hair_pals_path))
                is_custom_fashion = os.path.abspath(palette_path).startswith(os.path.abspath(custom_fashion_pals_path))
                is_old_custom_fashion = os.path.abspath(palette_path).startswith(os.path.abspath(old_custom_fashion_pals_path))
                is_custom = is_custom_hair or is_custom_fashion or is_old_custom_fashion
                display_name = f"{palette_name} (C)" if is_custom else palette_name
                
                rb = tk.Radiobutton(self.hair_scrollable_frame, text=display_name, variable=self.hair_var,
                              value=palette_path, command=self.on_hair_change)
                rb.configure(pady=2)
                rb.pack(anchor="w", padx=3, pady=1)
                self.register_focusable(rb, f"hair_{palette_path}")
        
        # Set default to NONE
        self.hair_var.set("NONE")

    def update_fashion_section(self):
        """Update the Fashion section"""
        # Clear existing widgets
        for widget in self.fashion_scrollable_frame.winfo_children():
            widget.destroy()
        
        if not hasattr(self, 'current_character') or not self.current_character:
            return
            
        char_id = self.current_character
        palette_char_id = self.get_palette_character_id(char_id)
        
        # Add fashion palette options
        if palette_char_id in self.fashion_palettes:
            # Group palettes by their actual palette type based on hardcoded ranges
            fashion_groups = {}
            
            # Sort fashion palettes by their actual palette type (based on index ranges)
            def sort_fashion_key(palette_path):
                palette_name = os.path.basename(palette_path)
                # First, categorize the palette to get its actual type
                palette_type = self.categorize_palette(palette_name)
                
                # Extract the character number and fashion number for sorting
                char_match = re.match(r'^chr(\d{3})_w(\d+)\.pal$', palette_name.lower())  # Keep the capture group for fashion number
                char_num = char_match.group(1) if char_match else "000"
                fashion_num = int(char_match.group(2)) if char_match else 0
                
                # Sort by palette type first, then by fashion number
                # For chr024, put fashion_5 (Full Suit) last
                if char_num == "024":
                    if palette_type == "fashion_1":
                        return (1, fashion_num)
                    elif palette_type == "fashion_2":
                        return (2, fashion_num)
                    elif palette_type == "fashion_3":
                        return (3, fashion_num)
                    elif palette_type == "fashion_4":
                        return (4, fashion_num)
                    elif palette_type == "fashion_6":
                        return (5, fashion_num)
                    elif palette_type == "fashion_5":
                        return (6, fashion_num)  # Full Suit last
                    else:
                        return (99, fashion_num)  # Unknown types go last
                else:
                    # Normal sorting for other characters
                    if palette_type == "fashion_1":
                        return (1, fashion_num)
                    elif palette_type == "fashion_2":
                        return (2, fashion_num)
                    elif palette_type == "fashion_3":
                        return (3, fashion_num)
                    elif palette_type == "fashion_4":
                        return (4, fashion_num)
                    elif palette_type == "fashion_5":
                        return (5, fashion_num)
                    elif palette_type == "fashion_6":
                        return (6, fashion_num)
                    else:
                        return (99, fashion_num)  # Unknown types go last
            
            for palette_path in sorted(self.fashion_palettes[palette_char_id], key=sort_fashion_key):
                palette_name = os.path.basename(palette_path)
                palette_type = self.categorize_palette(palette_name)
                if palette_type not in fashion_groups:
                    fashion_groups[palette_type] = []
                fashion_groups[palette_type].append((palette_name, palette_path))
            
            # Create radio buttons for each fashion type
            for fashion_type, palettes in fashion_groups.items():
                if fashion_type.startswith("fashion_"):
                    # Create a frame for this fashion type
                    type_frame = tk.Frame(self.fashion_scrollable_frame)
                    type_frame.pack(fill="x", pady=0)
                    
                    # Get proper fashion type name
                    fashion_name = self.get_fashion_type_name(char_id, fashion_type)
                    
                    # Label for fashion type
                    tk.Label(type_frame, text=f"{fashion_name}:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(1,0))
                    
                    # Radio buttons for this type
                    var = tk.StringVar()
                    self.fashion_vars[fashion_type] = var
                    
                    # Add "NONE" option for each fashion type
                    rb = tk.Radiobutton(type_frame, text="NONE", variable=var,
                                      value="NONE", command=self.on_fashion_change)
                    rb.configure(pady=2)
                    rb.pack(anchor="w", padx=(10, 0), pady=1)
                    
                    for palette_name, palette_path in palettes:
                        # Check if this is a custom palette
                        root_dir = getattr(self, "root_dir", 
                                          os.environ.get("FASHION_PREVIEWER_ROOT", 
                                                       os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                        custom_pals_path = os.path.join(root_dir, "exports", "custom_pals", "fashion")
                        # Also check old path for backward compatibility
                        old_custom_pals_path = os.path.join(root_dir, "exports", "custom_fashion_pals")
                        is_custom = (os.path.abspath(palette_path).startswith(os.path.abspath(custom_pals_path)) or
                                   os.path.abspath(palette_path).startswith(os.path.abspath(old_custom_pals_path)))
                        display_name = f"{palette_name} (C)" if is_custom else palette_name
                        
                        rb = tk.Radiobutton(type_frame, text=display_name, variable=var,
                                          value=palette_path, command=self.on_fashion_change)
                        rb.configure(pady=2)
                        rb.pack(anchor="w", padx=(10, 0), pady=0)
                        self.register_focusable(rb, f"fashion_{fashion_type}_{palette_path}")
                    
                    # Set default to NONE for all characters
                    var.set("NONE")

    def on_third_job_change(self):
        """Handle 3rd job base fashion selection change"""
        # Safety check: if current character is Paula, don't process 3rd job changes
        if hasattr(self, 'current_character') and self.current_character in ["chr025", "chr026", "chr027"]:
            return
        
        self.load_palettes()
        self._debounced_display_update()

    def on_hair_change(self):
        """Handle hair selection change"""
        # No warning on selection - warnings only appear when trying to edit
        self.load_palettes()
        self._debounced_display_update()

    def on_fashion_change(self):
        """Handle fashion selection change"""
        self.load_palettes()
        self._debounced_display_update()

    def load_palettes(self):
        """Load selected palettes"""
        # Store current UI mode before loading palettes
        current_ui_mode = getattr(self, 'live_pal_ui_mode', 'Simple')
        self.palette_layers = []
        
        # Load 3rd job base fashion palette (second from bottom layer)
        third_job_path = self.third_job_var.get()
        if third_job_path and third_job_path != "NONE":
            # Safety check: don't load 3rd job palettes for Paula characters
            if hasattr(self, 'current_character') and self.current_character in ["chr025", "chr026", "chr027"]:
                pass  # Don't return, continue to load other palettes
            else:
                layer = self.load_palette_file(third_job_path)
                if layer:
                    layer.palette_type = "3rd_job_base"
                    layer.active = True  # Ensure the layer is active
                    self.palette_layers.append(layer)
                    # Ensure UI mode is preserved when loading 3rd job base fashion
                    self.live_pal_ui_mode = current_ui_mode
        elif hasattr(self, 'current_character') and self.current_character:
            # For 3rd job characters (except Paula), automatically load the first available 3rd job palette
            char_id = self.current_character
            if char_id in CHARACTER_MAPPING and CHARACTER_MAPPING[char_id]["job"] == "3rd Job":
                if char_id not in ["chr025", "chr026", "chr027"]:  # Not Paula
                    palette_char_id = self.get_palette_character_id(char_id)
                    if palette_char_id in self.third_job_palettes and self.third_job_palettes[palette_char_id]:
                        first_palette = self.third_job_palettes[palette_char_id][0]
                        layer = self.load_palette_file(first_palette)
                        if layer:
                            layer.palette_type = "3rd_job_base"
                            layer.active = True  # Ensure the layer is active
                            self.palette_layers.append(layer)
                            # Update the variable to reflect the loaded palette
                            self.third_job_var.set(first_palette)

        # Restore UI mode after loading palettes
        self.live_pal_ui_mode = current_ui_mode
        
        # Load hair palette (bottom layer - processed first)
        hair_path = self.hair_var.get()
        if hair_path and hair_path != "NONE":
            layer = self.load_palette_file(hair_path)
            if layer:
                layer.palette_type = "hair"
                layer.active = True  # Ensure the layer is active
                self.palette_layers.append(layer)
            else:
                pass  # Failed to load hair palette
        else:
            pass  # No hair palette selected
        
        # Load selected fashion palettes (top layer - processed last)
        if hasattr(self, 'current_character') and self.current_character:
            char_id = self.current_character
            # Use the palette character ID for fashion palettes (handles Paula mapping)
            palette_char_id = self.get_palette_character_id(char_id)
            if palette_char_id in self.fashion_palettes:
                for fashion_type, var in self.fashion_vars.items():
                    selected_path = var.get()
                    if selected_path and selected_path != "NONE":
                        layer = self.load_palette_file(selected_path)
                        if layer:
                            layer.palette_type = fashion_type
                            layer.active = True  # Ensure the layer is active
                            self.palette_layers.append(layer)
                        else:
                            pass  # Failed to load palette
                    else:
                        pass  # No fashion selected
            else:
                pass  # No fashion palettes found

    def load_palette_file(self, file_path):
        """Load a palette file and return PaletteLayer object"""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                
            if len(data) != PALETTE_SIZE * 3:
                raise ValueError(f"Palette file size incorrect: {len(data)} bytes")
            
            colors = []
            for i in range(PALETTE_SIZE):
                r = data[i*3]
                g = data[i*3+1]
                b = data[i*3+2]
                colors.append((r, g, b))
            
            filename = os.path.basename(file_path)
            palette_type = self.categorize_palette(filename)
            
            # Track palette preview
            self.statistics.palettes_previewed += 1
            self._save_statistics()
            
            return PaletteLayer(filename, colors, palette_type, True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load palette {file_path}: {e}")
            return None

    def load_character_image(self):
        """Load the current character's image based on current_image_index"""
        if not hasattr(self, 'current_character') or not self.current_character:
            return
            
        char_id = self.current_character
        if char_id not in self.character_images or not self.character_images[char_id]:
            return
            
        images = self.character_images[char_id]
        if 0 <= self.current_image_index < len(images):
            self.load_image_from_path(images[self.current_image_index])

    def load_image_from_path(self, path):
        """Load image from a specific path"""
        # Track frame preview (but don't save during startup restoration)
        self.statistics.frames_previewed += 1
        if not getattr(self, '_is_restoring_session', False):
            self._save_statistics()
        try:
            img = Image.open(path)
            
            # Handle different image modes
            if img.mode == 'P':
                # Already palette mode
                self.original_image = img.copy()
                raw_palette = img.getpalette()
                self.original_palette = [
                    (raw_palette[i*3], raw_palette[i*3+1], raw_palette[i*3+2])
                    for i in range(PALETTE_SIZE)
                ]
            elif img.mode in ['RGB', 'RGBA']:
                # Convert to palette mode more carefully to preserve transparency
                if img.mode == 'RGBA':
                    # Handle alpha channel properly - use green background instead of white
                    background = Image.new('RGB', img.size, (0, 255, 0))  # Green background
                    img = Image.alpha_composite(background.convert('RGBA'), img).convert('RGB')
                
                # Use quantization without dithering to preserve keying colors
                img_palette = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
                raw_palette = img_palette.getpalette()
                if raw_palette:
                    self.original_palette = [
                        (raw_palette[i*3], raw_palette[i*3+1], raw_palette[i*3+2])
                        for i in range(min(len(raw_palette)//3, PALETTE_SIZE))
                    ]
                    while len(self.original_palette) < PALETTE_SIZE:
                        self.original_palette.append((0, 255, 0))  # Fill with green instead of black
                else:
                    self.original_palette = [(0, 255, 0)] * PALETTE_SIZE  # Use green instead of black
                
                self.original_image = img_palette
            else:
                messagebox.showerror("Error", f"Unsupported image mode: {img.mode}")
                return
            
            self.current_image_path = path
            # Update zoom combo state after image is loaded
            self.update_zoom_combo_state()
            self.update_image_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def on_preview_mode_change(self):
        """Handle preview mode change (single vs all frames)"""
        # Track mode changes for intelligent custom defaults
        new_mode = self.preview_var.get()
        old_mode = getattr(self, '_current_preview_mode', 'single')
        
        # Check if switching to "all" mode and show warning if needed
        if new_mode == "all" and old_mode != "all":
            if not self._get_all_mode_warning_preference():
                # Show warning dialogue
                result = self._show_all_mode_warning()
                if not result:
                    # User chose not to proceed, revert to previous mode
                    self.preview_var.set(old_mode)
                    return
        
        # If switching to custom mode, set intelligent defaults based on previous mode
        if new_mode == "custom" and old_mode != "custom":
            # Check if there are stored settings for this character/job
            current_job = self.job_var.get() if hasattr(self, 'job_var') else None
            char_settings = self.frame_range_settings.get(self.current_character, {}) if hasattr(self, 'current_character') else {}
            job_settings = char_settings.get(current_job, None)
            
            if not job_settings:
                # No stored custom settings, use intelligent defaults based on previous mode
                if old_mode == "single":
                    self.custom_frame_count = 1
                elif old_mode == "all" and hasattr(self, 'current_character') and self.current_character in self.character_images:
                    self.custom_frame_count = len(self.character_images[self.current_character])
                # If switching from custom to custom (shouldn't happen), keep existing
        
        # Update current mode tracking
        self._current_preview_mode = new_mode
        
        # Track frames based on mode
        if hasattr(self, 'current_character') and self.current_character in self.character_images:
            if new_mode == "all":
                self.statistics.frames_previewed += len(self.character_images[self.current_character])
            elif new_mode == "custom" and hasattr(self, 'custom_frame_count'):
                self.statistics.frames_previewed += self.custom_frame_count
            elif new_mode == "single":
                self.statistics.frames_previewed += 1
            self._save_statistics()
        
        self.update_zoom_combo_state()
        self.update_image_display()
        
        # Update navigation buttons after preview mode change
        self.update_navigation_buttons()
        
        # Add a delayed update to ensure zoom state is set correctly after UI updates
        self.master.after(100, self.update_zoom_combo_state)
    
    def get_current_displayed_frame(self):
        """Get the currently displayed frame index (0-based)"""
        if hasattr(self, 'current_character') and self.current_character:
            if self.preview_var.get() == "single":
                return self.current_image_index
            elif self.preview_var.get() == "all":
                # In all mode, default to first frame (index 0)
                return 0
            elif self.preview_var.get() == "custom":
                if self.use_frame_choice:
                    return self.chosen_frame - 1  # Convert 1-based to 0-based
                else:
                    # Return the first frame of the current custom display range
                    return getattr(self, 'custom_start_index', 0)
        return 0

    def open_custom_settings(self):
        """Open custom preview settings dialog"""
        if not hasattr(self, 'current_character') or not self.current_character:
            messagebox.showinfo("Notice", "Please select a character first.")
            return
        
        if self.current_character not in self.character_images:
            messagebox.showinfo("Notice", "No images found for this character.")
            return
        
        max_frames = len(self.character_images[self.current_character])
        
        # Get current job
        current_job = self.job_var.get() if hasattr(self, 'job_var') else None
        
        # Get the currently displayed frame
        current_frame = self.get_current_displayed_frame()
        current_mode = self.preview_var.get()
        
        # Special handling for "all" mode - always show full range
        if current_mode == "all":
            dialog = CustomPreviewDialog(self, max_frames, 
                                       start_frame=0, end_frame=max_frames-1, num_frames=max_frames,
                                       use_bmp=self.use_bmp_export,
                                       show_labels=self.show_frame_labels,
                                       initial_frame=current_frame)
        else:
            # Get stored settings for this character/job combination
            char_settings = self.frame_range_settings.get(self.current_character, {})
            job_settings = char_settings.get(current_job, None)
            
            if job_settings:
                frame_count, start_frame, end_frame = job_settings
                dialog = CustomPreviewDialog(self, max_frames, start_frame, end_frame, frame_count, 
                                           self.use_bmp_export, self.show_frame_labels,
                                           initial_frame=current_frame)
            else:
                # Always use the current custom frame count when in custom mode, don't flash to 3
                default_frames = getattr(self, 'custom_frame_count', 3)
                
                dialog = CustomPreviewDialog(self, max_frames, num_frames=default_frames,
                                           use_bmp=self.use_bmp_export,
                                           show_labels=self.show_frame_labels,
                                           initial_frame=current_frame)
            
        self.master.wait_window(dialog.dialog)
        
        if dialog.result is not None:
            # Handle both old and new result tuple formats for backward compatibility
            if len(dialog.result) >= 14:
                frame_count, start_frame, end_frame, use_bmp, show_labels, use_portrait, use_choice, chosen_frame, palette_format, cute_bg, live_pal_ui, show_export_pal, show_dev, show_excess_prompt = dialog.result
                self.live_pal_ui_mode = live_pal_ui
                self.show_export_palette_button = show_export_pal
                self.show_dev_buttons = show_dev
                self.dont_show_excess_colors_prompt = not show_excess_prompt  # Invert for storage
            elif len(dialog.result) >= 13:
                frame_count, start_frame, end_frame, use_bmp, show_labels, use_portrait, use_choice, chosen_frame, palette_format, cute_bg, live_pal_ui, show_export_pal, show_dev = dialog.result
                self.live_pal_ui_mode = live_pal_ui
                self.show_export_palette_button = show_export_pal
                self.show_dev_buttons = show_dev
            elif len(dialog.result) >= 11:
                frame_count, start_frame, end_frame, use_bmp, show_labels, use_portrait, use_choice, chosen_frame, palette_format, cute_bg, live_pal_ui = dialog.result
                self.live_pal_ui_mode = live_pal_ui
            else:
                frame_count, start_frame, end_frame, use_bmp, show_labels, use_portrait, use_choice, chosen_frame, palette_format, cute_bg = dialog.result
            
            self.custom_frame_count = frame_count
            self.use_bmp_export = use_bmp
            self.use_portrait_export = use_portrait
            self.show_frame_labels = show_labels
            self.custom_start_frame = start_frame
            self.custom_end_frame = end_frame
            self.cute_bg_option = cute_bg
            
            # If user chose a specific frame, set it as the start index
            if use_choice and chosen_frame is not None:
                self.custom_start_index = chosen_frame - 1  # Convert 1-based to 0-based for internal use
            else:
                self.custom_start_index = start_frame
            self.update_image_display()  # Refresh display to show/hide labels
            self.update_export_button_text()
            
            # Store settings for this character/job combination
            if self.current_character not in self.frame_range_settings:
                self.frame_range_settings[self.current_character] = {}
            self.frame_range_settings[self.current_character][current_job] = (frame_count, start_frame, end_frame)
            # Reset custom start index if it would exceed bounds
            if self.custom_start_index + self.custom_frame_count > max_frames:
                self.custom_start_index = max(0, max_frames - self.custom_frame_count)
            # Update zoom combo state based on new frame count
            self.update_zoom_combo_state()
            self.update_image_display()
    
    def get_custom_frame_range(self):
        """Get the range of frames to display in custom mode"""
        if not hasattr(self, 'current_character') or not self.current_character:
            return []
        
        if self.current_character not in self.character_images:
            return []
        
        images = self.character_images[self.current_character]
        max_frames = len(images)
        
        # Get current job
        current_job = self.job_var.get() if hasattr(self, 'job_var') else None
        
        # Get stored settings for this character/job combination
        char_settings = self.frame_range_settings.get(self.current_character, {})
        job_settings = char_settings.get(current_job, None)
        
        if job_settings:
            frame_count, start_frame, end_frame = job_settings
            # Validate stored settings
            
            # Calculate visually distributed frames
            if frame_count > 1:
                # Calculate the step size between frames for visual distribution
                total_range = end_frame - start_frame + 1
                if total_range >= frame_count:
                    # Use floating-point division for more accurate spacing
                    step = total_range / (frame_count - 1)
                    # Generate frame indices
                    frames = []
                    for i in range(frame_count):
                        frame_idx = int(start_frame + (i * step))
                        # Ensure we don't exceed the end frame
                        frame_idx = min(frame_idx, end_frame)
                        frames.append(frame_idx)
                    # Ensure the last frame is included if we have more than one frame
                    if frames and frames[-1] != end_frame and frame_count > 1:
                        frames[-1] = end_frame
                    return frames
                else:
                    # If range is smaller than frame count, return all frames in range
                    return list(range(start_frame, end_frame + 1))
            else:
                # For single frame, just return the start frame
                return [start_frame]
            
            if start_frame >= max_frames:
                start_frame = 0
            if end_frame >= max_frames:
                end_frame = max_frames - 1
            if start_frame > end_frame:
                start_frame = 0
                end_frame = max_frames - 1
            
            # Update instance variables
            self.custom_frame_count = frame_count
            self.custom_start_frame = start_frame
            self.custom_end_frame = end_frame
        else:
            # Use default values if no settings stored
            self.custom_frame_count = getattr(self, 'custom_frame_count', 3)
            self.custom_start_frame = getattr(self, 'custom_start_frame', 0)
            self.custom_end_frame = getattr(self, 'custom_end_frame', max_frames - 1)
            
        # Calculate frame indices within the selected range
        end_index = min(self.custom_start_index + self.custom_frame_count, max_frames)
        
        # Return the range of images to display
        return images[self.custom_start_index:end_index]

    def on_zoom_change(self):
        """Handle zoom level change"""
        # Force canvas update before recalculating layout
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
        self._debounced_display_update()

    def update_export_button_text(self):
        """Update the export button text based on the selected format"""
        if hasattr(self, 'export_button'):
            if self.use_bmp_export:
                self.export_button.config(text="Export Background BMP")
                self.export_button.config(command=self.export_background_bmp)
            else:
                self.export_button.config(text="Export Transparent PNG")
                self.export_button.config(command=self.export_transparent_png)
                
    def update_zoom_combo_state(self):
        """Update zoom combo state based on current preview mode"""
        preview_mode = self.preview_var.get()
        
        if hasattr(self, 'current_character') and self.current_character:
            char_id = self.current_character
            if char_id in self.character_images:
                # Enable zoom for all modes when images are loaded
                self.zoom_combo.config(state="readonly")
            else:
                # No images loaded, disable zoom
                self.zoom_combo.config(state="disabled")
        else:
            # No character selected, disable zoom
            self.zoom_combo.config(state="disabled")
        
        # Force update the UI
        self.zoom_combo.update()
        
        # Schedule another update after a short delay to ensure UI state is applied
        self.master.after(50, self._force_zoom_state_update)
    
    def _force_zoom_state_update(self):
        """Force update zoom combo state after a delay"""
        preview_mode = self.preview_var.get()
        if preview_mode == "custom":
            if hasattr(self, 'current_character') and self.current_character:
                char_id = self.current_character
                if char_id in self.character_images:
                    # Enable zoom for all frame counts
                    self.zoom_combo.config(state="readonly")

    def on_canvas_configure(self, event):
        # Configure scroll region for single frame mode and custom preview mode (up to 50 frames)
        preview_mode = self.preview_var.get()
        
        if preview_mode == "single" and self.original_image:
            w, h = self.original_image.size
            
            # Apply zoom based on current zoom setting
            zoom_level = self.zoom_var.get()
            display_w, display_h = w, h
            
            if zoom_level == "200%":
                display_w = int(w * 2)
                display_h = int(h * 2)
            elif zoom_level == "300%":
                display_w = int(w * 3)
                display_h = int(h * 3)
            elif zoom_level == "400%":
                display_w = int(w * 4)
                display_h = int(h * 4)
            elif zoom_level == "500%":
                display_w = int(w * 5)
                display_h = int(h * 5)
            elif zoom_level == "Fit":
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                if canvas_width > 1 and canvas_height > 1:
                    scale_x = canvas_width / w
                    scale_y = canvas_height / h
                    scale = min(scale_x, scale_y)
                    display_w = int(w * scale)
                    display_h = int(h * scale)
            
            # Configure scroll region to show full content with proper bounds
            self.canvas.config(scrollregion=(0, 0, display_w, display_h))
        elif preview_mode == "custom" and hasattr(self, 'current_character') and self.current_character:
            # For custom mode, only configure scroll region if we have 100 or fewer frames being displayed
            char_id = self.current_character
            if char_id in self.character_images:
                frames_to_display = getattr(self, 'custom_frame_count', 3)
                if frames_to_display <= 100:
                    # Let the custom frames display function handle the scroll region
                    # This will be called when update_custom_frames_display runs
                    pass

    def update_image_display(self):
        """Update the image display with current palette"""
        # Check if canvas exists and is valid
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return
            
        if not hasattr(self, 'current_character') or not self.current_character:
            self.canvas.delete("all")
            return
        
        preview_mode = self.preview_var.get()
        old_mode = getattr(self, '_last_preview_mode', None)
        # Only update _last_preview_mode if it's different and not the first time
        if old_mode is not None and old_mode != preview_mode:
            self._last_preview_mode = old_mode  # Keep the previous mode for intelligent switching
        elif old_mode is None:
            self._last_preview_mode = preview_mode  # Initialize on first run
        
        # Handle mode transitions
        if old_mode == "single" and preview_mode == "custom":
            # When switching from single to custom, start at current frame
            self.custom_start_index = self.current_image_index
        
        # Update zoom combo state before displaying (especially important for custom mode)
        self.update_zoom_combo_state()
        
        if preview_mode == "single":
            self.canvas.delete("all")
            self.update_single_frame_display()
        elif preview_mode == "all":
            self.update_all_frames_display()
        elif preview_mode == "custom":
            self.update_custom_frames_display()

    def update_single_frame_display(self):
        """Update display for single frame mode"""
        # Check if canvas exists and is valid
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return
            
        if not self.original_image:
            self.canvas.delete("all")
            return
        
        # Get the merged palette
        merged_palette = self.get_merged_palette()
        

        
        # Create a new image with the merged palette
        w, h = self.original_image.size
        display_img = Image.new("P", (w, h))
        
        # Apply the merged palette FIRST
        display_img.putpalette([color for palette_color in merged_palette for color in palette_color])
        
        # THEN copy the pixel data from original image
        display_img.putdata(self.original_image.getdata())
        

        
        # Replace transparency colors with background color in the merged palette
        merged_palette = self.get_merged_palette()
        display_palette = []
        
        for i, color in enumerate(merged_palette):
            if self.is_universal_keying_color(color) or color == (255, 0, 255):  # Green or magenta
                display_palette.append(self.background_color)
            else:
                display_palette.append(color)
        
        # Apply the modified palette to the display image
        display_img.putpalette([color for palette_color in display_palette for color in palette_color])
        
        # Convert to RGB for display
        rgb_img = display_img.convert("RGB")
        

        
        # Apply zoom based on zoom setting
        zoom_level = self.zoom_var.get()
        display_img = rgb_img
        display_w, display_h = w, h
        
        if zoom_level == "200%":
            # Scale up to 200%
            display_w = int(w * 2)
            display_h = int(h * 2)
            display_img = rgb_img.resize((display_w, display_h), Image.Resampling.NEAREST)
        elif zoom_level == "300%":
            # Scale up to 300%
            display_w = int(w * 3)
            display_h = int(h * 3)
            display_img = rgb_img.resize((display_w, display_h), Image.Resampling.NEAREST)
        elif zoom_level == "400%":
            # Scale up to 400%
            display_w = int(w * 4)
            display_h = int(h * 4)
            display_img = rgb_img.resize((display_w, display_h), Image.Resampling.NEAREST)
        elif zoom_level == "500%":
            # Scale up to 500%
            display_w = int(w * 5)
            display_h = int(h * 5)
            display_img = rgb_img.resize((display_w, display_h), Image.Resampling.NEAREST)
        elif zoom_level == "Fit":
            # Fit to canvas size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if canvas_width <= 1:  # Canvas not yet configured
                canvas_width = 400
            if canvas_height <= 1:
                canvas_height = 400
            
            # Calculate scale to fit within canvas
            scale_x = canvas_width / w
            scale_y = canvas_height / h
            scale = min(scale_x, scale_y)
            
            display_w = int(w * scale)
            display_h = int(h * scale)
            display_img = rgb_img.resize((display_w, display_h), Image.Resampling.LANCZOS)
        
        self.tk_image = ImageTk.PhotoImage(display_img)
        # Clear canvas and recreate image
        self.canvas.delete("all")
        
        # Get canvas dimensions for centering
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1:  # Canvas not yet configured
            canvas_width = 400
        if canvas_height <= 1:
            canvas_height = 400
        
        # For single view: always center horizontally, center vertically if fits, otherwise top-align
        img_x = canvas_width // 2  # Always center horizontally
        
        # Ensure we don't exceed canvas bounds for wide images
        if display_w > canvas_width:
            # If image is wider than canvas, we need horizontal scrolling
            scroll_w = max(display_w, canvas_width)
        else:
            scroll_w = canvas_width
            
        if display_h <= canvas_height:
            # Image fits vertically - center it completely
            img_y = canvas_height // 2
            anchor = "center"
            # Set scroll region to canvas size for centered content
            self.canvas.config(scrollregion=(0, 0, scroll_w, canvas_height))
        else:
            # Image extends past bottom - center horizontally but align to top
            img_y = 0
            anchor = "n"  # North anchor (center horizontally, top vertically)
            # Set scroll region to image size for scrollable content
            self.canvas.config(scrollregion=(0, 0, scroll_w, display_h + 25))
        
        self.img_id = self.canvas.create_image(img_x, img_y, anchor=anchor, image=self.tk_image)
        
        # Add frame number text below the image
        if self.show_frame_labels:
            frame_number = self.current_image_index + 1
            if anchor == "center":
                # For fully centered images, position text below center
                text_x = img_x
                text_y = img_y + (display_h // 2) + 10
            else:
                # For top-aligned images (anchor="n"), position text below image center
                text_x = img_x  # Use same x as image (centered)
                text_y = display_h + 5
            
            self.canvas.create_text(text_x, text_y, text=str(frame_number), 
                                  anchor="n", font=("Arial", 8))
        # Force canvas update
        self.canvas.update()
        self.canvas.update_idletasks()
        self.master.update()

    def update_all_frames_display(self):
        """Update display for all frames mode"""
        # Check if canvas exists and is valid
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return
            
        if not hasattr(self, 'current_character') or self.current_character not in self.character_images:
            self.canvas.delete("all")
            return
        
        images = self.character_images[self.current_character]
        if not images:
            self.canvas.delete("all")
            return
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Get canvas dimensions - ensure canvas is updated first
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1:  # Canvas not yet configured
            canvas_width = 400
        if canvas_height <= 1:
            canvas_height = 400
        
        # Get zoom level and calculate scale factor
        zoom_level = self.zoom_var.get()
        zoom_scale = 1.0
        
        if zoom_level == "200%":
            zoom_scale = 2.0
        elif zoom_level == "300%":
            zoom_scale = 3.0
        elif zoom_level == "400%":
            zoom_scale = 4.0
        elif zoom_level == "500%":
            zoom_scale = 5.0
        elif zoom_level == "Fit":
            # Fit mode: only one image per row, scaled to fit canvas
            zoom_scale = 1.0
        # 100% stays at 1.0
        
        # Constants
        image_spacing = 10
        padding = 10
        
        # Process all images and calculate total height needed
        processed_images = []
        max_width = 0
        max_height = 0
        
        for i, image_path in enumerate(images):
            try:
                # Load and process image similar to single frame
                img = Image.open(image_path)
                
                # Apply palette processing
                if img.mode == 'P':
                    original_img = img.copy()
                    raw_palette = img.getpalette()
                    original_palette = [
                        (raw_palette[j*3], raw_palette[j*3+1], raw_palette[j*3+2])
                        for j in range(PALETTE_SIZE)
                    ]
                else:
                    # Convert to palette mode
                    if img.mode in ['RGBA', 'LA', 'PA']:
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    img_palette = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
                    raw_palette = img_palette.getpalette()
                    if raw_palette:
                        original_palette = [
                            (raw_palette[j*3], raw_palette[j*3+1], raw_palette[j*3+2])
                            for j in range(min(len(raw_palette)//3, PALETTE_SIZE))
                        ]
                        while len(original_palette) < PALETTE_SIZE:
                            original_palette.append((0, 0, 0))
                    else:
                        original_palette = [(0, 0, 0)] * PALETTE_SIZE
                    
                    original_img = img_palette
                
                # Apply current palette layers using the same logic as single frame
                # Temporarily set the original_palette for this image
                original_original_palette = self.original_palette
                self.original_palette = original_palette
                
                # Get the merged palette using the same method as single frame
                result_palette = self.get_merged_palette()
                
                # Restore the original palette
                self.original_palette = original_original_palette
                
                # Create display image
                w, h = original_img.size
                display_img = Image.new("P", (w, h))
                display_img.putpalette([color for palette_color in result_palette for color in palette_color])
                display_img.putdata(original_img.getdata())
                
                # Convert to RGBA and apply transparency
                rgba_img = display_img.convert("RGBA")
                pixels = rgba_img.load()
                
                # Apply character-specific transparency based on original palette colors
                char_num = self.current_character[3:]
                
                # Debug: Count transparent pixels for this frame
                transparent_count = 0
                total_pixels = w * h
                
                # Debug: Track unique colors in this frame
                unique_colors = set()
                
                # Get original image pixel data to check original palette indices
                original_pixel_data = list(original_img.getdata())
                
                for y in range(h):
                    for x in range(w):
                        r, g, b, a = pixels[x, y]
                        color = (r, g, b)
                        unique_colors.add(color)
                        
                        should_make_transparent = False
                        
                        # Get the original palette index for this pixel
                        pixel_index = y * w + x
                        if pixel_index < len(original_pixel_data):
                            palette_index = original_pixel_data[pixel_index]
                            if palette_index < len(original_palette):
                                original_color = original_palette[palette_index]
                                
                                # Check if the original color was a keying color
                                # Never make black transparent
                                if original_color != (0, 0, 0):
                                    # Use character-specific keying logic
                                    if char_num == "014":
                                        # chr014 uses more selective keying
                                        if self.is_chr014_keying_color(original_color):
                                            should_make_transparent = True
                                    else:
                                        # Universal keying colors for other characters
                                        if self.is_universal_keying_color(original_color) or original_color == (255, 0, 255):  # Magenta
                                            should_make_transparent = True
                        
                        if should_make_transparent:
                            pixels[x, y] = (0, 0, 0, 0)
                            transparent_count += 1
                    
                    # Debug: Show transparency info for this frame
                    transparency_percentage = (transparent_count / total_pixels) * 100
    
                    
                    # Debug: Show unique colors if transparency is very low (might indicate issue)
                    if transparency_percentage < 1.0:
    
                        # Check for potential transparency colors that weren't detected
                        potential_transparency_colors = []
                        for color in unique_colors:
                            r, g, b = color
                            if g > 250 and r < 10 and b < 10:  # Very green colors
                                potential_transparency_colors.append(color)
                            elif r > 250 and g < 10 and b > 250:  # Very magenta colors
                                potential_transparency_colors.append(color)
                        if potential_transparency_colors:
                            # print(f"Debug: Potential transparency colors found: {potential_transparency_colors}")
                            pass
                
                # Convert to RGB (transparent pixels become background color)
                rgb_img = self.convert_rgba_to_rgb_with_green_transparency(rgba_img, self.background_color)
                
                # Store original dimensions for this image
                original_w, original_h = w, h
                
                # Apply zoom scaling - preserve original image sizes
                if zoom_level == "Fit":
                    # Fit mode: scale each image to fit canvas width with padding, one per row
                    available_width = canvas_width - (padding * 2)
                    available_height = canvas_height - (padding * 2)
                    
                    # Scale to fit within available space while maintaining aspect ratio
                    scale_x = available_width / w
                    scale_y = available_height / h
                    scale = min(scale_x, scale_y, 1.0)  # Don't scale up beyond 100%
                    
                    new_width = int(w * scale)
                    new_height = int(h * scale)
                    if scale != 1.0:
                        rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    # Apply zoom scaling based on original image size
                    new_width = int(w * zoom_scale)
                    new_height = int(h * zoom_scale)
                    
                    if zoom_scale != 1.0:
                        rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.NEAREST)
                
                processed_images.append((rgb_img, new_width, new_height))
                max_width = max(max_width, new_width)
                max_height = max(max_height, new_height)
                
            except Exception as e:
                continue
        
        if not processed_images:
            return
        
        # Dynamic layout calculation based on actual image sizes and zoom
        if zoom_level == "Fit":
            # Fit mode: one image per row, centered
            rows = []
            current_y = padding
            
            for i, (rgb_img, img_width, img_height) in enumerate(processed_images):
                # Center each image horizontally
                x_pos = (canvas_width - img_width) // 2
                rows.append((i, x_pos, current_y, img_width, img_height))
                current_y += img_height + image_spacing
                
                # Add space for frame label
                current_y += 15  # Additional space for text
            
            total_height = current_y - image_spacing + padding  # Remove last spacing, add bottom padding
        else:
            # Dynamic rows: pack images efficiently based on their actual sizes
            rows = []
            current_row = []
            current_row_width = 0
            current_y = padding
            available_width = canvas_width - (padding * 2)
            
            for i, (rgb_img, img_width, img_height) in enumerate(processed_images):
                # Check if this image fits in the current row
                needed_width = img_width
                if current_row:  # Add spacing if not first in row
                    needed_width += image_spacing
                
                if current_row and (current_row_width + needed_width) > available_width:
                    # Start a new row
                    # First, finalize the current row
                    if current_row:
                        rows.append(current_row)
                        # Calculate row height (tallest image in row)
                        row_height = max(img_data[2] for img_data in current_row)
                        current_y += row_height + image_spacing + 15  # Add space for text
                    
                    # Start new row with this image
                    current_row = [(i, img_width, img_height)]
                    current_row_width = img_width
                else:
                    # Add to current row
                    current_row.append((i, img_width, img_height))
                    current_row_width += needed_width
            
            # Add the last row if it has images
            if current_row:
                rows.append(current_row)
                row_height = max(img_data[2] for img_data in current_row)
                current_y += row_height + image_spacing + 15  # Add space for text
            
            total_height = current_y + padding
            
            # Convert rows to positioned items
            positioned_items = []
            current_y = padding
            
            for row in rows:
                # Calculate total width of this row
                row_width = sum(img_data[1] for img_data in row) + (len(row) - 1) * image_spacing
                # Center the row horizontally
                start_x = (canvas_width - row_width) // 2
                
                # Calculate row height
                row_height = max(img_data[2] for img_data in row)
                
                # Position each image in the row
                current_x = start_x
                for img_index, img_width, img_height in row:
                    # Center vertically within row
                    y_pos = current_y + (row_height - img_height) // 2
                    positioned_items.append((img_index, current_x, y_pos, img_width, img_height))
                    current_x += img_width + image_spacing
                
                current_y += row_height + image_spacing + 15  # Add space for text
            
            rows = positioned_items
        
        # Create PhotoImage objects and place them
        for item in rows:
            if zoom_level == "Fit":
                img_index, x_pos, y_pos, img_width, img_height = item
            else:
                img_index, x_pos, y_pos, img_width, img_height = item
            
            rgb_img, _, _ = processed_images[img_index]
            
            # Create PhotoImage and store reference
            photo_img = ImageTk.PhotoImage(rgb_img)
            # Create the image
            self.canvas.create_image(x_pos, y_pos, anchor="nw", image=photo_img)
            
            # Add frame number text below the image
            frame_number = img_index + 1  # Add 1 since frame numbers are 0-based internally
            text_y = y_pos + img_height + 5  # Position text 5 pixels below the image
            # Add frame number
            self.canvas.create_text(x_pos + img_width // 2, text_y, text=str(frame_number), 
                                  anchor="n", font=("Arial", 8))
            
            # Store reference to prevent garbage collection
            if not hasattr(self, 'all_frame_images'):
                self.all_frame_images = []
            self.all_frame_images.append(photo_img)
        
        # Set vertical scroll region only - width matches canvas width
        self.canvas.config(scrollregion=(0, 0, canvas_width, total_height))
        
        # Force canvas update to ensure display refreshes
        self.canvas.update()
        self.canvas.update_idletasks()
        self.master.update()

    def update_custom_frames_display(self):
        """Update display for custom frames mode"""
        # Check if canvas exists and is valid
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return
            
        if not hasattr(self, 'current_character') or self.current_character not in self.character_images:
            self.canvas.delete("all")
            return
            
        # Get all images for the current character
        all_images = self.character_images[self.current_character]
        if not all_images:
            self.canvas.delete("all")
            return
            
        # Get current job and frame range settings
        current_job = self.job_var.get() if hasattr(self, 'job_var') else None
        char_settings = self.frame_range_settings.get(self.current_character, {})
        job_settings = char_settings.get(current_job, None)
        
        if job_settings:
            frame_count, start_frame, end_frame = job_settings
        else:
            frame_count = getattr(self, 'custom_frame_count', 3)
            start_frame = getattr(self, 'custom_start_frame', 0)
            end_frame = getattr(self, 'custom_end_frame', len(all_images) - 1)
            
        # Ensure custom_start_index is within bounds
        if self.custom_start_index >= len(all_images):
            self.custom_start_index = 0
        if self.custom_start_index < 0:
            self.custom_start_index = 0
            
        # Get frames to display based on custom_start_index
        frames_to_show = min(frame_count, len(all_images) - self.custom_start_index)
        if frames_to_show <= 0:
            # If no frames to show, reset to beginning
            self.custom_start_index = 0
            frames_to_show = min(frame_count, len(all_images))
            
        frame_indices = range(self.custom_start_index, self.custom_start_index + frames_to_show)
        
        # Get the selected frames
        custom_images = [all_images[i] for i in frame_indices]
        if not custom_images:
            self.canvas.delete("all")
            return
            
        # Store the frame indices for reference
        self.custom_frames = list(frame_indices)
        
        # Clear canvas and previous image references
        self.canvas.delete("all")
        
        # Clear previous custom frame images to prevent memory issues
        if hasattr(self, 'custom_frame_images'):
            self.custom_frame_images.clear()
        else:
            self.custom_frame_images = []
        
        # Get canvas dimensions - ensure canvas is updated first
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1:  # Canvas not yet configured
            canvas_width = 400
        if canvas_height <= 1:
            canvas_height = 400
        
        # Get zoom level and calculate scale factor
        zoom_level = self.zoom_var.get()
        zoom_scale = 1.0
        
        if zoom_level == "200%":
            zoom_scale = 2.0
        elif zoom_level == "300%":
            zoom_scale = 3.0
        elif zoom_level == "400%":
            zoom_scale = 4.0
        elif zoom_level == "500%":
            zoom_scale = 5.0
        elif zoom_level == "Fit":
            # Fit mode: only one image per row, scaled to fit canvas
            zoom_scale = 1.0
        # 100% stays at 1.0
        
        # Constants
        image_spacing = 10
        padding = 10
        
        # Process custom images and calculate total height needed
        processed_images = []
        max_width = 0
        max_height = 0
        
        for i, image_path in enumerate(custom_images):
            try:
                # Load and process image similar to single frame
                img = Image.open(image_path)
                
                # Apply palette processing
                if img.mode == 'P':
                    original_img = img.copy()
                    raw_palette = img.getpalette()
                    original_palette = [
                        (raw_palette[j*3], raw_palette[j*3+1], raw_palette[j*3+2])
                        for j in range(PALETTE_SIZE)
                    ]
                else:
                    # Convert to palette mode
                    if img.mode in ['RGBA', 'LA', 'PA']:
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            background.paste(img, mask=img.split()[-1])
                            img = background
                        else:
                            background.paste(img)
                            img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    img_palette = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
                    raw_palette = img_palette.getpalette()
                    if raw_palette:
                        original_palette = [
                            (raw_palette[j*3], raw_palette[j*3+1], raw_palette[j*3+2])
                            for j in range(min(len(raw_palette)//3, PALETTE_SIZE))
                        ]
                        while len(original_palette) < PALETTE_SIZE:
                            original_palette.append((0, 0, 0))
                    else:
                        original_palette = [(0, 0, 0)] * PALETTE_SIZE
                    
                    original_img = img_palette
                
                # Apply current palette layers using the same logic as single frame
                # Temporarily set the original_palette for this image
                original_original_palette = self.original_palette
                self.original_palette = original_palette
                
                # Get the merged palette using the same method as single frame
                result_palette = self.get_merged_palette()
                
                # Restore the original palette
                self.original_palette = original_original_palette
                
                # Create display image
                w, h = original_img.size
                display_img = Image.new("P", (w, h))
                display_img.putpalette([color for palette_color in result_palette for color in palette_color])
                display_img.putdata(original_img.getdata())
                
                # Convert to RGBA and apply transparency
                rgba_img = display_img.convert("RGBA")
                pixels = rgba_img.load()
                
                # Apply character-specific transparency based on original palette colors
                char_num = self.current_character[3:]
                
                # Debug: Count transparent pixels for this frame
                transparent_count = 0
                total_pixels = w * h
                
                # Debug: Track unique colors in this frame
                unique_colors = set()
                
                # Get original image pixel data to check original palette indices
                original_pixel_data = list(original_img.getdata())
                
                for y in range(h):
                    for x in range(w):
                        r, g, b, a = pixels[x, y]
                        color = (r, g, b)
                        unique_colors.add(color)
                        
                        should_make_transparent = False
                        
                        # Get the original palette index for this pixel
                        pixel_index = y * w + x
                        if pixel_index < len(original_pixel_data):
                            palette_index = original_pixel_data[pixel_index]
                            if palette_index < len(original_palette):
                                original_color = original_palette[palette_index]
                                
                                # Check if the original color was a keying color
                                # Never make black transparent
                                if original_color != (0, 0, 0):
                                    # Use character-specific keying logic
                                    if char_num == "014":
                                        # chr014 uses more selective keying
                                        if self.is_chr014_keying_color(original_color):
                                            should_make_transparent = True
                                    else:
                                        # Universal keying colors for other characters
                                        if self.is_universal_keying_color(original_color) or original_color == (255, 0, 255):  # Magenta
                                            should_make_transparent = True
                        
                        if should_make_transparent:
                            pixels[x, y] = (0, 0, 0, 0)
                            transparent_count += 1
                    
                    # Debug: Show transparency info for this frame
                    transparency_percentage = (transparent_count / total_pixels) * 100
    
                    
                    # Debug: Show unique colors if transparency is very low (might indicate issue)
                    if transparency_percentage < 1.0:
    
                        # Check for potential transparency colors that weren't detected
                        potential_transparency_colors = []
                        for color in unique_colors:
                            r, g, b = color
                            if g > 250 and r < 10 and b < 10:  # Very green colors
                                potential_transparency_colors.append(color)
                            elif r > 250 and g < 10 and b > 250:  # Very magenta colors
                                potential_transparency_colors.append(color)
                        if potential_transparency_colors:
                            # print(f"Debug: Potential transparency colors found: {potential_transparency_colors}")
                            pass
                
                # Convert to RGB (transparent pixels become background color)
                rgb_img = self.convert_rgba_to_rgb_with_green_transparency(rgba_img, self.background_color)
                
                # Store original dimensions for this image
                original_w, original_h = w, h
                
                # Apply zoom scaling - preserve original image sizes
                if zoom_level == "Fit":
                    # Fit mode: scale each image to fit canvas width with padding, one per row
                    available_width = canvas_width - (padding * 2)
                    available_height = canvas_height - (padding * 2)
                    
                    # Scale to fit within available space while maintaining aspect ratio
                    scale_x = available_width / w
                    scale_y = available_height / h
                    scale = min(scale_x, scale_y, 1.0)  # Don't scale up beyond 100%
                    
                    new_width = int(w * scale)
                    new_height = int(h * scale)
                    if scale != 1.0:
                        rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    # Apply zoom scaling based on original image size
                    new_width = int(w * zoom_scale)
                    new_height = int(h * zoom_scale)
                    
                    if zoom_scale != 1.0:
                        rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.NEAREST)
                
                processed_images.append((rgb_img, new_width, new_height))
                max_width = max(max_width, new_width)
                max_height = max(max_height, new_height)
                
            except Exception as e:
                continue
        
        if not processed_images:
            return
        
        # Dynamic layout calculation based on actual image sizes and zoom
        if zoom_level == "Fit":
            # Fit mode: one image per row, centered
            rows = []
            current_y = padding
            
            for i, (rgb_img, img_width, img_height) in enumerate(processed_images):
                # Center each image horizontally
                x_pos = (canvas_width - img_width) // 2
                rows.append((i, x_pos, current_y, img_width, img_height))
                current_y += img_height + image_spacing
                
                # Add space for frame label if enabled
                if self.show_frame_labels:
                    current_y += 15  # Additional space for text
            
            total_height = current_y - image_spacing + padding  # Remove last spacing, add bottom padding
        else:
            # Dynamic rows: pack images efficiently based on their actual sizes
            rows = []
            current_row = []
            current_row_width = 0
            current_y = padding
            available_width = canvas_width - (padding * 2)
            
            for i, (rgb_img, img_width, img_height) in enumerate(processed_images):
                # Check if this image fits in the current row
                needed_width = img_width
                if current_row:  # Add spacing if not first in row
                    needed_width += image_spacing
                
                if current_row and (current_row_width + needed_width) > available_width:
                    # Start a new row
                    # First, finalize the current row
                    if current_row:
                        rows.append(current_row)
                        # Calculate row height (tallest image in row)
                        row_height = max(img_data[2] for img_data in current_row)
                        current_y += row_height + image_spacing
                        if self.show_frame_labels:
                            current_y += 15  # Additional space for text
                    
                    # Start new row with this image
                    current_row = [(i, img_width, img_height)]
                    current_row_width = img_width
                else:
                    # Add to current row
                    current_row.append((i, img_width, img_height))
                    current_row_width += needed_width
            
            # Add the last row if it has images
            if current_row:
                rows.append(current_row)
                row_height = max(img_data[2] for img_data in current_row)
                current_y += row_height
                if self.show_frame_labels:
                    current_y += 15
            
            total_height = current_y + padding
            
            # Convert rows to positioned items
            positioned_items = []
            current_y = padding
            
            for row in rows:
                # Calculate total width of this row
                row_width = sum(img_data[1] for img_data in row) + (len(row) - 1) * image_spacing
                # Center the row horizontally
                start_x = (canvas_width - row_width) // 2
                
                # Calculate row height
                row_height = max(img_data[2] for img_data in row)
                
                # Position each image in the row
                current_x = start_x
                for img_index, img_width, img_height in row:
                    # Center vertically within row
                    y_pos = current_y + (row_height - img_height) // 2
                    positioned_items.append((img_index, current_x, y_pos, img_width, img_height))
                    current_x += img_width + image_spacing
                
                current_y += row_height + image_spacing
                if self.show_frame_labels:
                    current_y += 15
            
            rows = positioned_items
        
        # Create PhotoImage objects and place them
        for item in rows:
            if zoom_level == "Fit":
                img_index, x_pos, y_pos, img_width, img_height = item
            else:
                img_index, x_pos, y_pos, img_width, img_height = item
            
            rgb_img, _, _ = processed_images[img_index]
            
            # Create PhotoImage and store reference
            photo_img = ImageTk.PhotoImage(rgb_img)
            # Create the image
            self.canvas.create_image(x_pos, y_pos, anchor="nw", image=photo_img)
            
            # Add frame number text below the image if enabled
            if self.show_frame_labels:
                frame_number = self.custom_frames[img_index] + 1  # Add 1 since frame numbers are 0-based internally
                text_y = y_pos + img_height + 5  # Position text 5 pixels below the image
                # Add frame number
                self.canvas.create_text(x_pos + img_width // 2, text_y, text=str(frame_number), 
                                      anchor="n", font=("Arial", 8))
            
            # Store reference to prevent garbage collection
            self.custom_frame_images.append(photo_img)
        
        # Set vertical scroll region only - width matches canvas width
        self.canvas.config(scrollregion=(0, 0, canvas_width, total_height))
        
        # Force canvas update to ensure display refreshes
        self.canvas.update()
        self.canvas.update_idletasks()
        self.master.update()
        
        # Update navigation buttons to ensure they're properly enabled
        self.update_navigation_buttons()

    def get_merged_palette(self):
        """Get the merged palette, respecting keying colors and transparency"""
        if not self.original_palette:
            return [(0, 0, 0)] * PALETTE_SIZE
        
        result = self.original_palette.copy()
        
        # Check if we have a live editor open and get the current selection
        live_editor_active = (hasattr(self, '_live_editor_window') and 
                            self._live_editor_window and 
                            self._live_editor_window.winfo_exists())
        
        current_live_selection = None
        if live_editor_active and hasattr(self, '_live_target_name'):
            current_live_selection = self._live_target_name.get()
        
        # First, apply 3rd job base fashion to establish the base
        for layer in reversed(self.palette_layers):
            if not layer.active or layer.palette_type != "3rd_job_base":
                continue
            
            # Get allowed indices for this palette type and character
            char_num = self.current_character[3:] if self.current_character else None  # Extract number from chr001
            allowed_indices = self.get_allowed_indices_for_palette(layer, char_num)
            
            for i in range(PALETTE_SIZE):
                color = layer.colors[i]
                
                # Check if this color should be ignored based on palette type
                should_ignore = self.is_fashion_palette_keying_color(layer, color, i)
                
                # Only apply colors that aren't keying colors AND are in allowed indices
                if (color is not None and not should_ignore and (i in allowed_indices or (getattr(layer, 'palette_type', '') == 'fashion_4' and char_num == '020'))):
                    result[i] = color
                elif layer.palette_type == "hair" and (i in allowed_indices or (getattr(layer, 'palette_type', '') == 'fashion_4' and char_num == '020')) and color is None:
                    # For hair palettes, if a color is None (not defined in palette), 
                    # keep the original color instead of leaving it unchanged
                    # This ensures all hair indices get processed
                    if i < len(self.original_palette):
                        result[i] = self.original_palette[i]
        
        # Then apply other layers (hair and regular fashion)
        for layer in reversed(self.palette_layers):
            if not layer.active or layer.palette_type == "3rd_job_base":
                continue
            
            # Get allowed indices for this palette type and character
            char_num = self.current_character[3:] if self.current_character else None  # Extract number from chr001
            allowed_indices = self.get_allowed_indices_for_palette(layer, char_num)
            
            # Check if this layer matches the current live editor selection
            layer_matches_live_editor = False
            if live_editor_active and current_live_selection:
                # Extract the fashion type from the display name (format: "Hoodie — chr001_w07")
                if " — " in current_live_selection:
                    selected_fashion_type = current_live_selection.split(" — ")[0]
                    selected_char_id = current_live_selection.split(" — ")[1]
                else:
                    selected_fashion_type = current_live_selection
                    selected_char_id = ""
                
                # Get the layer's character ID and palette type
                layer_name = getattr(layer, 'name', '')
                layer_palette_type = getattr(layer, 'palette_type', '')
                
                # Match based on character ID and palette type
                if selected_char_id and layer_name:
                    # Extract character ID from layer name (e.g., "chr001_w07" -> "chr001")
                    char_match = re.search(r'(chr\d{3})', layer_name)
                    if char_match:
                        layer_char_id = char_match.group(1)
                        if layer_char_id == selected_char_id and layer_palette_type:
                            layer_matches_live_editor = True
            
            for i in range(PALETTE_SIZE):
                # Use original colors for layers that don't match the live editor selection
                if live_editor_active and not layer_matches_live_editor and hasattr(self, '_live_original_colors'):
                    layer_name = getattr(layer, 'name', '')
                    if layer_name in self._live_original_colors:
                        color = self._live_original_colors[layer_name][i]
                    else:
                        color = layer.colors[i]
                else:
                    color = layer.colors[i]
                
                # Check if this color should be ignored based on palette type
                should_ignore = False
                
                if layer.palette_type == "hair":
                    # For hair palettes, don't ignore any colors (apply all)
                    should_ignore = False
                    

                elif layer.palette_type.startswith("fashion_"):
                    # For fashion palettes, use fashion-specific keying colors
                    should_ignore = self.is_fashion_palette_keying_color(layer, color, i)
                else:
                    # For other palettes, use standard green/magenta keying
                    should_ignore = (self.is_green_padding(color) or 
                                   self.is_magenta_transparency(color))
                
                # Only apply colors that aren't keying colors AND are in allowed indices
                if (color is not None and not should_ignore and 
                    (i in allowed_indices or (getattr(layer, 'palette_type', '') == 'fashion_4' and char_num == '020'))):
                    result[i] = color
                elif layer.palette_type == "hair" and (i in allowed_indices or (getattr(layer, 'palette_type', '') == 'fashion_4' and char_num == '020')) and color is None:
                    # For hair palettes, if a color is None (not defined in palette), 
                    # keep the original color instead of leaving it unchanged
                    # This ensures all hair indices get processed
                    if i < len(self.original_palette):
                        result[i] = self.original_palette[i]

        return result

    def get_allowed_indices_for_palette(self, layer, char_num):
        """Get the allowed index range for a palette based on character and palette type"""
        if not char_num or not layer:
            return set()  # No character loaded or no layer
        
        # For Paula characters, use the mapped character ID for palette ranges
        if char_num in ["025", "026", "027"]:
            if char_num == "025":
                palette_char_num = "100"  # Paula 1st Job
            elif char_num == "026":
                palette_char_num = "101"  # Paula 2nd Job
            elif char_num == "027":
                palette_char_num = "102"  # Paula 3rd Job
        else:
            palette_char_num = char_num
        
        # Get the ranges for this character and palette type
        ranges = self.get_character_palette_ranges(palette_char_num, layer.palette_type)
        
        # Convert ranges to a set of indices
        allowed_indices = set()
        for r in ranges:
            allowed_indices.update(r)
        
        return allowed_indices

    def categorize_palette(self, filename):
        """Categorize palette by its purpose based on filename - only uses character ID"""
        if not filename:
            return "unknown"
        
        filename_lower = filename.lower()
        
        # Hair palettes (chr###_0.pal to chr###_20.pal) - all are hair palettes
        # Must NOT start with 'w' to avoid matching fashion palettes like chr###_w00.pal
        if re.match(r'^chr\d{3}_\d+\.pal$', filename_lower):
            return "hair"
        
        # Fashion palettes (chr###_w##.pal) - categorize based on palette content analysis
        match = re.match(r'^chr(\d{3})_w\d+\.pal$', filename_lower)
        if match:
            char_num = match.group(1)
            
            # Always try to determine fashion type by analyzing palette content
            # Use the character number from the filename to analyze the palette
            return self.determine_fashion_type_from_palette_content(filename, char_num)
        
        return "unknown"

    def determine_fashion_type_from_palette_content(self, filename, char_num=None):
        """Determine fashion type by analyzing palette content"""
        if not char_num:
            if hasattr(self, 'current_character') and self.current_character:
                char_num = self.current_character[3:]  # Extract "001" from "chr001"
            else:
                return "unknown"
        
        # Load the palette file
        try:
            # Try different possible paths for the palette file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = getattr(self, "root_dir", 
                              os.environ.get("FASHION_PREVIEWER_ROOT", 
                                           os.path.dirname(script_dir)))
            possible_paths = [
                os.path.join("nonremovable_assets", "vanilla_pals", "fashion", filename),
                os.path.join(root_dir, "exports", "custom_pals", "fashion", filename),
                os.path.join(root_dir, "exports", "custom_fashion_pals", filename)  # backwards compatibility
            ]
            
            palette_data = None
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        data = f.read()
                    if len(data) == PALETTE_SIZE * 3:
                        palette_data = []
                        for i in range(PALETTE_SIZE):
                            r = data[i*3]
                            g = data[i*3+1] 
                            b = data[i*3+2]
                            palette_data.append((r, g, b))
                        break
            
            if not palette_data:
                return "unknown"
            
            # Use the provided character number for range lookup
            
            # For chr003, use the specific ranges provided
            if char_num == "003":
                # Define chr003 specific fashion ranges
                chr003_ranges = {
                    "fashion_1": [range(111, 125)],  # 111-124
                    "fashion_2": [range(128, 135)],  # 128-134
                    "fashion_3": [range(137, 144)],  # 137-143
                    "fashion_4": [range(144, 154)],  # 144-153
                    "fashion_5": [range(155, 160)],  # 155-159
                    "fashion_6": [range(160, 175)]   # 160-174
                }
                
                best_match = "unknown"
                max_non_keying_colors = 0
                
                for fashion_type, ranges in chr003_ranges.items():
                    # Count non-keying colors in this fashion type's ranges
                    non_keying_count = 0
                    for r in ranges:
                        for i in r:
                            if i < len(palette_data):
                                color = palette_data[i]
                                # Check if this color is not a keying color for chr003
                                if not self.is_chr003_keying_color(color):
                                    non_keying_count += 1
                    
                    # If this fashion type has more non-keying colors, it's likely the correct one
                    if non_keying_count > max_non_keying_colors:
                        max_non_keying_colors = non_keying_count
                        best_match = fashion_type
                
                return best_match if max_non_keying_colors > 0 else "unknown"
            # For chr008, use the specific ranges provided
            elif char_num == "008":
                # Define chr008 specific fashion ranges
                chr008_ranges = {
                    "fashion_1": [range(111, 134)],  # 111-133
                    "fashion_2": [range(137, 144)],  # 137-143
                    "fashion_3": [range(144, 151)]   # 144-150
                }
                
                best_match = "unknown"
                max_non_keying_colors = 0
                
                for fashion_type, ranges in chr008_ranges.items():
                    # Count non-keying colors in this fashion type's ranges
                    non_keying_count = 0
                    for r in ranges:
                        for i in r:
                            if i < len(palette_data):
                                color = palette_data[i]
                                # Check if this color is not a keying color for chr008
                                if not self.is_chr008_keying_color(color):
                                    non_keying_count += 1
                    
                    # If this fashion type has more non-keying colors, it's likely the correct one
                    if non_keying_count > max_non_keying_colors:
                        max_non_keying_colors = non_keying_count
                        best_match = fashion_type
                
                return best_match if max_non_keying_colors > 0 else "unknown"
            # For chr011, use the same keying logic as chr003 since they share the same patterns
            elif char_num == "011":
                # Define chr011 specific fashion ranges
                chr011_ranges = {
                    "fashion_1": [range(0, 110), range(111, 137)],  # 0-109, 111-136
                    "fashion_2": [range(0, 137), range(138, 149)],  # 0-136, 138-148
                    "fashion_3": [range(150, 158)],  # Satchel: 150-157
                    "fashion_4": [range(159, 176)],  # Gloves: 159-175
                    "fashion_5": [range(177, 201)]   # Shoes: 177-200
                }
                
                best_match = "unknown"
                max_non_keying_colors = 0
                
                for fashion_type, ranges in chr011_ranges.items():
                    # Count non-keying colors in this fashion type's ranges
                    non_keying_count = 0
                    for r in ranges:
                        for i in r:
                            if i < len(palette_data):
                                color = palette_data[i]
                                # Check if this color is not a keying color for chr011
                                if not self.is_chr011_keying_color(color):
                                    non_keying_count += 1
                    
                    # If this fashion type has more non-keying colors, it's likely the correct one
                    if non_keying_count > max_non_keying_colors:
                        max_non_keying_colors = non_keying_count
                        best_match = fashion_type
                
                return best_match if max_non_keying_colors > 0 else "unknown"
            # For Paula characters (chr100, chr101, chr102), use their specific ranges
            elif char_num in ["100", "101", "102"]:
                # Get the ranges for this character from the existing function
                fashion_types = ["fashion_1", "fashion_2", "fashion_3", "fashion_4", 
                               "fashion_5", "fashion_6", "fashion_7", "fashion_8"]
                
                best_match = "unknown"
                max_non_keying_colors = 0
                
                for fashion_type in fashion_types:
                    ranges = self.get_character_palette_ranges(char_num, fashion_type)
                    if ranges == [range(256)]:  # Skip fallback ranges
                        continue
                    
                    # Count non-keying colors in this fashion type's ranges
                    non_keying_count = 0
                    for r in ranges:
                        for i in r:
                            if i < len(palette_data):
                                color = palette_data[i]
                                # Check if this color is not a keying color for Paula characters
                                # Paula characters use the same keying colors as Sheep and Raccoon characters
                                if not (self.is_chr003_keying_color(color) or 
                                       self.is_chr008_keying_color(color) or 
                                       color == (255, 0, 255)):  # Magenta
                                    non_keying_count += 1
                    
                    # If this fashion type has more non-keying colors, it's likely the correct one
                    if non_keying_count > max_non_keying_colors:
                        max_non_keying_colors = non_keying_count
                        best_match = fashion_type
                
                return best_match if max_non_keying_colors > 0 else "unknown"
            # For chr024, use content-based categorization with fashion_5 subgroups
            elif char_num == "024":
                # Define chr024 specific fashion ranges with fashion_5 subgroups
                chr024_ranges = {
                    "fashion_1": [range(111, 131)],  # 111-130
                    "fashion_2": [range(134, 149)],  # 134-148
                    "fashion_3": [range(150, 165)],  # 150-164
                    "fashion_4": [range(166, 174)],  # 166-173
                    "fashion_5_comprehensive": [range(1, 34), range(111, 131), range(134, 149), range(150, 165), range(166, 174), range(208, 219)],  # w02, w12, w22, w32, w42 pattern (excluding 176-181)
                    "fashion_5_pure": [range(176, 182)]   # w40, w41, w43 pattern
                }
                
                # Count non-keying colors in each range and calculate density
                range_analysis = {}
                for fashion_type, ranges in chr024_ranges.items():
                    total_indices = 0
                    non_keying_count = 0
                    for r in ranges:
                        for i in r:
                            total_indices += 1
                            if i < len(palette_data):
                                color = palette_data[i]
                                # Check if this color is not a keying color for chr024
                                if not self.is_palette_keying_color(color, i, char_num):
                                    non_keying_count += 1
                    
                    # Calculate density (percentage of non-keying colors in this range)
                    density = (non_keying_count / total_indices) if total_indices > 0 else 0
                    range_analysis[fashion_type] = {
                        'count': non_keying_count,
                        'total': total_indices,
                        'density': density
                    }
                
                # Also check fashion_6 range (176-182) separately
                fashion_6_ranges = [range(176, 182)]
                fashion_6_total = 0
                fashion_6_count = 0
                for r in fashion_6_ranges:
                    for i in r:
                        fashion_6_total += 1
                        if i < len(palette_data):
                            color = palette_data[i]
                            if not self.is_palette_keying_color(color, i, char_num):
                                fashion_6_count += 1
                
                fashion_6_density = (fashion_6_count / fashion_6_total) if fashion_6_total > 0 else 0
                range_analysis["fashion_6"] = {
                    'count': fashion_6_count,
                    'total': fashion_6_total,
                    'density': fashion_6_density
                }
                
                # Find the range with the highest density of non-keying colors
                # For chr024, check fashion_5 first (w02 group with ALL required indexes)
                # If it doesn't fit there, then filter to other categories
                
                # Check if this palette has non-keying colors in ALL required ranges for fashion_5
                required_ranges = [
                    range(1, 34),      # 1-33
                    range(111, 131),   # 111-130
                    range(134, 149),   # 134-148
                    range(150, 165),   # 150-164
                    range(166, 174),   # 166-173
                    range(176, 182),   # 176-181
                    range(208, 219)    # 208-218
                ]
                
                all_ranges_have_colors = True
                for r in required_ranges:
                    range_has_colors = False
                    for i in r:
                        if i < len(palette_data):
                            color = palette_data[i]
                            if not self.is_palette_keying_color(color, i, char_num):
                                range_has_colors = True
                                break
                    if not range_has_colors:
                        all_ranges_have_colors = False
                        break
                
                # If it fits fashion_5 criteria, return fashion_5
                if all_ranges_have_colors:
                    return "fashion_5"
                
                # Check if indices before and after the fashion_6 range (176-181) are keyed out
                # This helps distinguish comprehensive vs pure palettes
                before_range_keyed = True
                after_range_keyed = True
                
                # Check index 175 (before 176-181)
                if 175 < len(palette_data):
                    color_175 = palette_data[175]
                    if not self.is_palette_keying_color(color_175, 175, char_num):
                        before_range_keyed = False
                
                # Check index 182 (after 176-181)
                if 182 < len(palette_data):
                    color_182 = palette_data[182]
                    if not self.is_palette_keying_color(color_182, 182, char_num):
                        after_range_keyed = False
                
                # If fashion_6 has colors AND surrounding indices are keyed out, it's likely a pure palette
                fashion_6_analysis = range_analysis.get("fashion_6", {'count': 0, 'total': 0, 'density': 0})
                if fashion_6_analysis['count'] > 0 and before_range_keyed and after_range_keyed:
                    return "fashion_6"
                
                # If it doesn't fit fashion_5 or fashion_6, check other categories (1-4)
                max_density = 0
                best_match = "unknown"
                min_total = float('inf')
                
                for fashion_type, analysis in range_analysis.items():
                    if fashion_type in ["fashion_1", "fashion_2", "fashion_3", "fashion_4"] and analysis['count'] > 0:
                        if analysis['density'] > max_density:
                            max_density = analysis['density']
                            best_match = fashion_type
                            min_total = analysis['total']
                        elif analysis['density'] == max_density and analysis['total'] < min_total:
                            # Same density but fewer total indices (more specialized)
                            best_match = fashion_type
                            min_total = analysis['total']
                
                return best_match if max_density > 0 else "unknown"
            else:
                # For other characters, use the existing logic
                fashion_types = ["fashion_1", "fashion_2", "fashion_3", "fashion_4", 
                               "fashion_5", "fashion_6", "fashion_7", "fashion_8"]
                
                best_match = "unknown"
                max_non_keying_colors = 0
                
                for fashion_type in fashion_types:
                    ranges = self.get_character_palette_ranges(char_num, fashion_type)
                    if ranges == [range(256)]:  # Skip fallback ranges
                        continue
                    
                    # Count non-keying colors in this fashion type's ranges
                    non_keying_count = 0
                    for r in ranges:
                        for i in r:
                            if i < len(palette_data):
                                color = palette_data[i]
                                # Check if this color is not a keying color
                                if not self.is_palette_keying_color(color, i, char_num):
                                    non_keying_count += 1
                    
                    # If this fashion type has more non-keying colors, it's likely the correct one
                    if non_keying_count > max_non_keying_colors:
                        max_non_keying_colors = non_keying_count
                        best_match = fashion_type
                
                return best_match if max_non_keying_colors > 0 else "unknown"

        except Exception as e:
            return "unknown"

    def is_universal_keying_color(self, color):
        """Check if a color is a universal keying color for ALL characters"""
        r, g, b = color
        
        # Pure green (0, 255, 0) - used by ALL characters including chr010
        if color == (0, 255, 0):
            return True
        
        # (0~25, 255, 0) pattern - used by chr002, chr008, chr024, and others
        # Analysis found: (5, 255, 0), (10, 255, 0), (14, 255, 0), (19, 255, 0), (23, 255, 0)
        if g == 255 and b == 0 and 0 <= r <= 25:
            return True
        
        # (0, 255, 0~21) pattern - used by chr003, chr011, chr019, and others
        # Analysis found: (0, 255, 21)
        if g == 255 and r == 0 and 0 <= b <= 21:
            return True
        
        return False

    def convert_rgba_to_rgb_with_green_transparency(self, rgba_img, background_color=None):
        """Convert RGBA image to RGB, making transparent pixels use the specified background color (defaults to green)"""
        if rgba_img.mode != 'RGBA':
            return rgba_img.convert('RGB')
        
        # Use custom background color if provided, otherwise default to green
        if background_color is None:
            background_color = (0, 255, 0)  # Default green
        
        # Create a new RGB image
        rgb_img = Image.new('RGB', rgba_img.size)
        rgba_pixels = rgba_img.load()
        rgb_pixels = rgb_img.load()
        
        for y in range(rgba_img.height):
            for x in range(rgba_img.width):
                r, g, b, a = rgba_pixels[x, y]
                if a == 0:  # Transparent pixel
                    rgb_pixels[x, y] = background_color  # Use custom background color
                else:
                    rgb_pixels[x, y] = (r, g, b)  # Keep original color
        
        return rgb_img

    def is_palette_keying_color(self, color, index, char_num):
        """Check if a color at a specific index is a keying color for the character"""
        # Universal keying colors for ALL characters
        if self.is_universal_keying_color(color) or color == (255, 0, 255):  # Magenta
            return True
        
        # Character-specific keying rules
        if char_num == "004":  # chr004 specific rules
            if color == (0, 0, 0):  # Black
                return True
            if index == 255:  # Last color in palette
                return True
        
        return False

    def is_chr003_keying_color(self, color):
        """Check if a color is a keying color for chr003 (Sheep)"""
        # chr003 uses universal keying colors
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr008_keying_color(self, color):
        """Check if a color is a keying color for chr008 (Raccoon)"""
        # chr008 uses universal keying colors
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr011_keying_color(self, color):
        """Check if a color is a keying color for chr011 (Sheep 2nd Job)"""
        # chr011 uses the same keying patterns as chr003
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr014_keying_color(self, color):
        """Check if a color is a keying color for chr014 (Lion 2nd Job)"""
        # chr014 uses more selective keying to avoid over-transparency
        # Only key out pure green and magenta, not green variants
        if color == (0, 255, 0) or color == (255, 0, 255):  # Pure green and magenta
            return True
        return False



    def is_green_padding(self, color):
        """Check if a color is green padding (0, 255, 0)"""
        return color == (0, 255, 0)

    def is_magenta_transparency(self, color):
        """Check if a color is magenta transparency (255, 0, 255)"""
        return color == (255, 0, 255)

    def is_blonde_like_color(self, color):
        """Check if a color is blonde-like (light yellow/orange)"""
        if not color or len(color) != 3:
            return False
        r, g, b = color
        # Check if it's a light color with yellow/orange tint
        return (r > 150 and g > 120 and b < 150 and 
                r > g and g > b and  # Red > Green > Blue (yellow/orange tint)
                (r + g + b) > 400)  # Light overall
    
    def is_hair_palette_keying_color(self, layer, color):
        """Check if a color is the keying color for a specific hair palette"""
        if layer.palette_type != "hair":
            return False
        
        # For chr001 hair palettes, always ignore 00FF00 (pure green)
        if self.current_character == "chr001" and color == (0, 255, 0):
            return True
        
        # For chr014 hair palettes, be more selective to avoid over-transparency
        if self.current_character == "chr014":
            # Only key out pure green and magenta, not green variants
            if color == (0, 255, 0) or color == (255, 0, 255):  # Pure green and magenta
                return True
            return False
        
        # Universal keying colors for other characters
        if self.is_universal_keying_color(color) or color == (255, 0, 255):  # Magenta
            return True
    
        return False

    def is_fashion_palette_keying_color(self, layer, color, index):
        """Check if a color is a keying color for a fashion palette"""
        if not layer.palette_type.startswith("fashion_"):
            return False
        
        # For chr004 fashion palettes, ignore 00FF00 and the last color (index 255) no matter what
        if self.current_character == "chr004":
            if color == (0, 255, 0):  # Pure green
                return True
            if index == 255:  # Last color in palette - always ignore
                return True
            return False
        
        # Universal keying colors for ALL characters
        if self.is_universal_keying_color(color) or color == (255, 0, 255):  # Magenta
            return True
        
        # For other characters, use standard keying colors
        return (self.is_green_padding(color) or 
                self.is_magenta_transparency(color))

    def get_character_palette_ranges(self, char_num, palette_type):
        """Get the allowed index ranges for a specific character and palette type"""
        # Comprehensive hard-coded palette ranges based on gap analysis
        character_ranges = {
            "001": {
                "fashion_1": [range(111, 128)],  # w00-w06: 111-127
                "fashion_2": [range(128, 152)],  # w10-w16: 128-151
                "fashion_3": [range(154, 160)],  # w20-w26: 154-159
                "fashion_4": [range(160, 169)],  # w30-w36: 160-168
                "fashion_5": [range(173, 192)],  # w40-w46: 173-191
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "002": {
                "fashion_1": [range(111, 128)],  # w00-w06: 111-127
                "fashion_2": [range(128, 137)],  # w10-w16: 128-136
                "fashion_3": [range(140, 144)],  # w20-w26: 140-143
                "fashion_4": [range(144, 154)],  # w30-w36: 144-153
                "fashion_5": [range(160, 172)],  # w40-w46: 160-171
                "fashion_6": [range(176, 185)],  # w50-w56: 176-184
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "003": {
                "fashion_1": [range(0, 254)],  # w00-w06: 0-253
                "fashion_2": [range(0, 135)],  # w10-w16: 0-134
                "fashion_3": [range(0, 136), range(137, 144)],  # w20-w26: 0-135, 137-143
                "fashion_4": [range(0, 136), range(144, 154)],  # w30-w36: 0-135, 144-153
                "fashion_5": [range(0, 154), range(155, 160)],  # w40-w46: 0-153, 155-159
                "fashion_6": [range(0, 175)],  # w50-w56: 0-174
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "004": {
                "fashion_1": [range(111, 133)],  # w00-w06: 111-132
                "fashion_2": [range(134, 145)],  # w10-w16: 134-144
                "fashion_3": [range(146, 160)],  # w20-w26: 146-159
                "fashion_4": [range(160, 172)],  # w30-w36: 160-171
                "fashion_5": [range(176, 198)],  # w40-w46: 176-197
                "hair": [range(208, 226)]  # Hair palettes: 208-219
            },
            "005": {
                "fashion_1": [range(111, 119)],  # w00-w06: 111-118
                "fashion_2": [range(122, 128)],  # w10-w16: 122-127
                "fashion_3": [range(128, 139)],  # w20-w26: 128-138
                "fashion_4": [range(140, 144)],  # w30-w36: 140-143
                "fashion_5": [range(144, 208)],  # w40-w46: 144-207
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "006": {
                "fashion_1": [range(111, 147)],  # w00-w06: 111-146
                "fashion_2": [range(148, 166)],  # w10-w16: 148-165
                "fashion_3": [range(167, 190)],  # w20-w26: 167-189
                "fashion_4": [range(191, 202)],  # w30-w36: 191-201
                "fashion_5": [range(202, 208)],  # w40-w46: 202-207
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "007": {
                "fashion_1": [range(111, 120)],  # w00-w06: 111-119
                "fashion_2": [range(124, 128)],  # w10-w16: 124-127
                "fashion_3": [range(128, 138)],  # w20-w26: 128-137
                "fashion_4": [range(144, 168)],  # w30-w36: 144-167
                "fashion_5": [range(169, 192)],  # w40-w46: 169-191
                "fashion_6": [range(192, 202)],  # w50-w56: 192-201
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "008": {
                "fashion_1": [range(0, 95), range(111, 134)],  # w00-w06: 0-94, 111-133
                "fashion_2": [range(137, 144)],  # w10-w16: 137-143
                "fashion_3": [range(144, 151)],  # w20-w26: 144-150
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "009": {
                "fashion_1": [range(111, 127)],  # w00-w04: 111-126
                "fashion_2": [range(128, 152)],  # w10-w14: 128-151
                "fashion_3": [range(153, 157)],  # w20-w24: 153-156
                "fashion_4": [range(158, 163)],  # w30-w34: 158-162
                "fashion_5": [range(164, 171)],  # w40-w44: 164-170
                "fashion_6": [range(172, 178)],  # w50-w54: 172-177
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "010": {
                "fashion_1": [range(111, 122)],  # w00-w04: 111-121
                "fashion_2": [range(123, 149)],  # w10-w14: 123-148
                "fashion_3": [range(150, 158)],  # w20-w24: 150-157
                "fashion_4": [range(159, 176)],  # w30-w34: 159-175
                "fashion_5": [range(177, 201)],  # w40-w44: 177-200
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "011": {
                "fashion_1": [range(0, 110), range(111, 137)],  # w00-w04: 0-109, 111-136
                "fashion_2": [range(0, 137), range(138, 149)],  # w10-w14: 0-136, 138-148
                "fashion_3": [range(0, 149), range(150, 236)],  # w20-w24: 0-148, 150-235
                "fashion_4": [range(0, 177)],  # w30-w34: 0-176
                "fashion_5": [range(0, 177), range(178, 198)],  # w40-w44: 0-176, 178-197
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "012": {
                "fashion_1": [range(111, 121)],  # w00-w04: 111-120
                "fashion_2": [range(122, 133)],  # w10-w14: 122-132
                "fashion_3": [range(134, 159)],  # w20-w24: 134-158
                "fashion_4": [range(160, 172)],  # w30-w34: 160-171
                "fashion_5": [range(173, 195)],  # w40-w44: 173-194
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "013": {
                "fashion_1": [range(111, 131)],  # w00-w04: 111-130
                "fashion_2": [range(132, 148)],  # w10-w14: 131-148
                "fashion_3": [range(149, 153)],  # w20-w24: 149-157
                "fashion_4": [range(154, 157)],  # w30-w34: 158-165
                "fashion_5": [range(158, 177)],  # Shoes: 166-176
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "014": {
                "fashion_1": [range(111, 116)],  # w00-w04: 111-115
                "fashion_2": [range(118, 155)],  # w10-w14: 118-154
                "fashion_3": [range(156, 165)],  # w20-w24: 156-164
                "fashion_4": [range(166, 172)],  # w30-w34: 166-171
                "fashion_5": [range(173, 185)],  # w40-w44: 173-184
                "hair": [range(208, 232)]  # Hair palettes: 208-231
            },
            "015": {
                "fashion_1": [range(111, 123)],  # w00-w04: 111-122
                "fashion_2": [range(124, 132)],  # w10-w14: 124-131
                "fashion_3": [range(133, 143)],  # w20-w24: 133-142
                "fashion_4": [range(144, 149)],  # w30-w34: 144-148
                "fashion_5": [range(150, 164)],  # w40-w44: 150-163
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "016": {
                "fashion_1": [range(111, 121)],  # w00-w04: 111-120
                "fashion_2": [range(122, 148)],  # w10-w14: 122-147
                "fashion_3": [range(149, 156)],  # w20-w24: 149-155
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "017": {
                "fashion_1": [range(111, 124)],  # w00-w03: 111-123
                "fashion_2": [range(128, 141)],  # w10-w13: 128-140
                "fashion_3": [range(144, 160)],  # w20-w23: 144-159
                "fashion_4": [range(160, 168), range(170, 176)],  # w30-w33: 160-167, 170-175
                "fashion_5": [range(176, 190)],  # w40-w43, w50: 176-189
                "3rd_job_base": [range(111, 190)],  # 3rd job base fashion: 111-189
                "hair": [range(208, 232)]  # Hair palettes: 208-231
            },
            "018": {
                "fashion_1": [range(111, 113)],  # w00-w03: 111-112
                "fashion_2": [range(116, 149)],  # w10-w13: 116-148
                "fashion_3": [range(150, 157), range(158, 174)],  # w20-w23: 150-156, 158-173
                "fashion_4": [range(176, 181)],  # w30-w33: 176-180
                "fashion_5": [range(181, 184), range(187, 205)],  # w40-w41, w43: 181-183, 187-204
                "fashion_6": [range(187, 205)],  # w50-w51: 187-204
                "3rd_job_base": [range(111, 205)],  # 3rd job base fashion: 111-204
                "hair": [range(208, 231)]  # Hair palettes: 208-230
            },
            "019": {
                "fashion_1": [range(0, 110), range(111, 141)],  # w00-w03: 0-109, 111-140
                "fashion_2": [range(0, 143), range(144, 155)],  # w10-w13: 0-142, 144-154
                "fashion_3": [range(0, 155), range(156, 174)],  # w20-w23: 0-154, 156-173
                "fashion_4": [range(0, 174), range(175, 192)],  # w30-w33: 0-173, 175-191
                "fashion_5": [range(0, 191), range(195, 208)],  # w40-w43: 0-190, 195-207
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "020": {
                "fashion_1": [range(111, 138)],  # w00-w03: 111-137
                "fashion_2": [range(140, 148)],  # w10-w13: 140-147
                "fashion_3": [range(150, 158)],  # w20-w23: 150-157
                "fashion_4": [range(160, 172)],  # w30-w33: 160-171
                "fashion_5": [range(173, 192)],  # w40-w43: 173-191
                "3rd_job_base": [range(111, 192)],  # 3rd job base fashion: 111-191
                "hair": [range(208, 219)]  # Hair palettes: 208-218
            },
            "021": {
                "fashion_1": [range(111, 132)],  # w00-w03: 111-131
                "fashion_2": [range(133, 137)],  # w10-w13: 133-136
                "fashion_3": [range(140, 152)],  # w20-w23: 140-151
                "fashion_4": [range(153, 168)],  # w30-w33: 153-167
                "fashion_5": [range(173, 185)],  # w40: 173-184
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "022": {
                "fashion_1": [range(111, 137)],  # w00-w03: 111-136
                "fashion_2": [range(140, 161)],  # w10-w13: 140-160
                "fashion_3": [range(164, 177)],  # w20-w23: 164-176
                "fashion_4": [range(180, 198)],  # w30-w33: 180-197
                "fashion_5": [range(158, 177)],  # w40: 158-176
                "3rd_job_base": [range(111, 198)],  # 3rd job base fashion: 111-197
                "hair": [range(208, 232)]  # Hair palettes: 208-231
            },
            "023": {
                "fashion_1": [range(111, 125), range(126, 144)],  # w00-w03: 111-124, 126-143
                "fashion_2": [range(144, 148)],  # w10-w13: 144-147
                "fashion_3": [range(150, 156), range(160, 186)],  # w20-w23: 150-155, 160-185
                "fashion_4": [range(188, 194)],  # w30-w33, w40-w41: 188-193
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "024": {
                "fashion_1": [range(111, 131)],  # 111-130
                "fashion_2": [range(134, 149)],  # 134-148
                "fashion_3": [range(150, 165)],  # 150-164
                "fashion_4": [range(166, 174)],  # 166-173
                "fashion_5": [range(1, 34), range(111, 131), range(134, 149), range(150, 165), range(166, 174), range(176, 182), range(208, 219)],  # w02, w12, w22, w32, w42 pattern (includes ALL required ranges)
                "fashion_6": [range(176, 182)],  # w40, w41, w43 pattern
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "100": {
                "fashion_1": [range(111, 142)],  # group 1: 111-141
                "fashion_2": [range(142, 154)],  # group 2: 142-153
                "fashion_3": [range(154, 168)],  # group 3: 154-167
                "fashion_4": [range(168, 174), range(189, 193)],  # group 4: 168-173 AND 189-192
                "fashion_5": [range(174, 177)],  # group 5: 174-176
                "fashion_6": [range(177, 189)],  # group 6: 177-188
                "fashion_7": [range(189, 193)],  # group 7: 189-192
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "101": {
                "fashion_1": [range(111, 142)],  # w00-w04: 111-141
                "fashion_2": [range(142, 156)],  # w10-w14: 142-155
                "fashion_3": [range(156, 174)],  # w20-w24: 156-173
                "fashion_4": [range(174, 178)],  # w30-w34: 174-177
                "fashion_5": [range(178, 190)],  # w40-w44: 178-189
                "fashion_6": [range(190, 193)],  # w50-w54: 190-192
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            },
            "102": {
                "fashion_1": [range(111, 118)],  # w00-w03: 111-117
                "fashion_2": [range(119, 147)],  # w10-w13: 119-146
                "fashion_3": [range(148, 151)],  # w20-w23: 148-150
                "fashion_4": [range(152, 166)],  # w30-w33: 152-165
                "fashion_5": [range(167, 175)],  # w40-w43: 167-174
                "fashion_6": [range(176, 182)],  # w50-w53: 176-181
                "fashion_7": [range(183, 192)],  # w60-w63: 183-191
                "fashion_8": [range(192, 208)],  # w70-w73: 192-207
                "hair": [range(208, 226)]  # Hair palettes: 208-225
            }
        }
        
        # Get ranges for this character and palette type
        if char_num in character_ranges and palette_type in character_ranges[char_num]:
            return character_ranges[char_num][palette_type]
        
        # Fallback: return all indices for unknown characters or palette types
        return [range(256)]

    def reset_scroll_positions(self):
        """Reset hair and fashion scroll positions to top"""
        if hasattr(self, 'hair_canvas'):
            self.hair_canvas.yview_moveto(0)
        if hasattr(self, 'fashion_canvas'):
            self.fashion_canvas.yview_moveto(0)

    def get_display_image_for_export(self):
        """Get the current image with palettes applied without updating display"""
        if not self.original_image:
            return None
            
        # Get the current frame index (respects user choice)
        frame_index = self.get_current_displayed_frame()
            
        original_img = self.character_images[self.current_character][frame_index]
        
        # Check if frame is within selected range
        if hasattr(self, 'custom_start_frame') and hasattr(self, 'custom_end_frame'):
            if frame_index < self.custom_start_frame or frame_index > self.custom_end_frame:
                # Return solid color image for out-of-range frames
                w, h = Image.open(original_img).size
                bg_img = Image.new("RGB", (w, h), self.background_color)
                return bg_img
        
        # Get the original palette
        original_palette = []
        try:
            with open(original_img, 'rb') as f:
                bmp = Image.open(f)
                original_palette = list(bmp.getpalette())
                bmp.close()
        except Exception:
            return None
            
        # Load original image and get its data
        with Image.open(original_img) as img:
            pixel_data = list(img.getdata())
            w, h = img.size

        # Create new image with background color
        bg_img = Image.new("RGB", (w, h), self.background_color)
        
        # Create a mask for non-transparent pixels (index 0 is transparent)
        mask_img = Image.new("L", (w, h), 0)  # L mode for single channel
        mask_data = [255 if p != 0 else 0 for p in pixel_data]
        mask_img.putdata(mask_data)
        
        # Create foreground image with current palettes
        fg_img = Image.new("P", (w, h))
        fg_img.putpalette([color for palette_color in self.get_merged_palette() for color in palette_color])
        fg_img.putdata(pixel_data)
        fg_img = fg_img.convert("RGB")
        
        # Composite foreground onto background using mask
        bg_img.paste(fg_img, (0, 0), mask_img)
        return bg_img
        
    def export_background_bmp(self, frame=None, force_portrait=False):
        """Export current image as BMP with background color
        
        Args:
            frame: Optional frame to export instead of current frame
            force_portrait: If True, forces portrait mode regardless of settings"""
        if not self.original_image:
            messagebox.showinfo("Notice", "No image loaded.")
            return
            
        # Save current state
        current_layers = [layer.active for layer in self.palette_layers]
            
        # Get base paths
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        export_dir = os.path.join(root_dir, "exports", "images")
        
        # Get the frame index for export (respects user choice)
        frame_index = frame if frame is not None else self.get_current_displayed_frame()
        
        # Save current portrait setting if forcing portrait
        old_portrait = self.use_portrait_export
        if force_portrait:
            self.use_portrait_export = True
        
        # Get base file name without extension using view count from statistics
        key = f"{self.current_character}_{self.current_job}"
        view_count = self.statistics.character_edits.get(key, {'views': 0})['views']
        base_name = f"{self.current_character}_view{view_count}"
        
        # Get the current image with all palettes applied
        if not hasattr(self, 'update_single_frame_display'):
            raise AttributeError("Cannot get current display image")
            
        img = self.get_display_image_for_export()
        if img is None:
            raise AttributeError("Failed to get current display image")
        
        try:
            # Get save path for regular BMP
            default_path = os.path.join(export_dir, f"{base_name}.bmp")
            file_path = filedialog.asksaveasfilename(
                defaultextension=".bmp",
                filetypes=[("BMP files", "*.bmp")],
                initialfile=os.path.basename(default_path),
                initialdir=os.path.dirname(default_path)
            )
            
            if not file_path:
                return
                
            # Get the target directory and base filename from user's chosen path
            target_dir = os.path.dirname(file_path)
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            
            # Prepare all export operations
            export_ops = []
            
            # Get save paths for each format
            regular_path = file_path  # Use exactly what the user chose
            portrait_path = os.path.join(target_dir, f"{base_filename}_illu.bmp")  # Just _illu for regular portraits
            
            # Regular BMP export
            def save_regular():
                img.save(regular_path, "BMP")
                return "Regular BMP"
            export_ops.append(save_regular)
            
            # Portrait export (if selected)
            if self.use_portrait_export:
                def save_portrait():
                    # Create a 105x105 image
                    x = (105 - img.width) // 2
                    y = (105 - img.height) // 2
                    
                    # Create mask for non-background pixels in the frame
                    mask = Image.new("L", img.size, 0)
                    for i, pixel in enumerate(img.getdata()):
                        if pixel != self.background_color:
                            mask.putpixel((i % img.width, i // img.width), 255)
                    
                    outputs = []
                    
                    # Handle regular background color output
                    if self.cute_bg_option in ["no_cute_bg", "both"]:
                        # Create image with user's background color
                        regular_img = Image.new("RGB", (105, 105), self.background_color)
                        regular_img.paste(img, (x, y), mask)
                        regular_img.save(portrait_path.replace(".bmp", "_illu.bmp"), "BMP", quality=24)
                        outputs.append("Portrait (105x105) with Background Color")
                    
                    # Handle cute background output
                    if self.cute_bg_option in ["cute_bg", "both"]:
                        if self.myshop_base is None:
                            messagebox.showerror("Error", "MyShop base image not found. Please ensure myshop_base.bmp exists in the nonremovable_assets folder.")
                            return "Failed: MyShop base image not found"
                        
                        # Create a copy of the base image and convert to RGB
                        cute_img = self.myshop_base.copy().convert("RGB")
                        
                        # Replace magenta (255, 0, 255) with user's background color
                        data = list(cute_img.getdata())
                        for i, pixel in enumerate(data):
                            if pixel == (255, 0, 255):  # Magenta
                                data[i] = self.background_color
                        cute_img.putdata(data)
                        
                        # Paste the frame onto the base image
                        cute_img.paste(img, (x, y), mask)
                        cute_img.save(portrait_path.replace(".bmp", "_illu_cute.bmp"), "BMP", quality=24)
                        outputs.append("Portrait (105x105) with Cute BG")
                    
                    return " & ".join(outputs)
                export_ops.append(save_portrait)
            
            
            # Execute all export operations
            exported = []
            errors = []
            for export_op in export_ops:
                try:
                    result = export_op()
                    exported.append(result)
                except Exception as e:
                    errors.append(str(e))
            
            # Show results
            if exported:
                success_msg = "Exported:\n- " + "\n- ".join(exported)
                if errors:
                    success_msg += "\n\nErrors:\n- " + "\n- ".join(errors)
                messagebox.showinfo("Export Complete", success_msg)
            else:
                error_msg = "Failed to export any files:\n- " + "\n- ".join(errors)
                messagebox.showerror("Export Failed", error_msg)
                
            # Restore layer state
            for layer, was_active in zip(self.palette_layers, current_layers):
                layer.active = was_active
                
            # Restore portrait setting if it was forced
            if force_portrait:
                self.use_portrait_export = old_portrait
            
        except Exception as e:
            # Restore layer state even on error
            for layer, was_active in zip(self.palette_layers, current_layers):
                layer.active = was_active
                
            # Restore portrait setting if it was forced
            if force_portrait:
                self.use_portrait_export = old_portrait
                
            messagebox.showerror("Error", f"Failed to export image: {e}")
            
    def export_transparent_png(self):
        """Export the current frame as a transparent PNG with palettes applied"""
        if not self.original_image:
            messagebox.showinfo("Notice", "Please load a character image first.")
            return
            
        # Save current state
        current_layers = [layer.active for layer in self.palette_layers]
        
        # Get base paths
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        export_dir = os.path.join(root_dir, "exports", "images")
        
        # Get the frame index for export (respects user choice)
        frame_index = self.get_current_displayed_frame()
        
        # Get base file name without extension using view count from statistics
        key = f"{self.current_character}_{self.current_job}"
        view_count = self.statistics.character_edits.get(key, {'views': 0})['views']
        base_name = f"{self.current_character}_view{view_count}"
        
        # Get save path for regular PNG
        default_path = os.path.join(export_dir, f"{base_name}.png")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Images", "*.png")],
            initialfile=os.path.basename(default_path),
            initialdir=os.path.dirname(default_path)
        )
        
        if not file_path:
            return
            
        # Get the target directory and base filename from user's chosen path
        target_dir = os.path.dirname(file_path)
        base_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        try:
            # Get the merged palette
            merged_palette = self.get_merged_palette()
            
            # Get the current image with all palettes applied
            img = self.get_display_image_for_export()
            if img is None:
                raise AttributeError("Failed to get current display image")
            
            # Prepare export operations
            export_ops = []
            
            # Regular PNG export
            def save_regular():
                # Convert to RGBA to handle transparency
                rgba_img = img.convert("RGBA")
                pixels = rgba_img.load()
                
                # Apply character-specific transparency
                if hasattr(self, 'current_character') and self.current_character:
                    char_num = self.current_character[3:]
                    transparent_count = 0
                    total_pixels = img.width * img.height
                    
                    for y in range(img.height):
                        for x in range(img.width):
                            pixel = img.getpixel((x, y))
                            should_make_transparent = False
                            
                            # Check if the pixel should be transparent
                            if pixel != (0, 0, 0):  # Never make black transparent
                                if char_num == "014":
                                    if self.is_chr014_keying_color(pixel):
                                        should_make_transparent = True
                                else:
                                    if self.is_universal_keying_color(pixel) or pixel == (255, 0, 255):  # Magenta
                                        should_make_transparent = True
                            
                            if should_make_transparent:
                                pixels[x, y] = (0, 0, 0, 0)  # Transparent
                                transparent_count += 1
                
                # Save regular PNG
                rgba_img.save(file_path, "PNG")
                return "Regular PNG"
            
            export_ops.append(save_regular)
            
            # Portrait export (if selected)
            if self.use_portrait_export:
                def save_portrait():
                    # Create a 105x105 image
                    x = (105 - img.width) // 2
                    y = (105 - img.height) // 2
                    
                    # Create mask for non-background pixels in the frame
                    mask = Image.new("L", img.size, 0)
                    for i, pixel in enumerate(img.getdata()):
                        if pixel != self.background_color:
                            mask.putpixel((i % img.width, i // img.width), 255)
                    
                    outputs = []
                    
                    # Handle regular portrait output with transparency
                    if self.cute_bg_option in ["no_cute_bg", "both"]:
                        # Create transparent base image
                        portrait_img = Image.new("RGBA", (105, 105), (0, 0, 0, 0))
                        # Convert frame to RGBA for transparency
                        frame_rgba = img.convert("RGBA")
                        # Make background color transparent
                        frame_data = list(frame_rgba.getdata())
                        for i, pixel in enumerate(frame_data):
                            if pixel[:3] == self.background_color:
                                frame_data[i] = (0, 0, 0, 0)
                        frame_rgba.putdata(frame_data)
                        # Paste the frame onto the transparent base
                        portrait_img.paste(frame_rgba, (x, y), mask)
                        # Save as PNG with _illu suffix (no "regular" suffix)
                        portrait_path = os.path.join(target_dir, f"{base_filename}_illu.png")
                        portrait_img.save(portrait_path, "PNG")
                        outputs.append("Portrait (105x105) with Transparency")
                    
                    # Handle cute background output
                    if self.cute_bg_option in ["cute_bg", "both"]:
                        if self.myshop_base is None:
                            messagebox.showerror("Error", "MyShop base image not found. Please ensure myshop_base.bmp exists in the nonremovable_assets folder.")
                            return "Failed: MyShop base image not found"
                        
                        # Create a copy of the base image and convert to RGBA
                        cute_img = self.myshop_base.copy().convert("RGBA")
                        
                        # Replace magenta with transparency
                        data = list(cute_img.getdata())
                        for i, pixel in enumerate(data):
                            if pixel[:3] == (255, 0, 255):  # Magenta
                                data[i] = (0, 0, 0, 0)  # Transparent
                        cute_img.putdata(data)
                        
                        # Convert frame to RGBA and make background transparent
                        frame_rgba = img.convert("RGBA")
                        frame_data = list(frame_rgba.getdata())
                        for i, pixel in enumerate(frame_data):
                            if pixel[:3] == self.background_color:
                                frame_data[i] = (0, 0, 0, 0)
                        frame_rgba.putdata(frame_data)
                        
                        # Paste the frame onto the base image
                        cute_img.paste(frame_rgba, (x, y), mask)
                        # Save as PNG with _illu_cute suffix
                        cute_path = os.path.join(target_dir, f"{base_filename}_illu_cute.png")
                        cute_img.save(cute_path, "PNG")
                        outputs.append("Portrait (105x105) with Cute BG")
                    
                    return " & ".join(outputs)
                
                export_ops.append(save_portrait)
            
            # Execute all export operations
            exported = []
            errors = []
            for export_op in export_ops:
                try:
                    result = export_op()
                    exported.append(result)
                except Exception as e:
                    errors.append(str(e))
            
            # Show results
            if exported:
                success_msg = "Exported:\n- " + "\n- ".join(exported)
                if errors:
                    success_msg += "\n\nErrors:\n- " + "\n- ".join(errors)
                messagebox.showinfo("Export Complete", success_msg)
            else:
                error_msg = "Failed to export any files:\n- " + "\n- ".join(errors)
                messagebox.showerror("Export Failed", error_msg)
                
            # Restore layer state
            for layer, was_active in zip(self.palette_layers, current_layers):
                layer.active = was_active
            
        except Exception as e:
            # Restore layer state even on error
            for layer, was_active in zip(self.palette_layers, current_layers):
                layer.active = was_active
            messagebox.showerror("Error", f"Export failed: {e}")

    def export_all_frames(self):
        """Export all frames in the current character's folder with current palettes applied"""
        if not hasattr(self, 'current_character') or not self.current_character:
            messagebox.showinfo("Notice", "Please select a character first.")
            return
            
        # Save current state
        current_layers = [layer.active for layer in self.palette_layers]
        
        if not self.character_images or self.current_character not in self.character_images:
            messagebox.showinfo("Notice", "No images found for this character.")
            return
        
        # Create a folder name based on character and current palettes
        char_name = self.character_var.get()
        job_name = self.job_var.get()
        
        # Clean up job name (remove "Job" part)
        if job_name.endswith(" Job"):
            job_name = job_name[:-4]  # Remove " Job" suffix
        
        # Get selected palette names for folder naming
        palette_parts = []
        
        # Add hair palette (h# format)
        if self.hair_var.get() != "NONE":
            hair_name = os.path.basename(self.hair_var.get())
            hair_name = hair_name.replace('.pal', '')
            if hair_name.startswith('chr') and '_' in hair_name:
                hair_name = hair_name.split('_', 1)[1]  # Remove chr###_ prefix
            palette_parts.append(f"h{hair_name}")
        
        # Add fashion palettes (f1w##, f2w##, etc.)
        for fashion_type, var in self.fashion_vars.items():
            if var.get() != "NONE":
                fashion_name = os.path.basename(var.get())
                fashion_name = fashion_name.replace('.pal', '')
                if fashion_name.startswith('chr') and '_' in fashion_name:
                    fashion_name = fashion_name.split('_', 1)[1]  # Remove chr###_ prefix
                
                # Extract fashion type number (fashion_1 -> f1, fashion_2 -> f2, etc.)
                fashion_num = fashion_type.split('_')[1]
                palette_parts.append(f"f{fashion_num}{fashion_name}")
        
        # Add 3rd job base fashion (just the number)
        if hasattr(self, 'third_job_var') and self.third_job_var.get() != "NONE":
            third_job_name = os.path.basename(self.third_job_var.get())
            third_job_name = third_job_name.replace('.pal', '')
            palette_parts.append(third_job_name)
        
        # Create folder name
        if palette_parts:
            folder_name = f"{char_name}_{job_name}_{'_'.join(palette_parts)}"
        else:
            folder_name = f"{char_name}_{job_name}_original"
        
        # Clean folder name (remove invalid characters and fix path separators)
        folder_name = "".join(c for c in folder_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        folder_name = folder_name.replace(' ', '_')
        folder_name = folder_name.replace('\\', '_')  # Replace backslashes with underscores
        folder_name = folder_name.replace('/', '_')   # Replace forward slashes with underscores
        
        # Ask user for base output directory (default to exports/images)
        default_export_dir = os.path.join(self.root_dir, "exports", "images")
        base_output_dir = filedialog.askdirectory(
            title="Select base directory for export",
            initialdir=default_export_dir
        )
        if not base_output_dir:
            return
        
        # Create the specific folder
        output_dir = os.path.join(base_output_dir, folder_name)
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Export directory created: {output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create export directory: {e}")
            return
        
        try:
            images = self.character_images[self.current_character]
            total_images = len(images)
            
            # Show progress dialog
            progress_window = tk.Toplevel(self.master)
            progress_window.title("Exporting Frames")
            progress_window.transient(self.master)
            progress_window.grab_set()
            
            progress_label = tk.Label(progress_window, text="Exporting frames...")
            progress_label.pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_window, length=250, mode='determinate')
            progress_bar.pack(pady=5)
            
            # Center the progress window after content is created
            progress_window.update_idletasks()
            self._center_window_on_parent(progress_window, self.master)
            
            exported_count = 0
            
            for i, image_path in enumerate(images):
                # Update progress
                progress_bar['value'] = (i / total_images) * 100
                progress_label.config(text=f"Exporting frame {i+1}/{total_images}")
                progress_window.update()
                
                try:
                    # Load the image
                    img = Image.open(image_path)
                    
                    # Apply the same processing as the current frame
                    if img.mode == 'P':
                        # Already palette mode - preserve original structure
                        original_img = img.copy()
                        raw_palette = img.getpalette()
                        original_palette = [
                            (raw_palette[j*3], raw_palette[j*3+1], raw_palette[j*3+2])
                            for j in range(PALETTE_SIZE)
                        ]
                    else:
                        # For non-palette images, convert more carefully to preserve transparency
                        if img.mode in ['RGBA', 'LA', 'PA']:
                            # Handle alpha channel properly
                            if img.mode == 'RGBA':
                                # Create a new image with transparent background
                                new_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
                                new_img.paste(img, mask=img.split()[-1])
                                img = new_img
                            else:
                                # Convert to RGBA first
                                img = img.convert('RGBA')
                        
                        # Convert to RGB if needed, but preserve transparency info
                        if img.mode == 'RGBA':
                            # Create a palette that preserves transparency
                            background = Image.new('RGB', img.size, (0, 255, 0))  # Use green as background
                            background.paste(img, mask=img.split()[-1])
                            img = background
                        elif img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Use a more careful quantization that preserves keying colors
                        img_palette = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
                        raw_palette = img_palette.getpalette()
                        if raw_palette:
                            original_palette = [
                                (raw_palette[j*3], raw_palette[j*3+1], raw_palette[j*3+2])
                                for j in range(min(len(raw_palette)//3, PALETTE_SIZE))
                            ]
                            while len(original_palette) < PALETTE_SIZE:
                                original_palette.append((0, 255, 0))  # Fill with green instead of black
                        else:
                            original_palette = [(0, 255, 0)] * PALETTE_SIZE  # Use green instead of black
                        
                        original_img = img_palette
                    
                    # Apply current palette layers using the same logic as single frame
                    # Temporarily set the original_palette for this image
                    original_original_palette = self.original_palette
                    self.original_palette = original_palette
                    
                    # Get the merged palette using the same method as single frame
                    result_palette = self.get_merged_palette()
                    
                    # Restore the original palette
                    self.original_palette = original_original_palette
                    
                    # Create output image
                    w, h = original_img.size
                    display_img = Image.new("P", (w, h))
                    display_img.putpalette([color for palette_color in result_palette for color in palette_color])
                    display_img.putdata(original_img.getdata())
                    
                    # Convert to RGBA and apply transparency
                    rgba_img = display_img.convert("RGBA")
                    pixels = rgba_img.load()
                    
                    # Apply character-specific transparency based on original palette colors
                    char_num = self.current_character[3:]
                    
                    # Debug: Count transparent pixels for this frame
                    transparent_count = 0
                    total_pixels = w * h
                    
                    # Get original image pixel data to check original palette indices
                    original_pixel_data = list(original_img.getdata())
                    
                    for y in range(h):
                        for x in range(w):
                            should_make_transparent = False
                            
                            # Get the original palette index for this pixel
                            pixel_index = y * w + x
                            if pixel_index < len(original_pixel_data):
                                palette_index = original_pixel_data[pixel_index]
                                if palette_index < len(original_palette):
                                    original_color = original_palette[palette_index]
                                    
                                    # Check if the original color was a keying color
                                    # Never make black transparent
                                    if original_color != (0, 0, 0):
                                        # Use character-specific keying logic
                                        if char_num == "014":
                                            # chr014 uses more selective keying
                                            if self.is_chr014_keying_color(original_color):
                                                should_make_transparent = True
                                        else:
                                            # Universal keying colors for other characters
                                            if self.is_universal_keying_color(original_color) or original_color == (255, 0, 255):  # Magenta
                                                should_make_transparent = True
                            
                            if should_make_transparent:
                                pixels[x, y] = (0, 0, 0, 0)
                                transparent_count += 1
                    
                    # Debug: Show transparency info for this frame
                    transparency_percentage = (transparent_count / total_pixels) * 100
    
                    
                    # Save the image
                    filename = os.path.basename(image_path)
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(output_dir, f"{name}.png")
                    rgba_img.save(output_path, "PNG")
                    
                    exported_count += 1
                    
                except Exception as e:
                    print(f"CONSOLE ERROR MSG: Error processing {image_path}: {e}")
                    continue
            
            progress_window.destroy()
            messagebox.showinfo("Success", f"Exported {exported_count}/{total_images} frames to:\n{output_dir}")
            
            # Restore layer state
            for layer, was_active in zip(self.palette_layers, current_layers):
                layer.active = was_active
            
        except Exception as e:
            # Restore layer state even on error
            for layer, was_active in zip(self.palette_layers, current_layers):
                layer.active = was_active
            messagebox.showerror("Error", f"Export failed: {e}")

    def update_bg_color_button(self):
        """Update the background color button appearance"""
        self.bg_color_button.configure(bg=f'#{self.background_color[0]:02x}{self.background_color[1]:02x}{self.background_color[2]:02x}')

    def pick_background_color(self):
        """Open color picker to change background color for preview"""
        from tkinter import colorchooser
        
        # Open color picker dialog
        color = colorchooser.askcolor(title="Choose Background Color", color=self.background_color)
        
        if color[1]:  # color[1] contains the hex color, color[0] contains RGB tuple
            # Convert hex to RGB
            hex_color = color[1]
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            self.background_color = (r, g, b)
            
            # Update the button color to show current background
            self.bg_color_button.configure(bg=hex_color)
            
            # Refresh the display with new background color
            self._debounced_display_update()
    
    def export_pal(self):
        """Export all active palettes as one combined palette in either VGA 24-bit format or PNG grid"""
        if not self.palette_layers:
            messagebox.showinfo("Notice", "No palette layers loaded.")
            return
        
        # Get all active layers
        active_layers = [layer for layer in self.palette_layers if layer.active]
        
        if not active_layers:
            messagebox.showinfo("Notice", "No active palette layers to export.")
            return
        
        # Set initial directory based on palette format
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Set file type and initial directory based on palette format
        if self.palette_format == "pal":
            file_types = [("VGA 24-bit Palette Files", "*.pal")]
            default_ext = ".pal"
            initial_dir = os.path.join(root_dir, "exports", "full_pals")
        else:  # png
            file_types = [("PNG Files", "*.png")]
            default_ext = ".png"
            initial_dir = os.path.join(root_dir, "exports", "images")
        
        path = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            initialdir=initial_dir,
            filetypes=file_types
        )
        if not path:
            return
        
        try:
            # Get the merged palette (same logic as used for display/export)
            merged_palette = self.get_merged_palette()
            
            if self.palette_format == "pal":
                # Ensure we have exactly 256 colors for VGA palette
                while len(merged_palette) < 256:
                    merged_palette.append((0, 0, 0))  # Fill with black if needed
                
                # Write VGA 24-bit format: each color as 3 bytes (R, G, B) in sequence
                with open(path, "wb") as f:
                    for r, g, b in merged_palette[:256]:  # Ensure exactly 256 colors
                        f.write(bytes([r, g, b]))
            else:  # PNG grid
                # Create a 503x503 image (16x16 grid where each color is ~31.4375x31.4375)
                grid_img = Image.new("RGB", (503, 503), (0, 0, 0))
                cell_size = 503 // 16  # This gives us 31 pixels with some remainder
                
                # Fill in the colors in a 16x16 grid
                for i, color in enumerate(merged_palette):
                    if i >= 256:  # Maximum 256 colors in 16x16 grid
                        break
                    
                    # Calculate position in 16x16 grid
                    grid_x = i % 16
                    grid_y = i // 16
                    
                    # Calculate pixel ranges for this cell, handling the remainder
                    x_start = (grid_x * 503) // 16
                    x_end = ((grid_x + 1) * 503) // 16
                    y_start = (grid_y * 503) // 16
                    y_end = ((grid_y + 1) * 503) // 16
                    
                    # Fill the exact pixel range for this cell
                    for px in range(x_start, x_end):
                        for py in range(y_start, y_end):
                            grid_img.putpixel((px, py), color)
                
                # Save the PNG
                grid_img.save(path, "PNG")
            
            # Show which layers were combined
            layer_names = [layer.name for layer in active_layers]
            messagebox.showinfo("Success", f"Exported VGA 24-bit palette to {path}\n\nCombined layers:\n" + "\n".join(f"• {name}" for name in layer_names))
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    # === Live Edit Palette (Per-Item with Dropdown) ===
    
    # === Live Edit Palette (Per-Item) with Embedded Color Picker ===
    
    def open_live_palette_editor(self):
        """Edit ONE active palette layer with an embedded RGB/HEX picker.
        Added: Multi-select mode + Shift-click range selection."""
        # Store current UI mode before opening editor
        current_ui_mode = getattr(self, 'live_pal_ui_mode', 'Simple')
        
        # Check if live editor is already open
        if hasattr(self, '_live_editor_window') and self._live_editor_window and self._live_editor_window.winfo_exists():
            self._live_editor_window.lift()
            self._live_editor_window.focus_force()
            return
            
        # Track palette editing
        if hasattr(self, 'current_character'):
            current_job = self.job_var.get() if hasattr(self, 'job_var') else None
            if current_job:
                self.statistics.add_character_view(self.current_character, current_job)
                self._save_statistics()
            
        active_layers = [ly for ly in self.palette_layers if getattr(ly, "active", False)]
        if not active_layers:
            messagebox.showinfo("Live Edit Palette", "No active palette layer. Select Hair or a Fashion item first.")
            return

        # Prefer an active fashion layer if present
        default_idx = 0
        for i, ly in enumerate(active_layers):
            if str(getattr(ly, "palette_type", "")).startswith("fashion_"):
                default_idx = i
                break

        # Build display names
        names = []
        for ly in active_layers:
            ptype = str(getattr(ly, "palette_type", ""))
            if ptype == "hair":
                disp = "Hair"
            elif ptype == "3rd_job_base":
                disp = "3rd Job Base"
            elif ptype.startswith("fashion_"):
                try:
                    disp = self.get_fashion_type_name(self.current_character, ptype)
                except Exception:
                    disp = ptype.replace("fashion_", "Fashion ").replace("_"," ").title()
            else:
                disp = ptype
            names.append(f"{disp} — {ly.name}")
        # Session warning tracker for non-impact edits
        self._live_warned_types = set()
        # Warn up front if default target is Hair or 3rd Job Base
        try:
            default_layer = active_layers[default_idx]
            # Store UI mode before warning dialog
            current_ui_mode = getattr(self, 'live_pal_ui_mode', 'Simple')
            if not self._warn_if_nonimpact(getattr(default_layer, "palette_type", "")):
                # If user clicked "No", bring existing live editor to front if it exists
                if hasattr(self, '_live_editor_window') and self._live_editor_window and self._live_editor_window.winfo_exists():
                    self._live_editor_window.lift()
                    self._live_editor_window.focus_force()
                return
            # Restore UI mode after warning dialog
            self.live_pal_ui_mode = current_ui_mode
            self._live_prev_target_name = ""
        except Exception:
            pass


        # State
        self._live_layers = active_layers
        self._live_target_name = tk.StringVar(value=names[default_idx])
        self._live_prev_target_name = names[default_idx]
        self._live_name_to_index = {n:i for i,n in enumerate(names)}
        self._live_selected_index = 0
        self._multi_select = tk.BooleanVar(value=False)
        self._selected_indices = set()
        self._last_clicked_index = None
        
        # Store original colors for all layers to restore when editor closes
        self._live_original_colors = {}
        self._live_saved_layers = set()  # Track which layers were saved
        self._updating_live_selection = False  # Flag to prevent grid recreation during selection updates
        
        # Temporary palette cache to preserve changes during editor session
        self._live_temp_palette_cache = {}  # Cache for temporary changes during session
        
        for i, layer in enumerate(active_layers):
            self._live_original_colors[names[i]] = layer.colors.copy()
            # Initialize temp cache with current colors (which may already have changes)
            self._live_temp_palette_cache[names[i]] = layer.colors.copy()
        
        # Track which job/character each palette type belongs to
        self._live_palette_job_mapping = {}
        # Initialize mapping based on current layers
        for i, layer in enumerate(active_layers):
            if hasattr(layer, "palette_type"):
                # Extract character number from the name (e.g. chr001)
                char_match = re.search(r'chr(\d{3})', names[i])
                if char_match:
                    char_num = char_match.group(1)
                    if char_num in CHARACTER_MAPPING:
                        char_info = CHARACTER_MAPPING[char_num]
                        self._live_palette_job_mapping[names[i]] = {
                            'palette_type': layer.palette_type,
                            'character': char_info['name'],
                            'job': char_info['job']
                        }

        self._live_editor_window = tk.Toplevel(self.master)
        self._live_editor_window.title("Live Edit Palette")
        self._live_editor_window.geometry("810x450")  # 30px wider window
        self._live_editor_window.resizable(False, False)
        
        # Restore the UI mode that was stored earlier
        self.live_pal_ui_mode = current_ui_mode
        
        # Add callback to refresh custom pals when window is closed
        def on_window_close():
            # Restore original colors only for layers that weren't saved
            colors_were_restored = False
            if hasattr(self, '_live_original_colors'):
                saved_layers = getattr(self, '_live_saved_layers', set())
                for layer_name, original_colors in self._live_original_colors.items():
                    if layer_name not in saved_layers and layer_name in self._live_name_to_index:
                        layer_idx = self._live_name_to_index[layer_name]
                        if layer_idx < len(self._live_layers):
                            self._live_layers[layer_idx].colors = original_colors.copy()
                            colors_were_restored = True
                # Clear the original colors storage
                delattr(self, '_live_original_colors')
                if hasattr(self, '_live_saved_layers'):
                    delattr(self, '_live_saved_layers')
                # Clear the temp cache
                if hasattr(self, '_live_temp_palette_cache'):
                    delattr(self, '_live_temp_palette_cache')
            
            self.refresh_custom_pals(update_ui=True)  # Update UI to refresh custom pals display
            
            # Update the main display to reflect restored palette colors
            if colors_were_restored:
                # Reload palettes to ensure the restored colors are properly applied
                self.load_palettes()
                self._debounced_display_update()
            
            self._live_editor_window.destroy()
            self._live_editor_window = None  # Clear the instance variable
            
            # Re-enable icon editor button when live editor closes
            self._update_icon_editor_button_state()
        
        self._live_editor_window.protocol("WM_DELETE_WINDOW", on_window_close)

        # Top bar
        top = tk.Frame(self._live_editor_window); top.pack(fill="x", padx=6, pady=6)
        tk.Label(top, text="Edit which:").pack(side="left")
        tk.OptionMenu(top, self._live_target_name, *names, command=self._live_on_target_changed).pack(side="left", padx=(4,8))
        tk.Checkbutton(top, text="Multi-select", variable=self._multi_select, command=self._live_multi_toggled).pack(side="left", padx=(8,8))
        tk.Button(top, text="Select All", command=self._live_select_all).pack(side="left", padx=(0,5))
        tk.Button(top, text="Clear Sel", command=self._live_clear_selection).pack(side="left")
        self._sel_count_lbl = tk.Label(top, text="(0 selected)"); self._sel_count_lbl.pack(side="left", padx=(6,0))
        tk.Button(top, text="Save Item .pal", command=self._live_save_item_pal).pack(side="left", padx=(12,8))
        tk.Button(top, text="Reset to Original", command=self._live_reset_to_original).pack(side="right")

        # Body - use grid for better control over proportions
        body = tk.Frame(self._live_editor_window); body.pack(fill="both", expand=True, padx=1, pady=0)
        body.grid_rowconfigure(0, weight=1)  # Allow row to expand
        
        # Ensure UI mode is preserved right before building UI
        self.live_pal_ui_mode = current_ui_mode
        
        # Swatches grid (left) - adjust width based on mode
        if self.live_pal_ui_mode == "Simple":
            grid = tk.Frame(body); grid.grid(row=0, column=0, padx=(0,0), pady=0, sticky="nsew")
            # Let the grid expand to fill the allocated column space
        else:
            grid = tk.Frame(body); grid.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        self._live_swatches = []
        ly = self._live_layers[self._live_name_to_index[self._live_target_name.get()]]
        
        # Check if we're in Simple mode
        if self.live_pal_ui_mode == "Simple":
            self._create_simple_palette_grid(grid, ly)
        else:
            self._create_advanced_palette_grid(grid, ly)

        # Picker panel (right) - adjust width based on mode
        if self.live_pal_ui_mode == "Simple":
            panel = tk.Frame(body, width=500)  # No border in Simple mode (120px wider for saved colors)
            panel.grid(row=0, column=1, padx=(4,0), pady=0, sticky="nsew")
        else:
            panel = tk.LabelFrame(body, text="Color Picker", padx=2, pady=1)
            panel.grid(row=0, column=1, padx=(4,0), pady=0, sticky="nsew")

        self._picker_idx_var = tk.StringVar(value="0")
        tk.Label(panel, text="Index:").grid(row=0, column=0, sticky="w")
        self._picker_idx_entry = tk.Entry(panel, width=5, textvariable=self._picker_idx_var)
        self._picker_idx_entry.grid(row=0, column=1, sticky="w")
        tk.Button(panel, text="Go", command=self._live_goto_index).grid(row=0, column=2, padx=(6,0))

        tk.Label(panel, text="Hex #RRGGBB:").grid(row=1, column=0, sticky="w", pady=(2,0))
        self._picker_hex = tk.Entry(panel, width=10)
        self._picker_hex.grid(row=1, column=1, columnspan=2, sticky="w")
        tk.Button(panel, text="Apply", command=self._live_apply_hex).grid(row=1, column=3, padx=(6,0))
        
        # Colorpicker button
        self._colorpicker_btn = tk.Button(panel, text="🎨 Pick", command=self._toggle_colorpicker)
        self._colorpicker_btn.grid(row=1, column=4, padx=(6,0))
        
        # Gradient button with rainbow colors
        self._gradient_btn = tk.Button(panel, text="🌈", command=self._open_gradient_menu, 
                                     bg="#FF4081", activebackground="#E91E63", width=3, height=1,
                                     font=("Arial", 10, "bold"), relief="raised")
        self._gradient_btn.grid(row=1, column=5, padx=(6,0))

        def mk_scale(label, row, varname):
            v = tk.IntVar(value=0)
            setattr(self, varname, v)
            tk.Label(panel, text=label).grid(row=row, column=0, sticky="w", pady=(8,0))
            sc = tk.Scale(panel, from_=0, to=255, orient="horizontal", variable=v,
                          command=lambda *_: self._live_slider_changed())
            sc.grid(row=row, column=1, columnspan=3, sticky="we", pady=(8,0))
        # Configure columns to properly accommodate all widgets including gradient button
        panel.grid_columnconfigure(1, weight=1)  # Make column 1 expandable for hex entry

                        
        # HSV controls - minimal spacing
        tk.Label(panel, text="Hue").grid(row=5, column=0, sticky="w", pady=(2,0))
        self._picker_h = tk.Scale(panel, from_=0, to=360, orient="horizontal", command=lambda *_: self._hsv_debounced_change())
        self._picker_h.grid(row=5, column=1, columnspan=5, sticky="we", pady=(1,0))
        tk.Label(panel, text="Sat").grid(row=6, column=0, sticky="w", pady=(1,0))
        self._picker_s = tk.Scale(panel, from_=0, to=100, orient="horizontal", command=lambda *_: self._hsv_debounced_change())
        self._picker_s.grid(row=6, column=1, columnspan=5, sticky="we", pady=(1,0))
        tk.Label(panel, text="Val").grid(row=7, column=0, sticky="w", pady=(1,0))
        self._picker_v = tk.Scale(panel, from_=0, to=100, orient="horizontal", command=lambda *_: self._hsv_debounced_change())
        self._picker_v.grid(row=7, column=1, columnspan=5, sticky="we", pady=(1,0))
        # --- Smooth-drag: mark dragging on press, clear on release ---
        def _start_drag(_e=None):
            self._is_dragging = True
        def _end_drag(_e=None):
            self._is_dragging = False
            try:
                self._hsv_debounced_change()
            except Exception:
                pass
        for w in (self._picker_h, self._picker_s, self._picker_v):
            try:
                w.bind("<ButtonPress-1>", _start_drag)
                w.bind("<ButtonRelease-1>", _end_drag)
            except Exception:
                pass


        # HSV numeric entry boxes (right of sliders)
        # H entry
        self._hsv_h_str = tk.StringVar(value="0")
        eH = tk.Entry(panel, textvariable=self._hsv_h_str, width=5)
        eH.grid(row=5, column=6, sticky="w", padx=(6,0))
        # S entry
        self._hsv_s_str = tk.StringVar(value="0")
        eS = tk.Entry(panel, textvariable=self._hsv_s_str, width=5)
        eS.grid(row=6, column=6, sticky="w", padx=(6,0))
        # V entry
        self._hsv_v_str = tk.StringVar(value="0")
        eV = tk.Entry(panel, textvariable=self._hsv_v_str, width=5)
        eV.grid(row=7, column=6, sticky="w", padx=(6,0))

        # --- Saved Colors panel (simple MS Paint style) ---
        if not hasattr(self, "_saved_colors"):
            self._saved_colors = [(0,0,0)] * 20
        sc_frame = tk.LabelFrame(panel, text="Saved Colors")
        sc_frame.grid(row=9, column=0, columnspan=7, sticky="we", padx=0, pady=(2,0))
        sc_top = tk.Frame(sc_frame); sc_top.pack(fill="x", padx=2, pady=2)
        
        # Mouse button toggle (right side)
        def toggle_click_mode():
            self.use_right_click = not self.use_right_click
            mouse_btn.config(text="R" if self.use_right_click else "L", 
                           relief="sunken" if self.use_right_click else "raised")
            # Update help text
            if self.use_right_click:
                help_label.config(text="Left click to apply color\nRight click to save color")
            else:
                help_label.config(text="Left click to save color\nRight click to apply color")
                
        mouse_btn = tk.Button(sc_top, text="R", font=("Arial", 10, "bold"), width=2, 
                            relief="sunken", bg="#d9d9d9", activebackground="#d9d9d9",
                            command=toggle_click_mode)
        mouse_btn.pack(side="right", padx=(4, 0))
        
        # Help text label that updates dynamically
        help_label = tk.Label(sc_frame, text="Left click to apply color\nRight click to save color",
                            anchor="w", justify="left", fg="gray40")
        help_label.pack(fill="x", padx=6)
        
        def _sc_save():
            from tkinter import filedialog
            import json
            # Default to exports/colors/json directory for saved colors
            root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            default_dir = os.path.join(root_dir, "exports", "colors", "json")

            os.makedirs(default_dir, exist_ok=True)
            p = filedialog.asksaveasfilename(
                defaultextension=".json", 
                filetypes=[("JSON","*.json")], 
                title="Save Colors",
                initialdir=default_dir
            )
            
            # Bring live editor to front after file dialog
            self._bring_live_editor_to_front()
            
            if not p: return
            try:
                # Create directory if it doesn't exist when actually saving
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(self._saved_colors, f)
            except Exception: pass
        def _sc_load():
            from tkinter import filedialog
            import json
            p = filedialog.askopenfilename(filetypes=[("JSON","*.json")], title="Load Colors")
            
            # Bring live editor to front after file dialog
            self._bring_live_editor_to_front()
            
            if not p: return
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list) and all(isinstance(t,(list,tuple)) and len(t)==3 for t in data):
                    data = [tuple(int(x) for x in t) for t in data][:20]
                    if len(data) < 20:
                        data += [(0,0,0)]*(20-len(data))
                    self._saved_colors = data
                    _sc_refresh()
            except Exception: pass
        def _sc_clear():
            self._saved_colors = [(0,0,0)] * 20
            _sc_refresh()
        tk.Button(sc_top, text="Save", width=6, command=_sc_save).pack(side="left")
        tk.Button(sc_top, text="Load", width=6, command=_sc_load).pack(side="left", padx=(6,0))
        tk.Button(sc_top, text="Clear", width=6, command=_sc_clear).pack(side="left", padx=(6,0))

        sc_grid = tk.Frame(sc_frame); sc_grid.pack(padx=2, pady=(0,2))
        self._sc_btns = []
        def _sc_refresh():
            for i, canvas in enumerate(self._sc_btns):
                r,g,b = self._saved_colors[i]
                try: 
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.delete("all")
                    canvas.create_rectangle(0, 0, 30, 30, fill=hex_color, outline="black")
                except Exception: pass
        def _sc_put(slot):
            ly = self._live_current_layer() if hasattr(self, "_live_current_layer") else None
            if ly is None: return
            idx = getattr(self, "_live_selected_index", 0)
            try: r,g,b = ly.colors[idx]
            except Exception: r=g=b=0
            self._saved_colors[slot] = (int(r),int(g),int(b))
            _sc_refresh()
        def _sc_pick(slot):
            r,g,b = self._saved_colors[slot]
            ly = self._live_current_layer() if hasattr(self, "_live_current_layer") else None
            if ly is None: return
            idx = getattr(self, "_live_selected_index", 0)
            ly.colors[idx] = (int(r),int(g),int(b))
            try: 
                # Update swatch based on mode
                if self.live_pal_ui_mode == "Simple":
                    # Find the display index for this palette index
                    editable_indices = self._get_editable_color_indices()
                    if idx in editable_indices:
                        display_idx = editable_indices.index(idx)
                        if display_idx < len(self._live_swatches) and self._live_swatches[display_idx] is not None:
                            canvas = self._live_swatches[display_idx]
                            hex_color = f"#{r:02x}{g:02x}{b:02x}"
                            canvas.delete("all")
                            canvas.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="black", width=1)
                else:
                    # Advanced mode: direct index mapping
                    if idx < len(self._live_swatches) and self._live_swatches[idx] is not None:
                        canvas = self._live_swatches[idx]
                        hex_color = f"#{r:02x}{g:02x}{b:02x}"
                        canvas.delete("all")
                        canvas.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
            except Exception: pass
            try: self._picker_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")
            except Exception: pass
            try:
                self._picker_hex.delete(0,"end"); self._picker_hex.insert(0,f"#{r:02x}{g:02x}{b:02x}")
            except Exception: pass
            if hasattr(self, "_sync_hsv_from_rgb"): self._sync_hsv_from_rgb(int(r),int(g),int(b))
            if hasattr(self, "_debounced_display_update"): self._debounced_display_update()
            
            # Update simple mode preview if in simple mode
            if self.live_pal_ui_mode == "Simple" and hasattr(self, '_update_simple_preview'):
                self._update_simple_preview()
        def _handle_click(event, slot):
            """Handle click based on current mode"""
            if (event.num == 3) == self.use_right_click:  # Right click mode matches right click or vice versa
                _sc_put(slot)
            else:
                _sc_pick(slot)
                
        for i in range(20):
            # Create 30x30 pixel buttons using Canvas for exact size control (smaller for live editor)
            canvas = tk.Canvas(sc_grid, width=30, height=30, highlightthickness=1, highlightbackground="black")
            canvas.grid(row=i//10, column=i%10, padx=1, pady=1)  # Reduced padding
            
            # Draw the color rectangle
            color = self._saved_colors[i]
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            canvas.create_rectangle(0, 0, 30, 30, fill=hex_color, outline="black")
            
            # Bind click events
            canvas.bind("<Button-1>", lambda e, j=i: _handle_click(e, j))
            canvas.bind("<Button-3>", lambda e, j=i: _handle_click(e, j))
            self._sc_btns.append(canvas)
            
        _sc_refresh()

        # Close button directly under saved colors
        close_frame = tk.Frame(panel)
        close_frame.grid(row=10, column=0, columnspan=7, sticky="we", pady=(10,0))
        tk.Button(close_frame, text="Close", command=on_window_close, width=12).pack()

        def _clamp_int(val, lo, hi, default=0):
            try:
                n = int(float(val))
            except Exception:
                n = default
            return max(lo, min(hi, n))

        def _apply_hsv_entries(*_):
            H = _clamp_int(self._hsv_h_str.get(), 0, 360, 0)
            S = _clamp_int(self._hsv_s_str.get(), 0, 100, 0)
            V = _clamp_int(self._hsv_v_str.get(), 0, 100, 0)
            if not hasattr(self, "_in_sync"): self._in_sync = False
            if self._in_sync: return
            self._in_sync = True
            try:
                if not getattr(self, "_is_dragging", False):
                    self._picker_h.set(H)
                    self._picker_s.set(S)
                    self._picker_v.set(V)
            finally:
                self._in_sync = False
            try:
                self._hsv_debounced_change()
            except Exception:
                pass

        for w in (eH, eS, eV):
            w.bind("<Return>", lambda _e: _apply_hsv_entries())
            w.bind("<FocusOut>", lambda _e: _apply_hsv_entries())

        self._picker_preview = tk.Label(panel, text="            ", relief="sunken")
        self._picker_preview.grid(row=8, column=0, columnspan=4, sticky="we", pady=(2,0))

        self._live_select_index(0)  # seed picker
        self._live_window = self._live_editor_window
        self._update_selection_ui()
        
        # Center the live editor window after content is created
        self._live_editor_window.update_idletasks()
        self._center_window_on_parent(self._live_editor_window, self.master)
        
        # Update icon editor button state based on current palette type
        self._update_icon_editor_button_state()

    def _create_advanced_palette_grid(self, grid, ly):
        """Create the traditional 16x16 palette grid showing all 256 colors"""
        for i in range(PALETTE_SIZE):
            r,g,b = ly.colors[i] if isinstance(ly.colors[i], tuple) else (0,0,0)
            # Create canvas-based swatch for better border control
            canvas = tk.Canvas(grid, width=20, height=20, highlightthickness=0, relief="flat")
            canvas.grid(row=i//16, column=i%16, padx=1, pady=1)  # Reduced padding
            
            # Draw the color rectangle
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
            
            # Left-click with optional Shift
            canvas.bind("<Button-1>", lambda e, i=i: self._live_on_swatch_click(i, e))
            self._live_swatches.append(canvas)
    
    def _create_simple_palette_grid(self, grid, ly):
        """Create a simplified palette grid showing only editable colors like the icon editor"""
        # Get editable color indices for the specified layer only
        editable_indices = self._get_editable_color_indices(ly)
        
        if not editable_indices:
            # Fallback to showing all colors if we can't determine editable ones
            self._create_advanced_palette_grid(grid, ly)
            return
        
        # Create a mapping from display position to actual palette index
        self._simple_index_mapping = {}
        
        # Check if we already have a PanedWindow from previous simple mode usage
        existing_paned = None
        existing_main_container = None
        
        for child in grid.winfo_children():
            if isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.PanedWindow):
                        existing_paned = subchild
                        existing_main_container = child
                        break
                if existing_paned:
                    break
        
        if existing_paned and existing_main_container:
            # Reuse existing PanedWindow to prevent flash
            paned_window = existing_paned
            main_container = existing_main_container
            
            # Clear only the contents of the paned window, not the paned window itself
            for pane in paned_window.panes():
                paned_window.forget(pane)
        else:
            # Create new layout for first time
            for child in grid.winfo_children():
                child.destroy()
            
            # Create main container with resizable paned window
            main_container = tk.Frame(grid)
            main_container.pack(fill="both", expand=True)
            
            # Create PanedWindow for resizable divider between palette and preview
            paned_window = tk.PanedWindow(main_container, orient="vertical", sashwidth=5, sashrelief="raised", 
                                         sashpad=1, bd=1, relief="sunken")
            paned_window.pack(fill="both", expand=True)
        
        # Top part: Palette grid with scrollbar (compact height)
        palette_frame = tk.Frame(paned_window)
        palette_frame.configure(height=90)  # Initial height for palette area
        paned_window.add(palette_frame, minsize=60)  # Minimum size to keep palette visible
        
        # Create scrollable palette area
        palette_canvas_frame = tk.Frame(palette_frame)
        palette_canvas_frame.pack(fill="both", expand=True)
        
        # Create scrollbar for palette
        palette_scrollbar = tk.Scrollbar(palette_canvas_frame, orient="vertical")
        palette_scrollbar.pack(side="right", fill="y")
        
        # Create canvas for palette
        palette_canvas = tk.Canvas(palette_canvas_frame, yscrollcommand=palette_scrollbar.set)
        palette_canvas.pack(side="left", fill="both", expand=True)
        palette_scrollbar.config(command=palette_canvas.yview)
        
        # Create frame inside canvas for the color squares
        squares_frame = tk.Frame(palette_canvas)
        canvas_window = palette_canvas.create_window((0, 0), window=squares_frame, anchor="nw")
        
        # Make the frame expand to fill canvas width
        def _on_canvas_configure(event):
            palette_canvas.itemconfig(canvas_window, width=event.width)
        palette_canvas.bind("<Configure>", _on_canvas_configure)
        
        # Fixed layout: 8 boxes per row
        cols = 8
        square_size = 40  # 2x larger than advanced mode (20x20)
        padding = 2
        
        for display_idx, palette_idx in enumerate(editable_indices):
            row = display_idx // cols
            col = display_idx % cols
            
            r, g, b = ly.colors[palette_idx] if isinstance(ly.colors[palette_idx], tuple) else (0, 0, 0)
            
            # Create canvas for color square (same size as advanced mode)
            color_canvas = tk.Canvas(squares_frame, width=square_size, height=square_size, 
                                   highlightthickness=0, relief="flat")
            color_canvas.grid(row=row, column=col, padx=padding, pady=padding)
            
            # Draw the color rectangle
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            color_canvas.create_rectangle(1, 1, square_size-1, square_size-1, fill=hex_color, outline="black", width=1)
            
            # Bind click events - use the actual palette index
            color_canvas.bind("<Button-1>", lambda e, i=palette_idx: self._on_simple_palette_click(i, e))
            
            # Store mapping
            self._simple_index_mapping[display_idx] = palette_idx
            self._live_swatches.append(color_canvas)
        
        # Configure scroll region for palette
        squares_frame.update_idletasks()
        palette_canvas.configure(scrollregion=palette_canvas.bbox("all"))
        
        # Bind mousewheel to palette canvas
        def _on_palette_mousewheel(event):
            try:
                if palette_canvas.winfo_exists():
                    palette_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                # Canvas has been destroyed, ignore the event
                pass
        palette_canvas.bind_all("<MouseWheel>", _on_palette_mousewheel)
        
        # Bottom part: Live preview (remaining space) - added to PanedWindow
        preview_frame = tk.Frame(paned_window, bg="white")
        paned_window.add(preview_frame, minsize=100)  # Minimum size to keep preview visible
        
        # Set sash position - only on very first creation
        
        # Set sash position - only for new PanedWindow or when we have stored position to restore
        is_rebuilding = getattr(self, '_is_rebuilding_grid', False)
        has_stored_position = hasattr(self, '_stored_sash_position') and self._stored_sash_position is not None
        is_existing_paned = existing_paned is not None
        
        
        # Only position if it's a new PanedWindow or if we're reusing one and have a stored position
        if (not is_existing_paned) or (is_existing_paned and has_stored_position):
            if not is_existing_paned:
                self._simple_sash_position_set = True
            
            def set_sash_position():
                try:
                    
                    # Get the total height of the paned window
                    total_height = paned_window.winfo_height()
                    
                    if total_height > 1:  # Window is configured
                        # Use stored position if available, otherwise use 1/3 from top
                        if hasattr(self, '_stored_sash_position') and self._stored_sash_position is not None:
                            target_position = self._stored_sash_position
                        else:
                            target_position = total_height // 3
                        
                        paned_window.sash_place(0, 0, target_position)
                    else:
                        # Window not yet configured, try again later (but only once more)
                        retry_key = f'_simple_sash_retry_count_{id(paned_window)}'
                        if not hasattr(self, retry_key):
                            setattr(self, retry_key, 1)
                            main_container.after(100, set_sash_position)
                        else:
                            pass  # Already retried, give up
                except Exception as e:
                    pass  # Error in sash placement
            
            # Schedule the sash positioning after the window is fully rendered
            main_container.after(100, set_sash_position)
        else:
            pass  # Skip sash positioning
        
        # Create preview controls at the top of preview frame
        preview_controls = tk.Frame(preview_frame)
        preview_controls.pack(fill="x", padx=5, pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(preview_controls)
        nav_frame.pack(side="left")
        
        self._simple_prev_btn = tk.Button(nav_frame, text="◀", command=self._simple_prev_frame, width=3)
        self._simple_prev_btn.pack(side="left", padx=(0, 2))
        
        self._simple_next_btn = tk.Button(nav_frame, text="▶", command=self._simple_next_frame, width=3)
        self._simple_next_btn.pack(side="left")
        
        # Frame info label
        self._simple_frame_label = tk.Label(preview_controls, text="Frame 1")
        self._simple_frame_label.pack(side="left", padx=(10, 0))
        
        # Zoom controls
        zoom_frame = tk.Frame(preview_controls)
        zoom_frame.pack(side="right")
        
        tk.Label(zoom_frame, text="Zoom:").pack(side="left")
        self._simple_zoom_var = tk.StringVar(value="100%")
        self._simple_zoom_combo = ttk.Combobox(zoom_frame, textvariable=self._simple_zoom_var,
                                             values=["100%", "200%", "300%", "400%", "500%", "Fit"], state="readonly", width=8)
        self._simple_zoom_combo.pack(side="left", padx=(5, 0))
        self._simple_zoom_combo.bind("<<ComboboxSelected>>", self._simple_on_zoom_change)
        
        # Create canvas for the preview image that fills the available space
        self._simple_preview_canvas = tk.Canvas(preview_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        self._simple_preview_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bind resize event to update canvas dimensions for click handling
        self._simple_preview_canvas.bind("<Configure>", self._on_simple_canvas_configure)
        
        # Bind click event to preview for color selection
        self._simple_preview_canvas.bind("<Button-1>", self._on_simple_preview_click)
        
        # Change cursor to indicate clickability
        self._simple_preview_canvas.bind("<Enter>", lambda e: self._simple_preview_canvas.configure(cursor="hand2"))
        self._simple_preview_canvas.bind("<Leave>", lambda e: self._simple_preview_canvas.configure(cursor=""))
        
        # Store reference to current preview image
        self._simple_current_image = None
        # Initialize to the current frame from the main UI
        self._simple_current_frame = getattr(self, 'current_image_index', 0)
        
        # Update the preview
        self._update_simple_preview()
        
        # Add keyboard bindings for simple mode navigation
        def _on_simple_key(event):
            if event.keysym == "Left":
                self._simple_prev_frame()
            elif event.keysym == "Right":
                self._simple_next_frame()
        
        # Bind arrow keys to the live editor window
        if hasattr(self, '_live_editor_window') and self._live_editor_window:
            self._live_editor_window.bind("<Left>", _on_simple_key)
            self._live_editor_window.bind("<Right>", _on_simple_key)
            self._live_editor_window.focus_set()  # Make sure window can receive key events
        
        # Fill remaining positions with None to maintain structure
        while len(self._live_swatches) < PALETTE_SIZE:
            self._live_swatches.append(None)

    def _get_editable_color_indices(self, layer=None):
        """Get the list of editable color indices for the specified layer or current character/fashion type"""
        try:
            # Import the CHARACTER_RANGES
            from palette_ranges import CHARACTER_RANGES
            
            # Use the provided layer or get current layer from the live editor
            current_layer = layer if layer is not None else self._live_current_layer()
            if not current_layer or not hasattr(current_layer, 'name'):
                return []
            
            # Use the palette_type that's already set by the original UI's categorization
            fashion_type = getattr(current_layer, 'palette_type', None)
            
            if not fashion_type:
                return []
            
            # Extract character number from layer name
            layer_name = current_layer.name.lower()
            char_num = None
            import re
            
            # Try different patterns for character extraction
            for pattern in [r'chr(\d{3})', r'chr(\d+)', r'(\d{3})', r'(\d+)']:
                char_match = re.search(pattern, layer_name)
                if char_match:
                    char_num = char_match.group(1).zfill(3)  # Pad to 3 digits
                    break
            
            if not char_num:
                return []
            
            # Special handling for 3rd_job_base - use keyed colors instead of predefined ranges
            if fashion_type == "3rd_job_base":
                editable_indices = []
                
                # Check all palette indices for non-keying colors
                for idx in range(256):  # Full palette range
                    if idx == 0:  # Skip index 0 (always keying)
                        continue
                        
                    # Get the color at this index
                    if hasattr(current_layer, 'colors') and idx < len(current_layer.colors):
                        color = current_layer.colors[idx]
                        
                        # Skip ALL green variant keying colors (00FF00 through 00FF15)
                        if isinstance(color, (tuple, list)) and len(color) >= 3:
                            r, g, b = color
                            if g == 255 and r == 0 and 0 <= b <= 21:  # Catches all 00FFxx variants
                                continue
                        
                        # Skip character-specific keying colors
                        if char_num == "014":  # Lion
                            if hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(color):
                                continue
                        elif char_num == "008":  # Raccoon
                            if hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(color):
                                continue
                                
                        # Skip universal keying colors and magenta
                        if hasattr(self, 'is_universal_keying_color') and (self.is_universal_keying_color(color) or color == (255, 0, 255)):
                            continue
                            
                        editable_indices.append(idx)
                
                return editable_indices
            
            # Get ranges for this character/fashion type (non-3rd_job_base)
            ranges = CHARACTER_RANGES.get(char_num, {}).get(fashion_type, [])
            
            if not ranges:
                return []
            
            editable_indices = []
            for r in ranges:
                for idx in range(r.start, r.stop - 1):  # Skip last index in each range (keying color)
                    if idx == 0:  # Skip index 0 (keying color)
                        continue
                        
                    # Get the color at this index
                    if hasattr(current_layer, 'colors') and idx < len(current_layer.colors):
                        color = current_layer.colors[idx]
                        
                        # Skip ALL green variant keying colors (00FF00 through 00FF15)
                        if isinstance(color, (tuple, list)) and len(color) >= 3:
                            r, g, b = color
                            if g == 255 and r == 0 and 0 <= b <= 21:  # Catches all 00FFxx variants
                                continue
                        
                        # Skip character-specific keying colors
                        if char_num == "014":  # Lion
                            if self.is_chr014_keying_color(color):
                                continue
                        elif char_num == "008":  # Raccoon
                            if self.is_chr008_keying_color(color):
                                continue
                            
                        # Skip universal keying colors and magenta
                        if self.is_universal_keying_color(color) or color == (255, 0, 255):
                            continue
                            
                    editable_indices.append(idx)
            
            # Don't sort by brightness - preserve original order to prevent auto-sorting after edits
            # The original order from the ranges is more predictable for users
            
            return editable_indices
            
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error getting editable color indices: {e}")
            return []

    def _simple_prev_frame(self):
        """Navigate to previous frame in simple mode preview"""
        if not hasattr(self, 'current_character') or not self.current_character:
            return
        
        if self.current_character in self.character_images:
            total_frames = len(self.character_images[self.current_character])
            if total_frames > 0:
                self._simple_current_frame = (self._simple_current_frame - 1) % total_frames
                self._update_simple_preview()

    def _simple_next_frame(self):
        """Navigate to next frame in simple mode preview"""
        if not hasattr(self, 'current_character') or not self.current_character:
            return
        
        if self.current_character in self.character_images:
            total_frames = len(self.character_images[self.current_character])
            if total_frames > 0:
                self._simple_current_frame = (self._simple_current_frame + 1) % total_frames
                self._update_simple_preview()

    def _simple_on_zoom_change(self, *args):
        """Handle zoom change in simple mode preview"""
        self._update_simple_preview()

    def _on_simple_canvas_configure(self, event):
        """Handle canvas resize to update image display"""
        # Update the preview when canvas size changes
        self._update_simple_preview()

    def _on_simple_preview_click(self, event):
        """Handle click on simple mode preview to select color index or pick color."""
        if self.colorpicker_active:
            self._colorpick_from_simple_preview(event)
            return
        
        # Original preview click behavior for color selection
        try:
            if not hasattr(self, 'current_character') or not self.current_character:
                return
            
            if self.current_character not in self.character_images:
                return
            
            images = self.character_images[self.current_character]
            if not images or self._simple_current_frame >= len(images):
                return
            
            # Get click coordinates relative to the canvas
            click_x = event.x
            click_y = event.y
            
            # Get the current zoom and image dimensions
            zoom = self._simple_zoom_var.get()
            # Get actual canvas dimensions dynamically
            canvas_width = self._simple_preview_canvas.winfo_width()
            canvas_height = self._simple_preview_canvas.winfo_height()
            
            # Fallback to reasonable defaults if canvas not yet configured
            if canvas_width <= 1:
                canvas_width = 500
            if canvas_height <= 1:
                canvas_height = 200
            
            # Load the original image to get pixel data
            original_img_path = images[self._simple_current_frame]
            original_img = Image.open(original_img_path).convert("P")
            img_width, img_height = original_img.size
            
            # Calculate the displayed image size based on zoom
            if zoom == "Fit":
                scale_x = canvas_width / img_width
                scale_y = canvas_height / img_height
                scale = min(scale_x, scale_y)
                display_width = int(img_width * scale)
                display_height = int(img_height * scale)
            elif zoom == "200%":
                display_width = img_width * 2
                display_height = img_height * 2
            elif zoom == "300%":
                display_width = img_width * 3
                display_height = img_height * 3
            elif zoom == "400%":
                display_width = img_width * 4
                display_height = img_height * 4
            elif zoom == "500%":
                display_width = img_width * 5
                display_height = img_height * 5
            else:  # 100%
                display_width = img_width
                display_height = img_height
            
            # Calculate the image position (centered in canvas)
            image_x = (canvas_width - display_width) / 2
            image_y = (canvas_height - display_height) / 2
            
            # Check if click is within the image bounds
            if (click_x < image_x or click_x >= image_x + display_width or
                click_y < image_y or click_y >= image_y + display_height):
                return  # Click outside image
            
            # Convert click coordinates to original image coordinates
            relative_x = click_x - image_x
            relative_y = click_y - image_y
            
            # Scale back to original image coordinates
            if zoom == "Fit":
                original_x = int(relative_x / scale)
                original_y = int(relative_y / scale)
            elif zoom == "200%":
                original_x = int(relative_x / 2)
                original_y = int(relative_y / 2)
            elif zoom == "300%":
                original_x = int(relative_x / 3)
                original_y = int(relative_y / 3)
            elif zoom == "400%":
                original_x = int(relative_x / 4)
                original_y = int(relative_y / 4)
            elif zoom == "500%":
                original_x = int(relative_x / 5)
                original_y = int(relative_y / 5)
            else:  # 100%
                original_x = int(relative_x)
                original_y = int(relative_y)
            
            # Ensure coordinates are within image bounds
            if (0 <= original_x < img_width and 0 <= original_y < img_height):
                # Get the palette index at this pixel
                pixel_index = original_img.getpixel((original_x, original_y))
                
                # Check if this index is in our editable indices for the current layer
                current_layer = self._live_current_layer()
                editable_indices = self._get_editable_color_indices(current_layer)
                if pixel_index in editable_indices:
                    # Select this index in the live editor
                    self._live_select_index(pixel_index)
                    
                    # Update selection UI
                    self._selected_indices.clear()
                    self._selected_indices.add(pixel_index)
                    self._update_selection_ui()
                    
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error handling simple preview click: {e}")

    def _update_simple_preview(self):
        """Update the simple mode preview image"""
        if not hasattr(self, '_simple_preview_canvas') or not self._simple_preview_canvas:
            return
        
        if not hasattr(self, 'current_character') or not self.current_character:
            self._simple_preview_canvas.delete("all")
            return
        
        if self.current_character not in self.character_images:
            self._simple_preview_canvas.delete("all")
            return
        
        images = self.character_images[self.current_character]
        if not images or self._simple_current_frame >= len(images):
            self._simple_preview_canvas.delete("all")
            return
        
        # Get the current image with palettes applied
        try:
            # Get the original image for the current frame
            original_img = images[self._simple_current_frame]
            
            # Apply palettes to this specific frame
            current_img = self._apply_palettes_to_image_path(original_img)
            
            if not current_img:
                # Fallback to original image
                current_img = Image.open(original_img)
            
            if current_img:
                # Apply zoom
                zoom = self._simple_zoom_var.get()
                img_width, img_height = current_img.size
                
                # Get actual canvas dimensions dynamically for fit calculation
                canvas_width = self._simple_preview_canvas.winfo_width()
                canvas_height = self._simple_preview_canvas.winfo_height()
                
                # Fallback to reasonable defaults if canvas not yet configured
                if canvas_width <= 1:
                    canvas_width = 380
                if canvas_height <= 1:
                    canvas_height = 200
                
                if zoom == "Fit":
                    # Calculate scale to fit within the canvas
                    scale_x = canvas_width / img_width
                    scale_y = canvas_height / img_height
                    scale = min(scale_x, scale_y)  # Allow scaling up or down
                    new_width = int(img_width * scale)
                    new_height = int(img_height * scale)
                elif zoom == "200%":
                    new_width = img_width * 2
                    new_height = img_height * 2
                elif zoom == "300%":
                    new_width = img_width * 3
                    new_height = img_height * 3
                elif zoom == "400%":
                    new_width = img_width * 4
                    new_height = img_height * 4
                elif zoom == "500%":
                    new_width = img_width * 5
                    new_height = img_height * 5
                else:  # 100%
                    new_width = img_width
                    new_height = img_height
                
                # Resize image
                display_img = current_img.resize((new_width, new_height), Image.NEAREST)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(display_img)
                
                # Clear canvas and display image
                self._simple_preview_canvas.delete("all")
                
                # Center the image in the canvas using dynamic dimensions
                center_x = canvas_width // 2
                center_y = canvas_height // 2
                self._simple_preview_canvas.create_image(center_x, center_y, anchor="center", image=photo)
                
                # Keep reference to prevent garbage collection
                self._simple_current_image = photo
                
                # Update frame label
                if hasattr(self, '_simple_frame_label'):
                    total_frames = len(images)
                    self._simple_frame_label.config(text=f"Frame {self._simple_current_frame + 1} / {total_frames}")
                
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error updating simple preview: {e}")
            self._simple_preview_canvas.delete("all")

    def _apply_palettes_to_image_path(self, image_path):
        """Apply current active palettes to a specific image file and return the result"""
        try:
            # Load the image
            original_img = Image.open(image_path).convert("P")
            
            # Get the merged palette (same logic as update_single_frame_display)
            merged_palette = self.get_merged_palette()
            
            # Create a new image with the merged palette
            w, h = original_img.size
            display_img = Image.new("P", (w, h))
            
            # Apply the merged palette FIRST
            display_img.putpalette([color for palette_color in merged_palette for color in palette_color])
            
            # THEN copy the pixel data from original image
            display_img.putdata(original_img.getdata())
            
            # Replace transparency colors with background color in the merged palette
            display_palette = []
            
            for i, color in enumerate(merged_palette):
                if self.is_universal_keying_color(color) or color == (255, 0, 255):  # Green or magenta
                    display_palette.append(self.background_color)
                else:
                    display_palette.append(color)
            
            # Apply the modified palette to the display image
            display_img.putpalette([color for palette_color in display_palette for color in palette_color])
            
            # Convert to RGB for display
            rgb_img = display_img.convert("RGB")
            
            return rgb_img
            
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error applying palettes to image: {e}")
            return None
    
    def _toggle_colorpicker(self):
        """Toggle colorpicker mode on/off for simple palette editor."""
        self.colorpicker_active = not self.colorpicker_active
        
        if self.colorpicker_active:
            self._colorpicker_btn.configure(text="🎨 Exit")
            # Change cursor for all clickable areas
            if hasattr(self, '_simple_preview_canvas'):
                self._simple_preview_canvas.configure(cursor="crosshair")
            for swatch in self._live_swatches:
                if swatch and swatch.winfo_exists():
                    swatch.configure(cursor="crosshair")
        else:
            self._colorpicker_btn.configure(text="🎨 Pick")
            # Reset cursors
            if hasattr(self, '_simple_preview_canvas'):
                self._simple_preview_canvas.configure(cursor="")
            for swatch in self._live_swatches:
                if swatch and swatch.winfo_exists():
                    swatch.configure(cursor="")
    
    def _on_simple_palette_click(self, palette_idx, event):
        """Handle palette square clicks - either for selection or colorpicking."""
        if self.colorpicker_active:
            self._colorpick_from_simple_palette(palette_idx)
        else:
            self._live_on_swatch_click(palette_idx, event)
    
    def _colorpick_from_simple_palette(self, palette_idx):
        """Pick color from simple palette square."""
        current_layer = self._live_current_layer()
        if current_layer and palette_idx < len(current_layer.colors):
            picked_color = current_layer.colors[palette_idx]
            
            # Check if picked color is a keying color and find alternative if needed
            if self._is_keyed_color(picked_color):
                picked_color = self._find_nearest_non_keyed_color(picked_color)
                print(f"Avoided keying color, using alternative: {picked_color}")
            
            self._apply_colorpicked_color_simple(picked_color)
    
    def _colorpick_from_simple_preview(self, event):
        """Pick color from simple preview image."""
        try:
            if not hasattr(self, 'current_character') or not self.current_character:
                return
            
            if self.current_character not in self.character_images:
                return
            
            images = self.character_images[self.current_character]
            if not images or self._simple_current_frame >= len(images):
                return
            
            # Get click coordinates relative to the canvas
            click_x = event.x
            click_y = event.y
            
            # Get the current zoom and image dimensions
            zoom = self._simple_zoom_var.get()
            canvas_width = self._simple_preview_canvas.winfo_width()
            canvas_height = self._simple_preview_canvas.winfo_height()
            
            if canvas_width <= 1:
                canvas_width = 380
            if canvas_height <= 1:
                canvas_height = 200
            
            # Load the original image to get pixel data
            original_img_path = images[self._simple_current_frame]
            original_img = Image.open(original_img_path).convert("P")
            img_width, img_height = original_img.size
            
            # Calculate the displayed image size based on zoom
            if zoom == "Fit":
                scale_x = canvas_width / img_width
                scale_y = canvas_height / img_height
                scale = min(scale_x, scale_y)
                display_width = int(img_width * scale)
                display_height = int(img_height * scale)
            elif zoom == "200%":
                display_width = img_width * 2
                display_height = img_height * 2
                scale = 2
            elif zoom == "300%":
                display_width = img_width * 3
                display_height = img_height * 3
                scale = 3
            elif zoom == "400%":
                display_width = img_width * 4
                display_height = img_height * 4
                scale = 4
            elif zoom == "500%":
                display_width = img_width * 5
                display_height = img_height * 5
                scale = 5
            else:  # 100%
                display_width = img_width
                display_height = img_height
                scale = 1
            
            # Calculate image position (centered)
            image_x = (canvas_width - display_width) // 2
            image_y = (canvas_height - display_height) // 2
            
            # Check if click is within the image
            if (image_x <= click_x <= image_x + display_width and 
                image_y <= click_y <= image_y + display_height):
                
                # Convert click coordinates to image coordinates
                relative_x = click_x - image_x
                relative_y = click_y - image_y
                
                # Scale back to original image coordinates
                if zoom == "Fit":
                    original_x = int(relative_x / scale)
                    original_y = int(relative_y / scale)
                else:
                    original_x = int(relative_x / scale)
                    original_y = int(relative_y / scale)
                
                # Ensure coordinates are within image bounds
                if 0 <= original_x < img_width and 0 <= original_y < img_height:
                    # Get the palette index at this pixel
                    pixel_index = original_img.getpixel((original_x, original_y))
                    
                    # Get the actual color from the merged palette
                    merged_palette = self.get_merged_palette()
                    if pixel_index < len(merged_palette):
                        picked_color = merged_palette[pixel_index]
                        
                        # Check if it's a transparency color and use background color instead
                        if self.is_universal_keying_color(picked_color) or picked_color == (255, 0, 255):
                            picked_color = self.background_color
                        
                        self._apply_colorpicked_color_simple(picked_color)
                        
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error picking color from simple preview: {e}")
    
    def _apply_colorpicked_color_simple(self, picked_color):
        """Apply a picked color to the selected palette indices in simple mode."""
        current_layer = self._live_current_layer()
        if not current_layer:
            return
        
        # Check if picked color is a keying color and find alternative if needed
        if self._is_keyed_color(picked_color):
            picked_color = self._find_nearest_non_keyed_color(picked_color)
            print(f"Avoided keying color, using alternative: {picked_color}")
        
        # Get selected indices or current index
        targets = sorted(self._selected_indices) if self._multi_select.get() and self._selected_indices else [self._live_selected_index]
        
        for i in targets:
            if i < len(current_layer.colors):
                current_layer.colors[i] = picked_color
                
                # Update statistics
                self.statistics.indexes_changed += 1
                self.statistics.colors_saved += 1
                if hasattr(self, 'current_character') and hasattr(self, 'current_job'):
                    self.statistics.add_palette_edit(self.current_character, self.current_job)
                    self.statistics.live_palette_files_edited.add(current_layer.name)
                self._save_statistics()
                
                # Update swatch if in simple mode
                if self.live_pal_ui_mode == "Simple":
                    editable_indices = self._get_editable_color_indices()
                    if i in editable_indices:
                        display_idx = editable_indices.index(i)
                        if display_idx < len(self._live_swatches) and self._live_swatches[display_idx] is not None:
                            canvas = self._live_swatches[display_idx]
                            hex_color = f"#{picked_color[0]:02x}{picked_color[1]:02x}{picked_color[2]:02x}"
                            canvas.delete("all")
                            canvas.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="black", width=1)
        
        # Update UI elements
        if hasattr(self, "_update_selection_ui"):
            self._update_selection_ui()
        
        r, g, b = picked_color
        self._picker_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")
        self._picker_hex.delete(0, "end")
        self._picker_hex.insert(0, f"#{r:02x}{g:02x}{b:02x}")
        
        self._debounced_display_update()
        self._sync_hsv_from_rgb(r, g, b)
        
        # Update simple mode preview if in simple mode
        if hasattr(self, '_update_simple_preview'):
            self._update_simple_preview()
        
        # Exit colorpicker mode after picking
        if self.colorpicker_active:
            self._toggle_colorpicker()

    def _rebuild_live_palette_grid(self):
        """Rebuild the palette grid when UI mode changes"""
        if not hasattr(self, '_live_editor_window') or not self._live_editor_window or not self._live_editor_window.winfo_exists():
            return
        
        # Set flag to indicate this is a rebuild, not initial creation
        self._is_rebuilding_grid = True
            
        # Clear current selection and existing swatches
        self._selected_indices.clear()
        self._last_clicked_index = None
        
        # Destroy existing swatches
        for canvas in self._live_swatches:
            try:
                if canvas is not None:
                    canvas.destroy()
            except:
                pass
        self._live_swatches.clear()
        
        # Find the grid frame (it's the first Frame child of body)
        grid = None
        for child in self._live_editor_window.winfo_children():
            if isinstance(child, tk.Frame):  # This is the body frame
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Frame) and subchild.grid_info():  # This is the grid frame
                        grid = subchild
                        break
                if grid:
                    break
        
        if grid:
            # Get current layer
            ly = self._live_current_layer()
            if ly is None:
                return
            
            # Create grid based on current mode
            if self.live_pal_ui_mode == "Simple":
                self._create_simple_palette_grid(grid, ly)
            else:
                self._create_advanced_palette_grid(grid, ly)
            
            # Reset selection to first index
            self._live_select_index(0)
            self._update_selection_ui()
            
            # Update simple mode preview if in simple mode
            if self.live_pal_ui_mode == "Simple" and hasattr(self, '_update_simple_preview'):
                self._update_simple_preview()
        
        # Clear the rebuild flag
        self._is_rebuilding_grid = False

    def _update_simple_palette_colors(self, ly):
        """Update only the colors in simple mode without rebuilding the entire UI"""
        # Set flag to prevent color changes during palette switching
        self._updating_live_selection = True
        
        # Get editable indices for the new layer
        editable_indices = self._get_editable_color_indices(ly)
        
        if not editable_indices:
            return
        
        # Update existing swatches with new colors
        if hasattr(self, '_live_swatches') and self._live_swatches:
            # Clear existing swatches first
            for canvas in self._live_swatches:
                if canvas is not None:
                    try:
                        canvas.destroy()
                    except:
                        pass
            self._live_swatches.clear()
            
            # Find the existing palette squares frame
            squares_frame = None
            try:
                if hasattr(self, '_live_editor_window') and self._live_editor_window:
                    def find_squares_frame(widget):
                        # Look for the specific Frame that's inside a Canvas (scrollable palette area)
                        # The palette squares frame is created inside a Canvas for scrolling
                        if isinstance(widget, tk.Canvas):
                            # Check if this canvas has a window (our squares frame)
                            try:
                                for item in widget.find_all():
                                    item_type = widget.type(item)
                                    if item_type == "window":
                                        # Get the widget from the window item
                                        window_widget = widget.nametowidget(widget.itemcget(item, "window"))
                                        if isinstance(window_widget, tk.Frame):
                                            return window_widget
                            except:
                                pass
                        
                        # Check children
                        try:
                            for child in widget.winfo_children():
                                result = find_squares_frame(child)
                                if result:
                                    return result
                        except:
                            pass
                        return None
                    
                    squares_frame = find_squares_frame(self._live_editor_window)
            except Exception as e:
                pass  # Error finding squares frame
            
            if squares_frame:
                
                # Clear existing squares in the frame
                child_count = 0
                for child in squares_frame.winfo_children():
                    try:
                        child.destroy()
                        child_count += 1
                    except:
                        pass
                
                # Recreate squares with new colors
                cols = 8
                square_size = 40
                padding = 2
                
                created_count = 0
                for display_idx, palette_idx in enumerate(editable_indices):
                    row = display_idx // cols
                    col = display_idx % cols
                    
                    r, g, b = ly.colors[palette_idx] if isinstance(ly.colors[palette_idx], tuple) else (0, 0, 0)
                    
                    # Create canvas for color square
                    color_canvas = tk.Canvas(squares_frame, width=square_size, height=square_size, 
                                           highlightthickness=0, relief="flat")
                    color_canvas.grid(row=row, column=col, padx=padding, pady=padding)
                    
                    # Draw the color rectangle
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    color_canvas.create_rectangle(1, 1, square_size-1, square_size-1, fill=hex_color, outline="black", width=1)
                    
                    # Bind click events - use the actual palette index
                    color_canvas.bind("<Button-1>", lambda e, i=palette_idx: self._live_on_swatch_click(i, e))
                    
                    # Store mapping
                    if not hasattr(self, '_simple_index_mapping'):
                        self._simple_index_mapping = {}
                    self._simple_index_mapping[display_idx] = palette_idx
                    self._live_swatches.append(color_canvas)
                    created_count += 1
                
                
                # Update the scroll region
                try:
                    squares_frame.update_idletasks()
                    # Find the parent canvas to update scroll region
                    parent = squares_frame.winfo_parent()
                    if parent:
                        parent_widget = squares_frame.nametowidget(parent)
                        if isinstance(parent_widget, tk.Canvas):
                            parent_widget.configure(scrollregion=parent_widget.bbox("all"))
                except Exception as e:
                    pass  # Error updating scroll region
            else:
                self._rebuild_live_palette_grid()
        
            # Fill remaining positions with None to maintain structure
            while len(self._live_swatches) < 256:  # PALETTE_SIZE
                self._live_swatches.append(None)

    def _live_multi_toggled(self):
        # Collapse to single index if turning off multi-select
        if not self._multi_select.get():
            if self._selected_indices:
                last = sorted(self._selected_indices)[-1]
                self._selected_indices.clear()
                self._live_select_index(last)
        self._update_selection_ui()

    
    def _update_selection_ui(self):
        # Visual highlight for selected tiles and selection count
        # Use simple outline approach to avoid flashing and color corruption
        
        if self.live_pal_ui_mode == "Simple":
            # Simple mode: only update visible editable colors
            editable_indices = self._get_editable_color_indices()
            for display_idx, palette_idx in enumerate(editable_indices):
                if display_idx >= len(self._live_swatches) or self._live_swatches[display_idx] is None:
                    continue
                    
                btn = self._live_swatches[display_idx]
                if palette_idx in self._selected_indices:
                    # Get the current color to preserve it
                    r, g, b = self._live_layers[self._live_name_to_index[self._live_target_name.get()]].colors[palette_idx]
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # Always use red border for selected colors
                    border_color = "red"
                    
                    # Redraw with border highlight (40x40 for simple mode)
                    btn.delete("all")
                    # Draw border
                    btn.create_rectangle(0, 0, 40, 40, fill=border_color, outline="")
                    # Draw color rectangle inside
                    btn.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="")
                else:
                    # Get the current color to preserve it
                    r, g, b = self._live_layers[self._live_name_to_index[self._live_target_name.get()]].colors[palette_idx]
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # Redraw with normal appearance
                    btn.delete("all")
                    btn.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="black", width=1)
        else:
            # Advanced mode: update all 256 colors
            for i, btn in enumerate(self._live_swatches):
                if btn is None:
                    continue
                    
                if i in self._selected_indices:
                    # Get the current color to preserve it
                    r, g, b = self._live_layers[self._live_name_to_index[self._live_target_name.get()]].colors[i]
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # Always use red border for selected colors
                    border_color = "red"
                    
                    # Redraw with border highlight (keep 20x20 and 19x19 as requested)
                    btn.delete("all")
                    # Draw border
                    btn.create_rectangle(0, 0, 20, 20, fill=border_color, outline="")
                    # Draw color rectangle inside
                    btn.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="")
                else:
                    # Get the current color to preserve it
                    r, g, b = self._live_layers[self._live_name_to_index[self._live_target_name.get()]].colors[i]
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # Redraw with normal appearance
                    btn.delete("all")
                    btn.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
        
        if hasattr(self, "_sel_count_lbl"):
            self._sel_count_lbl.config(text=f"({len(self._selected_indices)} selected)")

    def _live_select_all(self):
        """Select all editable color swatches in the current palette."""
        if hasattr(self, '_live_swatches'):
            # Prevent HSV slider callbacks from applying changes during selection
            self._updating_live_selection = True
            try:
                # Enable multi-select mode to allow relative HSV adjustments
                self._multi_select.set(True)
                
                # Select based on UI mode
                if self.live_pal_ui_mode == "Simple":
                    # Simple mode: select all editable color indices (display indices)
                    editable_indices = self._get_editable_color_indices()
                    # In simple mode, _live_swatches contains only editable colors
                    # so we select all available swatches
                    self._selected_indices = set(range(len(self._live_swatches)))
                else:
                    # Advanced mode: select only editable colors from all 256
                    editable_indices = self._get_editable_color_indices()
                    # In advanced mode, _live_swatches contains all 256 colors
                    # so we select only the editable indices
                    self._selected_indices = set(editable_indices)
                
                if self._selected_indices:
                    self._last_clicked_index = min(self._selected_indices)
                    # Update sliders to show first selected color
                    self._live_select_index(self._last_clicked_index)
                self._update_selection_ui()
                # Force pending events to process before clearing flag
                if hasattr(self, '_live_editor_window') and self._live_editor_window:
                    self._live_editor_window.update_idletasks()
            finally:
                self._updating_live_selection = False
    
    def _live_clear_selection(self):
        self._selected_indices.clear()
        self._last_clicked_index = None
        self._update_selection_ui()

    def _live_reset_to_original(self):
        """Reset the current layer's colors back to their original state"""
        if not hasattr(self, '_live_original_colors') or not hasattr(self, '_live_layers'):
            return
        
        current_name = self._live_target_name.get()
        if current_name not in self._live_original_colors:
            return
        
        # Find the current layer
        current_layer = None
        
        # Extract just the filename from the current_name if it contains a display prefix
        target_filename = current_name
        if " — " in current_name:
            target_filename = current_name.split(" — ")[-1]  # Get the part after the last " — "
        
        for layer in self._live_layers:
            # Try both exact match and filename match
            if hasattr(layer, 'name') and (layer.name == current_name or layer.name == target_filename):
                current_layer = layer
                break
        
        if not current_layer:
            return
        
        # Restore original colors to the layer data
        original_colors = self._live_original_colors[current_name]
        current_layer.colors = original_colors.copy()
        
        # Update temp cache with reset colors
        if hasattr(self, '_live_temp_palette_cache'):
            self._live_temp_palette_cache[current_name] = current_layer.colors.copy()
        
        # Handle reset differently for Simple vs Advanced mode
        if self.live_pal_ui_mode == "Simple":
            self._simple_mode_reset(current_layer)
        else:
            self._advanced_mode_reset(current_layer)
    
    def _simple_mode_reset(self, current_layer):
        """Reset colors specifically for Simple mode using EXACT _live_hsv_changed logic"""
        # Get all editable indices to reset
        editable_indices = self._get_editable_color_indices()
        
        # Reset each editable color using the EXACT same logic as _live_hsv_changed
        for i in editable_indices:
            # Get the original color for this palette index (already restored to current_layer.colors)
            r, g, b = current_layer.colors[i] if isinstance(current_layer.colors[i], tuple) else (0, 0, 0)
            
            # Update swatch based on mode (EXACT copy from _live_hsv_changed)
            if self.live_pal_ui_mode == "Simple":
                # Find the display index for this palette index
                editable_indices_check = self._get_editable_color_indices()
                if i in editable_indices_check:
                    display_idx = editable_indices_check.index(i)
                    
                    if display_idx < len(self._live_swatches) and self._live_swatches[display_idx] is not None:
                        canvas = self._live_swatches[display_idx]
                        hex_color = f"#{r:02x}{g:02x}{b:02x}"
                        
                        try:
                            canvas.delete("all")
                            canvas.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="black", width=1)
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Error updating palette swatch {display_idx}: {e}")
        
        # Try forcing a palette refresh
        try:
            self._live_refresh_swatches()
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error refreshing palette swatches: {e}")
        
        # Reapply selection highlighting after color changes
        if hasattr(self, "_update_selection_ui"):
            try:
                self._update_selection_ui()
            except Exception as e:
                print(f"CONSOLE ERROR MSG: Error updating selection UI: {e}")
        
        # Update color picker
        focus = self._live_selected_index
        if focus < len(current_layer.colors):
            fr, fg, fb = current_layer.colors[focus]
            try:
                self._picker_preview.config(bg=f"#{fr:02x}{fg:02x}{fb:02x}")
                self._picker_hex.delete(0, "end")
                self._picker_hex.insert(0, f"#{fr:02x}{fg:02x}{fb:02x}")
            except Exception as e:
                print(f"CONSOLE ERROR MSG: Error updating color picker: {e}")
        
        # Update main image display (debounced to prevent flickering)
        try:
            self._debounced_display_update()
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error updating main image display: {e}")
        
        # Update simple mode preview if in simple mode
        if self.live_pal_ui_mode == "Simple" and hasattr(self, '_update_simple_preview'):
            try:
                self._update_simple_preview()
            except Exception as e:
                print(f"CONSOLE ERROR MSG: Error updating simple mode preview: {e}")
    
    def _advanced_mode_reset(self, current_layer):
        """Reset colors specifically for Advanced mode"""
        # Advanced mode: update all 256 colors
        cols = current_layer.colors
        for i in range(256):  # PALETTE_SIZE = 256
            r, g, b = cols[i] if isinstance(cols[i], tuple) else (0, 0, 0)
            try:
                canvas = self._live_swatches[i]
                hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
                canvas.delete("all")
                canvas.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
            except Exception as e:
                print(f"CONSOLE ERROR MSG: Error updating advanced mode swatch {i}: {e}")
        
        # Keep selection visuals
        if hasattr(self, "_update_selection_ui"):
            try:
                self._update_selection_ui()
            except Exception as e:
                print(f"CONSOLE ERROR MSG: Error updating selection UI: {e}")
        
        # Update color picker
        focus = self._live_selected_index
        if focus < len(current_layer.colors):
            fr, fg, fb = current_layer.colors[focus]
            try:
                self._picker_preview.config(bg=f"#{fr:02x}{fg:02x}{fb:02x}")
                self._picker_hex.delete(0, "end")
                self._picker_hex.insert(0, f"#{fr:02x}{fg:02x}{fb:02x}")
            except Exception as e:
                print(f"CONSOLE ERROR MSG: Error updating color picker: {e}")
        
        # Update main image display (debounced to prevent flickering)
        try:
            self._debounced_display_update()
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error updating main image display: {e}")

    def _open_icon_editor(self):
        """Open the icon palette editor for the current character and fashion type"""
        if not self.current_character:
            messagebox.showwarning("Warning", "Please open a base fashion piece first.")
            return
            
        # Check if hair or third job is selected
        if self.hair_var.get() != "NONE" or self.third_job_var.get() != "NONE":
            messagebox.showwarning("Warning", "You can't do that here!")
            return
            
        # Check if any active layers are base fashion pieces
        has_base_fashion = False
        for layer in self.palette_layers:
            if (layer.active and 
                hasattr(layer, "palette_type") and 
                layer.palette_type.startswith("fashion_") and 
                not (layer.name and ("hair" in layer.name.lower() or "third" in layer.name.lower()))):
                has_base_fashion = True
                break
                
        if not has_base_fashion:
            messagebox.showwarning("Warning", "Please open a base fashion piece first.")
            return
            
        # Track icon editing
        if hasattr(self, 'current_character') and hasattr(self, 'current_job'):
            self.statistics.icons_edited.add(f"{self.current_character}_{self.current_job}")
            self.statistics.preview_indexes_selected['live_icon'] += 1
            self._save_statistics()
        
        # Get the current character ID - use the image folder ID (chr025), not palette ID (chr100)
        char_id = self.current_character
        
        # For Paula, we need to use the image folder ID, not the palette ID
        # The icons are stored in chr025, chr026, chr027 folders, not chr100, chr101, chr102
        image_char_id = char_id  # Keep the original ID for icon folder lookup
        
        try:
            from icon_handler import IconPaletteEditor, IconHandler
            icon_handler = IconHandler()
            icon_handler.main_window = self
            editor = IconPaletteEditor(
                char_id=image_char_id,
                fashion_type="fashion_1",  # Default fashion type
                custom_palette=[(0, 0, 0)] * 256,  # Default palette
                palette_path="temp_main_ui.pal",
                palette_layers=self.palette_layers,
                live_editor_window=None,
                is_quicksave_mode=False,
                icon_handler=icon_handler
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not open icon editor: {str(e)}")

    def reset_to_original(self):
        """Reset all palette selections to their initial state as if the program just started"""
        if not self.original_image:
            messagebox.showinfo("Reset", "No image loaded")
            return
        
        # Reset hair selection to NONE
        self.hair_var.set("NONE")
        
        # Reset all fashion selections to NONE
        for fashion_type, var in self.fashion_vars.items():
            var.set("NONE")
        
        # Special handling for third job characters (except Paula)
        if hasattr(self, 'current_character') and self.current_character:
            char_id = self.current_character
            if (char_id in CHARACTER_MAPPING and 
                CHARACTER_MAPPING[char_id]["job"] == "3rd Job" and
                char_id not in ["chr025", "chr026", "chr027", "chr100", "chr101", "chr102"]):  # Not Paula
                
                # Set the first third job palette as default (like initial load)
                palette_char_id = self.get_palette_character_id(char_id)
                if palette_char_id in self.third_job_palettes and self.third_job_palettes[palette_char_id]:
                    first_palette = self.third_job_palettes[palette_char_id][0]
                    self.third_job_var.set(first_palette)
                else:
                    self.third_job_var.set("NONE")
            else:
                # For all other characters, set third job to NONE
                self.third_job_var.set("NONE")
        else:
            self.third_job_var.set("NONE")
        
        # Reload palettes with the new selections (this will handle third job auto-loading)
        self.load_palettes()
        
        # Update the image display
        self._debounced_display_update()
        messagebox.showinfo("Reset", "Reset all palette selections to initial state")

    def _live_on_swatch_click(self, i, event):
        # Prevent clicks during palette switching to avoid cross-palette contamination
        current_time = time.time()
        switch_time = getattr(self, '_palette_switch_time', 0)
        if current_time - switch_time < 0.1:  # 100ms debounce for clicks
            return
        
        # Set flag to prevent any potential grid recreation during selection updates
        self._updating_live_selection = True
        
        # Detect Shift key for range selection (state bit 0x0001 usually indicates Shift)
        shift = bool(getattr(event, "state", 0) & 0x0001)
        if self._multi_select.get():
            if shift and self._last_clicked_index is not None:
                a, b = sorted((self._last_clicked_index, i))
                for j in range(a, b+1):
                    self._selected_indices.add(j)
            else:
                if i in self._selected_indices:
                    self._selected_indices.remove(i)
                else:
                    self._selected_indices.add(i)
            self._last_clicked_index = i
            self._update_selection_ui()
            # Keep picker synced to last clicked
            self._live_select_index(i)
        else:
            # Single-select - clear previous selection and add current one
            self._selected_indices.clear()
            self._selected_indices.add(i)  # Add the selected index for highlighting
            self._last_clicked_index = i
            self._update_selection_ui()
            self._live_select_index(i)
        
        # Clear the flag to allow any potential grid operations again
        self._updating_live_selection = False

    def _sync_hsv_from_rgb(self, r, g, b):
        try:
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            # guard flag to avoid recursive callbacks
            self._in_sync = True
            if not getattr(self, "_is_dragging", False):
                self._picker_h.set(int(round(h*360)))
                self._picker_s.set(int(round(s*100)))
                self._picker_v.set(int(round(v*100)))
        finally:
            self._in_sync = False

    def _sync_rgb_from_hsv(self, h_deg, s_pct, v_pct):
        """Return RGB ints from HSV without touching non-existent RGB widgets."""
        h = (h_deg % 360) / 360.0
        s = max(0, min(100, int(s_pct))) / 100.0
        v = max(0, min(100, int(v_pct))) / 100.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(round(r*255)), int(round(g*255)), int(round(b*255))


    def _live_hsv_changed(self):
        if getattr(self, "_in_sync", False):
            return

        ly = self._live_current_layer()
        if ly is None:
            return
        
        # Prevent applying colors during palette switching to avoid color copying between palettes
        if getattr(self, '_updating_live_selection', False):
            return
        
        # Additional protection: Check if we just switched palettes recently (debounce)
        current_time = time.time()
        switch_time = getattr(self, '_palette_switch_time', 0)
        if current_time - switch_time < 0.2:  # 200ms debounce
            return
        
        # Verify we're still on the same palette to prevent cross-contamination
        current_name = self._live_target_name.get()
        if hasattr(self, '_current_live_palette_name') and current_name != self._current_live_palette_name:
            return

        H_new = int(self._picker_h.get())
        S_new = int(self._picker_s.get())
        V_new = int(self._picker_v.get())

        targets = sorted(self._selected_indices) if self._multi_select.get() and self._selected_indices else [self._live_selected_index]
        use_relative = self._multi_select.get() and len(targets) > 1

        if use_relative:
            base_i = self._live_selected_index
            br, bg, bb = ly.colors[base_i] if isinstance(ly.colors[base_i], tuple) else (0, 0, 0)
            bh, bs, bv = colorsys.rgb_to_hsv(br/255.0, bg/255.0, bb/255.0)
            bh = int(round(bh * 360))
            bs = int(round(bs * 100))
            bv = int(round(bv * 100))

            dH = H_new - bh
            EPS = 1  # treat <=1% as zero-ish to avoid stuck scaling
            use_scaleS = bs > EPS
            use_scaleV = bv > EPS
            scaleS = (S_new/100.0) / (bs/100.0) if use_scaleS else None
            scaleV = (V_new/100.0) / (bv/100.0) if use_scaleV else None
            # Clamp additive deltas to prevent extreme changes when base color is near black/gray
            dS = max(-50, min(50, S_new - bs)) if not use_scaleS else 0
            dV = max(-50, min(50, V_new - bv)) if not use_scaleV else 0
        else:
            dH = 0; scaleS = 1.0; scaleV = 1.0; dS = 0; dV = 0

        for i in targets:
            r, g, b = ly.colors[i] if isinstance(ly.colors[i], tuple) else (0, 0, 0)
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = int(round(h * 360)); s = int(round(s * 100)); v = int(round(v * 100))

            if use_relative:
                h = (h + dH) % 360
                EPS_TGT = 2
                # Saturation per-swatch: additive if target near zero or scale unavailable; else multiplicative
                if s <= EPS_TGT or scaleS is None:
                    s = max(0, min(100, int(round(s + dS))))
                else:
                    s = max(0, min(100, int(round(s * scaleS))))
                # Value per-swatch: additive if target near zero or scale unavailable; else multiplicative
                if v <= EPS_TGT or scaleV is None:
                    # Additional safety: don't apply extreme negative dV to colors that aren't already dark
                    if dV < -20 and v > 20:  # If trying to apply large negative change to bright color
                        v = max(20, min(100, int(round(v + max(dV, -20)))))  # Limit the darkening
                    else:
                        v = max(0, min(100, int(round(v + dV))))
                else:
                    v = max(0, min(100, int(round(v * scaleV))))
            else:
                h, s, v = H_new % 360, max(0, min(100, S_new)), max(0, min(100, V_new))

            # --- FIX: ensure self.char_num exists ---
            if not hasattr(self, "char_num"):
                import re
                cid = str(getattr(self, "char_id", ""))
                m = re.search(r"(\d+)$", cid)   # e.g. "chr019" -> "019"
                self.char_num = m.group(1) if m else "000"
            # ---------------------------------------

            # Skip if current color is keyed
            current_color = ly.colors[i]
            if (self.is_universal_keying_color(current_color) or 
                current_color == (255, 0, 255) or  # Magenta
                (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(current_color)) or  # Sheep
                (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(current_color)) or  # Raccoon
                (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(current_color)) or  # Sheep 2nd Job
                (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(current_color)) or  # Lion 2nd Job
                (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(current_color, i, self.char_num))):  # Any other character-specific rules
                continue

            rr, gg, bb = colorsys.hsv_to_rgb((h % 360)/360.0, s/100.0, v/100.0)
            rr, gg, bb = int(round(rr*255)), int(round(gg*255)), int(round(bb*255))
            
            # Check if new color would be a keying color
            candidate_color = (rr, gg, bb)
            if (self.is_universal_keying_color(candidate_color) or 
                candidate_color == (255, 0, 255) or  # Magenta
                (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(candidate_color)) or  # Sheep
                (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(candidate_color)) or  # Raccoon
                (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(candidate_color)) or  # Sheep 2nd Job
                (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(candidate_color)) or  # Lion 2nd Job
                (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(candidate_color, i, self.char_num))):  # Any other character-specific rules
                candidate_color = self._find_nearest_non_keyed_color(candidate_color)
                rr, gg, bb = candidate_color
            
            ly.colors[i] = (rr, gg, bb)
            
            # Update temp cache with the new color
            if hasattr(self, '_live_temp_palette_cache') and hasattr(self, '_current_live_palette_name'):
                current_name = getattr(self, '_current_live_palette_name', None)
                if current_name and current_name in self._live_temp_palette_cache:
                    self._live_temp_palette_cache[current_name] = ly.colors.copy()
            
            # Update swatch based on mode
            if self.live_pal_ui_mode == "Simple":
                # Find the display index for this palette index
                editable_indices = self._get_editable_color_indices()
                if i in editable_indices:
                    display_idx = editable_indices.index(i)
                    if display_idx < len(self._live_swatches) and self._live_swatches[display_idx] is not None:
                        canvas = self._live_swatches[display_idx]
                        hex_color = f"#{rr:02x}{gg:02x}{bb:02x}"
                        canvas.delete("all")
                        canvas.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="black", width=1)
            else:
                # Advanced mode: direct index mapping
                if i < len(self._live_swatches) and self._live_swatches[i] is not None:
                    canvas = self._live_swatches[i]
                    hex_color = f"#{rr:02x}{gg:02x}{bb:02x}"
                    canvas.delete("all")
                    canvas.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
        # Reapply selection highlighting after color changes
        if hasattr(self, "_update_selection_ui"):
            self._update_selection_ui()
        focus = self._live_selected_index
        fr, fg, fb = ly.colors[focus]
        self._picker_preview.config(bg=f"#{fr:02x}{fg:02x}{fb:02x}")
        self._picker_hex.delete(0, "end"); self._picker_hex.insert(0, f"#{fr:02x}{fg:02x}{fb:02x}")

        self._debounced_display_update()
        
        # Update simple mode preview if in simple mode
        if self.live_pal_ui_mode == "Simple" and hasattr(self, '_update_simple_preview'):
            self._update_simple_preview()

        self._in_sync = True
        try:
            if not getattr(self, "_is_dragging", False):
                if use_relative:
                    self._picker_h.set(int(H_new % 360))
                    self._picker_s.set(int(max(0, min(100, S_new))))
                    self._picker_v.set(int(max(0, min(100, V_new))))
                else:
                    fh, fs, fv = colorsys.rgb_to_hsv(fr/255.0, fg/255.0, fb/255.0)
                    self._picker_h.set(int(round(fh * 360)))
                    self._picker_s.set(int(round(fs * 100)))
                    self._picker_v.set(int(round(fv * 100)))
        finally:
            self._in_sync = False
        # Sync numeric entry boxes if present
        try:
            self._hsv_h_str.set(str(int(self._picker_h.get())))
            self._hsv_s_str.set(str(int(self._picker_s.get())))
            self._hsv_v_str.set(str(int(self._picker_v.get())))
        except Exception:
            pass




    def _live_refresh_swatches(self):
        """Refresh swatch button colors from the currently selected layer; keep selection highlight."""
        # Don't refresh if we're currently updating selection to prevent conflicts
        if getattr(self, '_updating_live_selection', False):
            return
            
        ly = self._live_current_layer()
        if ly is None:
            return
        cols = ly.colors
        
        if self.live_pal_ui_mode == "Simple":
            # Simple mode: only update editable color swatches
            editable_indices = self._get_editable_color_indices()
            for display_idx, palette_idx in enumerate(editable_indices):
                if display_idx >= len(self._live_swatches) or self._live_swatches[display_idx] is None:
                    continue
                
                r, g, b = cols[palette_idx] if isinstance(cols[palette_idx], tuple) else (0, 0, 0)
                try:
                    canvas = self._live_swatches[display_idx]
                    hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
                    canvas.delete("all")
                    # Use larger rectangle size for simple mode (40x40)
                    canvas.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="black", width=1)
                except Exception:
                    pass
        else:
            # Advanced mode: update all 256 colors
            for i in range(PALETTE_SIZE):
                r,g,b = cols[i] if isinstance(cols[i], tuple) else (0,0,0)
                try:
                    # Update canvas rectangle color
                    canvas = self._live_swatches[i]
                    if canvas is None:
                        continue
                    hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
                    canvas.delete("all")
                    canvas.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
                except Exception:
                    pass
        
        # Keep selection visuals
        if hasattr(self, "_update_selection_ui"):
            self._update_selection_ui()
        
        # Update simple mode preview if in simple mode
        if self.live_pal_ui_mode == "Simple" and hasattr(self, '_update_simple_preview'):
            self._update_simple_preview()

    def _live_on_target_changed(self, *_):
        """Called when the item dropdown changes; rebuild swatches for the new layer and reset selection."""
        
        # Ask warning if switching to Hair or 3rd Job Base
        try:
            new_name = self._live_target_name.get()
            idx = self._live_name_to_index.get(new_name, 0)
            ly = self._live_layers[idx]
            
            # Update palette job mapping for the new selection
            if hasattr(ly, "palette_type"):
                char_match = re.search(r'chr(\d{3})', new_name)
                if char_match:
                    char_num = char_match.group(1)
                    if char_num in CHARACTER_MAPPING:
                        char_info = CHARACTER_MAPPING[char_num]
                        self._live_palette_job_mapping[new_name] = {
                            'palette_type': ly.palette_type,
                            'character': char_info['name'],
                            'job': char_info['job']
                        }
            
            # Store UI mode before warning dialog
            current_ui_mode = getattr(self, 'live_pal_ui_mode', 'Simple')
            if not self._warn_if_nonimpact(getattr(ly, "palette_type", "")):
                # Revert selection
                try:
                    self._live_target_name.set(getattr(self, "_live_prev_target_name", new_name))
                except Exception:
                    pass
                # Restore UI mode after warning dialog
                self.live_pal_ui_mode = current_ui_mode
                # Bring live editor window to front after user clicked "No"
                if hasattr(self, '_live_editor_window') and self._live_editor_window and self._live_editor_window.winfo_exists():
                    self._live_editor_window.lift()
                    self._live_editor_window.focus_force()
                return
            # Restore UI mode after warning dialog
            self.live_pal_ui_mode = current_ui_mode
            self._live_prev_target_name = new_name
            
            # Update icon editor button state after switching palette types
            self._update_icon_editor_button_state()
        except Exception:
            pass
        # Save current palette's temporary changes to cache before switching
        if hasattr(self, '_current_live_palette_name') and hasattr(self, '_live_temp_palette_cache'):
            old_name = getattr(self, '_current_live_palette_name', None)
            if old_name and old_name in self._live_name_to_index:
                old_idx = self._live_name_to_index[old_name]
                if old_idx < len(self._live_layers):
                    # Save current state to temp cache
                    self._live_temp_palette_cache[old_name] = self._live_layers[old_idx].colors.copy()
        
        # Clear all selection state to prevent color copying between palettes
        self._selected_indices = set()
        self._last_clicked_index = None
        self._live_selected_index = 0  # Reset to first color
        
        # Track current palette to prevent cross-palette contamination
        self._current_live_palette_name = new_name
        
        # Set flag to prevent color changes during palette switching with timestamp
        self._updating_live_selection = True
        self._palette_switch_time = time.time() if hasattr(time, 'time') else 0
        
        # Restore temporary changes for the newly selected layer from cache
        if hasattr(self, '_live_temp_palette_cache') and new_name in self._live_temp_palette_cache:
            # Restore from temp cache to preserve temporary changes
            ly.colors = self._live_temp_palette_cache[new_name].copy()
        elif hasattr(self, '_live_original_colors') and new_name in self._live_original_colors:
            # Fallback to original colors if not in temp cache (shouldn't happen normally)
            ly.colors = self._live_original_colors[new_name].copy()
            # Also add to temp cache for future switches
            if hasattr(self, '_live_temp_palette_cache'):
                self._live_temp_palette_cache[new_name] = ly.colors.copy()
        
        # Update palette colors for the new layer without rebuilding entire UI
        if self.live_pal_ui_mode == "Simple":
            self._update_simple_palette_colors(ly)
        else:
            # For advanced mode, update existing swatches
            if hasattr(self, '_live_swatches') and self._live_swatches:
                for i, canvas in enumerate(self._live_swatches):
                    if canvas is not None and i < len(ly.colors):
                        r, g, b = ly.colors[i] if isinstance(ly.colors[i], tuple) else (0, 0, 0)
                        hex_color = f"#{r:02x}{g:02x}{b:02x}"
                        try:
                            canvas.delete("all")
                            canvas.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
                        except:
                            pass
        
        # Update simple mode preview if in simple mode
        if self.live_pal_ui_mode == "Simple" and hasattr(self, '_update_simple_preview'):
            self._update_simple_preview()
        
        # Notify the icon editor if it's open
        self._notify_icon_editor_palette_change()
        # Seed picker with index 0 for the new layer
        self._live_select_index(0)
        
        # Clear the updating flag after a short delay to ensure all palette switching is complete
        def clear_protection():
            self._updating_live_selection = False
            # Update the palette name tracking
            self._current_live_palette_name = new_name
        
        # Use a small delay to ensure all UI updates are complete before allowing color changes
        try:
            self.master.after(250, clear_protection)  # 250ms delay
        except:
            # Fallback if master doesn't exist
            clear_protection()
    
    def _notify_icon_editor_palette_change(self):
        """Notify the icon editor that palette layers have changed."""
        try:
            from icon_handler import IconHandler
            if (IconHandler._icon_editor_instance and 
                IconHandler._icon_editor_instance.window and 
                IconHandler._icon_editor_instance.window.winfo_exists()):
                # Update the icon editor's palette layers
                IconHandler._icon_editor_instance.update_palette_layers(self.palette_layers)
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error notifying icon editor of palette change: {e}")

    def _live_current_layer(self):
        if not hasattr(self, "_live_layers") or not self._live_layers:
            return None
        idx = self._live_name_to_index.get(self._live_target_name.get(), 0)
        idx = max(0, min(idx, len(self._live_layers)-1))
        return self._live_layers[idx]

    def _live_select_index(self, i):
        i = int(i)
        # Don't update if it's the same index (prevents double-click issues)
        if hasattr(self, '_live_selected_index') and self._live_selected_index == i:
            return
            
        # Track index selection
        self.statistics.indexes_selected += 1
        self.statistics.preview_indexes_selected['live_pal'] += 1
        self._save_statistics()
            
        self._live_selected_index = i
        self._picker_idx_var.set(str(i))
        ly = self._live_current_layer()
        if ly is None:
            return
        r,g,b = ly.colors[i] if isinstance(ly.colors[i], tuple) else (0,0,0)
        # Update HEX + preview
        self._picker_hex.delete(0, "end"); self._picker_hex.insert(0, f"#{int(r):02x}{int(g):02x}{int(b):02x}")
        self._picker_preview.config(bg=f"#{int(r):02x}{int(g):02x}{int(b):02x}")
        # Sync HSV sliders from this RGB
        self._sync_hsv_from_rgb(int(r), int(g), int(b))


    def _live_goto_index(self):
        try:
            i = int(self._picker_idx_var.get())
        except Exception:
            i = 0
        i = max(0, min(255, i))
        self._live_select_index(i)

    def _live_apply_hex(self):

        txt = self._picker_hex.get().strip()
        if txt.startswith("#"):
            txt = txt[1:]
        if len(txt) != 6:
            return
        try:
            r = int(txt[0:2], 16); g = int(txt[2:4], 16); b = int(txt[4:6], 16)
        except Exception:
            return
        # Directly apply RGB to the palette
        ly = self._live_current_layer()
        if ly is None:
            return
        
        # Prevent applying colors during palette switching to avoid color copying between palettes
        if getattr(self, '_updating_live_selection', False):
            return
        
        # Additional protection: Check if we just switched palettes recently (debounce)
        current_time = time.time()
        switch_time = getattr(self, '_palette_switch_time', 0)
        if current_time - switch_time < 0.2:  # 200ms debounce
            return
        
        # Verify we're still on the same palette to prevent cross-contamination
        current_name = self._live_target_name.get()
        if hasattr(self, '_current_live_palette_name') and current_name != self._current_live_palette_name:
            return
            
        targets = sorted(self._selected_indices) if self._multi_select.get() and self._selected_indices else [self._live_selected_index]
        for i in targets:
            ly.colors[i] = (r, g, b)
            # Track statistics
            self.statistics.indexes_changed += 1
            self.statistics.colors_saved += 1
            if hasattr(self, 'current_character') and hasattr(self, 'current_job'):
                self.statistics.add_palette_edit(self.current_character, self.current_job)
                self.statistics.live_palette_files_edited.add(ly.name)
            self._save_statistics()
            
            # Update swatch based on mode
            if self.live_pal_ui_mode == "Simple":
                # Find the display index for this palette index
                editable_indices = self._get_editable_color_indices()
                if i in editable_indices:
                    display_idx = editable_indices.index(i)
                    if display_idx < len(self._live_swatches) and self._live_swatches[display_idx] is not None:
                        canvas = self._live_swatches[display_idx]
                        hex_color = f"#{r:02x}{g:02x}{b:02x}"
                        canvas.delete("all")
                        canvas.create_rectangle(1, 1, 39, 39, fill=hex_color, outline="black", width=1)
            else:
                # Advanced mode: direct index mapping
                if i < len(self._live_swatches) and self._live_swatches[i] is not None:
                    canvas = self._live_swatches[i]
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.delete("all")
                    canvas.create_rectangle(1, 1, 19, 19, fill=hex_color, outline="black", width=1)
        # Reapply selection highlighting after color changes
        if hasattr(self, "_update_selection_ui"):
            self._update_selection_ui()
        self._picker_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")
        self._debounced_display_update()
        # Sync HSV sliders from this RGB
        self._sync_hsv_from_rgb(r, g, b)
        
        # Update simple mode preview if in simple mode
        if self.live_pal_ui_mode == "Simple" and hasattr(self, '_update_simple_preview'):
            self._update_simple_preview()


    def _live_slider_changed(self):
        # RGB sliders removed in HSV-only mode; keep as no-op to satisfy any callers.
        return


    def _open_gradient_menu(self):
        """Open the gradient/hue adjustment menu."""
        import colorsys
        
        # Create gradient menu window
        gradient_window = tk.Toplevel(self._live_editor_window)
        gradient_window.title("Gradient Hue Adjustment")
        gradient_window.resizable(False, False)
        gradient_window.transient(self._live_editor_window)
        gradient_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(gradient_window)
        main_frame.pack(padx=15, pady=15)
        
        # Title
        tk.Label(main_frame, text="Adjust all colors to match:", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        
        # HSL adjustment checkboxes
        checkbox_frame = tk.Frame(main_frame)
        checkbox_frame.pack(pady=(0, 10))
        
        # Hue checkbox
        hue_var = tk.BooleanVar(value=self._gradient_adjust_hue)
        hue_cb = tk.Checkbutton(checkbox_frame, text="Hue", variable=hue_var,
                               command=lambda: self._update_gradient_settings('hue', hue_var.get()))
        hue_cb.pack(side="left", padx=5)
        
        # Saturation checkbox
        sat_var = tk.BooleanVar(value=self._gradient_adjust_saturation)
        sat_cb = tk.Checkbutton(checkbox_frame, text="Saturation", variable=sat_var,
                               command=lambda: self._update_gradient_settings('saturation', sat_var.get()))
        sat_cb.pack(side="left", padx=5)
        
        # Value checkbox
        value_var = tk.BooleanVar(value=self._gradient_adjust_value)
        value_cb = tk.Checkbutton(checkbox_frame, text="Value", variable=value_var,
                               command=lambda: self._update_gradient_settings('value', value_var.get()))
        value_cb.pack(side="left", padx=5)
        
        # Define expanded gradient colors with light/dark variants and additional colors
        gradient_colors = [
            # Row 1: Pastel variants
            ("Pastel Pink", "#FFD1DC", 350, "pastel"),
            ("Pastel Peach", "#FFDBCC", 20, "pastel"),
            ("Pastel Yellow", "#FFFACD", 60, "pastel"),
            ("Pastel Mint", "#F0FFF0", 120, "pastel"),
            ("Pastel Blue", "#E6E6FA", 240, "pastel"),
            ("Pastel Lavender", "#E6E6FA", 270, "pastel"),
            ("Pastel Rose", "#F8BBD0", 330, "pastel"),
            ("Pastel Aqua", "#E0FFFF", 180, "pastel"),
            
            # Row 2: Light variants
            ("Light Red", "#FFB3B3", 0, "light"),
            ("Light Orange", "#FFD9B3", 30, "light"), 
            ("Light Yellow", "#FFFF99", 60, "light"),
            ("Light Green", "#B3FFB3", 120, "light"),
            ("Light Blue", "#B3B3FF", 240, "light"),
            ("Light Purple", "#D9B3FF", 270, "light"),
            ("Pink", "#FF69B4", 330),
            ("Cyan", "#00FFFF", 180),
            
            # Row 3: Standard colors (ROYGBIV + extras)
            ("Red", "#FF0000", 0),
            ("Orange", "#FF8000", 30), 
            ("Yellow", "#FFFF00", 60),
            ("Green", "#00FF00", 120),
            ("Blue", "#0000FF", 240),
            ("Purple", "#8000FF", 270),
            ("Magenta", "#FF00FF", 300),
            ("Teal", "#008080", 180),
            
            # Row 4: Dark variants
            ("Dark Red", "#800000", 0, "dark"),
            ("Dark Orange", "#CC4400", 30, "dark"), 
            ("Dark Yellow", "#CCCC00", 60, "dark"),
            ("Dark Green", "#008000", 120, "dark"),
            ("Dark Blue", "#000080", 240, "dark"),
            ("Dark Purple", "#4B0082", 270, "dark"),
            ("Brown", "#8B4513", 30, "brown"),
            ("Navy", "#191970", 240, "dark"),
            
            # Row 5: Cool colors
            ("Cool Blue", "#0080FF", 210, "cool"),
            ("Cool Cyan", "#00BFFF", 195, "cool"),
            ("Cool Teal", "#008B8B", 180, "cool"),
            ("Cool Green", "#00FF80", 150, "cool"),
            ("Cool Purple", "#8000FF", 270, "cool"),
            ("Cool Violet", "#4000FF", 255, "cool"),
            ("Cool Indigo", "#4B0082", 275, "cool"),
            ("Cool Mint", "#00FF9F", 165, "cool"),
            
            # Row 6: Warm colors
            ("Warm Red", "#FF4000", 15, "warm"),
            ("Warm Orange", "#FF8000", 30, "warm"),
            ("Warm Yellow", "#FFD700", 51, "warm"),
            ("Warm Pink", "#FF69B4", 330, "warm"),
            ("Warm Coral", "#FF7F50", 16, "warm"),
            ("Warm Peach", "#FFCBA4", 28, "warm"),
            ("Warm Gold", "#FFD700", 51, "warm"),
            ("Warm Amber", "#FFBF00", 45, "warm"),
            
            # Row 7: Secondary colors
            ("Orange", "#FF8000", 30, "secondary"),
            ("Green", "#00FF00", 120, "secondary"),
            ("Purple", "#8000FF", 270, "secondary"),
            ("Lime", "#80FF00", 90, "secondary"),
            ("Teal", "#00FF80", 150, "secondary"),
            ("Magenta", "#FF0080", 315, "secondary"),
            ("Chartreuse", "#80FF00", 90, "secondary"),
            ("Spring Green", "#00FF80", 150, "secondary"),
            
            # Row 8: Tertiary colors
            ("Red-Orange", "#FF4000", 15, "tertiary"),
            ("Yellow-Orange", "#FFBF00", 45, "tertiary"),
            ("Yellow-Green", "#80FF00", 90, "tertiary"),
            ("Blue-Green", "#00FF80", 150, "tertiary"),
            ("Blue-Purple", "#4000FF", 255, "tertiary"),
            ("Red-Purple", "#FF0080", 315, "tertiary"),
            ("Vermillion", "#FF4000", 15, "tertiary"),
            ("Turquoise", "#00FFBF", 165, "tertiary"),
            
            # Row 9: Neutrals and special
            ("Light Grey", "#C0C0C0", None, "light_grey"),
            ("Grey", "#808080", None, "grey"),
            ("Dark Grey", "#404040", None, "dark_grey"),
            ("White", "#FFFFFF", None, "white"),
            ("Black", "#000000", None, "black"),
            ("Beige", "#F5F5DC", 60, "beige"),
            ("Cream", "#FFFDD0", 60, "cream"),
            ("Tan", "#D2B48C", 30, "tan")
        ]
        
        # Create frame for color buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=(0, 10))
        
        # Create color buttons in a grid (9 rows of 8)
        rows_data = [
            ("Pastel:", gradient_colors[:8]),
            ("Light:", gradient_colors[8:16]),
            ("Standard:", gradient_colors[16:24]),
            ("Dark:", gradient_colors[24:32]),
            ("Cool:", gradient_colors[32:40]),
            ("Warm:", gradient_colors[40:48]),
            ("Secondary:", gradient_colors[48:56]),
            ("Tertiary:", gradient_colors[56:64]),
            ("Neutral:", gradient_colors[64:72])
        ]
        
        for row_idx, (label, colors) in enumerate(rows_data):
            row = tk.Frame(button_frame)
            if row_idx < len(rows_data) - 1:  # All rows except last
                row.pack(pady=(0, 3), anchor="w")
            else:  # Last row
                row.pack(anchor="w")
            
            tk.Label(row, text=label, font=("Arial", 8)).pack(side="left", padx=(0, 5))
            
            for color_data in colors:
                if color_data:  # Check if color_data exists
                    name, hex_color = color_data[0], color_data[1]
                    target_hue = color_data[2] if len(color_data) > 2 else None
                    variant = color_data[3] if len(color_data) > 3 else None
                    btn = tk.Button(row, text="  ", bg=hex_color, width=3, height=1,
                                  command=lambda h=target_hue, n=name, v=variant: self._apply_gradient_hue(h, n, v))
                    btn.pack(side="left", padx=1)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=(10, 0))
        
        # Reset to Original button
        tk.Button(buttons_frame, text="Reset to Original", command=self._reset_gradient_colors).pack(side="left", padx=(0, 10))
        
        # Close button
        tk.Button(buttons_frame, text="Close", command=gradient_window.destroy).pack(side="left")
        
        # Center the window
        gradient_window.update_idletasks()
        width = gradient_window.winfo_width()
        height = gradient_window.winfo_height()
        x = self._live_editor_window.winfo_x() + (self._live_editor_window.winfo_width() - width) // 2
        y = self._live_editor_window.winfo_y() + (self._live_editor_window.winfo_height() - height) // 2
        gradient_window.geometry(f"+{x}+{y}")
        
        # Add arrow key bindings to control simple preview frames when gradient menu is open
        def _on_gradient_key(event):
            if self.live_pal_ui_mode == "Simple":
                if event.keysym == "Left":
                    self._simple_prev_frame()
                elif event.keysym == "Right":
                    self._simple_next_frame()
        
        gradient_window.bind("<Left>", _on_gradient_key)
        gradient_window.bind("<Right>", _on_gradient_key)
        gradient_window.focus_set()  # Make sure gradient window can receive key events

    def _apply_gradient_hue(self, target_hue, color_name, variant=None):
        """Apply hue adjustment to colors in the current palette."""
        import colorsys

        # --- FIX: ensure self.char_num exists ---
        if not hasattr(self, "char_num"):
            import re
            cid = str(getattr(self, "char_id", ""))
            m = re.search(r"(\d+)$", cid)   # e.g. "chr019" -> "019"
            self.char_num = m.group(1) if m else "000"
        # ---------------------------------------

        ly = self._live_current_layer()
        if ly is None:
            return

        # Determine which indices to modify based on multiselect state
        if self._multi_select.get() and self._selected_indices:
            indices_to_modify = self._selected_indices
        else:
            indices_to_modify = range(len(ly.colors))
            
        # Special handling for neutral colors and variants
        if target_hue is None or variant in ["grey", "light_grey", "dark_grey", "black", "white"]:
            if variant == "light_grey" or color_name == "Light Grey":
                # Convert to light greyscale
                for i in indices_to_modify:
                    if i < len(ly.colors) and isinstance(ly.colors[i], tuple):
                        r, g, b = ly.colors[i]
                        grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                        # Make it lighter
                        light_grey = min(255, int(grey * 1.5))
                        ly.colors[i] = (light_grey, light_grey, light_grey)
            elif variant == "dark_grey" or color_name == "Dark Grey":
                # Convert to dark greyscale
                for i in indices_to_modify:
                    if i < len(ly.colors) and isinstance(ly.colors[i], tuple):
                        r, g, b = ly.colors[i]
                        grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                        # Make it darker
                        dark_grey = int(grey * 0.5)
                        ly.colors[i] = (dark_grey, dark_grey, dark_grey)
            elif variant == "grey" or color_name == "Grey":
                # Convert all colors to greyscale
                for i in indices_to_modify:
                    if i < len(ly.colors) and isinstance(ly.colors[i], tuple):
                        r, g, b = ly.colors[i]
                        grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                        ly.colors[i] = (grey, grey, grey)
            elif variant == "black" or color_name == "Black":
                # Make all colors darker (reduce value significantly)
                for i in indices_to_modify:
                    if i < len(ly.colors) and isinstance(ly.colors[i], tuple):
                        r, g, b = ly.colors[i]
                        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                        v = v * 0.2  # Reduce brightness to 20%
                        rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                        ly.colors[i] = (int(rr*255), int(gg*255), int(bb*255))
            elif variant == "white" or color_name == "White":
                # Make all colors lighter (increase value significantly)
                for i in indices_to_modify:
                    if i < len(ly.colors) and isinstance(ly.colors[i], tuple):
                        r, g, b = ly.colors[i]
                        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                        v = min(1.0, v + (1.0 - v) * 0.8)  # Increase brightness towards white
                        rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                        ly.colors[i] = (int(rr*255), int(gg*255), int(bb*255))
        else:
            # Apply hue adjustment with optional lightness/darkness variants
            for i in indices_to_modify:
                if i < len(ly.colors) and isinstance(ly.colors[i], tuple):
                    r, g, b = ly.colors[i]
                    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                    
                    # Store original HSV values
                    orig_h, orig_s, orig_v = h, s, v
                    
                    # Only adjust hue if enabled and color has some saturation
                    if self._gradient_adjust_hue and s > 0.1:  # Threshold to avoid adjusting near-grey colors
                        # Calculate hue difference and apply it
                        current_hue = h * 360
                        hue_diff = target_hue - current_hue
                        
                        # Normalize hue difference to [-180, 180] range for shortest rotation
                        if hue_diff > 180:
                            hue_diff -= 360
                        elif hue_diff < -180:
                            hue_diff += 360
                            
                        new_hue = (current_hue + hue_diff) % 360
                        h = new_hue / 360.0
                    
                    # Adjust saturation if enabled
                    if self._gradient_adjust_saturation:
                        s = orig_s  # Use original saturation as target
                        
                    # Adjust value if enabled
                    if self._gradient_adjust_value:
                        v = orig_v  # Use original value as target
                    
                    # Apply value variants
                    if variant == "pastel":
                        # Make colors very light and soft by increasing value and significantly reducing saturation
                        v = min(1.0, v + (1.0 - v) * 0.8)  # Increase brightness significantly
                        s = s * 0.3  # Reduce saturation significantly for soft pastel effect
                    elif variant == "light":
                        # Make colors lighter by increasing value and reducing saturation slightly
                        v = min(1.0, v + (1.0 - v) * 0.6)  # Increase brightness
                        s = s * 0.7  # Reduce saturation for pastel effect
                    elif variant == "dark":
                        # Make colors darker by decreasing value
                        v = v * 0.4  # Reduce brightness significantly
                    elif variant in ["beige", "cream", "tan"]:
                        # Special handling for earth tones - reduce saturation and adjust value
                        s = s * 0.3  # Very low saturation
                        if variant == "cream":
                            v = min(1.0, v + (1.0 - v) * 0.7)  # Light
                        elif variant == "tan":
                            v = v * 0.8  # Medium
                        else:  # beige
                            v = min(1.0, v + (1.0 - v) * 0.4)  # Light-medium
                elif variant == "brown":
                    # Brown is essentially dark orange with low saturation
                    s = s * 0.6
                    v = v * 0.5
                elif variant == "cool":
                    # Cool colors: slightly increase saturation and maintain cooler hues
                    s = min(1.0, s * 1.2)  # Increase saturation slightly
                    v = min(1.0, v * 1.1)  # Slightly brighter
                elif variant == "warm":
                    # Warm colors: increase saturation and warmth
                    s = min(1.0, s * 1.3)  # Increase saturation more
                    v = min(1.0, v * 1.05)  # Slightly brighter
                elif variant == "secondary":
                    # Secondary colors: full saturation, balanced brightness
                    s = min(1.0, s * 1.5)  # High saturation
                    v = min(1.0, v * 1.1)  # Slightly brighter
                elif variant == "tertiary":
                    # Tertiary colors: balanced saturation and brightness
                    s = min(1.0, s * 1.2)  # Moderate saturation increase
                    v = min(1.0, v * 1.05)  # Slightly brighter
                    
                # Skip if current color is keyed
                current_color = ly.colors[i]
                if (self.is_universal_keying_color(current_color) or 
                    current_color == (255, 0, 255) or  # Magenta
                    (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(current_color)) or  # Sheep
                    (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(current_color)) or  # Raccoon
                    (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(current_color)) or  # Sheep 2nd Job
                    (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(current_color)) or  # Lion 2nd Job
                    (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(current_color, i, self.char_num))):  # Any other character-specific rules
                    continue
                    
                # Convert back to RGB (for all variants)
                rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                candidate_color = (int(rr*255), int(gg*255), int(bb*255))
                
                # Check if new color would be a keying color
                if (self.is_universal_keying_color(candidate_color) or 
                    candidate_color == (255, 0, 255) or  # Magenta
                    (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(candidate_color)) or  # Sheep
                    (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(candidate_color)) or  # Raccoon
                    (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(candidate_color)) or  # Sheep 2nd Job
                    (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(candidate_color)) or  # Lion 2nd Job
                    (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(candidate_color, i, self.char_num))):  # Any other character-specific rules
                    candidate_color = self._find_nearest_non_keyed_color(candidate_color)
                
                ly.colors[i] = candidate_color
        
        # Update the UI
        self._live_refresh_swatches()
        self._debounced_display_update()
        
        # Update selection UI if available
        if hasattr(self, "_update_selection_ui"):
            self._update_selection_ui()
    
    def _update_gradient_settings(self, setting, value):
        """Update the HSL adjustment settings."""
        if setting == 'hue':
            self._gradient_adjust_hue = value
        elif setting == 'saturation':
            self._gradient_adjust_saturation = value
        elif setting == 'value':
            self._gradient_adjust_value = value
    
    def _reset_gradient_colors(self):
        """Reset colors to original palette colors before gradient changes and reset HSL settings."""
        # Reset HSL settings to defaults
        self._gradient_adjust_hue = True
        self._gradient_adjust_saturation = False
        self._gradient_adjust_value = False
        ly = self._live_current_layer()
        if ly is None:
            return
        
        # Check if we have original colors stored
        if hasattr(ly, '_original_colors') and ly._original_colors:
            # Restore from stored original colors
            ly.colors = ly._original_colors.copy()
        else:
            # Fallback: try to reload from the original palette file
            try:
                # Try to reload the vanilla palette for this layer
                if hasattr(ly, 'name') and ly.name:
                    # Extract character and palette type info from layer name
                    import re
                    char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
                    if char_match:
                        char_num = char_match.group(1)
                        palette_type = getattr(ly, 'palette_type', '')
                        
                        # Load vanilla palette
                        vanilla_colors = self._load_vanilla_palette_for_layer(char_num, palette_type, ly.name)
                        if vanilla_colors:
                            ly.colors = vanilla_colors.copy()
                            # Store as original colors for future resets
                            ly._original_colors = vanilla_colors.copy()
                        else:
                            print(f"Could not load vanilla palette for {ly.name}")
                    else:
                        print(f"Could not extract character info from layer name: {ly.name}")
                else:
                    print("CONSOLE ERROR MSG: Layer has no name attribute for vanilla palette lookup")
            except Exception as e:
                print(f"CONSOLE ERROR MSG: Error resetting gradient colors: {e}")
        
        # Update the UI
        self._live_refresh_swatches()
        self._debounced_display_update()
        
        # Update selection UI if available
        if hasattr(self, "_update_selection_ui"):
            self._update_selection_ui()
    
    def _load_vanilla_palette_for_layer(self, char_num, palette_type, layer_name):
        """Load original palette colors for a specific layer (handles both custom and vanilla palettes)."""
        try:
            # First, check if this is a custom palette by looking in custom directories
            root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Check custom hair directory
            if palette_type == "hair":
                custom_hair_dir = os.path.join(root_dir, "exports", "custom_pals", "hair")
                custom_hair_file = os.path.join(custom_hair_dir, layer_name)
                
                if os.path.exists(custom_hair_file):
                    # This is a custom hair palette, load the original custom file
                    print(f"Loading original custom hair palette: {custom_hair_file}")
                    with open(custom_hair_file, 'rb') as f:
                        pal_data = f.read()
                    
                    colors = []
                    for i in range(0, len(pal_data), 3):
                        if i + 2 < len(pal_data):
                            r, g, b = pal_data[i], pal_data[i+1], pal_data[i+2]
                            colors.append((r, g, b))
                    return colors
            
            # Check custom fashion directories
            elif palette_type.startswith("fashion_"):
                custom_fashion_dir = os.path.join(root_dir, "exports", "custom_pals", "fashion")
                old_custom_fashion_dir = os.path.join(root_dir, "exports", "custom_fashion_pals")
                
                for custom_dir in [custom_fashion_dir, old_custom_fashion_dir]:
                    custom_fashion_file = os.path.join(custom_dir, layer_name)
                    if os.path.exists(custom_fashion_file):
                        # This is a custom fashion palette, load the original custom file
                        print(f"Loading original custom fashion palette: {custom_fashion_file}")
                        with open(custom_fashion_file, 'rb') as f:
                            pal_data = f.read()
                        
                        colors = []
                        for i in range(0, len(pal_data), 3):
                            if i + 2 < len(pal_data):
                                r, g, b = pal_data[i], pal_data[i+1], pal_data[i+2]
                                colors.append((r, g, b))
                        return colors
            
            # If not found in custom directories, try vanilla directories
            script_dir = os.path.dirname(os.path.abspath(__file__))
            vanilla_dir = os.path.join(script_dir, "nonremovable_assets", "vanilla_pals")
            
            if palette_type == "hair":
                # For vanilla hair palettes, use the exact layer name
                vanilla_file = os.path.join(vanilla_dir, "hair", layer_name)
            elif palette_type.startswith("fashion_"):
                # For vanilla fashion palettes, use the exact layer name
                vanilla_file = os.path.join(vanilla_dir, "fashion", layer_name)
            elif palette_type == "3rd_job_base":
                vanilla_file = os.path.join(vanilla_dir, "3rd_default_fashion", layer_name)
            else:
                return None
            
            if os.path.exists(vanilla_file):
                # Load vanilla palette file
                print(f"Loading original vanilla palette: {vanilla_file}")
                with open(vanilla_file, 'rb') as f:
                    pal_data = f.read()
                
                # Parse palette data
                colors = []
                for i in range(0, len(pal_data), 3):
                    if i + 2 < len(pal_data):
                        r, g, b = pal_data[i], pal_data[i+1], pal_data[i+2]
                        colors.append((r, g, b))
                
                return colors
            else:
                print(f"Original palette file not found: {vanilla_file}")
                return None
                
        except Exception as e:
            print(f"CONSOLE ERROR MSG: Error loading original palette: {e}")
            return None
    
    def _is_keyed_color(self, color, index):
        """Check if a color would be a keying color that should be avoided."""
        r, g, b = color
        # Check if it matches common keying colors
        if (r, g, b) == (255, 0, 255):  # Magenta
            return True
        if (r, g, b) == (0, 255, 0):    # Green
            return True
        # Check if it's very close to keying colors (within 10 units)
        if abs(r - 255) < 10 and abs(g - 0) < 10 and abs(b - 255) < 10:  # Close to magenta
            return True
        if abs(r - 0) < 10 and abs(g - 255) < 10 and abs(b - 0) < 10:    # Close to green
            return True
        return False
    
    def _find_nearest_non_keyed_color(self, color):
        """Find the nearest color that isn't a keying color."""
        r, g, b = color
        # Simple approach: adjust the color slightly to avoid keying
        if self._is_keyed_color((r, g, b), 0):
            # Try adjusting each channel slightly
            for offset in [5, -5, 10, -10, 15, -15]:
                for channel in ['r', 'g', 'b']:
                    test_color = [r, g, b]
                    if channel == 'r':
                        test_color[0] = max(0, min(255, r + offset))
                    elif channel == 'g':
                        test_color[1] = max(0, min(255, g + offset))
                    elif channel == 'b':
                        test_color[2] = max(0, min(255, b + offset))
                    
                    if not self._is_keyed_color(tuple(test_color), 0):
                        return tuple(test_color)
        
        # If all else fails, return the original color
        return color

    def _live_save_item_pal(self):
        from tkinter import messagebox
        
        ly = self._live_current_layer()
        if ly is None:
            return
        colors = ly.colors
        default_name = os.path.splitext(ly.name)[0] + ".pal"
        
        # Set initial directory to exports/custom_pals/fashion
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        initial_dir = os.path.join(root_dir, "exports", "custom_pals", "fashion")
        os.makedirs(initial_dir, exist_ok=True)
        
        path = filedialog.asksaveasfilename(
            title="Save Item .pal", 
            defaultextension=".pal",
            initialfile=default_name, 
            initialdir=initial_dir,
            filetypes=[("VGA 24-bit Palette Files","*.pal")]
        )
        if not path:
            return
            
        try:
            # First save the palette file
            # Ensure we have exactly 256 colors for VGA palette
            vga_colors = list(colors)
            while len(vga_colors) < 256:
                vga_colors.append((0, 0, 0))  # Fill with black if needed
            
            # Write VGA 24-bit format: each color as 3 bytes (R, G, B) in sequence
            non_keyed_count = 0
            with open(path, "wb") as f:
                for r,g,b in vga_colors[:256]:  # Ensure exactly 256 colors
                    f.write(bytes([r,g,b]))
                    # Count non-keying colors (not magenta)
                    if (r,g,b) != (255,0,255):
                        non_keyed_count += 1
            messagebox.showinfo("Saved", f"Saved VGA 24-bit palette {os.path.basename(path)} for {ly.name}")
            
            # Track statistics
            self.statistics.indexes_saved_in_pals += non_keyed_count
            self.statistics.live_palette_files_saved.add(path)
            if hasattr(self, 'current_character') and hasattr(self, 'current_job'):
                key = f"{self.current_character}_{self.current_job}"
                if key in self.statistics.character_edits:
                    self.statistics.character_edits[key]['palette_saves'] += 1
            self._save_statistics()
            
            # Mark this layer as saved so we don't restore its original colors when closing
            if hasattr(self, '_live_saved_layers'):
                layer_name = getattr(ly, 'name', '')
                self._live_saved_layers.add(layer_name)
                
            # Update temp cache with saved colors
            if hasattr(self, '_live_temp_palette_cache'):
                current_name = self._live_target_name.get()
                if current_name:
                    self._live_temp_palette_cache[current_name] = ly.colors.copy()
                
            # Track palette save in statistics
            if hasattr(self, 'current_character'):
                current_job = self.job_var.get() if hasattr(self, 'job_var') else None
                if current_job:
                    self.statistics.live_palette_files_saved.add(path)
                    key = (self.current_character, current_job)
                    if key in self.statistics.character_edits:
                        self.statistics.character_edits[key]['palette_saves'] += 1
                    self._save_statistics()
            
            # After successful save, ask about icon (but skip for hair/3rd job)
            from tkinter import messagebox
            
            # Check if this is a hair or 3rd job palette - if so, skip the dialog entirely
            if hasattr(ly, 'palette_type'):
                palette_type = str(ly.palette_type).lower()
                if palette_type in ("hair", "3rd_job_base"):
                    # Skip the post-save dialog for hair and 3rd job palettes
                    icon_choice = "no"  # Act as if user clicked "No I'm good"
                else:
                    icon_choice = self._ask_icon_save_choice(path, ly)
            else:
                icon_choice = self._ask_icon_save_choice(path, ly)
            # Note: "quicksave" and "saveportrait" are handled within the dialog
            if icon_choice == "openeditor":
                # Extract character ID and item name from the layer
                char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
                if char_match:
                    num = char_match.group(1)
                    char_id = f"chr{num}"  # Normalize to chr format
                    
                    # Get the fashion type from the layer
                    fashion_type = getattr(ly, "palette_type", "")
                    if fashion_type:
                        # Read the newly saved palette
                        try:
                            with open(path, 'rb') as f:
                                saved_pal_data = f.read()
                            
                            # Convert to RGB tuples
                            saved_palette = []
                            for i in range(0, len(saved_pal_data), 3):
                                r = saved_pal_data[i]
                                g = saved_pal_data[i+1]
                                b = saved_pal_data[i+2]
                                saved_palette.append((r, g, b))
                            
                            print(f"\nRead saved palette from: {path}")
                            print(f"Found {len(saved_palette)} colors")
                            
                            # Open the icon palette editor
                            from icon_handler import IconPaletteEditor
                            # Create icon handler and set main window reference
                            from icon_handler import IconHandler
                            icon_handler = IconHandler()
                            icon_handler.main_window = self
                            
                            editor = IconPaletteEditor(
                                char_id=char_id,
                                fashion_type=fashion_type,
                                custom_palette=saved_palette,
                                palette_path=path,
                                palette_layers=None,  # Don't pass palette layers to avoid refresh issues
                                live_editor_window=self._live_editor_window,
                                is_quicksave_mode=False,  # Editor mode - allow user to name file
                                icon_handler=icon_handler
                            )
                            # Bring the icon editor to the front after creation
                            editor._bring_to_front()
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Error reading saved palette: {e}")
                            messagebox.showerror("Error", f"Failed to open icon editor: {e}")
            
            # Only bring the PAL editor window to the front if we didn't open the icon editor
            if icon_choice != "openeditor":
                self._bring_live_editor_to_front()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
            # Bring live editor to front even on error
            self._bring_live_editor_to_front()
    
    def _live_open_icon_editor(self):
        """Open the icon editor directly without saving a palette first."""
        ly = self._live_current_layer()
        if ly is None:
            return
        
        # Extract character ID and item name from the layer
        char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
        if not char_match:
            messagebox.showerror("Error", "Could not determine character ID from layer name")
            return
        
        num = char_match.group(1)
        char_id = f"chr{num}"  # Normalize to chr format
        
        # Get the fashion type from the layer
        fashion_type = getattr(ly, "palette_type", "")
        if not fashion_type:
            messagebox.showerror("Error", "Could not determine fashion type from layer")
            return
        
        # Get current colors from the layer
        colors = ly.colors
        
        # Validate colors before proceeding
        if not colors or not isinstance(colors, list):
            messagebox.showerror("Error", "No valid color data found in the selected layer")
            return
        
        # Validate that colors contain valid RGB tuples
        valid_colors = []
        for i, color in enumerate(colors):
            if isinstance(color, (list, tuple)) and len(color) >= 3:
                try:
                    r, g, b = int(color[0]), int(color[1]), int(color[2])
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        valid_colors.append((r, g, b))
                    else:
                        print(f"CONSOLE ERROR MSG: Color values out of range at index {i}: {color}")
                        valid_colors.append((128, 128, 128))  # Default gray
                except (ValueError, TypeError):
                    print(f"CONSOLE ERROR MSG: Invalid color at index {i}: {color}")
                    valid_colors.append((128, 128, 128))  # Default gray
            else:
                print(f"CONSOLE ERROR MSG: Invalid color format at index {i}: {color}")
                valid_colors.append((128, 128, 128))  # Default gray
        
        if not valid_colors:
            messagebox.showerror("Error", "No valid colors found in the selected layer")
            return
        
        # Create a temporary palette path for the editor
        temp_palette_path = f"temp_{ly.name}.pal"
        
        try:
            # Open the icon palette editor directly
            from icon_handler import IconPaletteEditor
            # Create icon handler and set main window reference
            from icon_handler import IconHandler
            icon_handler = IconHandler()
            icon_handler.main_window = self
            
            editor = IconPaletteEditor(
                char_id=char_id,
                fashion_type=fashion_type,
                custom_palette=valid_colors,
                palette_path=temp_palette_path,
                palette_layers=self.palette_layers,  # Pass palette layers to enable dropdown refresh
                live_editor_window=self._live_editor_window,
                is_quicksave_mode=False,  # Editor mode - allow user to name file
                icon_handler=icon_handler
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open icon editor: {e}")
    
    def _update_icon_editor_button_state(self):
        """Update the icon editor button state based on current palette types"""
        if not hasattr(self, 'icon_editor_button'):
            return
            
        # Check if live palette editor is open and editing non-impact types
        if hasattr(self, '_live_editor_window') and self._live_editor_window and self._live_editor_window.winfo_exists():
            # Check if current layer is hair or third job
            try:
                current_layer = self._live_current_layer()
                if current_layer and hasattr(current_layer, 'palette_type'):
                    palette_type = str(current_layer.palette_type).lower()
                    if palette_type in ("hair", "3rd_job_base"):
                        self.icon_editor_button.config(state="disabled", text="Icon Editor (N/A)")
                        return
            except Exception:
                pass
        
        # Default state - enabled
        self.icon_editor_button.config(state="normal", text="Icon Editor")

    def _open_icon_editor(self):
        """Open the icon editor from the main screen."""
        from icon_handler import IconHandler
        icon_handler = IconHandler()
        # Pass the live editor window if it exists
        live_editor = getattr(self, '_live_editor_window', None)
        # Set the main window reference
        icon_handler.main_window = self
        icon_handler.open_icon_editor(self.palette_layers, live_editor)
    
    def _quick_export_icon(self):
        """Quickly export icon without opening the editor."""
        import re
        from tkinter import messagebox
        from icon_handler import IconHandler
        
        # Check if we have active layers
        active_layers = [ly for ly in self.palette_layers if getattr(ly, "active", False)]
        if not active_layers:
            return  # Silently return - no prompt
            
        # Check if current layer is hair or third job - if so, silently return
        current_layer = None
        for layer in active_layers:
            if hasattr(layer, 'palette_type'):
                palette_type = str(layer.palette_type).lower()
                if palette_type in ("hair", "3rd_job_base"):
                    return  # Silently return - no prompt for hair/third job
        
        # Filter out hair and third job layers
        base_fashion_layers = [ly for ly in active_layers if hasattr(ly, "palette_type") and 
                             ly.palette_type.startswith("fashion_") and 
                             not (ly.name and ("hair" in ly.name.lower() or "third" in ly.name.lower()))]
                             
        if not base_fashion_layers:
            return  # Silently return - no prompt

        # Prefer an active fashion layer if present
        default_idx = 0
        for i, ly in enumerate(active_layers):
            if hasattr(ly, "palette_type") and ly.palette_type.startswith("fashion"):
                default_idx = i
                break

        ly = active_layers[default_idx]
        
        # Extract character ID and item name from the layer
        char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
        if not char_match:
            messagebox.showerror("Error", "Could not determine character ID from layer name")
            return
        
        num = char_match.group(1)
        char_id = f"chr{num}"  # Normalize to chr format
        
        # Get the fashion type from the layer
        fashion_type = getattr(ly, "palette_type", "")
        if not fashion_type:
            messagebox.showerror("Error", "Could not determine fashion type from layer")
            return
        
        # Get the current colors from the layer
        try:
            current_colors = []
            for i, color in enumerate(ly.colors):
                if isinstance(color, (list, tuple)) and len(color) >= 3:
                    r, g, b = color[:3]
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        current_colors.append((int(r), int(g), int(b)))
                    else:
                        print(f"CONSOLE ERROR MSG: Color values out of range at index {i}: {color}")
                        current_colors.append((128, 128, 128))  # Default gray
                else:
                    print(f"CONSOLE ERROR MSG: Invalid color format at index {i}: {color}")
                    current_colors.append((128, 128, 128))  # Default gray
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get colors from layer: {e}")
            return
        
        if not current_colors:
            messagebox.showerror("Error", "No valid colors found in the selected layer")
            return
        
        # Create icon handler and export
        icon_handler = IconHandler()
        icon_handler.main_window = self
        
        # Create a temporary palette path for naming
        temp_palette_path = f"temp_{ly.name}.pal"
        
        try:
            success = icon_handler.save_as_icon(
                char_id,
                fashion_type,
                current_colors,
                temp_palette_path
            )
            if success:
                messagebox.showinfo("Success", "Icon exported successfully!")
            else:
                messagebox.showerror("Error", "Failed to export icon.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export icon: {e}")
    
    def _quick_export_icon_from_dialog(self, path, ly, dialog):
        """Quick export icon from the Post-Pal Save Menu dialog."""
        import re
        from tkinter import messagebox
        from icon_handler import IconHandler
        
        # Extract character ID and item name from the layer
        char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
        if not char_match:
            messagebox.showerror("Error", "Could not determine character ID from layer name")
            return
        
        num = char_match.group(1)
        char_id = f"chr{num}"  # Normalize to chr format
        
        # Get the fashion type from the layer
        fashion_type = getattr(ly, "palette_type", "")
        if not fashion_type:
            messagebox.showerror("Error", "Could not determine fashion type from layer")
            return
        
        try:
            # Read the newly saved palette
            with open(path, 'rb') as f:
                saved_pal_data = f.read()
            
            # Convert to RGB tuples
            saved_palette = []
            for i in range(0, len(saved_pal_data), 3):
                r = saved_pal_data[i]
                g = saved_pal_data[i+1]
                b = saved_pal_data[i+2]
                saved_palette.append((r, g, b))
            
            # Create icon handler and export
            icon_handler = IconHandler()
            icon_handler.main_window = self
            
            success = icon_handler.save_as_icon(
                char_id,
                fashion_type,
                saved_palette,
                path
            )
            if success:
                messagebox.showinfo("Success", "Icon exported successfully!")
                # Close the dialog after successful export
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to export icon.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export icon: {e}")
    
    def _quick_export_icon_from_dialog_no_close(self, path, ly):
        """Quick export icon from the Post-Pal Save Menu dialog without closing it."""
        import re
        from tkinter import messagebox
        from icon_handler import IconHandler
        
        # Extract character ID and item name from the layer
        char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
        if not char_match:
            messagebox.showerror("Error", "Could not determine character ID from layer name")
            return
        
        num = char_match.group(1)
        char_id = f"chr{num}"  # Normalize to chr format
        
        # Get the fashion type from the layer
        fashion_type = getattr(ly, "palette_type", "")
        if not fashion_type:
            messagebox.showerror("Error", "Could not determine fashion type from layer")
            return
        
        try:
            # Read the newly saved palette
            with open(path, 'rb') as f:
                saved_pal_data = f.read()
            
            # Convert to RGB tuples
            saved_palette = []
            for i in range(0, len(saved_pal_data), 3):
                r = saved_pal_data[i]
                g = saved_pal_data[i+1]
                b = saved_pal_data[i+2]
                saved_palette.append((r, g, b))
            
            # Create icon handler and export
            icon_handler = IconHandler()
            icon_handler.main_window = self
            
            success = icon_handler.save_as_icon(
                char_id,
                fashion_type,
                saved_palette,
                path
            )
            if success:
                messagebox.showinfo("Success", "Icon exported successfully!")
                # Don't close the dialog - keep it open
            else:
                messagebox.showerror("Error", "Failed to export icon.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export icon: {e}")
    
    def _ask_icon_save_choice(self, path, ly):
        """Show a simple dialog asking how to handle icon saving."""
        dialog = tk.Toplevel(self._live_editor_window)
        dialog.title("Post-Pal QuickSave Menu")
        dialog.resizable(False, False)
        dialog.transient(self._live_editor_window)
        dialog.grab_set()
        
        # Make it modal
        result = {"choice": None}
        
        # Helper functions that perform actions without closing dialog
        def save_icon():
            """Save icon - quick export if checkbox is checked, otherwise prompt for filename"""
            from tkinter import messagebox, filedialog
            
            # Check if quick export is enabled
            if quick_export_var.get():
                # Quick export mode - directly export the icon without closing dialog
                self._quick_export_icon_from_dialog_no_close(path, ly)
            else:
                # Normal mode - prompt user for filename and save icon
                # Extract character ID and item name from the layer
                char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
                if char_match:
                    num = char_match.group(1)
                    char_id = f"chr{num}"  # Normalize to chr format
                    
                    # Get the fashion type from the layer
                    fashion_type = getattr(ly, "palette_type", "")
                    if fashion_type:
                        # Read the newly saved palette
                        try:
                            with open(path, 'rb') as f:
                                saved_pal_data = f.read()
                            
                            # Convert to RGB tuples
                            saved_palette = []
                            for i in range(0, len(saved_pal_data), 3):
                                r = saved_pal_data[i]
                                g = saved_pal_data[i+1]
                                b = saved_pal_data[i+2]
                                saved_palette.append((r, g, b))
                            
                            print(f"\nRead saved palette from: {path}")
                            print(f"Found {len(saved_palette)} colors")
                            
                            # Prompt user for filename
                            default_name = f"{char_id}_{fashion_type}.bmp"
                            file_path = filedialog.asksaveasfilename(
                                title="Save Icon As",
                                defaultextension=".bmp",
                                filetypes=[("BMP files", "*.bmp"), ("All files", "*.*")],
                                initialname=default_name,
                                parent=dialog
                            )
                            
                            if file_path:
                                # Ensure the file has .bmp extension
                                if not file_path.lower().endswith('.bmp'):
                                    file_path += '.bmp'
                                
                                # Create icon handler and save with user-specified filename
                                from icon_handler import IconHandler
                                icon_handler = IconHandler()
                                icon_handler.main_window = self
                                
                                # Find the base BMP path for the character/fashion
                                base_bmp_name = icon_handler._find_base_bmp_name(char_id, fashion_type)
                                if base_bmp_name:
                                    # Construct the BMP path
                                    bmp_path = os.path.join(icon_handler.root_dir, "src", "rawbmps", char_id, f"{base_bmp_name}.bmp")
                                    
                                    # Get keying color
                                    keying_color = icon_handler._determine_keying_color(saved_palette)
                                    
                                    success = icon_handler.save_as_icon_with_colors(
                                        char_id,
                                        fashion_type,
                                        saved_palette,
                                        keying_color,
                                        bmp_path,
                                        file_path
                                    )
                                    if success:
                                        messagebox.showinfo("Success", f"Icon saved as: {os.path.basename(file_path)}")
                                    else:
                                        messagebox.showerror("Error", "Failed to save icon.")
                                else:
                                    messagebox.showerror("Error", "Could not find base BMP for this character/fashion.")
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Error saving icon: {e}")
                            messagebox.showerror("Error", f"Failed to save icon: {e}")
            
            # Bring dialog back to front
            dialog.lift()
            dialog.focus_force()
        
        def save_portrait():
            """Save portrait - quick export if checkbox is checked, otherwise prompt for filename"""
            from tkinter import messagebox
            try:
                frame = self.get_current_displayed_frame()
                if frame is not None:
                    # Both quick export and normal mode use the same method
                    # The export_background_bmp method already handles filename prompting
                    self.export_background_bmp(frame, force_portrait=True)
                else:
                    messagebox.showerror("Error", "No frame available for portrait export.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export portrait: {e}")
            
            # Bring dialog back to front
            dialog.lift()
            dialog.focus_force()
        
        # Simple layout
        tk.Label(dialog, text="Do you want to quicksave export or edit the icon?", 
                font=("Arial", 10)).pack(pady=10)
        
        # Quick Export checkbox
        checkbox_frame = tk.Frame(dialog)
        checkbox_frame.pack(pady=(0, 10))
        
        # Get initial value from settings
        initial_quick_export = getattr(self, 'use_quick_export', False)
        quick_export_var = tk.BooleanVar(value=initial_quick_export)
        
        # Three main action buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Save Icon", 
                 command=save_icon,
                 width=13).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Save Portrait", 
                 command=save_portrait,
                 width=13).pack(side=tk.LEFT, padx=5)
        
        # Live Edit Icon button (will be shown/hidden based on checkbox)
        live_edit_button = tk.Button(button_frame, text="Live Edit Icon", 
                                   command=lambda: self._close_dialog(dialog, result, "openeditor"),
                                   width=13)
        live_edit_button.pack(side=tk.LEFT, padx=5)
        
        def toggle_quick_export():
            """Toggle quick export mode and show/hide Live Edit Icon button"""
            self.use_quick_export = quick_export_var.get()
            # Save the setting
            self._save_settings()
            
            # Show/hide the Live Edit Icon button based on checkbox state
            if quick_export_var.get():
                live_edit_button.pack_forget()  # Hide the button
            else:
                live_edit_button.pack(side=tk.LEFT, padx=5)  # Show the button
        
        quick_export_checkbox = tk.Checkbutton(checkbox_frame, text="Quick Export (Skip Icon Editor)", 
                                             variable=quick_export_var,
                                             command=toggle_quick_export)
        quick_export_checkbox.pack()
        
        # Set initial button state based on checkbox
        if initial_quick_export:
            live_edit_button.pack_forget()
        
        # "No thanks" button at the bottom
        no_button_frame = tk.Frame(dialog)
        no_button_frame.pack(pady=(0, 10))
        
        tk.Button(no_button_frame, text="No I'm good c:", 
                 command=lambda: self._close_dialog(dialog, result, "no"),
                 width=13).pack()
        
        # Bring dialog to front and center it
        dialog.lift()
        dialog.focus_force()
        dialog.update_idletasks()
        self._center_window_on_parent(dialog, self._live_editor_window)
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result["choice"]
    
    def _close_dialog(self, dialog, result, choice):
        """Close the dialog and set the result."""
        result["choice"] = choice
        dialog.destroy()

    def refresh_custom_pals(self, update_ui=True):
        """Refresh custom pals by reloading them and optionally updating the UI"""
        # Remove the guard clause - we want to refresh all custom pals regardless of current character
        
        # Clear existing custom palettes from ALL data structures
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        for char_id in list(self.fashion_palettes.keys()):
            # Get the absolute paths of custom fashion palette directories
            custom_fashion_pals_path = os.path.join(root_dir, "exports", "custom_pals", "fashion")
            old_custom_fashion_pals_path = os.path.join(root_dir, "exports", "custom_fashion_pals")
            custom_fashion_abs = os.path.abspath(custom_fashion_pals_path)
            old_custom_fashion_abs = os.path.abspath(old_custom_fashion_pals_path)
            
            # Only keep palettes that are NOT in custom fashion directories
            self.fashion_palettes[char_id] = [
                path for path in self.fashion_palettes[char_id] 
                if not (os.path.abspath(path).startswith(custom_fashion_abs) or 
                       os.path.abspath(path).startswith(old_custom_fashion_abs))
            ]
        
        for char_id in list(self.hair_palettes.keys()):
            # Get the absolute paths of custom hair palette directories
            custom_hair_pals_path = os.path.join(root_dir, "exports", "custom_pals", "hair")
            old_custom_fashion_pals_path = os.path.join(root_dir, "exports", "custom_fashion_pals")
            custom_hair_abs = os.path.abspath(custom_hair_pals_path)
            old_custom_fashion_abs = os.path.abspath(old_custom_fashion_pals_path)
            
            # Only keep palettes that are NOT in custom directories
            self.hair_palettes[char_id] = [
                path for path in self.hair_palettes[char_id] 
                if not (os.path.abspath(path).startswith(custom_hair_abs) or 
                       os.path.abspath(path).startswith(old_custom_fashion_abs))
            ]
        
        # Reload custom palettes from new directory structure
        custom_pals_paths = self.get_custom_pals_paths()
        for custom_pals_path in custom_pals_paths:
            if not os.path.exists(custom_pals_path):
                continue
            for file in os.listdir(custom_pals_path):
                if file.lower().endswith('.pal'):
                    # Check for fashion palettes (chr###_w#.pal through chr###_w######.pal)
                    fashion_match = re.match(r'^chr(\d{3})_w\d+\.pal$', file.lower())
                    if fashion_match:
                        char_num = fashion_match.group(1)
                        char_id_for_pal = f"chr{char_num}"
                        if char_id_for_pal not in self.fashion_palettes:
                            self.fashion_palettes[char_id_for_pal] = []
                        
                        # Validate the palette file before adding it
                        palette_path = os.path.join(custom_pals_path, file)
                        try:
                            with open(palette_path, "rb") as f:
                                data = f.read()
                            
                            if len(data) != PALETTE_SIZE * 3:
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            valid_file = True
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    valid_file = False
                                    break
                            
                            if valid_file:
                                self.fashion_palettes[char_id_for_pal].append(palette_path)
                            
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Failed to load custom fashion palette {file}: {e}")
                            continue
                    
                    # Check for hair palettes (chr###_#.pal)
                    hair_match = re.match(r'^chr(\d{3})_\d+\.pal$', file.lower())
                    if hair_match:
                        char_num = hair_match.group(1)
                        char_id_for_pal = f"chr{char_num}"
                        if char_id_for_pal not in self.hair_palettes:
                            self.hair_palettes[char_id_for_pal] = []
                        
                        # Validate the palette file before adding it
                        palette_path = os.path.join(custom_pals_path, file)
                        try:
                            with open(palette_path, "rb") as f:
                                data = f.read()
                            
                            if len(data) != PALETTE_SIZE * 3:
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            valid_file = True
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    valid_file = False
                                    break
                            
                            if valid_file:
                                self.hair_palettes[char_id_for_pal].append(palette_path)
                            
                        except Exception as e:
                            print(f"CONSOLE ERROR MSG: Failed to load custom hair palette {file}: {e}")
                            continue
        
        # Update the UI sections to reflect the new custom pals (only if requested)
        if update_ui:
            # Save current selections before updating UI
            saved_hair_selection = getattr(self, 'hair_var', tk.StringVar()).get() if hasattr(self, 'hair_var') else "NONE"
            saved_third_job_selection = getattr(self, 'third_job_var', tk.StringVar()).get() if hasattr(self, 'third_job_var') else "NONE"
            saved_fashion_selections = {}
            if hasattr(self, 'fashion_vars'):
                for fashion_type, var in self.fashion_vars.items():
                    saved_fashion_selections[fashion_type] = var.get()
            
            self.update_hair_section()
            self.update_fashion_section()
            
            # Restore selections after updating UI
            if hasattr(self, 'hair_var') and saved_hair_selection != "NONE":
                self.hair_var.set(saved_hair_selection)
            
            if hasattr(self, 'third_job_var') and saved_third_job_selection != "NONE":
                self.third_job_var.set(saved_third_job_selection)
            
            if hasattr(self, 'fashion_vars'):
                for fashion_type, saved_value in saved_fashion_selections.items():
                    if fashion_type in self.fashion_vars and saved_value != "NONE":
                        self.fashion_vars[fashion_type].set(saved_value)

    def get_custom_pals_paths(self):
        """Get list of custom palette directories to check"""
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Use new structure: custom_pals/fashion and custom_pals/hair
        custom_fashion_path = os.path.join(root_dir, "exports", "custom_pals", "fashion")
        custom_hair_path = os.path.join(root_dir, "exports", "custom_pals", "hair")
        # Also check old path for backward compatibility
        old_custom_fashion_path = os.path.join(root_dir, "exports", "custom_fashion_pals")
        
        # Ensure directories exist
        os.makedirs(custom_fashion_path, exist_ok=True)
        os.makedirs(custom_hair_path, exist_ok=True)
        
        paths = [custom_fashion_path, custom_hair_path]
        if os.path.exists(old_custom_fashion_path):
            paths.append(old_custom_fashion_path)
        
        return paths

    def debug_info(self):
        """Show debug information"""
        info = f"Current Character: {self.character_var.get()}\n"
        info += f"Current Job: {self.job_var.get()}\n"
        info += f"Selected Hair: {self.hair_var.get()}\n"
        info += f"Selected 3rd Job Base: {self.third_job_var.get()}\n"
        
        
        # Add preview mode info
        info += f"Preview Mode: {self.preview_var.get()}\n"
        info += f"Zoom Level: {self.zoom_var.get()}\n"
        
        # Add frame info
        if self.preview_var.get() == "custom":
            info += f"Frames Displayed: {getattr(self, 'custom_frame_count', 3)}\n"
            info += f"Starting Frame: {getattr(self, 'custom_start_index', 0) + 1}\n"  # +1 for 1-based display
            if hasattr(self, 'chosen_frame'):
                info += f"Selected Frame for Export: {self.chosen_frame}\n"  # Already 1-based
        elif self.preview_var.get() == "all":
            total_frames = len(self.character_images.get(self.current_character, []))
            info += f"Frames Displayed: {total_frames}\n"
            info += f"Starting Frame: 1\n"  # All frames mode always starts at 1
        else:  # single mode
            info += f"Frames Displayed: 1\n"
            current_frame = self.current_image_index + 1 if hasattr(self, 'current_image_index') else 1
            info += f"Current Frame: {current_frame}\n"
        
        # Add palette layers info
        # Add custom pals info
        char_id = self.current_character
        active_custom_pals = 0
        for layer in self.palette_layers:
            if layer.active and layer.name.startswith("Active"):
                active_custom_pals += 1
        info += f"Active Custom Pals Loaded: {active_custom_pals}\n"
        info += f"Loaded Palette Layers: {len(self.palette_layers)}\n"
        for i, layer in enumerate(self.palette_layers):
            info += f"  {i+1}. {layer.name} ({layer.palette_type}) - {'Active' if layer.active else 'Inactive'}\n"
        
        messagebox.showinfo("Debug Info", info)

    def show_credits(self):
        """Show credits dialog"""
        # Create credits dialog window
        credits_dialog = tk.Toplevel(self.master)
        credits_dialog.title("Credits")
        credits_dialog.transient(self.master)
        credits_dialog.grab_set()
        credits_dialog.resizable(False, False)
        
        # Main frame with padding
        main_frame = tk.Frame(credits_dialog)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Credits message
        credits_text = ("This program has been brought to you by the wonderful staff of CoraTO: "
                       "Dino, Yuki, and Mewsie, and the initial foundation for the project as well as "
                       "additional research provided by KusanagiKyo.\n\n"
                       "Thank you all, truly, for your hard work and dedication to this community, "
                       "to providing this awesome, free tool for everyone!")
        
        credits_label = tk.Label(main_frame, text=credits_text, wraplength=400, justify="center", 
                                font=("Arial", 11))
        credits_label.pack(pady=(0, 20))
        
        # Thank you button
        thank_you_btn = tk.Button(main_frame, text="Thank you guys :)", 
                                 command=credits_dialog.destroy, font=("Arial", 10))
        thank_you_btn.pack()
        
        # Center the dialog
        credits_dialog.update_idletasks()
        dialog_width = credits_dialog.winfo_width()
        dialog_height = credits_dialog.winfo_height()
        
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        credits_dialog.geometry(f"+{x}+{y}")
    
    def show_statistics(self):
        """Show statistics dialog"""
        StatisticsDialog(self)
    
    def _center_window(self):
        """Center the main window on the screen."""
        # Update the window to get accurate dimensions
        self.master.update_idletasks()
        
        # Get window dimensions
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        
        # Get screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set the window position
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _bring_live_editor_to_front(self):
        """Bring the live palette editor window to the front with multiple methods for reliability across platforms."""
        try:
            if hasattr(self, '_live_editor_window') and self._live_editor_window and self._live_editor_window.winfo_exists():
                import platform
                system = platform.system().lower()
                
                # Common methods that work on both platforms
                self._live_editor_window.deiconify()  # Ensure window is not minimized
                self._live_editor_window.lift()  # Bring to front in stacking order
                
                if system == "windows":
                    # Windows-specific focus handling
                    self._live_editor_window.focus_force()  # Force keyboard focus
                    self._live_editor_window.attributes('-topmost', True)  # Temporarily make topmost
                    self._live_editor_window.after(100, lambda: self._live_editor_window.attributes('-topmost', False))  # Remove topmost after 100ms
                    
                    # Additional Windows focus methods
                    try:
                        self._live_editor_window.wm_attributes('-topmost', 1)
                        self._live_editor_window.after(10, lambda: self._live_editor_window.wm_attributes('-topmost', 0))
                    except:
                        pass
                        
                elif system == "linux":
                    # Linux-specific focus handling
                    self._live_editor_window.focus_set()  # Set focus (gentler than focus_force)
                    self._live_editor_window.tkraise()  # Raise window in stacking order
                    
                    # Try to activate the window (X11 specific)
                    try:
                        self._live_editor_window.wm_attributes('-topmost', True)
                        self._live_editor_window.after(50, lambda: self._live_editor_window.wm_attributes('-topmost', False))
                    except:
                        pass
                        
                    # Additional method for some Linux window managers
                    try:
                        self._live_editor_window.focus()
                    except:
                        pass
                        
                else:
                    # Fallback for other systems (macOS, etc.)
                    self._live_editor_window.focus_set()
                    self._live_editor_window.tkraise()
                
        except Exception as e:
            pass
    
    def _center_window_on_parent(self, window, parent=None, width=None, height=None):
        """Center a window on its parent window or screen if no parent."""
        if parent is None:
            parent = self.master
        
        # Use provided dimensions or get from window
        if width is None or height is None:
            window.update_idletasks()
            window_width = window.winfo_width() if width is None else width
            window_height = window.winfo_height() if height is None else height
        else:
            window_width = width
            window_height = height
        
        if parent and parent.winfo_exists():
            # Center on parent window
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            
            # Calculate center position relative to parent
            x = parent_x + (parent_width - window_width) // 2
            y = parent_y + (parent_height - window_height) // 2
        else:
            # Center on screen if no parent
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
        
        # Set the window geometry with position
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaletteTool(root)
    app.statistics = Statistics()  # Initialize statistics
    app._load_statistics()  # Load saved statistics
    root.mainloop()

