def get_model(parent, file):
    parent.withdraw()  # Hide main window temporarily
    filepath = file.askopenfilename(
        title="Select a Plant Simulation model",
        filetypes=[("Plant Simulation Models", "*.spp")]
    )
    parent.deiconify()  # Show window again
    return filepath

def init_plantsim(parent, file, output_label, PS, messagebox):
    try:
        path = get_model(parent, file)
        if not path:
            output_label.config(text="No file selected")
            return
        
        PS.load_model(path)
        output_label.config(text="Model loaded successfully")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def set_event_controller(PS, default, output_label, messagebox):
    try:
        PS.set_path_context(default) # Set path context to default (root) to access the event controller
        PS.set_event_controller()
        output_label.config(text="Event controller set")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sim_start_stop(PS, output_label, messagebox):
    try:
        if PS.is_simulation_running():
            PS.stop_simulation()
            output_label.config(text="Simulation Stopped")
        else:
            PS.start_simulation()
            output_label.config(text="Simulation Started")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sim_reset(PS, output_label, messagebox):
    try:
        PS.reset_simulation()
        output_label.config(text="Simulation Reset")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sim_doc(PS, output_label):
    print(PS.__doc__)
    output_label.config(text="Documentation printed in console")

def sim_quit(PS, parent, messagebox):
    if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
        PS.quit()
        parent.destroy()

def sim_close(PS, output_label, messagebox):
    if messagebox.askokcancel("Close", "Do you want to close the current model?"):
        PS.close_model()
        output_label.config(text="Model closed")