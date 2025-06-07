from dal import crud


def analyze_orders_data():
    crud.insert_material_consumption()
    print("Daily material consumption saved")
