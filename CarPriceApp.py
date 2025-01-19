# -*- coding: utf-8 -*-
"""
Created on Mon May 16 15:19:05 2022

@author: T430s
"""
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from PIL import Image
from streamlit_option_menu import option_menu

st.write("""
#### CarPrice and Gas Mileage Prediction and Analysis App
--by A. Maharjan 
""")
image = Image.open('car.jpg')
st.image(image)


selected = option_menu(
    menu_title= None,
    options= ["Car Gas Mileage and Price Prediction","Analytics"],
    menu_icon = "cast",
    #default_index = 0,
    orientation= "horizontal",
    styles = {
        "nav-link":{"font-size":"14px","text-align":"center"},
        "nav-link-selected": {"background-color":"green"}
        }
    
    )



# for units
def units(u):
    if u=='Price':
        return('Price($)')
    elif u=='MPG_City':
        return('MPG_CIty(miles/gallon)')
    elif u=='MPG_Highway':
        return('MPG_Highway(miles/gallon)')
    elif u=='Horsepower':
        return('Horsepower(HP)')
    elif u=='Cylinders':
        return('Cylinders (no. of Cylinders)')
    elif u=='EngineSize':
       return('EngineSize(Cubic Inch)')
    elif u=='Weight':
       return('Weight(lbs)')
    elif u=='Wheelbase':
       return('Wheelbase(Inches)')
    elif u=='Length':
       return('Length(Inches)')
   
   
    
   
    
   
if selected == "Car Gas Mileage and Price Prediction":
    st.write('(Choose the variables from the left side bar)')
    # loading the saved model for Home Price(random forest model was used)
    df_car = pickle.load(open('df_car','rb'))
    model_carprice = pickle.load(open('Model_CarPrice','rb'))
    model_mpg_city = pickle.load(open('Model_MPG_City','rb'))
    model_mpg_highway = pickle.load(open('Model_MPG_Highway','rb'))

    
    #st.write('---')

    # Sidebar
    # Header of Specify Input Parameters
    st.sidebar.header('Specify Input Parameters')

    #def user_input_features():
    Make = np.append(' ', df_car['Make'].unique())
    Make = st.sidebar.selectbox('Make', Make)
    

    model = df_car[df_car['Make'] == Make]['Model'] # selecting the Model based off the Make
    Model = st.sidebar.selectbox('Model', model.unique())

    Type_Make = df_car[df_car['Model'] == Model]['Type'] # selecting the Model based off the Make
    Type = st.sidebar.selectbox('Type', Type_Make.unique())

    origin = df_car[df_car['Make'] == Make]['Origin'] # selecting the Model based off the Make
    Origin = st.sidebar.selectbox('Origin', origin.unique())

    DriveTrain = st.sidebar.selectbox('DriveTrain', df_car['DriveTrain'].unique())

    EngineSize = st.sidebar.slider('EngineSize (Liters)',df_car['EngineSize'].min(),df_car['EngineSize'].max(),df_car['EngineSize'].mean(),0.2)
    Cylinders = st.sidebar.slider('No. of Cylinders',df_car['Cylinders'].min(),df_car['Cylinders'].max(),4.0,1.0)
    Horsepower = st.sidebar.slider('Horsepower (HP)',df_car['Horsepower'].min(),df_car['Horsepower'].max(),df_car['Horsepower'].mean(),5.0)
    Weight = st.sidebar.slider('Weight (lbs)',df_car['Weight'].min(),df_car['Weight'].max(),df_car['Weight'].mean(),10.0)
    Wheelbase = st.sidebar.slider('Wheelbase (inch)',df_car['Wheelbase'].min(),df_car['Wheelbase'].max(),df_car['Wheelbase'].mean(),1.0)
    Length = st.sidebar.slider('Length (inch)',df_car['Length'].min(),df_car['Length'].max(),df_car['Length'].mean(),10.0)

    # dataframe for model prediction
    X_new = pd.DataFrame([[Make,Model,Type,Origin,DriveTrain,EngineSize,Cylinders,Horsepower,Weight,Wheelbase,Length]],
                         columns=['Make', 'Model', 'Type', 'Origin', 'DriveTrain', 
                                'EngineSize', 'Cylinders', 'Horsepower','Weight', 'Wheelbase', 'Length'])



    # Main Panel
    # Apply Model to Make Prediction
    prediction_price = model_carprice.predict(X_new)
    prediction_MPG_City = model_mpg_city.predict(X_new)
    prediction_MPG_Highway = model_mpg_highway.predict(X_new)   


    # results output
    st.write('-Estimated Car Price is: $ ','  ','%.2f' %prediction_price)
    st.write('-Estimated City Gas Mileage is:','  ','%.2f' %prediction_MPG_City, ' MPG')
    st.write('-Estimated Highway Gas Mileage is:','  ','%.2f' %prediction_MPG_Highway, ' MPG')


    

     
       


# analytics
if selected == "Analytics":
    df_car = pickle.load(open('df_car','rb'))

    st.write("""
    #### Histograms
    """)
    option = st.selectbox('choose to compare',(' ','Origin','DriveTrain'))
    out = st.selectbox('select',(' ','EngineSize', 'Cylinders', 'Horsepower','Price','MPG_City', 'MPG_Highway','Weight', 'Wheelbase', 'Length'))

    if st.button('Press for the histogram'):
        fig,ax = plt.subplots()
        sns.histplot(data = df_car,x=out,hue=option)
        #plt.show() # does not really need this for st pyplot
        plt.title('Histogram of'+' '+ units(out))
        st.pyplot(fig)
    st.write("-----")





    # scatterplots
    st.write("""
    #### Check Relationships
    """)

    X = st.selectbox('X',(' ','EngineSize', 'Cylinders', 'Horsepower','Price','MPG_City', 'MPG_Highway','Weight', 'Wheelbase', 'Length'))
    Y = st.selectbox('Y',(' ','EngineSize', 'Cylinders', 'Horsepower','Price','MPG_City', 'MPG_Highway','Weight', 'Wheelbase', 'Length'))
    options = st.selectbox('choose to compare with',(' ','Origin','DriveTrain'))
    if st.button('Press to see the relationship'):
        fig,ax = plt.subplots()
        sns.scatterplot(data = df_car,x = X,y = Y,hue = options)
        plt.xlabel(units(X))
        plt.ylabel(units(Y))
        st.pyplot(fig)



    # barplots
    st.write("""
    #### Barplots
    """)
    #option = st.selectbox('choose to compare',('Origin','DriveTrain'))
    out_barplot = st.selectbox('Choose for the barplot',(' ','Price','EngineSize', 'Cylinders', 'Horsepower','MPG_City', 'MPG_Highway','Weight', 'Wheelbase', 'Length'))
    option2 = st.selectbox('choose to compare with',(' ','Make','Origin','DriveTrain'))
    if st.button('Press for the BarPlot'):
        fig,ax = plt.subplots()
        sns.barplot(df_car, x = option2, y = out_barplot) # y is the nemerical value of the mean for the bar plot
        plt.ylabel(units(out_barplot))
        plt.xticks(rotation=90) # makes the x axis names vertical
        plt.tight_layout() # expands more horizotally
       
        st.pyplot(fig)

    st.write("-----")



    # pairplot
    #st.write("""
    #### PairPlot. May take few seconds
    #""")
    #if st.button('Press for PairPlot'):
        #option = st.selectbox('compare for pairplot',('Origin','DriveTrain'))
        #df_car['MPG Average'] = (df_car['MPG_City']+df_car['MPG_Highway'])/2
        #df_car_pairplot = df_car[['Origin','DriveTrain','EngineSize', 'Cylinders', 'Horsepower','Invoice','MPG Average']]

        #fig,ax = plt.subplots()

        #pairplot = sns.pairplot(data = df_car_pairplot,hue=option,diag_kind='hist', height=3, aspect=1.2)
        #plt.show()
        #st.pyplot(pairplot.fig) # pairplot needs this syntax to work, got from chatgpt
        
        







