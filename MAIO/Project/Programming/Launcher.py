# ------------------------------------------------------
# Choosing stations
# ------------------------------------------------------

which_CTD=9
which_SCAMP=22

# ------------------------------------------------------
# Defining parameters
# ------------------------------------------------------

Parameter_initial={
    'which_CTD':which_CTD,
    'which_SCAMP':which_SCAMP
    }
To_compare='temp'

# ------------------------------------------------------
# Run Class_Reading_Data
# ------------------------------------------------------

data_c=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data_c.GetCTDData()

data_s=ReadData(Parameter_initial,comparison=To_compare,initialvalue=0)
data_s.GetScampData()