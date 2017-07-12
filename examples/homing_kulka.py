            distance = (output['xpos']**2 + output['ypos']**2)**0.5
            if distance >= max_distance:
                print("Outside limit, homing")
                homing = True
            if homing == True:
                direction = (180 + int(np.arctan(output['ypos']/output['xpos']) * np.pi/180)) % 360
                if distance < 10:
                    print("In range of home, resuming exploration")
                    homing == False