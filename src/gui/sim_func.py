def get_model(parent, file):
    parent.withdraw()  # Hide main window temporarily
    filepath = file.askopenfilename(
        title="Select a Plant Simulation model",
        filetypes=[("Plant Simulation Models", "*.spp")]
    )
    parent.deiconify()  # Show window again
    return filepath

def init_plantsim(parent, file, log, PS, messagebox):
    try:
        path = get_model(parent, file)
        if not path:
            log("No file selected")
            return
        
        PS.load_model(path)
        log("Model loaded successfully")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def set_event_controller(PS, default, log, messagebox):
    try:
        PS.set_path_context(default) # Set path context to default (root) to access the event controller
        PS.set_event_controller()
        log("Event controller set")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sim_start_stop(PS, log, messagebox):
    try:
        if PS.is_simulation_running():
            PS.stop_simulation()
            log("Simulation Stopped")
        else:
            PS.start_simulation()
            log("Simulation Started")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sim_reset(PS, log, messagebox):
    try:
        PS.reset_simulation()
        log("Simulation Reset")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sim_doc(PS, log):
    print(PS.__doc__)
    log("Documentation printed in console")

def sim_quit(PS, parent, messagebox):
    if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
        PS.quit()
        parent.destroy()

def sim_close(PS, log, messagebox):
    if messagebox.askokcancel("Close", "Do you want to close the current model?"):
        PS.close_model()
        log("Model closed")