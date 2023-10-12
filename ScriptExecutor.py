   import tkinter as tk
   from tkinter import ttk, filedialog, messagebox
   import subprocess
   import threading
   import os
   from ttkthemes import ThemedTk

   class ScriptExecutor(ThemedTk):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.title("Script Executor")
           self.geometry("1920x1080")
           self.set_theme("yaru")
           self.grid_columnconfigure(0, weight=1)
           self.grid_rowconfigure(1, weight=1)

           self.scripts = {
               "Cover Art Resizer": "Cover Art Resizer.py",
               "Empty Folder Deleter": "Empty Folder Deleter.py",
               "Folder Mover Deluxe": "Folder Mover Deluxe.py",
               "Plex Movie Scrapper": "Plex Movie Scrapper.py",
               "Plex Stats GUI": "Plex Stats GUI.py",
               "Rename Existing Folders": "Rename Existing Folders.py",
               "TMDB Excel Exporter": "TMDB Excel Exporter.py",
               "Drive Stats": "drive_stats.py"
           }

           self.output_text = tk.Text(self)
           self.output_text.grid(row=1, column=0, sticky="nsew")

           self.script_buttons = {}
           for i, (name, path) in enumerate(self.scripts.items()):
               button = tk.Button(self, text=name, command=lambda p=path: self.run_script(p))
               button.grid(row=0, column=i, sticky="nsew")
               self.script_buttons[path] = button

           self.grid_columnconfigure(0, weight=1)
           for i in range(len(self.scripts)):
               self.grid_columnconfigure(i, weight=1)

       def run_script(self, script_path):
           for button in self.script_buttons.values():
               button["state"] = "disabled"
           self.output_text.delete(1.0, "end")
           threading.Thread(target=self.execute_script, args=(script_path,)).start()

       def execute_script(self, script_path):
           process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
           while True:
               output = process.stdout.readline()
               if output == "" and process.poll() is not None:
                   break
               if output:
                   self.output_text.insert(tk.END, output)
                   self.output_text.see(tk.END)
           for button in self.script_buttons.values():
               button["state"] = "normal"

   if __name__ == "__main__":
       app = ScriptExecutor()
       app.mainloop()