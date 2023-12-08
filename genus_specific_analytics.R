# install just one time
#options(repos = c(CRAN = "https://packagemanager.rstudio.com/all/latest"))
#install.packages("RPostgreSQL", lib="C:/Users/Moritz/AppData/Local/R/win-library/4.3")
library(RPostgreSQL)

# Database connection
con <- dbConnect(PostgreSQL(),
                 dbname = "Business_Analytics_Project",
                 user = "postgres",
                 password = "",
                 host = "localhost",
                 port = 5432)

# Query statement in the database
sql_query <- "SELECT * FROM animals"
dataAnimals <- dbGetQuery(con, sql_query)
# Count all animals
num_all_animals <- nrow(dataAnimals)
# Filter data in dataAnimals by genus
filter_genus <- dataAnimals[dataAnimals$genus_id == idGenus,]

calculate_numberAnimalsGenus <- function() {
  # Count rows in filter_genus
  num_animals <- nrow(filter_genus)

  # Return value rows
  return(num_animals)
}

calculate_averageAgeGenus <- function() {
  # Calculate average age with relvant data
  averageAge <- mean(filter_genus$estimated_age)

  # Return value of averageAge
  return(round(averageAge, digits = 2))
}

calculate_averageWeightGenus <- function() {
  # Calculate average weight with relvant data
  averageWeight <- mean(filter_genus$estimated_weight)

  # Return value of averageWeight
  return(round(averageWeight, digits = 2))
}

calculate_averageSizeGenus <- function() {
  # Calculate average size with relvant data
  averageSize <- mean(filter_genus$estimated_size)

  # Return value of averageSize
  return(round(averageSize, digits = 2))
}

calculate_medianAgeGenus <- function() {
  # Calculate median age with relvant data
  medianAge <- median(filter_genus$estimated_age)

  # Return value of median
  return(medianAge)
}

# Call functions
numberAnimalsOfGenus <- calculate_numberAnimalsGenus()
averageAgeGenus_result <- calculate_averageAgeGenus()
averageWeightGenus_result <- calculate_averageWeightGenus()
averageSizGenus_result <- calculate_averageSizeGenus()
medianAgeGenus_result <- calculate_medianAgeGenus()

standard_deviation_age <- round(sd(filter_genus$estimated_age), digits = 2)
standard_deviation_weight <- round(sd(filter_genus$estimated_weight), digits = 2)
standard_deviation_size <- round(sd(filter_genus$estimated_size), digits = 2)


# Safe results in RDS-File
saveRDS(list(numberAninmalsOfGenus = numberAnimalsOfGenus, numberOfAllAnimals = num_all_animals ,averageAgeGenus = averageAgeGenus_result, standardDeviationAge = standard_deviation_age, averageWeightGenus = averageWeightGenus_result, standardDeviationWeight = standard_deviation_weight, averageSizeGenus = averageSizGenus_result, standardDeviationSize = standard_deviation_size , medianAgeGenus = medianAgeGenus_result), file = "variables.RDS")
