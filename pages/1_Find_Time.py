import streamlit as st
import time
import numpy as np
import pandas as pd
from findCd import getCdA, getTime
#  getTime(g,p,c,Height, mass_kg, Cd,Area):
# getCdA(g,p,c,CdA_init, TimeTest, Height, mass_kg, error_rate=0.01, max_iter=50, cdA_max_limit=100.0):


st.set_page_config(page_title="Find Time", page_icon="📈")

st.markdown("""
<style>
    .main-title {
            font-size: 36px;
            font-weight: 700;
            border: 2px solid #85140c;
            padding: 12px 18px;
            border-radius: 20px;
            margin-bottom: 10px;
        }

        .sub-title {
            font-size: 16px;
            
            margin-top: 10px;
            margin-bottom: 10px;
            border-bottom: 2px solid #85140c;
            }
        .line{
            border-bottom: 2px solid #85140c;
            }
</style>
""", unsafe_allow_html=True)



st.markdown("<div class='main-title'>📈 โปรแกรมคำนวณหาค่าระยะเวลาในการตก</div>", unsafe_allow_html=True)
st.markdown(
    """<div class = 'sub-title'> โปรแกรมนี้เป็นโปรแกรมที่จัดทำขึ้นเพื่อ ประยุกต์ใช้คณิตศาตร์ในการหาค่าระยะเวลาในการตก
    โดยคิดแรงต้านอากาศร่วมด้วย </div>""" ,unsafe_allow_html=True)

#side bar

st.sidebar.header("ตั่งค่าเชิงลึก setting")
g = st.sidebar.number_input("แรงโน้มถ่วง (m/s²)",value=9.81)
p = st.sidebar.number_input("แรงดันอากาศโดยเฉลี่ย ณ พื้นที่นั้น kg/m³" , value= 1.2)
c = st.sidebar.number_input("ช่องว่างเวลาในการคำนวณ (s)", value = 0.01)


with st.form("grades_form"): 
    mass = st.number_input("มวลของวัตถุ(g)")
    height = st.number_input("ความสูง(m)")
    Cd = st.number_input("ค่าสัมประสิทธิ์แรงต้านอากาศ")
    Area = st.number_input("พื้นที่หน้าตัดของวัตถุ (m)")
    st.markdown("---")
    submit_button = st.form_submit_button(label="🚀 เริ่มการคำนวณ")

if  submit_button:
    st.header("ผลการหาเวลา")
   
    if height <=0 or Cd <= 0 or mass <= 0 or Area <=0:
        
        st.error(f"ไม่สามารถคำนวณได้โปรตัวสอบว่า มีค่าใดเป็น 0 หรือไม่")
    else :    
        try :
            time_output, acc_plot, vel_plot = getTime(g,p,c,height, mass, Cd,Area)
        except:
            st.error(f"ไม่สามารถคำนวณได้โปรตัวสอบว่าใส่ค่าถูกต้องหรือไม่")
        else:
            acc_vel_df = pd.DataFrame(data={"ความเร่ง,Acceleration (m/s²)" : acc_plot["Acceleration (m/s²)"],"อัตราเร้ว,Velocity (m/s)" :vel_plot["Velocity (m/s)"]})
            st.write(f"ระยะเวลาที่คำนวณได้คือ {time_output}")
            st.line_chart(acc_vel_df, x_label= "เวลา(s)")



