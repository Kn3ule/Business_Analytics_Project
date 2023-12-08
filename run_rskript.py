import rpy2.robjects as robjects
import pandas as pd
from sqlalchemy import create_engine


# Initialize an R session
r = robjects.r

# Create Python variables - (dynamic ID of genus)
x_value = 1

# Pass Python variables to R
r.assign('idGenus', x_value)

# Run the entire R script
r.source("genus_specific_analytics.R")

# Read RDS-File
r_variables = robjects.r['readRDS']("variables.RDS")

# Print RDS-Variables
print("---------")
print("")
print(r_variables)
print("")
print("---------")

ergebnis = r['*'](100, (r['/'](r_variables[0], r_variables[1])))
print(ergebnis)

"""
database_url = 'postgresql://postgres:@localhost:5432/Business_Analytics_Project'

engine = create_engine(database_url)
genus_query = 'SELECT species_name FROM genus WHERE id = int(x_value)'

dfGenus = pd.read_sql(genus_query, engine)
print(dfGenus)
"""