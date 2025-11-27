import streamlit as st
from findCd import getCdA

st.set_page_config(page_title="Find CdA", page_icon="📈")

# ==========================
#   Custom minimal CSS
# ==========================
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

# ==========================
#   Title
# ==========================
st.markdown("<div class='main-title'>📈 โปรแกรประมาณผลคูณสัมประสิทธิ์แรงต้านอากาศกับพื้นที่หน้าตัดของวัตถุ</div>", unsafe_allow_html=True)


st.markdown("""<div class = 'sub-title'>โปรแกรมนี้เป็นโปรแกรมที่จัดทำขึ้นเพื่อศึกษาการประมาณค่าผลคูณสัมประสิทธิ์แรงต้านอากาศกับพื้นที่หน้าตัดของวัตถุ 
            โดยใช้วิธีการแบ่งครึ่ง จัดทำโดยนักเรียน จากโรงเรียนสระบุรีวิทยาคม</div>""", unsafe_allow_html=True)

# ==========================
#   Sidebar (Settings)
# ==========================
st.sidebar.title("⚙️ ตั้งค่าเชิงลึก")
g = st.sidebar.number_input("แรงโน้มถ่วง (m/s²)", value=9.81)
p = st.sidebar.number_input("ความหนาแน่นของอากาศ kg/m³", value=1.2)
c = st.sidebar.number_input("ช่องว่างเวลาในการคำนวณ (s)", value=0.1, step=0.001, format="%0.5f")
cdA_init = st.sidebar.number_input("ค่า CdA เริ่มต้น", value=0.0)
error_rate = st.sidebar.number_input("ค่าความผิดพลาดที่ยอมรับได้", value=0.01, format="%0.5f", step=0.0001)
max_iter = st.sidebar.number_input("จำนวนรอบมากที่สุด", value=50)
max_cdA = st.sidebar.number_input("ค่า CdA สูงสุดที่อนุญาต", value=100.0)

# ==========================
#   Input section (main)
# ==========================
st.markdown("### 🔢 กรอกข้อมูลการทดลอง")


with st.form("grades_form"):    
    mass = st.number_input("มวลของวัตถุ (g)", min_value=0.0)
    height = st.number_input("ความสูงที่ตก (m)", min_value=0.0)
    time_test = st.number_input("เวลาที่ทดลองได้ (s)", min_value=0.0)

    st.markdown("---")
    submit_button = st.form_submit_button(label="🚀 เริ่มการคำนวณ")

# ==========================
#   Calculate Button
# ==========================

if submit_button:
    st.header("📉 ผลการคำนวณ CdA")
    
    if height <= 0 or time_test <= 0 or mass <= 0:
        st.error("ตรวจพบค่าที่เป็นศูนย์หรือค่าน้อยกว่า 0 โปรดตรวจสอบข้อมูลอีกครั้ง")
    else:
        try:
            cd_output, cd_plot = getCdA(g, p, c, cdA_init, time_test, height, mass, error_rate, max_iter, max_cdA)
        except Exception as e:
            st.error("ไม่สามารถคำนวณได้ กรุณาตรวจสอบข้อมูลหรือลองลด error rate")
            st.text(f"รายละเอียดเพิ่มเติม: {e}")
        else:
            # card style
            st.markdown(f"""
            <div style="font-size: 16px">
                <h3>ผลลัพธ์ที่คำนวณได้</h3>
                <p><b>ค่า CdA:</b> {cd_output}</p>
            </div>
            """, unsafe_allow_html=True)

            st.line_chart(cd_plot["Cd"], x_label="CdA", y_label="Iteration")
            
