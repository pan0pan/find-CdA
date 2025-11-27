from math import sqrt
import numpy as np
import pandas as pd

class Find_Time_And_CdA:

    # set base variable
    def __init__(self, g, p, c):
        self.GRAVITY = g  # m/s^2
        self.P = p  # kg/m^3 (air density)
        self.CAL_TIME = c  # time step


    # Find air resistance
    # this is a function for finding air resistance
    # this is Equation Fd = (0.5) * (v^2) * (Cd) * (A) * (P)
    # When Fd = Drag Force, v = object velocity, A = area , Cd = Drag Coefficient, p = 
    def FindDragForce(self, V, CdA, A):
        if A <= 0:
            return 0.5 * self.P * CdA * (V ** 2)
        return 0.5 * self.P * CdA * A * (V ** 2)

    #Find Acceleration 
    # from sum(F) = ma
    #      mg - Fd = ma
    #         a = (mg - Fd) / m
    def FindAcceleration(self,mass_kg, DragForce ):
        return ((mass_kg * self.GRAVITY) - DragForce) / mass_kg




    # this is function we use to find time before Terminal(Acceleration > 0)
    # -- return time, remaining Height, time left, acceleration, velocity
    def FindTimeBeforeTerminal(self,Height, mass_kg, CdA,Arae=0):
 
        # Set start variable
        velocity = [0]
        acceleration = [self.GRAVITY]
        time = [0]

        velocity_now = 0.0
        time_now = 0.0

        # Cd * a = 0 
        if CdA == 0.0:
            #from F = (0.5) * (v^2) * (Cd) * (A)
            #     F = (0.5) * (v^2) * (0) * (A)
            #     F = 0
            
            #from sum(F) = ma
            #     mg - F = ma
            #     mg - 0 = ma
            #          g = a
            
            #from S = ut + 0.5a(t^2)
            #     u = 0
            #     S = o(t) + 0.5a(t^2)  
            #     S = 0.5a(t^2)
            #     2S/a = t^2
            #         t = sqrt(2S/a)

            total_time = sqrt(2 * Height / self.GRAVITY)
            return total_time, 0.0, [0, total_time], [self.GRAVITY, self.GRAVITY], [0, self.GRAVITY * total_time]

        while True:
            Fd = self.FindDragForce(V = velocity_now, CdA= CdA, A = Arae)
            acc = self.FindAcceleration(mass_kg = mass_kg, DragForce=Fd)

            if abs(acc) < 1e-5:
                break

            velocity_now += acc * self.CAL_TIME
            time_now += self.CAL_TIME
            Height -= velocity_now * self.CAL_TIME

            time.append(time_now)
            acceleration.append(acc)
            velocity.append(velocity_now)

            if Height <= 0:
                h = 0
                break

        return time_now, Height, time, acceleration, velocity

     # this is function we use to find time after Terminal(Acceleration = 0)
     # we can use s = vt because a = 0
    def FindTimeAfterTerminal(self,Height, terminal_velocity):
        return Height / terminal_velocity

    # this is a function we use find all time that object use (before + after terminal)
    def FineAllTime(self,Height, mass_kg,  Cd, Area = 0):
        
        t1, remaining_Height, time, acceleration, velocity = \
            self. FindTimeBeforeTerminal(Height = Height, mass_kg = mass_kg, CdA = Cd,Arae=Area)
        t2 = self.FindTimeAfterTerminal(Height= remaining_Height, terminal_velocity= velocity[-1])
        
        # make a dataframe 
        df_acceleration_time = pd.DataFrame({'Acceleration (m/s²)': acceleration, 'Time (s)': time})
        df_velocity_time = pd.DataFrame({'Velocity (m/s)': velocity, 'Time (s)': time})

        # show 
        print(df_velocity_time)
        print(df_acceleration_time)
        return t1 + t2, df_acceleration_time, df_velocity_time


    # this is a function to find a Cd(A) 
    def FindCdA(self,CdA_init, TimeTest, Height, mass_kg, error_rate=0.01, max_iter=50, cdA_max_limit=100.0):

        cd_out = 0
        history = []

        try:
            time_freefall, _, _ = self.FineAllTime(Height=Height,mass_kg=mass_kg,Cd=CdA_init)
        except Exception as e:
            # กรณี find_time ขึ้น error เมื่อ C_dA=0 (ไม่คาดหวัง)
            # ก็ควร restore และ raise ต่อ
            cd_out = 0
            raise RuntimeError(f"Error computing free-fall time: {e}")

        if TimeTest < time_freefall:
            # ไม่สามารถหา C_dA ใดทำให้เวลาสั้นกว่า free-fall
            cd_out = CdA_init
            raise ValueError(
                f"time_test ({TimeTest:.3f}s) น้อยกว่า free-fall time ({time_freefall:.3f}s); no solution for C_d >= 0.")
        if abs(TimeTest - time_freefall) <= error_rate:
            # time_test ≈ free-fall => C_dA ≈ 0
            cd_out = 0.0
            return 0.0 , pd.DataFrame({'Cd': history, 'Iteration': list(range(len(history)))})

        cd_low = -1
        cdA_hi = 1

        for i in range(max_iter):
            cd_out = cdA_hi
            t_hi, _, _ = self.FineAllTime(Height=Height,mass_kg=mass_kg,Cd=cd_out)
            print(t_hi)
            if t_hi < TimeTest:
                # ยังต้องเพิ่ม C_dA
                cdA_hi *= 2
            else:
                # เจอขอบบน
                break

        cd_out = cdA_hi
        history.append(cd_low)
        history.append(cdA_hi)
        t_hi, _, _ = self.FineAllTime(Height=Height,mass_kg=mass_kg,Cd=cd_out)
        if t_hi < TimeTest:
            # แม้ cdA_hi = cdA_max_limit แล้ว เวลาก็ยังสั้นกว่า time_test
            # แสดงว่า C_dA ต้อง > cdA_max_limit หรือ data มีปัญหา
            cd_out = CdA_init
            raise ValueError(
                f"ไม่พบ upper bound สำหรับ C_dA ภายใน limit={cdA_max_limit}. t_hi ({t_hi:.3f}s) < time_test ({TimeTest:.3f}s).")
        # ถ้ามี t_hi >= time_test ก็ใช้ cdA_hi และ cdA_lo=0

        # 3. Bisection
        cdA_lo = 0.0
        # cdA_hi ได้มาจากข้างบน
        cdA_low = cdA_lo
        cdA_high = cdA_hi
        cdA_mid = None
        for i in range(max_iter):
            cdA_mid = 0.5 * (cdA_low + cdA_high)
            cd_out = cdA_mid
            t_mid, _, _ = self.FineAllTime(Height=Height,mass_kg=mass_kg,Cd=cd_out)
            diff = t_mid - TimeTest
            # ถ้าอยู่ใน tolerance
            if abs(diff) <= error_rate:
                # เจอคำตอบ
                cd_out = cdA_mid
                df_cd = pd.DataFrame({'Cd': history, 'Iteration': list(range(len(history)))})
                return cd_out, df_cd
            # ตัดช่วง
            if t_mid < TimeTest:
                # drag ยังน้อยไป ต้องเพิ่ม C_dA
                cdA_low = cdA_mid
            else:
                # drag มากไป ต้องลด C_dA
                cdA_high = cdA_mid
            history.append(cdA_mid)

        df_cd = pd.DataFrame({'Cd': history, 'Iteration': list(range(len(history)))})
        return cdA_mid, df_cd






#-----------------------------------
def getTime(g,p,c,Height, mass_kg, Cd,Area):
    offset = Find_Time_And_CdA(g,p,c)
    return  offset.FineAllTime(Height= Height, mass_kg= mass_kg,Cd =Cd, Area = Area)

def getCdA(g,p,c,CdA_init, TimeTest, Height, mass_kg, error_rate=0.01, max_iter=50, cdA_max_limit=100.0):
    offset = Find_Time_And_CdA(g,p,c)
    return  offset.FindCdA(CdA_init =CdA_init, TimeTest =TimeTest, Height =Height, mass_kg= mass_kg, error_rate=error_rate, max_iter=max_iter, cdA_max_limit=cdA_max_limit)
