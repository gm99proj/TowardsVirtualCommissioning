import pandas as pd
import xml.etree.ElementTree as ET

# ---------------- REAL RESOURCES ----------------

resource_ids = {
    65: "Bottom Cover Station",
    63: "Drilling Station",
    64: "Robot Cell",
    68: "Quality Check Station",
    66: "Top Cover Station",
    80: "Unload Station"
}

# ---------------- CONCEPTUAL RESOURCES ----------------

conceptual_resource_ids = {
    1: "Bottom Cover Station",
    2: "Top Cover Station"
}


# =====================================================
# UPDATE TABLE
# =====================================================

def update_resource_table(
        tree,
        file_path,
        conceptual=False):

    try:

        # -------------------------------------------------
        # RESET TABLE
        # -------------------------------------------------

        if conceptual:
            active_resources = conceptual_resource_ids
        else:
            active_resources = resource_ids

        for res_id, name in active_resources.items():

            if tree.exists(str(res_id)):

                tree.item(
                    str(res_id),
                    values=(
                        f"{res_id} - {name}",
                        "Free",
                        "-",
                        "-"
                    ),
                    tags=("Free",)
                )
        
        # -------------------------------------------------

        df = pd.read_excel(file_path)

        # Get latest per resource
        df = df.drop_duplicates(
            "resource_id",
            keep="last"
        )
        # =================================================
        # CONCEPTUAL MODE
        # =================================================

        if conceptual:

            for _, row in df.iterrows():

                try:
                    res = int(row["resource_id"])

                except:
                    continue

                if res in conceptual_resource_ids:

                    status = str(
                        row.get("status", "")
                    ).lower()

                    operation = row.get(
                        "operation_no",
                        ""
                    )

                    pallet = row.get(
                        "assignment",
                        ""
                    )

                    if status == "completed" or status == "":

                        if tree.exists(str(res)):

                            tree.item(
                                str(res),
                            values=(
                                f"{res} - {conceptual_resource_ids[res]}",
                                "Available",
                                "-",
                                "-"
                            ),
                            tags=("Free",)
                        )

                    else:

                        tree.item(
                            str(res),
                            values=(
                                f"{res} - {conceptual_resource_ids[res]}",
                                "In Use",
                                operation,
                                pallet
                            ),
                            tags=("Busy",)
                        )

        # =================================================
        # REAL MODE
        # =================================================

        else:
            for _, row in df.iterrows():

                try:
                    res = int(row["resource_id"])

                except:
                    continue

                if res in resource_ids:

                    status = str(
                        row.get("status", "")
                    ).lower()

                    operation = row.get(
                        "operation_no",
                        ""
                    )

                    pallet = row.get(
                        "assignment",
                        ""
                    )

                    if status == "completed" or status == "":

                        if tree.exists(str(res)):

                            tree.item(
                                str(res),
                            values=(
                                f"{res} - {resource_ids[res]}",
                                "Available",
                                "-",
                                "-"
                            ),
                            tags=("Free",)
                        )

                    else:

                        tree.item(
                            str(res),
                            values=(
                                f"{res} - {resource_ids[res]}",
                                "In Use",
                                operation,
                                pallet
                            ),
                            tags=("Busy",)
                        )

    except Exception as e:
        print("Error:", e)

    # -------------------------------------------------
    # AUTO REFRESH ONLY FOR REAL MODE
    # -------------------------------------------------

    return tree.after(
    500,
    lambda: update_resource_table(
        tree,
        file_path,
        conceptual
    )
)


# =====================================================
# RESET MES
# =====================================================

def reset_mes(tree, file_path):

    df = pd.read_excel(file_path).iloc[0:0]

    df.to_excel(file_path, index=False)

    # Reset only visible rows
    for item in tree.get_children():

        current_values = tree.item(item)["values"]

        tree.item(
            item,
            values=(
                current_values[0],
                "Free",
                "-",
                "-"
            ),
            tags=("Free",)
        )