import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Gelato Calculator', page_icon = ':ice_cream:')

st.markdown(
    "<h1 style='text-align:center; color:#ff9f40; font-size:64px;; margin-bottom:40px;'>Gelato Calculator</h1>",
    unsafe_allow_html=True
)

def get_total_ingredient_information(selected_ingredients_df):
    df = selected_ingredients_df.copy() # copy neded so that information in the original df is not modified
    for col in df.columns[1:]:
        if col == 'PAC' or col == 'POD': # since PAC and POD calculations are done from sugar amount
            df.loc[:, col] = df.loc[:, col] * selected_ingredients_df.loc[:, 'Total Sugar (g)'] * selected_ingredients_df.loc[:, 'Amount (g)']
        else:
            df.loc[:, col] *= selected_ingredients_df.loc[:, 'Amount (g)']
    for col in df.columns:
        df.loc['Total', col] = np.sum(df[col])
    return df # return the modified copied dataframe

if __name__ == '__main__':
    # read in the base excel sheet that has nutritional information of all the ingredients
    all_ingredients_df = pd.read_excel('ingredients.xlsx', index_col = 0)
    ingredient_types = all_ingredients_df.index.unique()

    selected_ingredients = {}
    ingredient_amounts = {}
    ingredient_max_amounts = [200, 1000, 100, 100, 200, 10, 10, 100]
    cols = st.columns(len(ingredient_types))
    for i, ingredient_type in enumerate(ingredient_types):
        with cols[i]:
            # select which particular ingredient is selected for every ingredient type
            chosen_ingredient = st.selectbox(ingredient_type, all_ingredients_df.loc[all_ingredients_df.index == ingredient_type, 'Name'])
            selected_ingredients.update({ingredient_type: chosen_ingredient})
            # change ingredient amounts
            ingredient_amount = st.slider('Amount (g)', 0, ingredient_max_amounts[i], 1, key = chosen_ingredient)
            ingredient_amounts.update({ingredient_type: ingredient_amount})
            
    all_ingredients_df.reset_index(inplace=True)
    all_ingredients_df.drop(all_ingredients_df.columns[0], axis = 1, inplace = True)
    all_ingredients_df.set_index(all_ingredients_df.columns[0], inplace = True)
    # make a dataframe of just the actual selected ingredients from the entire ingredient database (all_ingredients_df)
    selected_ingredients_df = pd.DataFrame(columns = all_ingredients_df.columns)

    for key, value in selected_ingredients.items():
        selected_ingredients_df.loc[value, :] = all_ingredients_df.loc[value, :]/100.0
    selected_ingredients_df.loc[:, 'Amount (g)'] = ingredient_amounts.values()
    col = selected_ingredients_df.pop("Amount (g)")
    selected_ingredients_df.insert(0, "Amount (g)", col)

    # make a dataframe of the nutritional information due to the actual ingredients
    gelato_df = get_total_ingredient_information(selected_ingredients_df)
    st.dataframe(gelato_df, use_container_width = True) 

    total_water = gelato_df.loc['Total', 'Water (g)']
    total_weight = gelato_df.loc['Total', 'Amount (g)']
    total_cost = gelato_df.loc['Total', 'Cost']

    col1, col2, col3 = st.columns(3, gap = 'large')
    with col1:
        st.subheader('Gelato Composition')
        # min and max limits for general gelato composition
        min_limits = [4.0, 14.0, 8.0, 0.180, 0.140, 58, 0.2, 0.15]
        max_limits = [8.0, 22.0, 11.0, 0.260, 0.180, 62, 0.4, 0.25]
        actual_values = [gelato_df.loc['Total', 'Total Fat (g)']/total_weight * 100,
                              gelato_df.loc['Total', 'Total Sugar (g)']/total_weight * 100,
                              gelato_df.loc['Total', 'MSNF (g)']/total_weight * 100,
                              gelato_df.loc['Total', 'PAC']/ total_weight,
                              gelato_df.loc['Total', 'POD']/total_weight,
                              gelato_df.loc['Total', 'Water (g)']/total_weight * 100,
                              gelato_df.loc[selected_ingredients['Emulsifier'], 'Amount (g)']/total_weight * 100,
                              gelato_df.loc[selected_ingredients['Stabilizer'], 'Amount (g)']/total_weight * 100]
        labels = ["Total Fat (%)", "Total Sugar (%)", "MSNF (%)", "PAC Index", "POD Index", "Water (%)", 
                  'Emulsifier (%)', 'Stabilizer (%)']
        gelato_limits_df = pd.DataFrame({'Min': min_limits, 'Max': max_limits, 'Value': actual_values}, index = labels)
        st.dataframe(gelato_limits_df, use_container_width = True)
        
    with col2:
        st.subheader('Nutritional Value per 100 grams')
        cols = ['Energy (Kcal)', 'Total Fat (g)', 'Carbohydrates (g)', 'Total Sugar (g)',
                'Protein (g)', 'Cholestrol (mg)', 'Calcium (mg)', 'Sodium (mg)']
        gelato_composition_df = gelato_df.loc['Total', cols].to_frame(name='Value')
        gelato_composition_df['Value'] = gelato_composition_df['Value']/total_weight * 100
        st.dataframe(gelato_composition_df, use_container_width = True)
        
    with col3:
        st.subheader(f'**Total cost - INR {np.round(total_cost)}**')
        st.subheader(f'**Unit cost - INR {np.round(total_cost/total_weight, 2)}**')