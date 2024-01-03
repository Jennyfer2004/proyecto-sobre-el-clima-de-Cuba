import streamlit as st 
import pandas as pd
import sys
import os
ruta = os.getcwd()
ruta = ruta.replace("\\", "/")
sys.path.append(f'{ruta}' + '/Análisis Multivariado')
import mvLogic

st.title("Análisis Multivariado")

df = pd.read_csv("./data/base_datos.csv")
df = df.loc[:, ["Estación", "Año", "Mes", "Temperatura max med", "Temperatura min med", "Temperatura med", "Humedad Relat", "Precipitaciones",
        "Nombres Estaciónes", "Latitud", "Longitud", "Región", "Provincias"]]

df = df.rename(columns={"Temperatura max med": "Temperatura Máxima Media", "Temperatura min med": "Temperatura Minima Media", "Temperatura med": "Temperatura Media", "Humedad Relat": "Humedad Relativa",
        "Nombres Estaciónes": "Nombre de Estación"})

df_Occidente = df.loc[df['Región'] == 'Occidente']
df_Centro = df.loc[df['Región'] == 'Centro']
df_Oriente = df.loc[df['Región'] == 'Oriente']

df_Pdr = df.loc[df['Provincias'] == 'Pinar del Río'] 
df_Art = df.loc[df['Provincias'] == 'Artemisa']
df_Hab = df.loc[df['Provincias'] == 'La Habana']
df_May = df.loc[df['Provincias'] == 'Mayabeque']
df_Mat = df.loc[df['Provincias'] == 'Matanzas']
df_Vcl = df.loc[df['Provincias'] == 'Villa Clara']
df_Cfg = df.loc[df['Provincias'] == 'Cienfuegos']
df_Ssp = df.loc[df['Provincias'] == 'Sancti Spíritus'] 
df_Cav = df.loc[df['Provincias'] == 'Ciego de Ávila']
df_Cam = df.loc[df['Provincias'] == 'Camagüey']
df_Ltu = df.loc[df['Provincias'] == 'Las Tunas']
df_Hol = df.loc[df['Provincias'] == 'Holguín']
df_Gra = df.loc[df['Provincias'] == 'Granma']
df_Sdc = df.loc[df['Provincias'] == 'Santiago de Cuba']
df_Gua = df.loc[df['Provincias'] == 'Guantánamo']

st.markdown("## Seleccione la región en la que quiere explorar datos")

opciónes = ['General', 'Occidente', 'Centro', 'Oriente']
selección = st.selectbox('Selecciona una Región:', opciónes)

######################################################################################################################################################################################
#Análisis Multivariado General
######################################################################################################################################################################################

if selección == "General":
    
        st.markdown("### Coeficiente de Correlación entre las variables")
        df_corr = df[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        st.markdown("### Gráficos de Dispersión")
        mvLogic.ScatLogic(df)

        st.markdown("### Gráficos de Regresión Lineal")
        mvLogic.RegLogic(df)


###########################################################################################################################################################################
#Análisis Multivariado Occidente
############################################################################################################################################################################
    
if selección == "Occidente":

        opciónes = ['General', 'Pinar del Río', 'Artemisa', 'La Habana', 'Mayabeque', 'Matanzas']
        selección = st.selectbox('Selecciona una Provincia:', opciónes)

        

################################################
#GENERAL
################################################
        if selección == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Occidente[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Occidente)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Occidente)


###############################################
#PINAR DEL Río
###############################################

        elif selección == 'Pinar del Río':    

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Pdr[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Pdr)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Pdr)

###############################################
#ARTEMISA
###############################################

        elif selección == 'Artemisa':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Art[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Art)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Art)

###############################################
#La HABANA
###############################################

        elif selección == 'La Habana':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Hab[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Hab)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Hab)

###############################################
#MAYABEQUE
###############################################

        elif selección == 'Mayabeque':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_May[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_May)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_May)

###############################################
#MATANZAS
###############################################

        elif selección == 'Matanzas':

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Mat[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Mat)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Mat)


##################################################################################################################################
#Análisis Multivariado Centro
##################################################################################################################################
    
if selección == "Centro":

        opciónes = ['General', 'Villa Clara', 'Cienfuegos', 'Sancti Spíritus', 'Ciego de Ávila', 'Camagüey']
        selección = st.selectbox('Selecciona una Provincia:', opciónes)

        
################################################
#GENERAL
################################################
        if selección == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Centro[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Centro)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Centro)

################################################
#Villa Clara
################################################
        if selección == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Vcl[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Vcl)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Vcl)

################################################
#CIENFUEGOS
################################################
        if selección == 'Cienfuegos':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Cfg[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Cfg)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Cfg)


################################################
#SANCTI SPS
################################################
        if selección == 'Sancti Spíritus':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Ssp[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Ssp)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Ssp)

################################################
#CIEGO DE ÁviLA
################################################
        if selección == 'Ciego de Ávila':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Cav[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Cav)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Cav)

################################################
#Camagüey
################################################
                
        if selección == 'Camagüey':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Cam[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Cam)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Cam)



##################################################################################################################################
#Análisis Multivariado Oriente
##################################################################################################################################
    
if selección == "Oriente":

        opciónes = ['General', 'Las Tunas', 'Granma', 'Holguín', 'Santiago de Cuba', 'Guantánamo']
        selección = st.selectbox('Selecciona una Provincia:', opciónes)

        

################################################
#GENERAL
################################################
        if selección == 'General':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Occidente[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Occidente)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Occidente)

################################################
#LAS TUNAS
################################################
        if selección == 'Las Tunas':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Ltu[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Ltu)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Ltu)

################################################
#Holguín
################################################
        if selección == 'Holguín':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Hol[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Hol)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Hol)

################################################
#GRANMA
################################################
        if selección == 'Granma':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Gra[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Gra)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Gra)

################################################
#SANTIAGO DE CUBA
################################################
        if selección == 'Santiago de Cuba':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Sdc[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Sdc)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Sdc)

################################################
#GUANtánamO
################################################
        if selección == 'Guantánamo':      

                st.markdown("### Coeficiente de Correlación entre las variables")
                df_corr = df_Gua[["Temperatura Media", "Temperatura Máxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
                st.write(df_corr.corr()) 

                st.markdown("### Gráficos de Dispersión")
                mvLogic.ScatLogic(df_Gua)

                st.markdown("### Gráficos de Regresión Lineal")
                mvLogic.RegLogic(df_Gua)
