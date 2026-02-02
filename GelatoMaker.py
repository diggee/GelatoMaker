import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Gelato Calculator')


def get_total_nutrition(ingredient, label):
    return ingredient['Name'][label]/100 * ingredient['Amount']


# region ALL INGREDIENTS
whipping_cream = {
    'Name': "D'electa Dairy Whipping Cream",
    'Energy (Kcal)': 355.55,
    'Protein (g)': 3.17,
    'Carbohydrates (g)': 5.95,
    'Total Sugar (g)': 3.06,
    'Added Sugar (g)': 0.01,
    'Total Fat (g)': 35,
    'Trans Fat (g)': 0.01,
    'Saturated Fat (g)': 25.32,
    'Cholestrol (mg)': 34.88,
    'Sodium (mg)': 1725.45,
    'Calcium (mg)': 0.0,
    'MSNF (%)': 0.0,
    'Water (%)': 60,
    'Cost/g': 0.58
}
amul_taaza = {
    'Name': 'Amul Taaza',
    'Energy (Kcal)': 57.8,
    'Protein (g)': 3.0,
    'Carbohydrates (g)': 4.7,
    'Total Sugar (g)': 4.7,
    'Added Sugar (g)': 0.0,
    'Total Fat (g)': 3.0,
    'Trans Fat (g)': 0.0,
    'Saturated Fat (g)': 2.0,
    'Cholestrol (mg)': 9.0,
    'Sodium (mg)': 40.0,
    'Calcium (mg)': 110.0,
    'MSNF (%)': 8.5,
    'Water (%)': 88.5,
    'Cost/g': 0.058
}
amul_gold = {
    'Name': 'Amul Gold',
    'Energy (Kcal)': 91.0,
    'Protein (g)': 3.2,
    'Carbohydrates (g)': 5.0,
    'Total Sugar (g)': 5.0,
    'Added Sugar (g)': 0.0,
    'Total Fat (g)': 6.5,
    'Trans Fat (g)': 0.0,
    'Saturated Fat (g)': 4.2,
    'Cholestrol (mg)': 17.0,
    'Sodium (mg)': 42.0,
    'Calcium (mg)': 120.0,
    'MSNF (%)': 9.0,
    'Water (%)': 84.5,
    'Cost/g': 0.07
}
country_delight = {
    'Name': 'Country Delight',
    'Energy (Kcal)': 63.0,
    'Protein (g)': 3.2,
    'Carbohydrates (g)': 4.4,
    'Total Sugar (g)': 4.0,
    'Added Sugar (g)': 0.0,
    'Total Fat (g)': 3.5,
    'Trans Fat (g)': 0.0,
    'Saturated Fat (g)': 2.9,
    'Cholestrol (mg)': 7.0,
    'Sodium (mg)': 40.0,
    'Calcium (mg)': 150.0,
    'MSNF (%)': 8.5,
    'Water (%)': 88,
    'Cost/g': 0.098
}
country_delight_full_cream = {
    'Name': 'Country Delight Full Cream',
    'Energy (Kcal)': 86.0,
    'Protein (g)': 3.2,
    'Carbohydrates (g)': 4.9,
    'Total Sugar (g)': 4.9,
    'Added Sugar (g)': 0.0,
    'Total Fat (g)': 6.0,
    'Trans Fat (g)': 0.0,
    'Saturated Fat (g)': 3.8,
    'Cholestrol (mg)': 13.0,
    'Sodium (mg)': 45.0,
    'Calcium (mg)': 150.0,
    'MSNF (%)': 9.0,
    'Water (%)': 85,
    'Cost/g': 0.12
}
amul_dark_chocolate_sugarfree = {
    'Name': 'Amul Dark Chocolate Sugar Free',
    'Energy (Kcal)': 558.0,
    'Protein (g)': 6.0,
    'Carbohydrates (g)': 56.7,
    'Total Sugar (g)': 0.5,
    'Added Sugar (g)': 0.0,
    'Total Fat (g)': 33.8,
    'Trans Fat (g)': 0.0,
    'Saturated Fat (g)': 20.7,
    'Cholestrol (mg)': 0.0,
    'Sodium (mg)': 38.0,
    'Calcium (mg)': 0.0,
    'MSNF (%)': 0.0,
    'Water (%)': 0.0,
    'Cost/g': 1.2
}
popular_essentials_refined_sugar = {
    'Name': 'Popular Essentials Refined Sugar',
    'Energy (Kcal)': 387.0,
    'Protein (g)': 0.0,
    'Carbohydrates (g)': 100.0,
    'Total Sugar (g)': 100.0,
    'Added Sugar (g)': 100.0,
    'Total Fat (g)': 0.0,
    'Trans Fat (g)': 0.0,
    'Saturated Fat (g)': 0.0,
    'Cholestrol (mg)': 0.0,
    'Sodium (mg)': 0.0,
    'Calcium (mg)': 0.0,
    'MSNF (%)': 0.0,
    'Water (%)': 0.0,
    'Cost/g': 0.073
}
weikfield_cornstarch = {
    'Name': 'Weikfield Cornstarch',
    'Energy (Kcal)': 350.0,
    'Protein (g)': 0.0,
    'Carbohydrates (g)': 87.2,
    'Total Sugar (g)': 0.0,
    'Added Sugar (g)': 0.0,
    'Total Fat (g)': 0.0,
    'Trans Fat (g)': 0.0,
    'Saturated Fat (g)': 0.0,
    'Cholestrol (mg)': 0.0,
    'Sodium (mg)': 14.7,
    'Calcium (mg)': 0.0,
    'MSNF (%)': 0.0,
    'Water (%)': 0.0,
    'Cost/g': 0.33
}
# endregion

milk_ingredients = [amul_taaza, amul_gold, country_delight, country_delight_full_cream]
whipping_cream_ingredients = [whipping_cream]
refined_sugar_ingredients = [popular_essentials_refined_sugar]
dark_chocolate_ingredients = [amul_dark_chocolate_sugarfree]
stabilizer_ingredients = [weikfield_cornstarch]
emulsifiers_ingredients = []
all_ingredients = {'Milk': milk_ingredients,
                   'Cream': whipping_cream_ingredients,
                   'Sugar': refined_sugar_ingredients,
                   'Dark Chocolate': dark_chocolate_ingredients,
                   'Stabilizer': stabilizer_ingredients,}
selected_ingredients = []

col_left, col_mid, col_right = st.columns([2, 3, 3])
with col_left:
    st.subheader('Ingredients')
    
    for label, items in all_ingredients.items():
        chosen_ingredient = st.selectbox(label, options = items, format_func = lambda x: x['Name'])
        selected_ingredients.append(chosen_ingredient)
        
    st.subheader('Nutritional information of chosen ingredients per 100g')
    if selected_ingredients:
        nutrition_df = pd.DataFrame(selected_ingredients).set_index('Name')
        st.dataframe(nutrition_df)
    else:
        st.info("Select ingredients to see nutrition")
 
    
general_gelato_composition = {
    'Total Fat (%)': [6.0, 9.0],
    'Total Sugar (%)': [16.0, 20.0],
    'MSNF (%)': [8.0, 11.0],
    'Stabilizers (%)': [0.25, 0.4],
    'Emulsifiers (%)': [0.0, 0.4],
    'Water (%)': [58.0, 65.0]
}

# INGREDIENTS USED
milk = {'Name': country_delight_full_cream, 'Amount': 450}
cream = {'Name': whipping_cream, 'Amount': 40}
chocolate = {'Name': amul_dark_chocolate_sugarfree, 'Amount': 40}
sugar = {'Name': popular_essentials_refined_sugar, 'Amount': 90}
cornstarch = {'Name': weikfield_cornstarch, 'Amount': 2}

milk_density = 1.03
overrun = 1.2
total_water = 0.0
total_weight = 0.0
total_cost = 0.0

ingredients_used = [milk, cream, chocolate, sugar, cornstarch]
for ingredient in ingredients_used:
    total_water += (ingredient['Name']['Water (%)']/100) * ingredient['Amount']
    if ingredient == milk:
        total_weight += (ingredient['Amount'] * milk_density)
    else:
        total_weight += ingredient['Amount']
    total_cost += ingredient['Name']['Cost/g'] * ingredient['Amount']

# gelato specific information
gelato_composition = {
    'Total Fat (%)': 0.0,
    'Total Sugar (%)': 0.0,
    'MSNF (%)': 0.0,
    'Stabilizers (%)': 0.0,
    'Emulsifiers (%)': 0.0,
    'Water (%)': 0.0
}
# generic nutritional information
nutritional_information = {
    'Energy (Kcal)': 0.0,
    'Protein (g)': 0.0,
    'Carbohydrates (g)': 0.0,
    'Total Sugar (g)': 0.0,
    'Total Fat (g)': 0.0,
    'Cholestrol (mg)': 0.0,
    'Calcium (mg)': 0.0,
}

for key in nutritional_information.keys():
    for ingredient in ingredients_used:
        nutritional_information[key] += get_total_nutrition(ingredient, key)
    nutritional_information[key] = nutritional_information[key] / total_weight * 100 
nutritional_information_df = pd.DataFrame.from_dict(nutritional_information, orient = 'index', columns = ['Value per 100 grams'])

for key in gelato_composition.keys():
    if key == 'Stabilizers (%)':
        gelato_composition[key] = cornstarch['Amount']
    elif key == 'Emulsifiers (%)':
        gelato_composition[key] = 0.0
    elif key == 'Total Fat (%)':		
        for ingredient in ingredients_used:
            gelato_composition[key] += get_total_nutrition(ingredient, 'Total Fat (g)')
    elif key == 'Total Sugar (%)':		
        for ingredient in ingredients_used:
            gelato_composition[key] += get_total_nutrition(ingredient, 'Total Sugar (g)')
    else:
        for ingredient in ingredients_used:
            gelato_composition[key] += get_total_nutrition(ingredient, key)
    gelato_composition[key] = gelato_composition[key] / total_weight * 100 

with col_right:
    st.subheader('Gelato Composition')
    for label, range in general_gelato_composition.items():
        st.slider(label, min_value = range[0], max_value = range[1], 
                  value = gelato_composition[label], step = 0.01, disabled = False)
        
    st.subheader('Nutritional information per 100g')
    st.write(nutritional_information_df)

gelato_composition_df = pd.DataFrame.from_dict(gelato_composition, orient = 'index', columns = ['Composition'])
print(gelato_composition_df)
