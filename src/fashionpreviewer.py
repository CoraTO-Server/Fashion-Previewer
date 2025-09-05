import tkinter as tk
import colorsys
from tkinter import filedialog, messagebox, Scrollbar, Canvas, ttk
import tkinter.colorchooser as colorchooser
from PIL import Image, ImageTk
import os
import re
import sys

PALETTE_SIZE = 256

# Fix working directory to the script's location
def fix_working_directory():
    """Change working directory to the script's location to ensure relative paths work"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Changed working directory to: {script_dir}")

# Character mapping based on the provided list
CHARACTER_MAPPING = {
    "chr001": {"name": "Bunny", "job": "1st Job"},
    "chr002": {"name": "Buffalo", "job": "1st Job"},
    "chr003": {"name": "Sheep", "job": "1st Job"},
    "chr004": {"name": "Dragon", "job": "1st Job"},
    "chr005": {"name": "Fox", "job": "1st Job"},
    "chr006": {"name": "Lion", "job": "1st Job"},
    "chr007": {"name": "Cat", "job": "1st Job"},
    "chr008": {"name": "Raccoon", "job": "1st Job"},
    "chr009": {"name": "Bunny", "job": "2nd Job"},
    "chr010": {"name": "Buffalo", "job": "2nd Job"},
    "chr011": {"name": "Sheep", "job": "2nd Job"},
    "chr012": {"name": "Dragon", "job": "2nd Job"},
    "chr013": {"name": "Fox", "job": "2nd Job"},
    "chr014": {"name": "Lion", "job": "2nd Job"},
    "chr015": {"name": "Cat", "job": "2nd Job"},
    "chr016": {"name": "Raccoon", "job": "2nd Job"},
    "chr017": {"name": "Bunny", "job": "3rd Job"},
    "chr018": {"name": "Buffalo", "job": "3rd Job"},
    "chr019": {"name": "Sheep", "job": "3rd Job"},
    "chr020": {"name": "Dragon", "job": "3rd Job"},
    "chr021": {"name": "Fox", "job": "3rd Job"},
    "chr022": {"name": "Lion", "job": "3rd Job"},
    "chr023": {"name": "Cat", "job": "3rd Job"},
    "chr024": {"name": "Raccoon", "job": "3rd Job"},
    "chr025": {"name": "Paula", "job": "1st Job"},
    "chr026": {"name": "Paula", "job": "2nd Job"},
    "chr027": {"name": "Paula", "job": "3rd Job"},
    "chr100": {"name": "Paula", "job": "1st Job"},
    "chr101": {"name": "Paula", "job": "2nd Job"},
    "chr102": {"name": "Paula", "job": "3rd Job"},
}

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
            self.use_myshop = parent.use_myshop_export
            self.show_labels = parent.show_frame_labels
        else:
            self.use_portrait = False
            self.use_myshop = False
        
        # Determine the widget parent for the dialog
        widget_parent = parent.master if isinstance(parent, PaletteTool) else parent
        
        # Create dialog window
        self.dialog = tk.Toplevel(widget_parent)
        self.dialog.title("Custom Preview Settings")
        self.dialog.geometry("300x420")  # Increased height
        self.dialog.transient(widget_parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (widget_parent.winfo_rootx() + 50, widget_parent.winfo_rooty() + 50))
        
        # Main frame
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill="both", padx=20, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Custom Frame Settings", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Frame count input
        count_frame = tk.Frame(main_frame)
        count_frame.pack(fill="x", pady=5)
        
        tk.Label(count_frame, text="Number of Frames:").pack(side="left")
        
        self.frame_var = tk.StringVar(value=str(num_frames))
        self.frame_entry = tk.Entry(count_frame, textvariable=self.frame_var, width=10)
        self.frame_entry.pack(side="left", padx=(5, 0))
        
        tk.Label(count_frame, text=f"(max: {max_frames})").pack(side="left", padx=(5, 0))
        
        # Frame range inputs
        range_frame = tk.Frame(main_frame)
        range_frame.pack(fill="x", pady=10)
        
        # Start frame
        start_frame_container = tk.Frame(range_frame)
        start_frame_container.pack(fill="x", pady=5)
        tk.Label(start_frame_container, text="Start Frame:").pack(side="left")
        # Use initial_frame for start_frame if no specific start_frame was provided, convert to 1-based
        initial_start = self.initial_frame if start_frame == 0 else start_frame
        self.start_var = tk.StringVar(value=str(initial_start + 1))  # Convert to 1-based
        self.start_entry = tk.Entry(start_frame_container, textvariable=self.start_var, width=10)
        self.start_entry.pack(side="left", padx=(5, 0))
        tk.Label(start_frame_container, text=f"(min: 1, max: {max_frames})", fg="gray40").pack(side="left", padx=(5, 0))
        
        # End frame
        end_frame_container = tk.Frame(range_frame)
        end_frame_container.pack(fill="x", pady=5)
        tk.Label(end_frame_container, text="End Frame:").pack(side="left")
        # Convert end frame to 1-based
        end_value = end_frame if end_frame is not None else max_frames - 1
        self.end_var = tk.StringVar(value=str(end_value + 1))  # Convert to 1-based
        self.end_entry = tk.Entry(end_frame_container, textvariable=self.end_var, width=10)
        self.end_entry.pack(side="left", padx=(5, 0))
        tk.Label(end_frame_container, text=f"(min: 1, max: {max_frames})", fg="gray40").pack(side="left", padx=(5, 0))
        
        # Export format toggle
        format_frame = tk.LabelFrame(main_frame, text="Export Format")
        format_frame.pack(fill="x", pady=(5,10), padx=5)
        
        self.format_var = tk.BooleanVar(value=self.use_bmp)
        # Add trace to update parent's export button when format changes
        def on_format_change(*args):
            if isinstance(parent, PaletteTool):
                parent.use_bmp_export = self.format_var.get()
                parent.update_export_button_text()
                parent.master.update()  # Force update of the main window
        self.format_var.trace_add("write", on_format_change)
        
        tk.Radiobutton(format_frame, text="Transparent PNG", variable=self.format_var, 
                      value=False).pack(anchor="w", padx=10, pady=2)
        tk.Radiobutton(format_frame, text="Background BMP", variable=self.format_var, 
                      value=True).pack(anchor="w", padx=10, pady=2)
        
        # Portrait checkbox for BMP export
        self.portrait_var = tk.BooleanVar(value=self.use_portrait)
        self.portrait_checkbox = tk.Checkbutton(format_frame, text="Portrait (103x103)", 
                                              variable=self.portrait_var, state="disabled")
        self.portrait_checkbox.pack(anchor="w", padx=25, pady=2)
        
        # MyShop checkbox for BMP export
        self.myshop_var = tk.BooleanVar(value=self.use_myshop)
        self.myshop_checkbox = tk.Checkbutton(format_frame, text="MyShop (105x105)", 
                                            variable=self.myshop_var, state="disabled")
        self.myshop_checkbox.pack(anchor="w", padx=25, pady=2)
        
        # Update parent's settings when any option changes
        def update_parent_settings(*args):
            if isinstance(self.parent, PaletteTool):
                self.parent.use_bmp_export = self.format_var.get()
                self.parent.use_portrait_export = self.portrait_var.get()
                self.parent.use_myshop_export = self.myshop_var.get()
                self.parent.show_frame_labels = self.labels_var.get()
                print(f"Dialog settings updated: BMP={self.format_var.get()}, Portrait={self.portrait_var.get()}, MyShop={self.myshop_var.get()}")
                
        # Update checkbox states when format changes
        def update_checkbox_states(*args):
            state = "normal" if self.format_var.get() else "disabled"
            self.portrait_checkbox.config(state=state)
            self.myshop_checkbox.config(state=state)
            if not self.format_var.get():
                self.portrait_var.set(False)
                self.myshop_var.set(False)
            update_parent_settings()
        
        # Frame label toggle
        label_frame = tk.Frame(main_frame)
        label_frame.pack(fill="x", pady=2)  # Reduced padding
        
        self.labels_var = tk.BooleanVar(value=self.show_labels)
        tk.Checkbutton(label_frame, text="Show Frame Numbers", variable=self.labels_var).pack(side="left")
        
        # User Choice Frame Export option
        choice_frame = tk.Frame(main_frame)
        choice_frame.pack(fill="x", pady=(2,10))  # Reduced padding
        
        # Initialize with parent's settings if available
        initial_choice = False
        
        if isinstance(self.parent, PaletteTool):
            initial_choice = self.parent.use_frame_choice
            # If frame choice was previously used, use that frame, otherwise use the initial frame
            if self.parent.use_frame_choice:
                initial_frame = self.parent.chosen_frame
            else:
                initial_frame = self.initial_frame
                # Enable frame choice by default when opening dialog
                initial_choice = True
        
        self.user_choice_var = tk.BooleanVar(value=initial_choice)
        choice_checkbox = tk.Checkbutton(choice_frame, text="User Choice Frame Export", 
                                       variable=self.user_choice_var,
                                       command=self.toggle_frame_choice)
        choice_checkbox.pack(side="left")
        
        # Frame number entry
        self.frame_choice_container = tk.Frame(choice_frame)
        self.frame_choice_container.pack(side="left", padx=(10,0))
        
        tk.Label(self.frame_choice_container, text="Frame:").pack(side="left")
        self.frame_choice_var = tk.StringVar(value=str(initial_frame + 1))  # Convert to 1-based
        self.frame_choice_entry = tk.Entry(self.frame_choice_container, 
                                         textvariable=self.frame_choice_var,
                                         width=5)
        self.frame_choice_entry.pack(side="left", padx=(5,5))
        
        # Show frame range
        if isinstance(self.parent, PaletteTool):
            max_frame = len(self.parent.character_images.get(self.parent.current_character, [])) - 1
            tk.Label(self.frame_choice_container, 
                    text=f"(min: 0, max: {max_frame})",
                    fg="gray40").pack(side="left")
        
        # Show/hide frame choice based on initial state
        if initial_choice:
            self.frame_choice_container.pack(side="left", padx=(10,0))
        else:
            self.frame_choice_container.pack_forget()
        
        # Add traces for immediate updates
        self.format_var.trace_add("write", update_checkbox_states)
        self.portrait_var.trace_add("write", update_parent_settings)
        self.myshop_var.trace_add("write", update_parent_settings)
        self.labels_var.trace_add("write", update_parent_settings)
        
        # Big-ass OK button right after the checkbox
        self.ok_button = tk.Button(main_frame, text="OK", command=self.ok_clicked, 
                                 width=20, height=2, font=("Arial", 10))
        self.ok_button.pack(pady=(5,10))  # Reduced top padding
        
        # Validation message at the very bottom
        self.validation_label = tk.Label(main_frame, text="", fg="red", wraplength=250)
        self.validation_label.pack(side="bottom", pady=5)
        
        # Bind validation to input changes
        self.frame_var.trace_add("write", lambda *args: self.validate_inputs())
        self.start_var.trace_add("write", lambda *args: self.validate_inputs())
        self.end_var.trace_add("write", lambda *args: self.validate_inputs())
        
        # Bind Enter key to OK
        self.dialog.bind("<Return>", lambda e: self.ok_clicked())
        self.dialog.bind("<Escape>", lambda e: self.cancel_clicked())
        
        # Focus on entry
        self.frame_entry.focus_set()
        self.frame_entry.select_range(0, tk.END)
        
        # Initial validation
        self.validate_inputs()
        
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
            # If frame count is larger than the range, auto-adjust it
            range_size = end_frame - start_frame + 1
            if range_size < frames:
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
            # Always switch to custom mode when confirming changes from this dialog
            if isinstance(self.parent, PaletteTool):
                current_mode = self.parent.preview_var.get()
                if current_mode in ["single", "all"]:
                    self.parent.preview_var.set("custom")
                    # Ensure UI reflects the mode change immediately
                    try:
                        self.parent.on_preview_mode_change()
                    except Exception:
                        pass
            # Validate frame choice if enabled
            if self.user_choice_var.get():
                try:
                    # Convert from 1-based to 0-based for validation
                    chosen_frame = int(self.frame_choice_var.get()) - 1
                    if isinstance(self.parent, PaletteTool):
                        max_frame = len(self.parent.character_images.get(self.parent.current_character, [])) - 1
                        if chosen_frame < 0 or chosen_frame > max_frame:
                            messagebox.showerror("Invalid Input", f"Frame number must be between 1 and {max_frame + 1}.")
                            return
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
                
            # Update parent's settings if it's a PaletteTool
            if isinstance(self.parent, PaletteTool):
                self.parent.use_bmp_export = self.format_var.get()
                self.parent.use_portrait_export = self.portrait_var.get()
                self.parent.use_myshop_export = self.myshop_var.get()
                self.parent.show_frame_labels = self.labels_var.get()
                self.parent.use_frame_choice = self.user_choice_var.get()
                if self.user_choice_var.get():
                    self.parent.chosen_frame = int(self.frame_choice_var.get())
                # Apply immediate frame settings for custom preview
                self.parent.custom_frame_count = frames
                if not self.user_choice_var.get():
                    self.parent.custom_start_index = start_frame
            
            # Include user's frame choice if enabled
            chosen_frame = int(self.frame_choice_var.get()) if self.user_choice_var.get() else None
            self.result = (frames, start_frame, end_frame, self.format_var.get(), self.labels_var.get(), 
                         self.portrait_var.get(), self.myshop_var.get(), self.user_choice_var.get(), chosen_frame)
            if close:
                self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    def cancel_clicked(self):
        self.dialog.destroy()

class PaletteLayer:
    def __init__(self, name, colors, palette_type, active=True):
        self.name = name
        self.colors = colors  # List of (r,g,b)
        self.palette_type = palette_type  # 'hair', 'gloves', 'fashion', etc.
        self.active = active

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
            msg = "Editing this part will not impact in game fashion, are you sure you want to continue?"
            from tkinter import messagebox
            ok = messagebox.askyesno("Heads up", msg, default="no")
            if ok:
                try:
                    self._live_warned_types.add(pt)
                except Exception:
                    pass
            return bool(ok)
        return True

    def __init__(self, master):
        self.master = master
        self.master.title("Fashion Previewer v3.0 - A CoraTO & Kyo Collab")

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
        
        # Custom preview settings
        self.custom_frame_count = 3
        self.custom_start_index = 0
        self.use_bmp_export = False  # False = PNG, True = BMP
        self.use_portrait_export = False  # Portrait mode (100x100)
        self.use_myshop_export = False  # MyShop mode (105x105)
        self.show_frame_labels = True  # Whether to show frame numbers
        self.use_right_click = False  # False = Left click, True = Right click for color saving
        self.use_frame_choice = False  # Whether to use user-chosen frame for export
        self.chosen_frame = 0  # User's chosen frame for export
        
        # Load MyShop base image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        myshop_base_path = os.path.join(script_dir, "rawbmps", "myshop_base.bmp")
        try:
            self.myshop_base = Image.open(myshop_base_path)
        except Exception as e:
            print(f"Failed to load MyShop base image: {e}")
            self.myshop_base = None
        
        # Available data
        self.available_characters = []
        self.available_jobs = []
        self.character_images = {}  # chr001 -> [list of image paths]
        self.fashion_palettes = {}  # chr001 -> [list of fashion palette paths]
        self.hair_palettes = {}     # chr001 -> [list of hair palette paths]
        self.third_job_palettes = {} # chr001 -> [list of 3rd job base fashion paths]
        
        # UI variables
        self.character_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.hair_var = tk.StringVar()
        self.third_job_var = tk.StringVar()
        self.zoom_var = tk.StringVar(value="100%")
        self.fashion_vars = {}  # Track fashion selection variables
        
        # Load all available data
        self.load_all_data()
        
        # Create UI
        self.create_ui()
        
        # Auto-load first character if available
        if self.available_characters:
            first_char = self.available_characters[0]
            if first_char in CHARACTER_MAPPING:
                char_info = CHARACTER_MAPPING[first_char]
                self.character_var.set(char_info['name'])
                self.job_var.set(char_info['job'])
                self.on_character_change()
        
        # Initialize zoom combo state based on preview mode (after character is loaded)
        self.update_zoom_combo_state()

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
    def load_all_data(self):
        """Load all available characters, images, and palettes"""
        # Fix working directory first
        fix_working_directory()
        
        # Load character images from rawbmps folder
        rawbmps_path = "rawbmps"
        print(f"Looking for rawbmps folder at: {os.path.abspath(rawbmps_path)}")
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
        
        # Load fashion palettes from vanilla_pals/fashion folder
        fashion_path = os.path.join("vanilla_pals", "fashion")
        print(f"Looking for fashion palettes at: {os.path.abspath(fashion_path)}")
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
                                print(f"Warning: Invalid fashion palette file {file} - incorrect size: {len(data)} bytes")
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            valid_file = True
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"Warning: Invalid fashion palette file {file} - invalid byte at position {i}")
                                    valid_file = False
                                    break
                            
                            if valid_file:
                                self.fashion_palettes[char_id].append(palette_path)
                            
                        except Exception as e:
                            print(f"Warning: Failed to load fashion palette {file}: {e}")
                            continue
        
        # Load custom fashion palettes from root/exports/custom_pals
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        custom_pals_path = os.path.join(root_dir, "exports", "custom_pals")
        if not os.path.exists(custom_pals_path):
            os.makedirs(custom_pals_path, exist_ok=True)
        else:
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
                                print(f"Warning: Invalid custom fashion palette file {file} - incorrect size: {len(data)} bytes")
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            valid_file = True
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"Warning: Invalid custom fashion palette file {file} - invalid byte at position {i}")
                                    valid_file = False
                                    break
                            
                            if valid_file:
                                self.fashion_palettes[char_id].append(palette_path)
                                print(f"Loaded custom fashion palette: {file}")
                            
                        except Exception as e:
                            print(f"Warning: Failed to load custom fashion palette {file}: {e}")
                            continue
                    
                    # Check for hair palettes (chr###_#.pal)
                    hair_match = re.match(r'^chr(\d{3})_\d+\.pal$', file.lower())
                    if hair_match:
                        char_num = hair_match.group(1)
                        char_id = f"chr{char_num}"
                        if char_id not in self.hair_palettes:
                            self.hair_palettes[char_id] = []
                        
                        # Validate the palette file before adding it
                        palette_path = os.path.join(custom_pals_path, file)
                        try:
                            with open(palette_path, "rb") as f:
                                data = f.read()
                            
                            if len(data) != PALETTE_SIZE * 3:
                                print(f"Warning: Invalid custom hair palette file {file} - incorrect size: {len(data)} bytes")
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            valid_file = True
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"Warning: Invalid custom hair palette file {file} - invalid byte at position {i}")
                                    valid_file = False
                                    break
                            
                            if valid_file:
                                self.hair_palettes[char_id].append(palette_path)
                                print(f"Loaded custom hair palette: {file}")
                            
                        except Exception as e:
                            print(f"Warning: Failed to load custom hair palette {file}: {e}")
                            continue
        
        # Load hair palettes from vanilla_pals/hair folder
        hair_path = os.path.join("vanilla_pals", "hair")
        print(f"Looking for hair palettes at: {os.path.abspath(hair_path)}")
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
                                print(f"Warning: Invalid hair palette file {file} - incorrect size: {len(data)} bytes")
                                continue
                            
                            # Validate that all bytes are valid (0-255)
                            for i in range(PALETTE_SIZE * 3):
                                if not (0 <= data[i] <= 255):
                                    print(f"Warning: Invalid hair palette file {file} - invalid byte at position {i}")
                                    continue
                            
                            self.hair_palettes[char_id].append(palette_path)
                            
                        except Exception as e:
                            print(f"Warning: Failed to load hair palette {file}: {e}")
                            continue
        
        # Load 3rd job base fashion palettes
        third_job_path = os.path.join("vanilla_pals", "3rd_default_fashion")
        print(f"Looking for 3rd job palettes at: {os.path.abspath(third_job_path)}")
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
                                    print(f"Warning: Invalid 3rd job palette file {file} - incorrect size: {len(data)} bytes")
                                    continue
                                
                                # Validate that all bytes are valid (0-255)
                                for i in range(PALETTE_SIZE * 3):
                                    if not (0 <= data[i] <= 255):
                                        print(f"Warning: Invalid 3rd job palette file {file} - invalid byte at position {i}")
                                        continue
                                
                                palettes.append(palette_path)
                                
                            except Exception as e:
                                print(f"Warning: Failed to load 3rd job palette {file}: {e}")
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
        print(f"\n=== Data Loading Summary ===")
        print(f"Working directory: {os.getcwd()}")
        print(f"Available characters: {len(self.available_characters)}")
        print(f"Available jobs: {self.available_jobs}")
        print(f"Characters with images: {list(self.character_images.keys())}")
        print(f"Characters with fashion palettes: {list(self.fashion_palettes.keys())}")
        print(f"Characters with hair palettes: {list(self.hair_palettes.keys())}")
        print(f"Characters with 3rd job palettes: {list(self.third_job_palettes.keys())}")
        print("=============================\n")
    def refresh_data(self):
        """Reloads assets from disk (rawbmps, pals, custom_pals, 3rd job) and rebuilds the UI without restarting."""
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
                print("[Refresh] Assets reloaded.")

        except Exception as e:
            try:
                messagebox.showerror("Refresh", f"Failed to refresh assets:\\n{e}")
            except Exception:
                print("Failed to refresh:", e)


    def create_ui(self):
        """Create the main UI"""
        # Set window size and make it resizable
        self.master.geometry("900x650")
        self.master.resizable(True, True)
        self.master.minsize(900, 650)
        
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
                                     values=["100%", "200%", "Fit"], state="readonly", width=10)
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
        self.preview_var = tk.StringVar(value="single")
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
        
        # Scrollable canvas for image (vertical only for all frames mode)
        self.v_scroll = Scrollbar(img_frame, orient="vertical")
        self.v_scroll.pack(side="right", fill="y")
        
        self.canvas = Canvas(img_frame, width=400, height=400,
                           yscrollcommand=self.v_scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.v_scroll.config(command=self.canvas.yview)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.img_id = None
        self.tk_image = None
        
        # Control panel (right side)
        control_frame = tk.Frame(content_frame)
        control_frame.pack(side="right", fill="y", padx=(10, 0))
        
        # 3rd Job Base Fashion section (only for 3rd jobs)
        self.third_job_frame = tk.LabelFrame(control_frame, text="3rd Job Base Fashion")
        self.third_job_frame.pack(fill="x", pady=(0, 5))
        self.third_job_frame.configure(height=120, width=300)
        
        # Hair section - reduced height to make room for 3rd job base fashion
        self.hair_frame = tk.LabelFrame(control_frame, text="Hair")
        self.hair_frame.pack(fill="x", pady=(0, 5))
        self.hair_frame.configure(height=100, width=300)
        
        # Fashion section with scrollbar - reduced height to make room for 3rd job base fashion
        self.fashion_frame = tk.LabelFrame(control_frame, text="Fashion")
        self.fashion_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        # Create scrollable frame for fashion palettes - reduced height
        self.fashion_canvas = tk.Canvas(self.fashion_frame, height=250, width=300)
        self.fashion_scrollbar = tk.Scrollbar(self.fashion_frame, orient="vertical", command=self.fashion_canvas.yview)
        self.fashion_scrollable_frame = tk.Frame(self.fashion_canvas)
        
        def update_scroll_region(event):
            self.fashion_canvas.configure(scrollregion=self.fashion_canvas.bbox("all"))
        
        self.fashion_scrollable_frame.bind("<Configure>", update_scroll_region)
        
        self.fashion_canvas.create_window((0, 0), window=self.fashion_scrollable_frame, anchor="nw")
        self.fashion_canvas.configure(yscrollcommand=self.fashion_scrollbar.set)
        
        self.fashion_canvas.pack(side="left", fill="both", expand=True)
        self.fashion_scrollbar.pack(side="right", fill="y")
        
        # Control buttons
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
        tk.Button(button_frame, text="Export All Frames", command=self.export_all_frames).pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Export Palette", command=self.export_pal).pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Live Edit Palette", command=self.open_live_palette_editor).pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Reset to Original", command=self.reset_to_original).pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Debug Info", command=self.debug_info).pack(side="left")
        
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
            
            # Reset custom preview settings for new character
            self.custom_start_index = 0
            
            # Update all UI sections
            self.update_third_job_section()
            self.update_hair_section()
            self.update_fashion_section()
            
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
        
        if preview_mode == "custom":
            self.next_custom_frames()
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
            
            # Reset custom preview settings for new character
            self.custom_start_index = 0
            
            # Update all UI sections
            self.update_third_job_section()
            self.update_hair_section()
            self.update_fashion_section()
            
            # Load palettes and update display immediately for 3rd job characters
            self.load_palettes()
            # Update zoom combo state based on new character's frame count
            self.update_zoom_combo_state()
            self.update_image_display()
            
            # Load first image for this character
            if char_id in self.character_images and self.character_images[char_id]:
                self.current_image_index = 0
                self.load_character_image()
                self.update_navigation_buttons()
            
            # Ensure zoom state is updated after job change
            self.update_zoom_combo_state()

    def update_third_job_section(self):
        """Update the 3rd Job Base Fashion section"""
        # Clear existing widgets
        for widget in self.third_job_frame.winfo_children():
            widget.destroy()
        
        if not hasattr(self, 'current_character') or not self.current_character:
            return
            
        char_id = self.current_character
        if char_id not in CHARACTER_MAPPING:
            return
        
        char_info = CHARACTER_MAPPING[char_id]
        
        # For 1st and 2nd jobs, hide the 3rd job section entirely
        if char_info["job"] in ["1st Job", "2nd Job"]:
            self.third_job_frame.pack_forget()
            return
        else:
            # Show the 3rd job frame for 3rd jobs
            self.third_job_frame.pack(fill="x", pady=(0, 5))
        
        # Special handling for Paula characters - they don't have 3rd job base fashion
        if char_id in ["chr025", "chr026", "chr027"]:
            tk.Label(self.third_job_frame, text="Silly, Paula doesn't have multiple 3rd jobs!", 
                    fg="red", font=("Arial", 9, "bold")).pack(anchor="w", pady=5)
            return
        
        # Check if this character has 3rd job base fashion palettes
        palette_char_id = self.get_palette_character_id(char_id)
        if palette_char_id in self.third_job_palettes:
            palettes = self.third_job_palettes[palette_char_id]
            
            # Add palette options (no NONE option for 3rd jobs)
            for palette_path in palettes:
                palette_name = os.path.basename(palette_path)
                tk.Radiobutton(self.third_job_frame, text=palette_name, variable=self.third_job_var,
                              value=palette_path, command=self.on_third_job_change).pack(anchor="w")
            
            # Set default to first palette if available
            if palettes:
                self.third_job_var.set(palettes[0])
            else:
                self.third_job_var.set("NONE")

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
                "fashion_1": "Shirt",
                "fashion_2": "Gloves", 
                "fashion_3": "Skirt",
                "fashion_4": "Backpack",
                "fashion_5": "Shoes"
            },
            "002": {  # chr002
                "fashion_1": "Shoes",
                "fashion_2": "Shirt",
                "fashion_3": "Belt", 
                "fashion_4": "Pants",
                "fashion_5": "Gloves",
                "fashion_6": "Sash"
            },
            "004": {  # chr004
                "fashion_1": "Overcoat",
                "fashion_2": "Undershirt",
                "fashion_3": "Pants",
                "fashion_4": "Shoes", 
                "fashion_5": "Staff"
            },
            "005": {  # chr005
                "fashion_1": "Blazer",
                "fashion_2": "Shoes",
                "fashion_3": "Skirt",
                "fashion_4": "Undershirt",
                "fashion_5": "Purse"
            },
            "006": {  # chr006
                "fashion_1": "Overcoat",
                "fashion_2": "Shorts",
                "fashion_3": "Shoes",
                "fashion_4": "Gloves",
                "fashion_5": "Shirt"
            },
            "007": {  # chr007
                "fashion_1": "Ribbon",
                "fashion_2": "Belt",
                "fashion_3": "Top",
                "fashion_4": "Shoes",
                "fashion_5": "Paws",
                "fashion_6": "Skirt"
            },
            "008": {  # chr008
                "fashion_1": "Coat",
                "fashion_2": "Pants",
                "fashion_3": "Shoes"
            },
            "009": {  # chr009
                "fashion_1": "Cloak",
                "fashion_2": "Gloves",
                "fashion_3": "Shorts",
                "fashion_4": "Wristbands",
                "fashion_5": "Shoes",
                "fashion_6": "Socks"
            },
            "010": {  # chr010
                "fashion_1": "Scruff",
                "fashion_2": "Tunic",
                "fashion_3": "Undershirt",
                "fashion_4": "Gloves",
                "fashion_5": "Shoes"
            },
            "012": {  # chr012
                "fashion_1": "Arm Straps",
                "fashion_2": "Necklace",
                "fashion_3": "Robes",
                "fashion_4": "Skirt",
                "fashion_5": "Shoes"
            },
            "013": {  # chr013
                "fashion_1": "Two-Piece",
                "fashion_2": "Harness",
                "fashion_3": "Armbands",
                "fashion_4": "Gloves",
                "fashion_5": "Shoes"
            },
            "014": {  # chr014
                "fashion_1": "Undershirt",
                "fashion_2": "Cloak",
                "fashion_3": "Belt",
                "fashion_4": "Gloves",
                "fashion_5": "Shoes"
            },
            "015": {  # chr015
                "fashion_1": "Shirt",
                "fashion_2": "Belt",
                "fashion_3": "Skirt",
                "fashion_4": "Stockings",
                "fashion_5": "Shoes"
            },
            "016": {  # chr016
                "fashion_1": "Undershirt",
                "fashion_2": "Two-Piece",
                "fashion_3": "Shoes"
            },
            "100": {  # chr100 (Paula 1st Job)
                "fashion_1": "Jacket",
                "fashion_2": "Skirt",
                "fashion_3": "Socks",
                "fashion_4": "Shoes",
                "fashion_5": "Ribbons",
                "fashion_6": "Armbands",
                "fashion_7": "Extra"
            },
            "101": {  # chr101 (Paula 2nd Job)
                "fashion_1": "Dress",
                "fashion_2": "Belt",
                "fashion_3": "Shoes",
                "fashion_4": "Ribbons",
                "fashion_5": "Armbands",
                "fashion_6": "Legband"
            },
            "102": {  # chr102 (Paula 3rd Job)
                "fashion_1": "Undershirt",
                "fashion_2": "Dress",
                "fashion_3": "Socks",
                "fashion_4": "Shoes",
                "fashion_5": "Hair Ribbon",
                "fashion_6": "Dress Ribbon",
                "fashion_7": "Belt",
                "fashion_8": "Gloves"
            },
            "003": {  # chr003
                "fashion_1": "Coat",
                "fashion_2": "Bow",
                "fashion_3": "Undercoat",
                "fashion_4": "Shoes",
                "fashion_5": "Socks",
                "fashion_6": "Book"
            },
            "020": {  # chr020
                "fashion_1": "Shawl",
                "fashion_2": "Underscarf",
                "fashion_3": "Undershirt",
                "fashion_4": "Coat",
                "fashion_5": "Shoes"
            },
            "017": {  # chr017
                "fashion_1": "Top",
                "fashion_2": "Shoulderpads",
                "fashion_3": "Gloves",
                "fashion_4": "Skirt",
                "fashion_5": "Shoes"
            },
            "018": {  # chr018
                "fashion_1": "Undershirt",
                "fashion_2": "Armored Top",
                "fashion_3": "Kilt",
                "fashion_4": "Wristbands",
                "fashion_5": "Shoes"
            },
            "011": {  # chr011
                "fashion_1": "Overcoat",
                "fashion_2": "Bow",
                "fashion_3": "Satchel",
                "fashion_4": "Gloves",
                "fashion_5": "Shoes"
            },
            "019": {  # chr019
                "fashion_1": "Bows",
                "fashion_2": "Sleeves",
                "fashion_3": "Brooch",
                "fashion_4": "Dress",
                "fashion_5": "Shoes"
            },
            "021": {  # chr021
                "fashion_1": "Trenchcoat",
                "fashion_2": "Shorts",
                "fashion_3": "Gloves",
                "fashion_4": "Shoes",
                "fashion_5": "Unknown"
            },
            "022": {  # chr022
                "fashion_1": "Overcoat",
                "fashion_2": "Undershirt",
                "fashion_3": "Shorts",
                "fashion_4": "Shoes",
                "fashion_5": "Unknown"
            },
            "023": {  # chr023
                "fashion_1": "Overcoat",
                "fashion_2": "Skirt",
                "fashion_3": "Shoes",
                "fashion_4": "Undershirt"
            },
            "024": {  # chr024 (Raccoon 3rd Job)
                "fashion_1": "Ruffled Shirt",
                "fashion_2": "Overcoat",
                "fashion_3": "Undercoat",
                "fashion_4": "Pants",
                "fashion_5": "Full Suit",
                "fashion_6": "Shoes"
            },
            "025": {  # chr025 (Paula 1st Job)
                "fashion_1": "Dress",
                "fashion_2": "Sash",
                "fashion_3": "Skirt",
                "fashion_4": "Gloves",
                "fashion_5": "Shoes",
                "fashion_6": "Accessories",
                "fashion_7": "Extra"
            },
            "026": {  # chr026 (Paula 2nd Job)
                "fashion_1": "Dress",
                "fashion_2": "Sash",
                "fashion_3": "Skirt",
                "fashion_4": "Gloves",
                "fashion_5": "Shoes",
                "fashion_6": "Accessories"
            },
            "027": {  # chr027 (Paula 3rd Job)
                "fashion_1": "Sash",
                "fashion_2": "Dress",
                "fashion_3": "Skirt",
                "fashion_4": "Gloves",
                "fashion_5": "Shoes",
                "fashion_6": "Accessories",
                "fashion_7": "Extra",
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
        for widget in self.hair_frame.winfo_children():
            widget.destroy()
        
        # Add "NONE" option outside the scrollable area
        tk.Radiobutton(self.hair_frame, text="NONE", variable=self.hair_var, 
                      value="NONE", command=self.on_hair_change).pack(anchor="w", padx=5, pady=(5,0))
        
        if not hasattr(self, 'current_character') or not self.current_character:
            return
            
        char_id = self.current_character
        palette_char_id = self.get_palette_character_id(char_id)
        
        # Add hair palette options (limit to about 6 lines)
        if palette_char_id in self.hair_palettes:
            # Create a scrollable frame for hair options if there are many
            hair_canvas = tk.Canvas(self.hair_frame, height=80, width=280)
            hair_scrollbar = tk.Scrollbar(self.hair_frame, orient="vertical", command=hair_canvas.yview)
            hair_scrollable_frame = tk.Frame(hair_canvas)
            
            def update_hair_scroll_region(event):
                hair_canvas.configure(scrollregion=hair_canvas.bbox("all"))
            
            hair_scrollable_frame.bind("<Configure>", update_hair_scroll_region)
            hair_canvas.create_window((0, 0), window=hair_scrollable_frame, anchor="nw")
            hair_canvas.configure(yscrollcommand=hair_scrollbar.set)
            
            for palette_path in sorted(self.hair_palettes[palette_char_id]):
                palette_name = os.path.basename(palette_path)
                # Check if this is a custom palette
                script_dir = os.path.dirname(os.path.abspath(__file__))
                root_dir = os.path.dirname(script_dir)
                custom_pals_path = os.path.join(root_dir, "exports", "custom_pals")
                is_custom = os.path.abspath(palette_path).startswith(os.path.abspath(custom_pals_path))
                display_name = f"{palette_name} (C)" if is_custom else palette_name
                
                tk.Radiobutton(hair_scrollable_frame, text=display_name, variable=self.hair_var,
                              value=palette_path, command=self.on_hair_change).pack(anchor="w")
            
            hair_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            hair_scrollbar.pack(side="right", fill="y", pady=5)
        
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
                    type_frame.pack(fill="x", pady=2)
                    
                    # Get proper fashion type name
                    fashion_name = self.get_fashion_type_name(char_id, fashion_type)
                    
                    # Label for fashion type
                    tk.Label(type_frame, text=f"{fashion_name}:", font=("Arial", 9, "bold")).pack(anchor="w")
                    
                    # Radio buttons for this type
                    var = tk.StringVar()
                    self.fashion_vars[fashion_type] = var
                    
                    # Add "NONE" option for each fashion type
                    tk.Radiobutton(type_frame, text="NONE", variable=var,
                                  value="NONE", command=self.on_fashion_change).pack(anchor="w", padx=(10, 0))
                    
                    for palette_name, palette_path in palettes:
                        # Check if this is a custom palette
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        root_dir = os.path.dirname(script_dir)
                        custom_pals_path = os.path.join(root_dir, "exports", "custom_pals")
                        is_custom = os.path.abspath(palette_path).startswith(os.path.abspath(custom_pals_path))
                        display_name = f"{palette_name} (C)" if is_custom else palette_name
                        
                        tk.Radiobutton(type_frame, text=display_name, variable=var,
                                      value=palette_path, command=self.on_fashion_change).pack(anchor="w", padx=(10, 0))
                    
                    # Set default to NONE for all characters
                    var.set("NONE")

    def on_third_job_change(self):
        """Handle 3rd job base fashion selection change"""
        # Safety check: if current character is Paula, don't process 3rd job changes
        if hasattr(self, 'current_character') and self.current_character in ["chr025", "chr026", "chr027"]:
            return
        
        self.load_palettes()
        self.update_image_display()

    def on_hair_change(self):
        """Handle hair selection change"""
        self.load_palettes()
        self.update_image_display()

    def on_fashion_change(self):
        """Handle fashion selection change"""
        self.load_palettes()
        self.update_image_display()

    def load_palettes(self):
        """Load selected palettes"""
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
        self.update_zoom_combo_state()
        self.update_image_display()
        
        # Add a delayed update to ensure zoom state is set correctly after UI updates
        self.master.after(100, self.update_zoom_combo_state)
    
    def get_current_displayed_frame(self):
        """Get the currently displayed frame index"""
        if hasattr(self, 'current_character') and self.current_character:
            if self.preview_var.get() == "single":
                return self.current_image_index
            elif self.preview_var.get() == "custom" and self.use_frame_choice:
                return self.chosen_frame
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
        
        # Get stored settings for this character/job combination
        char_settings = self.frame_range_settings.get(self.current_character, {})
        job_settings = char_settings.get(current_job, None)
        
        # Get the currently displayed frame
        current_frame = self.get_current_displayed_frame()
        
        if job_settings:
            frame_count, start_frame, end_frame = job_settings
            dialog = CustomPreviewDialog(self, max_frames, start_frame, end_frame, frame_count, 
                                       self.use_bmp_export, self.show_frame_labels,
                                       initial_frame=current_frame)
        else:
            dialog = CustomPreviewDialog(self, max_frames, use_bmp=self.use_bmp_export,
                                       show_labels=self.show_frame_labels,
                                       initial_frame=current_frame)
            
        self.master.wait_window(dialog.dialog)
        
        if dialog.result is not None:
            frame_count, start_frame, end_frame, use_bmp, show_labels, use_portrait, use_myshop, use_choice, chosen_frame = dialog.result
            self.custom_frame_count = frame_count
            self.use_bmp_export = use_bmp
            self.use_portrait_export = use_portrait
            self.use_myshop_export = use_myshop
            self.show_frame_labels = show_labels
            self.custom_start_frame = start_frame
            self.custom_end_frame = end_frame
            
            # If user chose a specific frame, set it as the start index
            if use_choice and chosen_frame is not None:
                self.custom_start_index = chosen_frame
            else:
                self.custom_start_index = start_frame
            print(f"=== DIALOG RESULT ===")
            print(f"BMP={use_bmp}")
            print(f"Portrait={use_portrait}")
            print(f"MyShop={use_myshop}")
            print("===================")
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
        self.update_image_display()

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
        
        if preview_mode == "all":
            # Disable "Fit" option when "all" is selected
            current_zoom = self.zoom_var.get()
            if current_zoom == "Fit":
                self.zoom_var.set("100%")
            # Disable the zoom combo to prevent selection
            self.zoom_combo.config(state="disabled")
        elif preview_mode == "custom":
            # For custom mode, check the number of frames being displayed (not total character frames)
            if hasattr(self, 'current_character') and self.current_character:
                char_id = self.current_character
                if char_id in self.character_images:
                    # Use custom_frame_count instead of total character frames
                    frames_to_display = getattr(self, 'custom_frame_count', 3)  # Default to 3 if not set
                    if frames_to_display <= 100:  # Check against frames being displayed
                        # Enable zoom for custom previews with 100 or fewer frames being displayed
                        self.zoom_combo.config(state="readonly")
                    else:
                        # Disable zoom for custom previews with more than 100 frames being displayed
                        current_zoom = self.zoom_var.get()
                        if current_zoom == "Fit":
                            self.zoom_var.set("100%")
                        self.zoom_combo.config(state="disabled")
                else:
                    # No images loaded, disable zoom
                    self.zoom_combo.config(state="disabled")
            else:
                # No character selected, disable zoom
                self.zoom_combo.config(state="disabled")
        else:
            # Re-enable the zoom combo for single mode
            self.zoom_combo.config(state="readonly")
        
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
                    # Use custom_frame_count instead of total character frames
                    frames_to_display = getattr(self, 'custom_frame_count', 3)
                    if frames_to_display <= 100:
                        self.zoom_combo.config(state="readonly")
                    else:
                        self.zoom_combo.config(state="disabled")

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
            elif zoom_level == "Fit":
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                if canvas_width > 1 and canvas_height > 1:
                    scale_x = canvas_width / w
                    scale_y = canvas_height / h
                    scale = min(scale_x, scale_y)
                    display_w = int(w * scale)
                    display_h = int(h * scale)
            
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
        self._last_preview_mode = preview_mode
        
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
        self.img_id = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        
        # Add frame number text below the image
        text_y = display_h + 5  # Position text 5 pixels below the image
        # Get the frame number from current_image_index (add 1 for display since it's 0-based)
        frame_number = self.current_image_index + 1
        # Add frame number if enabled
        if self.show_frame_labels:
            self.canvas.create_text(display_w // 2, text_y, text=str(frame_number), 
                                  anchor="n", font=("Arial", 8))
        
        self.canvas.config(scrollregion=(0, 0, display_w, display_h + 25))  # Add extra space for frame number
        # Force canvas update to ensure display refreshes
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
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:  # Canvas not yet configured
            canvas_width = 400
        
        # Calculate layout
        max_images_per_row = 3  # Show 3 images per row
        padding = 10
        image_spacing = 20
        
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
                
                # Resize image to fit canvas width
                available_width = (canvas_width - padding * 2 - image_spacing * (max_images_per_row - 1)) // max_images_per_row
                scale_factor = min(available_width / w, 1.0)  # Don't scale up, only down
                new_width = int(w * scale_factor)
                new_height = int(h * scale_factor)
                
                if scale_factor < 1.0:
                    rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                processed_images.append((rgb_img, new_width, new_height))
                max_width = max(max_width, new_width)
                max_height = max(max_height, new_height)
                
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
                continue
        
        if not processed_images:
            return
        
        # Calculate layout
        rows = (len(processed_images) + max_images_per_row - 1) // max_images_per_row
        total_height = rows * max_height + (rows - 1) * image_spacing + padding * 2
        
        # Create PhotoImage objects and place them
        y_offset = padding
        for i, (rgb_img, img_width, img_height) in enumerate(processed_images):
            row = i // max_images_per_row
            col = i % max_images_per_row
            
            x_offset = padding + col * (max_width + image_spacing) + (max_width - img_width) // 2
            y_pos = y_offset + row * (max_height + image_spacing) + (max_height - img_height) // 2
            
            # Create PhotoImage and store reference
            photo_img = ImageTk.PhotoImage(rgb_img)
            # Create the image
            self.canvas.create_image(x_offset, y_pos, anchor="nw", image=photo_img)
            
            # Add frame number text below the image
            frame_number = i + 1  # Add 1 since frame numbers are 0-based internally
            text_y = y_pos + img_height + 5  # Position text 5 pixels below the image
            # Add frame number
            self.canvas.create_text(x_offset + img_width // 2, text_y, text=str(frame_number), 
                                  anchor="n", font=("Arial", 8))
            
            # Store reference to prevent garbage collection
            if not hasattr(self, 'all_frame_images'):
                self.all_frame_images = []
            self.all_frame_images.append(photo_img)
        
        # Set scroll region
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
            
        # Get frames to display based on custom_start_index
        frames_to_show = min(frame_count, len(all_images) - self.custom_start_index)
        frame_indices = range(self.custom_start_index, self.custom_start_index + frames_to_show)
        
        # Get the selected frames
        custom_images = [all_images[i] for i in frame_indices]
        if not custom_images:
            self.canvas.delete("all")
            return
            
        # Store the frame indices for reference
        self.custom_frames = list(frame_indices)
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:  # Canvas not yet configured
            canvas_width = 400
        
        # Calculate layout
        max_images_per_row = 3  # Show 3 images per row
        padding = 10
        image_spacing = 20
        
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
                
                # Apply zoom settings for custom preview (up to 50 frames)
                zoom_level = self.zoom_var.get()
                new_width, new_height = w, h
                
                # Check if we have 100 or fewer frames being displayed to enable zoom
                frames_to_display = getattr(self, 'custom_frame_count', 3)
                
                if frames_to_display <= 100:
                    if zoom_level == "200%":
                        # Scale up to 200%
                        new_width = int(w * 2)
                        new_height = int(h * 2)
                        rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.NEAREST)
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
                        
                        new_width = int(w * scale)
                        new_height = int(h * scale)
                        rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    else:
                        # 100% - resize to fit canvas width (original behavior)
                        available_width = (canvas_width - padding * 2 - image_spacing * (max_images_per_row - 1)) // max_images_per_row
                        scale_factor = min(available_width / w, 1.0)  # Don't scale up, only down
                        new_width = int(w * scale_factor)
                        new_height = int(h * scale_factor)
                        
                        if scale_factor < 1.0:
                            rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    # More than 100 frames being displayed - use original behavior (no zoom)
                    available_width = (canvas_width - padding * 2 - image_spacing * (max_images_per_row - 1)) // max_images_per_row
                    scale_factor = min(available_width / w, 1.0)  # Don't scale up, only down
                    new_width = int(w * scale_factor)
                    new_height = int(h * scale_factor)
                    
                    if scale_factor < 1.0:
                        rgb_img = rgb_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                processed_images.append((rgb_img, new_width, new_height))
                max_width = max(max_width, new_width)
                max_height = max(max_height, new_height)
                
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
                continue
        
        if not processed_images:
            return
        
        # Calculate layout
        rows = (len(processed_images) + max_images_per_row - 1) // max_images_per_row
        total_height = rows * max_height + (rows - 1) * image_spacing + padding * 2
        
        # Create PhotoImage objects and place them
        y_offset = padding
        for i, (rgb_img, img_width, img_height) in enumerate(processed_images):
            row = i // max_images_per_row
            col = i % max_images_per_row
            
            x_offset = padding + col * (max_width + image_spacing) + (max_width - img_width) // 2
            y_pos = y_offset + row * (max_height + image_spacing) + (max_height - img_height) // 2
            
            # Create PhotoImage and store reference
            photo_img = ImageTk.PhotoImage(rgb_img)
            # Create the image
            self.canvas.create_image(x_offset, y_pos, anchor="nw", image=photo_img)
            
            # Add frame number text below the image if enabled
            if self.show_frame_labels:
                frame_number = self.custom_frames[i] + 1  # Add 1 since frame numbers are 0-based internally
                text_y = y_pos + img_height + 5  # Position text 5 pixels below the image
                # Add frame number
                self.canvas.create_text(x_offset + img_width // 2, text_y, text=str(frame_number), 
                                      anchor="n", font=("Arial", 8))
            
            # Store reference to prevent garbage collection
            if not hasattr(self, 'custom_frame_images'):
                self.custom_frame_images = []
            self.custom_frame_images.append(photo_img)
        
        # Set scroll region
        self.canvas.config(scrollregion=(0, 0, canvas_width, total_height))
        # Force canvas update to ensure display refreshes
        self.canvas.update()
        self.canvas.update_idletasks()
        self.master.update()

    def get_merged_palette(self):
        """Get the merged palette, respecting keying colors and transparency"""
        if not self.original_palette:
            return [(0, 0, 0)] * PALETTE_SIZE
        
        result = self.original_palette.copy()
        
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
            
            for i in range(PALETTE_SIZE):
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
                if (color is not None and not should_ignore and (i in allowed_indices or (getattr(layer, 'palette_type', '') == 'fashion_4' and char_num == '020'))):
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
            root_dir = os.path.dirname(script_dir)
            possible_paths = [
                os.path.join("vanilla_pals", "fashion", filename),
                os.path.join(root_dir, "exports", "custom_pals", filename)
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
                    "fashion_3": [range(0, 149), range(150, 236)],  # 0-148, 150-235
                    "fashion_4": [range(0, 177)],  # 0-176
                    "fashion_5": [range(0, 177), range(178, 198)]   # 0-176, 178-197
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
                "fashion_2": [range(134, 149)],  # w10-w14: 134-148
                "fashion_3": [range(150, 165)],  # w20-w24: 150-164
                "fashion_4": [range(166, 174)],  # w30-w34: 166-173
                "fashion_5": [range(176, 182)],  # w40-w44: 176-181
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

    def reset_to_original(self):
        """Reset to show the original image without any palette modifications"""
        if not self.original_image:
            messagebox.showinfo("Reset", "No image loaded")
            return
        
        # Deactivate all palette layers
        for layer in self.palette_layers:
            layer.active = False
        
        self.update_image_display()
        messagebox.showinfo("Reset", "Reset to original image")

    def get_display_image_for_export(self):
        """Get the current image with palettes applied without updating display"""
        if not self.original_image:
            return None
            
        # Get the current frame based on preview mode
        preview_mode = self.preview_var.get()
        if preview_mode == "custom":
            # In custom mode, use the first frame from the current display
            if hasattr(self, 'custom_frames') and self.custom_frames:
                frame_index = self.custom_frames[0]
            else:
                frame_index = self.custom_start_index
        else:
            frame_index = self.current_image_index
            
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
        
    def export_background_bmp(self):
        """Export current image as BMP with background color"""
        if not self.original_image:
            messagebox.showinfo("Notice", "No image loaded.")
            return
            
        # Debug: Print export settings
        print(f"=== EXPORT SETTINGS ===")
        print(f"BMP={self.use_bmp_export}")
        print(f"Portrait={self.use_portrait_export}")
        print(f"MyShop={self.use_myshop_export}")
        print("======================")
            
        # Get base paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        export_dir = os.path.join(root_dir, "exports", "images")
        
        # Get base file name without extension
        base_name = f"{self.current_character}_{self.current_image_index:03d}"
        
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
            portrait_path = os.path.join(target_dir, f"{base_filename}_illu.bmp")
            myshop_path = os.path.join(target_dir, f"{base_filename}_shop.bmp")
            
            # Regular BMP export
            def save_regular():
                img.save(regular_path, "BMP")
                return "Regular BMP"
            export_ops.append(save_regular)
            
            # Portrait export (if selected)
            if self.use_portrait_export:
                def save_portrait():
                    portrait_img = Image.new("RGB", (103, 103), self.background_color)
                    x = (103 - img.width) // 2
                    y = (103 - img.height) // 2
                    portrait_img.paste(img, (x, y))
                    portrait_img.save(portrait_path, "BMP", quality=24)
                    return "Portrait (103x103)"
                export_ops.append(save_portrait)
            
            # MyShop export (if selected)
            if self.use_myshop_export:
                def save_myshop():
                    if self.myshop_base is None:
                        raise AttributeError("MyShop base image not loaded")
                    
                    # Create a copy of the base image and convert to RGB
                    myshop_img = self.myshop_base.copy().convert("RGB")
                    
                    # Replace magenta (255, 0, 255) with user's background color
                    data = list(myshop_img.getdata())
                    for i, pixel in enumerate(data):
                        if pixel == (255, 0, 255):  # Magenta
                            data[i] = self.background_color
                    myshop_img.putdata(data)
                    
                    # Create mask for non-background pixels in the frame
                    mask = Image.new("L", img.size, 0)
                    for i, pixel in enumerate(img.getdata()):
                        if pixel != self.background_color:
                            mask.putpixel((i % img.width, i // img.width), 255)
                    
                    # Center the frame
                    x = (105 - img.width) // 2
                    y = (105 - img.height) // 2
                    myshop_img.paste(img, (x, y), mask)
                    myshop_img.save(myshop_path, "BMP", quality=24)
                    return "MyShop (105x105)"
                export_ops.append(save_myshop)
            
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
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export image: {e}")
            
    def export_transparent_png(self):
        """Export the current frame as a transparent PNG with palettes applied"""
        if not self.original_image:
            messagebox.showinfo("Notice", "Please load a character image first.")
            return
        
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Images", "*.png")])
        if not path:
            return
        
        try:
            # Get the merged palette
            merged_palette = self.get_merged_palette()
            
            # Create a new image with the merged palette
            w, h = self.original_image.size
            display_img = Image.new("P", (w, h))
            
            # Apply the merged palette FIRST
            display_img.putpalette([color for palette_color in merged_palette for color in palette_color])
            
            # THEN copy the pixel data from original image
            display_img.putdata(self.original_image.getdata())
            
            # Convert to RGBA to handle transparency
            rgba_img = display_img.convert("RGBA")
            
            # Get the pixel data
            pixels = rgba_img.load()
            
            # Apply character-specific transparency based on original palette colors
            if hasattr(self, 'current_character') and self.current_character:
                char_num = self.current_character[3:]
                
                # Debug: Count transparent pixels
                transparent_count = 0
                total_pixels = w * h
                
                # Get original image pixel data to check original palette indices
                original_pixel_data = list(self.original_image.getdata())
                
                for y in range(h):
                    for x in range(w):
                        should_make_transparent = False
                        
                        # Get the original palette index for this pixel
                        pixel_index = y * w + x
                        if pixel_index < len(original_pixel_data):
                            palette_index = original_pixel_data[pixel_index]
                            if palette_index < len(self.original_palette):
                                original_color = self.original_palette[palette_index]
                                
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
                            pixels[x, y] = (0, 0, 0, 0)  # Transparent
                            transparent_count += 1
                
                # Debug: Show transparency info
                transparency_percentage = (transparent_count / total_pixels) * 100

            
            # Save as PNG with transparency
            rgba_img.save(path, "PNG")
            messagebox.showinfo("Success", f"Exported transparent PNG to {path}\nTransparency: {transparent_count}/{total_pixels} pixels ({transparency_percentage:.1f}%)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    def export_all_frames(self):
        """Export all frames in the current character's folder with current palettes applied"""
        if not hasattr(self, 'current_character') or not self.current_character:
            messagebox.showinfo("Notice", "Please select a character first.")
            return
        
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
        
        # Ask user for base output directory
        base_output_dir = filedialog.askdirectory(title="Select base directory for export")
        if not base_output_dir:
            return
        
        # Create the specific folder using forward slashes for consistency
        output_dir = f"{base_output_dir}/{folder_name}"
        if not os.path.exists(output_dir):
            print(f"WARNING: Directory {output_dir} does not exist and will not be created.")
            return
        
        try:
            images = self.character_images[self.current_character]
            total_images = len(images)
            
            # Show progress dialog
            progress_window = tk.Toplevel(self.master)
            progress_window.title("Exporting Frames")
            progress_window.geometry("300x100")
            progress_window.transient(self.master)
            progress_window.grab_set()
            
            progress_label = tk.Label(progress_window, text="Exporting frames...")
            progress_label.pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_window, length=250, mode='determinate')
            progress_bar.pack(pady=5)
            
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
                    print(f"Error processing {image_path}: {e}")
                    continue
            
            progress_window.destroy()
            messagebox.showinfo("Success", f"Exported {exported_count}/{total_images} frames to:\n{output_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

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
            self.update_image_display()
    
    def export_pal(self):
        """Export all active palettes as one combined palette in VGA 24-bit format"""
        if not self.palette_layers:
            messagebox.showinfo("Notice", "No palette layers loaded.")
            return
        
        # Get all active layers
        active_layers = [layer for layer in self.palette_layers if layer.active]
        
        if not active_layers:
            messagebox.showinfo("Notice", "No active palette layers to export.")
            return
        
        # Set initial directory to exports/custom_pals in root directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        initial_dir = os.path.join(root_dir, "exports", "custom_pals")
        
        path = filedialog.asksaveasfilename(
            defaultextension=".pal",
            initialdir=initial_dir,
            filetypes=[("VGA 24-bit Palette Files", "*.pal")]
        )
        if not path:
            return
        
        try:
            # Get the merged palette (same logic as used for display/export)
            merged_palette = self.get_merged_palette()
            
            # Ensure we have exactly 256 colors for VGA palette
            while len(merged_palette) < 256:
                merged_palette.append((0, 0, 0))  # Fill with black if needed
            
            # Write VGA 24-bit format: each color as 3 bytes (R, G, B) in sequence
            with open(path, "wb") as f:
                for r, g, b in merged_palette[:256]:  # Ensure exactly 256 colors
                    f.write(bytes([r, g, b]))
            
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
            if not self._warn_if_nonimpact(getattr(default_layer, "palette_type", "")):
                return
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

        self._live_editor_window = tk.Toplevel(self.master)
        self._live_editor_window.title("Live Edit Palette")
        self._live_editor_window.resizable(False, False)
        
        # Add callback to refresh custom pals when window is closed
        def on_window_close():
            self.refresh_custom_pals()
            self._live_editor_window.destroy()
        
        self._live_editor_window.protocol("WM_DELETE_WINDOW", on_window_close)

        # Top bar
        top = tk.Frame(self._live_editor_window); top.pack(fill="x", padx=6, pady=6)
        tk.Label(top, text="Edit which:").pack(side="left")
        tk.OptionMenu(top, self._live_target_name, *names, command=self._live_on_target_changed).pack(side="left", padx=(4,8))
        tk.Checkbutton(top, text="Multi-select", variable=self._multi_select, command=self._live_multi_toggled).pack(side="left", padx=(8,8))
        tk.Button(top, text="Clear Sel", command=self._live_clear_selection).pack(side="left")
        self._sel_count_lbl = tk.Label(top, text="(0 selected)"); self._sel_count_lbl.pack(side="left", padx=(6,0))
        tk.Button(top, text="Save Item .pal", command=self._live_save_item_pal).pack(side="left", padx=(12,8))
        tk.Button(top, text="Close", command=on_window_close).pack(side="right")

        # Body
        body = tk.Frame(self._live_editor_window); body.pack(fill="both", expand=True, padx=6, pady=6)

        # Swatches grid (left)
        grid = tk.Frame(body); grid.pack(side="left", padx=(0,8))
        self._live_swatches = []
        ly = self._live_layers[self._live_name_to_index[self._live_target_name.get()]]
        for i in range(PALETTE_SIZE):
            r,g,b = ly.colors[i] if isinstance(ly.colors[i], tuple) else (0,0,0)
            btn = tk.Button(grid, width=2, height=1, relief="ridge",
                            bg=f"#{r:02x}{g:02x}{b:02x}")
            btn.grid(row=i//16, column=i%16, padx=1, pady=1)
            # Left-click with optional Shift
            btn.bind("<Button-1>", lambda e, i=i: self._live_on_swatch_click(i, e))
            self._live_swatches.append(btn)

        # Picker panel (right)
        panel = tk.LabelFrame(body, text="Color Picker", padx=8, pady=8)
        panel.pack(side="left", fill="y")

        self._picker_idx_var = tk.StringVar(value="0")
        tk.Label(panel, text="Index:").grid(row=0, column=0, sticky="w")
        self._picker_idx_entry = tk.Entry(panel, width=5, textvariable=self._picker_idx_var)
        self._picker_idx_entry.grid(row=0, column=1, sticky="w")
        tk.Button(panel, text="Go", command=self._live_goto_index).grid(row=0, column=2, padx=(6,0))

        tk.Label(panel, text="Hex #RRGGBB:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self._picker_hex = tk.Entry(panel, width=10)
        self._picker_hex.grid(row=1, column=1, columnspan=2, sticky="w")
        tk.Button(panel, text="Apply", command=self._live_apply_hex).grid(row=1, column=3, padx=(6,0))

        def mk_scale(label, row, varname):
            v = tk.IntVar(value=0)
            setattr(self, varname, v)
            tk.Label(panel, text=label).grid(row=row, column=0, sticky="w", pady=(8,0))
            sc = tk.Scale(panel, from_=0, to=255, orient="horizontal", variable=v,
                          command=lambda *_: self._live_slider_changed())
            sc.grid(row=row, column=1, columnspan=3, sticky="we", pady=(8,0))
        panel.grid_columnconfigure(2, weight=1)

                        
        # HSV controls
        tk.Label(panel, text="Hue").grid(row=5, column=0, sticky="w", pady=(8,0))
        self._picker_h = tk.Scale(panel, from_=0, to=360, orient="horizontal", command=lambda *_: self._hsv_debounced_change())
        self._picker_h.grid(row=5, column=1, columnspan=3, sticky="we", pady=(8,0))
        tk.Label(panel, text="Sat").grid(row=6, column=0, sticky="w", pady=(8,0))
        self._picker_s = tk.Scale(panel, from_=0, to=100, orient="horizontal", command=lambda *_: self._hsv_debounced_change())
        self._picker_s.grid(row=6, column=1, columnspan=3, sticky="we", pady=(8,0))
        tk.Label(panel, text="Val").grid(row=7, column=0, sticky="w", pady=(8,0))
        self._picker_v = tk.Scale(panel, from_=0, to=100, orient="horizontal", command=lambda *_: self._hsv_debounced_change())
        self._picker_v.grid(row=7, column=1, columnspan=3, sticky="we", pady=(8,0))
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
        eH.grid(row=5, column=4, sticky="w", padx=(6,0))
        # S entry
        self._hsv_s_str = tk.StringVar(value="0")
        eS = tk.Entry(panel, textvariable=self._hsv_s_str, width=5)
        eS.grid(row=6, column=4, sticky="w", padx=(6,0))
        # V entry
        self._hsv_v_str = tk.StringVar(value="0")
        eV = tk.Entry(panel, textvariable=self._hsv_v_str, width=5)
        eV.grid(row=7, column=4, sticky="w", padx=(6,0))

        # --- Saved Colors panel (simple MS Paint style) ---
        if not hasattr(self, "_saved_colors"):
            self._saved_colors = [(0,0,0)] * 20
        sc_frame = tk.LabelFrame(panel, text="Saved Colors")
        sc_frame.grid(row=9, column=0, columnspan=4, sticky="we", padx=0, pady=(6,0))
        sc_top = tk.Frame(sc_frame); sc_top.pack(fill="x", padx=4, pady=4)
        
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
                
        mouse_btn = tk.Button(sc_top, text="L", font=("Arial", 10, "bold"), width=2, 
                            relief="raised", bg="SystemButtonFace", activebackground="SystemButtonFace",
                            command=toggle_click_mode)
        mouse_btn.pack(side="right", padx=(4, 0))
        
        # Help text label
        help_label = tk.Label(sc_frame, text="Left click to save color\nRight click to apply color",
                            anchor="w", justify="left", fg="gray40")
        help_label.pack(fill="x", padx=6, pady=(0,6))
        
        def _sc_save():
            from tkinter import filedialog
            import json
            p = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")], title="Save Colors")
            if not p: return
            try:
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(self._saved_colors, f)
            except Exception: pass
        def _sc_load():
            from tkinter import filedialog
            import json
            p = filedialog.askopenfilename(filetypes=[("JSON","*.json")], title="Load Colors")
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

        sc_grid = tk.Frame(sc_frame); sc_grid.pack(padx=4, pady=(0,6))
        self._sc_btns = []
        def _sc_refresh():
            for i, btn in enumerate(self._sc_btns):
                r,g,b = self._saved_colors[i]
                try: btn.config(bg=f"#{r:02x}{g:02x}{b:02x}")
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
            try: self._live_swatches[idx].config(bg=f"#{r:02x}{g:02x}{b:02x}")
            except Exception: pass
            try: self._picker_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")
            except Exception: pass
            try:
                self._picker_hex.delete(0,"end"); self._picker_hex.insert(0,f"#{r:02x}{g:02x}{b:02x}")
            except Exception: pass
            if hasattr(self, "_sync_hsv_from_rgb"): self._sync_hsv_from_rgb(int(r),int(g),int(b))
            if hasattr(self, "update_image_display"): self.update_image_display()
        def _handle_click(event, slot):
            """Handle click based on current mode"""
            if (event.num == 3) == self.use_right_click:  # Right click mode matches right click or vice versa
                _sc_put(slot)
            else:
                _sc_pick(slot)
                
        for i in range(20):
            btn = tk.Button(sc_grid, width=3, text="")
            btn.grid(row=i//10, column=i%10, padx=2, pady=2)
            btn.bind("<Button-1>", lambda e, j=i: _handle_click(e, j))
            btn.bind("<Button-3>", lambda e, j=i: _handle_click(e, j))
            self._sc_btns.append(btn)
        # Helper text under saved colors grid
        try:
            self._click_help_text = tk.StringVar()
            def update_help_text():
                if self.use_right_click:
                    self._click_help_text.set("Left click to apply color\nRight click to save color")
                else:
                    self._click_help_text.set("Right click to apply color\nLeft click to save color")
            update_help_text()  # Set initial text
            tk.Label(sc_frame, textvariable=self._click_help_text,
                    anchor="w", justify="left", fg="gray40").pack(fill="x", padx=6, pady=(0,6))
            
            # Update help text when click mode changes
            def update_help_text():
                if self.use_right_click:
                    self._click_help_text.set("Left click to apply color\nRight click to save color")
                else:
                    self._click_help_text.set("Right click to apply color\nLeft click to save color")
            update_help_text()  # Set initial text
            # No need for additional update here
        except Exception:
            pass


        _sc_refresh()

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

        self._picker_preview = tk.Label(panel, text="      ", relief="sunken")
        self._picker_preview.grid(row=8, column=0, columnspan=4, sticky="we", pady=(10,0))

        self._live_select_index(0)  # seed picker
        self._live_window = self._live_editor_window
        self._update_selection_ui()

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
        for i, btn in enumerate(self._live_swatches):
            if i in self._selected_indices:
                btn.config(relief="sunken", bd=3)
            else:
                btn.config(relief="ridge", bd=1)
        if hasattr(self, "_sel_count_lbl"):
            self._sel_count_lbl.config(text=f"({len(self._selected_indices)} selected)")

    def _live_clear_selection(self):
        self._selected_indices.clear()
        self._last_clicked_index = None
        self._update_selection_ui()

    def _live_on_swatch_click(self, i, event):
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
            # Single-select
            self._selected_indices.clear()
            self._last_clicked_index = i
            self._update_selection_ui()
            self._live_select_index(i)

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
            dS = (S_new - bs) if not use_scaleS else 0
            dV = (V_new - bv) if not use_scaleV else 0
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
                    v = max(0, min(100, int(round(v + dV))))
                else:
                    v = max(0, min(100, int(round(v * scaleV))))
            else:
                h, s, v = H_new % 360, max(0, min(100, S_new)), max(0, min(100, V_new))

            rr, gg, bb = colorsys.hsv_to_rgb((h % 360)/360.0, s/100.0, v/100.0)
            rr, gg, bb = int(round(rr*255)), int(round(gg*255)), int(round(bb*255))
            ly.colors[i] = (rr, gg, bb)
            self._live_swatches[i].config(bg=f"#{rr:02x}{gg:02x}{bb:02x}")
        focus = self._live_selected_index
        fr, fg, fb = ly.colors[focus]
        self._picker_preview.config(bg=f"#{fr:02x}{fg:02x}{fb:02x}")
        self._picker_hex.delete(0, "end"); self._picker_hex.insert(0, f"#{fr:02x}{fg:02x}{fb:02x}")

        self.update_image_display()

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
        ly = self._live_current_layer()
        if ly is None:
            return
        cols = ly.colors
        for i in range(PALETTE_SIZE):
            r,g,b = cols[i] if isinstance(cols[i], tuple) else (0,0,0)
            try:
                self._live_swatches[i].config(bg=f"#{int(r):02x}{int(g):02x}{int(b):02x}")
            except Exception:
                pass
        # Keep selection visuals
        if hasattr(self, "_update_selection_ui"):
            self._update_selection_ui()

    def _live_on_target_changed(self, *_):
        """Called when the item dropdown changes; rebuild swatches for the new layer and reset selection."""
        
        # Ask warning if switching to Hair or 3rd Job Base
        try:
            new_name = self._live_target_name.get()
            idx = self._live_name_to_index.get(new_name, 0)
            ly = self._live_layers[idx]
            if not self._warn_if_nonimpact(getattr(ly, "palette_type", "")):
                # Revert selection
                try:
                    self._live_target_name.set(getattr(self, "_live_prev_target_name", new_name))
                except Exception:
                    pass
                return
            self._live_prev_target_name = new_name
        except Exception:
            pass
# Repaint buttons for the newly selected layer
        self._selected_indices = set()
        self._last_clicked_index = None
        self._live_refresh_swatches()
        # Seed picker with index 0 for the new layer
        self._live_select_index(0)

    def _live_current_layer(self):
        if not hasattr(self, "_live_layers") or not self._live_layers:
            return None
        idx = self._live_name_to_index.get(self._live_target_name.get(), 0)
        idx = max(0, min(idx, len(self._live_layers)-1))
        return self._live_layers[idx]

    def _live_select_index(self, i):
        self._live_selected_index = int(i)
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
        targets = sorted(self._selected_indices) if self._multi_select.get() and self._selected_indices else [self._live_selected_index]
        for i in targets:
            ly.colors[i] = (r, g, b)
            self._live_swatches[i].config(bg=f"#{r:02x}{g:02x}{b:02x}")
        self._picker_preview.config(bg=f"#{r:02x}{g:02x}{b:02x}")
        self.update_image_display()
        # Sync HSV sliders from this RGB
        self._sync_hsv_from_rgb(r, g, b)


    def _live_slider_changed(self):
        # RGB sliders removed in HSV-only mode; keep as no-op to satisfy any callers.
        return


    def _live_save_item_pal(self):
        ly = self._live_current_layer()
        if ly is None:
            return
        colors = ly.colors
        default_name = os.path.splitext(ly.name)[0] + ".pal"
        
        # Set initial directory to exports/custom_pals
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        initial_dir = os.path.join(root_dir, "exports", "custom_pals")
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
            # Ensure we have exactly 256 colors for VGA palette
            vga_colors = list(colors)
            while len(vga_colors) < 256:
                vga_colors.append((0, 0, 0))  # Fill with black if needed
            
            # Write VGA 24-bit format: each color as 3 bytes (R, G, B) in sequence
            with open(path, "wb") as f:
                for r,g,b in vga_colors[:256]:  # Ensure exactly 256 colors
                    f.write(bytes([r,g,b]))
            messagebox.showinfo("Saved", f"Saved VGA 24-bit palette {os.path.basename(path)} for {ly.name}")
            
            # Bring the PAL editor window to the front
            self._live_editor_window.lift()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def refresh_custom_pals(self):
        """Refresh custom pals by reloading them and updating the UI"""
        # Remove the guard clause - we want to refresh all custom pals regardless of current character
        
        # Clear existing custom palettes from ALL data structures
        for char_id in list(self.fashion_palettes.keys()):
            # Get the absolute path of exports/custom_pals
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(script_dir)
            custom_pals_path = os.path.join(root_dir, "exports", "custom_pals")
            custom_pals_abs = os.path.abspath(custom_pals_path)
            
            # Only keep palettes that are NOT in exports/custom_pals
            self.fashion_palettes[char_id] = [
                path for path in self.fashion_palettes[char_id] 
                if os.path.abspath(path).startswith(custom_pals_abs) == False
            ]
        
        for char_id in list(self.hair_palettes.keys()):
            # Get the absolute path of exports/custom_pals
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(script_dir)
            custom_pals_path = os.path.join(root_dir, "exports", "custom_pals")
            custom_pals_abs = os.path.abspath(custom_pals_path)
            
            # Only keep palettes that are NOT in exports/custom_pals
            self.hair_palettes[char_id] = [
                path for path in self.hair_palettes[char_id] 
                if os.path.abspath(path).startswith(custom_pals_abs) == False
            ]
        
        # Reload custom palettes from exports/custom_pals folder
        custom_pals_paths = self.get_custom_pals_paths()
        print("\n=== Refreshing Custom Palettes ===")
        print(f"Looking in paths: {custom_pals_paths}")
        for custom_pals_path in custom_pals_paths:
            print(f"\nChecking directory: {os.path.abspath(custom_pals_path)}")
            if not os.path.exists(custom_pals_path):
                print(f"Directory does not exist!")
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
                                print(f"\nLoaded custom fashion palette:")
                                print(f"  File: {file}")
                                print(f"  Path: {palette_path}")
                                print(f"  Character: {char_id_for_pal}")
                                print(f"  Current palettes: {[os.path.basename(p) for p in self.fashion_palettes[char_id_for_pal]]}")
                            else:
                                print(f"\nInvalid custom fashion palette:")
                                print(f"  File: {file}")
                                print(f"  Path: {palette_path}")
                                print(f"  Reason: Validation failed - invalid color values")
                            
                        except Exception as e:
                            print(f"\nError loading custom fashion palette:")
                            print(f"  File: {file}")
                            print(f"  Path: {palette_path}")
                            print(f"  Error: {e}")
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
                                print(f"Loaded custom hair palette: {file} at {palette_path}")
                                print(f"Current hair palettes for {char_id_for_pal}: {self.hair_palettes[char_id_for_pal]}")
                            else:
                                print(f"Invalid custom hair palette: {file} (validation failed)")
                            
                        except Exception as e:
                            print(f"Failed to load custom hair palette {file}: {e}")
                            continue
        
        # Update the UI sections to reflect the new custom pals
        self.update_hair_section()
        self.update_fashion_section()

    def get_custom_pals_paths(self):
        """Get list of custom palette directories to check"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        
        # ONLY use root/exports/custom_pals
        custom_pals_path = os.path.join(root_dir, "exports", "custom_pals")
        
        # Ensure directory exists
        os.makedirs(custom_pals_path, exist_ok=True)
        print(f"Using custom pals directory: {os.path.abspath(custom_pals_path)}")
        
        return [custom_pals_path]

    def debug_info(self):
        """Show debug information"""
        info = f"Current Character: {self.character_var.get()}\n"
        info += f"Current Job: {self.job_var.get()}\n"
        info += f"Selected Hair: {self.hair_var.get()}\n"
        info += f"Selected 3rd Job Base: {self.third_job_var.get()}\n"
        info += f"Loaded Palette Layers: {len(self.palette_layers)}\n"
        
        for i, layer in enumerate(self.palette_layers):
            info += f"  {i+1}. {layer.name} ({layer.palette_type}) - {'Active' if layer.active else 'Inactive'}\n"
        
        # Add frame count information for zoom support
        info += f"\nFrame Counts for Zoom Support (≤100 frames):\n"
        zoom_supported_chars = []
        # Sort characters numerically by their number
        def sort_char_key(char_id):
            # Extract the number from chr### format
            match = re.match(r'chr(\d+)', char_id)
            if match:
                return int(match.group(1))
            return 0
        
        for char_id in sorted(self.character_images.keys(), key=sort_char_key):
            frame_count = len(self.character_images[char_id])
            if frame_count <= 100:
                zoom_supported_chars.append(f"{char_id}: {frame_count} frames")
        
        if zoom_supported_chars:
            for char_info in zoom_supported_chars:
                info += f"  {char_info}\n"
        else:
            info += "  No characters with ≤100 frames found\n"
        
        messagebox.showinfo("Debug Info", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaletteTool(root)
    root.mainloop()

