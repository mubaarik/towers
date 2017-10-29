#GPS bounds for Rwanda
rwandan_bounds = [(-1.968389,28.727301),(-3.023214,29.587479),(-0.983030,30.340597),(-2.344680,30.905435)]

#GPS bounds of the TopFlight testing area
top_flight_area = [(41.532874, -70.832963),(42.072878, -70.653182),(42.061101, -69.992220),(41.505160, -69.907617)]

#Bound by geographical coordinates 
def bound(df, lat_l=41.505160,lat_h=42.072878,lon_l=-70.832963,lon_h=-69.907617):
    return df[(df.lat>lat_l)&(df.lat<lat_h)&(df.lon>lon_l)&(df.lon<lon_h)]