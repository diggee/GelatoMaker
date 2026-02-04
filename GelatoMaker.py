import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Gelato Calculator', page_icon = ':ice_cream:')

st.markdown(
    "<h1 style='text-align:center; color:#ff9f40; font-size:64px;; margin-bottom:40px;'>Gelato Calculator</h1>",
    unsafe_allow_html=True
)

def get_gelato_cost_and_weight(total_cost: float, 
                               total_water: float, 
                               total_weight: float, 
                               selected_ingredients: dict, 
                               ingredient_amount: dict) -> tuple[float, float, float]:
    '''
    Function to calculate the total weight, cost, and water content of the base mix.
    '''
    for ingredient, ingredient_info in selected_ingredients.items():
        total_water += (ingredient_info['Water (%)']/100) * ingredient_amount[ingredient]
        if ingredient == 'Milk': # as milk amount is in ml not grams
            total_weight += (ingredient_amount[ingredient] * milk_density)
        else:
            total_weight += ingredient_amount[ingredient]
        total_cost += ingredient_info['Cost/g'] * ingredient_amount[ingredient]
    return total_cost, total_water, total_weight


def get_nutrition(ingredient: str, 
                  label: str, 
                  nutrition_df: pd.DataFrame, 
                  ingredient_amount: dict, 
                  selected_ingredients: dict) -> float:
    '''
    Function to calculate the total amount of a nutritional element (fat, sugar, etc) coming from
    a single ingredient.
    '''
    return nutrition_df.loc[selected_ingredients[ingredient]['Name'], label]/100 * ingredient_amount


def get_gelato_nutritional_information(nutritional_information: dict):
    '''
    Function to calculate nutritional information per 100grams of the end product gelato
    
    All ingredients are considered - ingredients that go into the base and ingredients that 
    are add ons, such as melted chocolate in stracciatela.
    '''
    for key in nutritional_information.keys():
        for ingredient in selected_ingredients.keys():
            nutritional_information[key] += get_nutrition(ingredient, key, nutrition_df, 
                                                                ingredient_amount[ingredient], selected_ingredients)
        nutritional_information[key] = nutritional_information[key] / total_weight * 100 
    nutritional_information_df = pd.DataFrame.from_dict(nutritional_information, orient = 'index', 
                                                        columns = ['Value per 100 grams'])
    return nutritional_information_df


def get_gelato_composition_information(gelato_composition: dict):
    '''
    Function to calculate the % of every nutrition type (fat, sugar, etc) in the gelato. 
    
    There is some confusion regarding how this calculation should be done - whether only those
    ingredients should be considered that go into the gelato base, or should all the 
    ingredients be considered that are a part of the final product. Currently, all the 
    ingredients are considered; so fat from dark chocolate in stracciatela is considered.
    This calculation is done to ensure that the % target of every nutrition type is in the
    range suitable for gelato, like how sugar should be within [16, 20].
    '''
    for key in gelato_composition.keys():
        if key == 'Stabilizers (%)':
            gelato_composition[key] = ingredient_amount['Stabilizer']
        elif key == 'Emulsifiers (%)':
            gelato_composition[key] = ingredient_amount['Emulsifier']
        elif key == 'Total Fat (%)': 
            gelato_composition[key] = nutritional_information['Total Fat (g)']
            continue    # already normalized, so skip percent normalization in this loop
        elif key == 'Total Sugar (%)':
            gelato_composition[key] = nutritional_information['Total Sugar (g)']
            continue    # already normalized, so skip percent normalization in this loop
        else:
            for ingredient in selected_ingredients.keys():
                gelato_composition[key] += get_nutrition(ingredient, key, nutrition_df, 
                                                                ingredient_amount[ingredient], selected_ingredients)
        gelato_composition[key] = gelato_composition[key] / total_weight * 100
    return gelato_composition

all_ingredients_df = pd.read_excel('ingredients.xlsx', index_col = 0)
ingredient_types = all_ingredients_df.index.unique()

selected_ingredients = {}
cols = st.columns(len(ingredient_types))
for i, ingredient_type in enumerate(ingredient_types):
    with cols[i]:
        chosen_ingredient = st.selectbox(ingredient_type, all_ingredients_df.loc[all_ingredients_df.index == ingredient_type, 'Name'])
        selected_ingredients.update({ingredient_type: chosen_ingredient})

all_ingredients_df.reset_index(inplace=True)
all_ingredients_df.drop(all_ingredients_df.columns[0], axis = 1, inplace = True)
all_ingredients_df.set_index(all_ingredients_df.columns[0], inplace = True)
selected_ingredients_df = pd.DataFrame(columns = all_ingredients_df.columns)

for key, value in selected_ingredients.items():
    selected_ingredients_df.loc[value, :] = all_ingredients_df.loc[value, :]
nutrition_df = pd.DataFrame()
st.write(selected_ingredients_df)

col_left, col_mid, col_right = st.columns([2, 3, 3], gap = 'large')
with col_left:
    st.subheader('Ingredients')
    
    for label, items in all_ingredients.items():
        chosen_ingredient = st.selectbox(label, options = items,)
        selected_ingredients.update({label: chosen_ingredient})
        nutrition_df = pd.concat([nutrition_df, pd.DataFrame([chosen_ingredient])], ignore_index = True)
        
    nutrition_df.set_index(nutrition_df.columns[0], inplace = True)
    st.subheader('Nutritional information of chosen ingredients per 100g')
    st.dataframe(nutrition_df)

milk_density = 1.03
total_water = 0.0
total_weight = 0.0
total_cost = 0.0
ingredient_amount = {}

with col_mid:
    st.subheader('Ingredient Amount')
    st.write('_All amounts in grams, except milk (ml))_')
    for label in all_ingredients.keys():
        if label == 'Milk':
            ingredient_amount[label] = st.slider(label, 0, 1000, 500, 5)
        elif label == 'Cream' or label == 'Sugar':
            ingredient_amount[label] = st.slider(label, 0, 200, 50, 1)
        elif label == 'Chocolate' or label == 'Skimmed Milk Powder' or label == 'Dextrose':
            ingredient_amount[label] = st.slider(label, 0, 100, 50, 1)
        else:
            ingredient_amount[label] = st.slider(label, 0.0, 10.0, 3.0, 0.1)
    
    total_cost, total_water, total_weight = get_gelato_cost_and_weight(total_cost, total_water, total_weight, 
                                                                       selected_ingredients, ingredient_amount)
    
    st.write(f'**Base weight - {np.round(total_weight, 2)} grams**')
    st.write(f'**Total cost - INR {np.round(total_cost)}**')
    st.write(f'**Unit cost - INR {np.round(total_cost/total_weight, 2)}**')
    
# general gelato composition 
general_gelato_composition = {
    'Total Fat (%)': [6.0, 9.0],
    'Total Sugar (%)': [16.0, 20.0],
    'MSNF (%)': [8.0, 12.0],
    'Stabilizers (%)': [0.25, 0.4],
    'Emulsifiers (%)': [0.0, 0.4],
    'Water (%)': [58.0, 65.0]
}
# specific gelato composition
gelato_composition = {
    'Total Fat (%)': 0.0,
    'Total Sugar (%)': 0.0,
    'MSNF (%)': 0.0,
    'Stabilizers (%)': 0.0,
    'Emulsifiers (%)': 0.0,
    'Water (%)': 0.0
}
# nutritional information
nutritional_information = {
    'Energy (Kcal)': 0.0,
    'Protein (g)': 0.0,
    'Carbohydrates (g)': 0.0,
    'Total Sugar (g)': 0.0,
    'Total Fat (g)': 0.0,
    'Cholestrol (mg)': 0.0,
    'Calcium (mg)': 0.0,
}

nutritional_information_df = get_gelato_nutritional_information(nutritional_information)
gelato_composition = get_gelato_composition_information(gelato_composition) 

with col_right:
    st.subheader('Gelato Composition')
    st.write('_Calculations are done considering all ingredients_')
    for label, range in general_gelato_composition.items():
        st.slider(label, min_value = range[0], max_value = range[1], 
                  value = gelato_composition[label], step = 0.01, disabled = False, 
                  help = f'min value = {range[0]}, max value = {range[1]}')
        
    st.subheader('Nutritional information per 100g')
    st.write('_Estimate; all ingredients considered_')
    st.write(nutritional_information_df)
