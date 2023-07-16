# print(int("100",2))
l_set_spd = 100
r_set_spd = 100

wad = 0

s = "0"
for i in range(2):
    for j in range(8):
        l_out_spd = 0
        r_out_spd = 0
        wad = j
        s = i
        if(s&1):
            wad = int(wad,2)
            wad = '{0:03b}'.format(wad ^ 0b011)
        if(wad&0b111)|(wad&0b100): #forward
            l_out_spd = l_set_spd
            r_out_spd = r_set_spd
        elif(wad&0b110):# <- ^
            l_out_spd = l_set_spd
            r_out_spd = r_set_spd / 2
        elif(wad&0b010):# <- 
            l_out_spd = l_set_spd
            r_out_spd = 0
        elif(wad&0b101):# ^ ->
            l_out_spd = l_set_spd / 2
            r_out_spd = r_set_spd 
        elif(wad&0b001):# ->
            l_out_spd = 0
            r_out_spd = r_set_spd
        else:           # brake
            l_out_spd = 0
            r_out_spd = 0
            
        print(j,": ",bin(wad))
        print("L: ",l_out_spd,"R: ",r_out_spd)
        print("\n")