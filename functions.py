def calculate_maintenance_price(area_in_acres,price_per_acre):
    area_in_acres = float(area_in_acres)
    price_per_acre = float(price_per_acre)
    # 1 acre = 43,560 square feet
    SQUARE_FEET_PER_ACRE = 43560
    
    # Convert acres to square feet
    area_in_square_feet = area_in_acres * SQUARE_FEET_PER_ACRE
    
    # Calculate the price per square foot
    price_per_square_foot = price_per_acre / SQUARE_FEET_PER_ACRE
    
    # Calculate the total price of the plot
    plot_price = area_in_square_feet * price_per_square_foot
    return plot_price