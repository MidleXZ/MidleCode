import sys
import os
import shutil
import threading
import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_loader_and_output.ailoader import load_gguf_model
from ai_loader_and_output.aiconverter import convert_dsl_to_python

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MidleCodeStudio(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)

        self.title("MidleCode Studio")
        self.geometry("1100x700")

        self.llm = None
        self.is_processing = False
        self.current_project_dir = None
        self.active_file_path = None

        self.projects_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "projects"))
        os.makedirs(self.projects_dir, exist_ok=True)

        self._build_main_interface()
        
        # Hide main window until a project is opened or created
        self.withdraw()
        self.open_project_launcher()

    def _build_main_interface(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top Control Bar
        self.top_bar = ctk.CTkFrame(self, height=45, corner_radius=0)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.lbl_project = ctk.CTkLabel(self.top_bar, text="Project: None", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_project.pack(side="left", padx=15)

        self.btn_run = ctk.CTkButton(
            self.top_bar, text="▶ Run App", command=self.run_app, fg_color="#28a745", width=90
        )
        self.btn_run.pack(side="right", padx=(5, 15), pady=8)

        self.btn_convert = ctk.CTkButton(
            self.top_bar, text="⚡ Convert to .py", command=self.start_conversion, fg_color="#007ACC", width=120
        )
        self.btn_convert.pack(side="right", padx=5, pady=8)

        self.lbl_status = ctk.CTkLabel(self.top_bar, text="Status: Ready", text_color="gray")
        self.lbl_status.pack(side="right", padx=15)

        # Left Sidebar (File Explorer)
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        explorer_title = ctk.CTkLabel(self.sidebar, text="FILE EXPLORER", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray")
        explorer_title.pack(pady=(10, 5), padx=10, anchor="w")

        # Explorer Action Buttons
        btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(btn_frame, text="+ File", width=55, command=self.create_file).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="+ Folder", width=65, command=self.create_folder).pack(side="left", padx=2)

        # File Tree Container
        self.file_tree_frame = ctk.CTkScrollableFrame(self.sidebar)
        self.file_tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Switch Project button
        ctk.CTkButton(self.sidebar, text="Switch Project", command=self.open_project_launcher, fg_color="#444").pack(pady=5, padx=10, fill="x")

        # Main Editor Tabs
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.tab_dsl = self.tabs.add("Script Editor (.midlecode)")
        self.tab_py = self.tabs.add("Compiled Python (.py)")

        self.txt_dsl = ctk.CTkTextbox(self.tab_dsl, font=("Courier", 14))
        self.txt_dsl.pack(fill="both", expand=True, padx=5, pady=5)

        self.txt_py = ctk.CTkTextbox(self.tab_py, font=("Courier", 14))
        self.txt_py.pack(fill="both", expand=True, padx=5, pady=5)

    def open_project_launcher(self):
        """Startup Launcher Window"""
        launcher = ctk.CTkToplevel(self)
        launcher.title("MidleCode Launcher")
        launcher.geometry("450x380")
        launcher.grab_set()

        ctk.CTkLabel(launcher, text="MidleCode Studio", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))

        proj_list = ctk.CTkScrollableFrame(launcher, height=150)
        proj_list.pack(fill="x", padx=30, pady=10)

        selected_proj = tk.StringVar(value="")

        def refresh_launcher_list():
            for w in proj_list.winfo_children():
                w.destroy()
            projects = [d for d in os.listdir(self.projects_dir) if os.path.isdir(os.path.join(self.projects_dir, d))]
            for p in projects:
                ctk.CTkRadioButton(proj_list, text=p, variable=selected_proj, value=p).pack(anchor="w", pady=3)

        refresh_launcher_list()

        entry_name = ctk.CTkEntry(launcher, placeholder_text="New project name...")
        entry_name.pack(padx=30, pady=5, fill="x")

        def action_create():
            name = entry_name.get().strip()
            if name:
                p_dir = os.path.join(self.projects_dir, name)
                if not os.path.exists(p_dir):
                    os.makedirs(p_dir)
                    # Creates blank default file
                    with open(os.path.join(p_dir, "main.midlecode"), "w") as f:
                        f.write("")
                    self.load_project(p_dir)
                    launcher.destroy()

        def action_open():
            p = selected_proj.get()
            if p:
                self.load_project(os.path.join(self.projects_dir, p))
                launcher.destroy()

        def action_delete():
            p = selected_proj.get()
            if p and messagebox.askyesno("Delete", f"Delete project '{p}'?"):
                shutil.rmtree(os.path.join(self.projects_dir, p))
                refresh_launcher_list()

        btn_box = ctk.CTkFrame(launcher, fg_color="transparent")
        btn_box.pack(pady=10)
        ctk.CTkButton(btn_box, text="Open", command=action_open, width=90).pack(side="left", padx=5)
        ctk.CTkButton(btn_box, text="Create", command=action_create, fg_color="#1f7a8c", width=90).pack(side="left", padx=5)
        ctk.CTkButton(btn_box, text="Delete", command=action_delete, fg_color="#a83232", width=90).pack(side="left", padx=5)

    def load_project(self, project_path):
        self.current_project_dir = project_path
        self.lbl_project.configure(text=f"Project: {os.path.basename(project_path)}")
        self.deiconify()
        self.refresh_file_explorer()
        
        main_file = os.path.join(project_path, "main.midlecode")
        if os.path.exists(main_file):
            self.open_file(main_file)

    def refresh_file_explorer(self):
        for child in self.file_tree_frame.winfo_children():
            child.destroy()

        if not self.current_project_dir:
            return

        for root, dirs, files in os.walk(self.current_project_dir):
            rel_path = os.path.relpath(root, self.current_project_dir)
            indent = 0 if rel_path == "." else rel_path.count(os.sep) + 1
            
            if rel_path != ".":
                d_name = os.path.basename(root)
                lbl = ctk.CTkLabel(self.file_tree_frame, text="📁 " + d_name, font=ctk.CTkFont(weight="bold"))
                lbl.pack(anchor="w", padx=10 * indent)

            for f in files:
                f_path = os.path.join(root, f)
                item_frame = ctk.CTkFrame(self.file_tree_frame, fg_color="transparent")
                item_frame.pack(fill="x", anchor="w", padx=10 * (indent + 1), pady=1)

                btn = ctk.CTkButton(
                    item_frame, text=f, anchor="w", fg_color="transparent", text_color="#dce4ee",
                    command=lambda p=f_path: self.open_file(p), height=20
                )
                btn.pack(side="left", fill="x", expand=True)

                ren_btn = ctk.CTkButton(item_frame, text="✏️", width=20, height=20, fg_color="transparent", command=lambda p=f_path: self.rename_item(p))
                ren_btn.pack(side="right")
                del_btn = ctk.CTkButton(item_frame, text="🗑️", width=20, height=20, fg_color="transparent", command=lambda p=f_path: self.delete_item(p))
                del_btn.pack(side="right")

    def create_file(self):
        name = simpledialog.askstring("New File", "Enter file name (e.g. app.midlecode):")
        if name:
            if not name.endswith(".midlecode") and not name.endswith(".py"):
                name += ".midlecode"
            path = os.path.join(self.current_project_dir, name)
            with open(path, "w") as f:
                f.write("")
            self.refresh_file_explorer()
            self.open_file(path)

    def create_folder(self):
        name = simpledialog.askstring("New Folder", "Enter folder name:")
        if name:
            os.makedirs(os.path.join(self.current_project_dir, name), exist_ok=True)
            self.refresh_file_explorer()

    def rename_item(self, path):
        new_name = simpledialog.askstring("Rename", "Enter new name:", initialvalue=os.path.basename(path))
        if new_name:
            new_path = os.path.join(os.path.dirname(path), new_name)
            os.rename(path, new_path)
            self.refresh_file_explorer()

    def delete_item(self, path):
        if messagebox.askyesno("Delete", f"Delete {os.path.basename(path)}?"):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.refresh_file_explorer()

    def open_file(self, path):
        self.active_file_path = path
        self.txt_dsl.delete("1.0", tk.END)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            self.txt_dsl.insert("1.0", content)

    def start_conversion(self):
        if not self.active_file_path:
            return
        with open(self.active_file_path, "w") as f:
            f.write(self.txt_dsl.get("1.0", tk.END))

        if self.is_processing:
            return
        self.is_processing = True
        self.btn_convert.configure(state="disabled")
        self.lbl_status.configure(text="Status: Converting...")
        threading.Thread(target=self._conversion_worker, daemon=True).start()

    def _conversion_worker(self):
        try:
            if self.llm is None:
                self.lbl_status.configure(text="Status: Loading AI Engine...")
                self.llm = load_gguf_model()

            self.lbl_status.configure(text="Status: Compiling...")
            dsl_input = self.txt_dsl.get("1.0", tk.END).strip()
            py_code = convert_dsl_to_python(self.llm, dsl_input)

            self.txt_py.delete("1.0", tk.END)
            self.txt_py.insert("1.0", py_code)

            output_py = os.path.join(self.current_project_dir, "app.py")
            with open(output_py, "w") as f:
                f.write(py_code)

            self.lbl_status.configure(text="Status: Conversion Done!")
            self.tabs.set("Compiled Python (.py)")
            self.refresh_file_explorer()
        except Exception as e:
            self.lbl_status.configure(text=f"Error: {str(e)}")
        finally:
            self.is_processing = False
            self.btn_convert.configure(state="normal")

    def run_app(self):
        if not self.current_project_dir:
            return
        py_file = os.path.join(self.current_project_dir, "app.py")
        if os.path.exists(py_file):
            python_executable = sys.executable
            subprocess.Popen([python_executable, py_file])
        else:
            self.lbl_status.configure(text="No app.py file to run.")

if __name__ == "__main__":
    app = MidleCodeStudio()
    app.mainloop()