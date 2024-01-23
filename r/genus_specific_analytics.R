library(RPostgres)

# Establish a connection using RPostgres
con <- dbConnect(
  RPostgres::Postgres(),
  dbname = "BA_Project",
  user = "postgres",
  password = "password",
  host = "localhost",
  port = 5432
)
# Query statement in the database
sql_query <- "SELECT * FROM animals"
dataAnimals <- dbGetQuery(con, sql_query)
# Count all animals
num_all_animals <- nrow(dataAnimals)
# Filter data in dataAnimals by genus
filter_genus <- dataAnimals[dataAnimals$genus_id == idGenus,]

# Check if no data is available
tryCatch({
  max_age_value <- max(filter_genus$estimated_age)
},error = function(e) {
  cat("No data to calculate maxAge", conditionMessage(e), "\n")
})

calculate_numberAnimalsGenus <- function() {
  # Count rows in filter_genus
  num_animals <- nrow(filter_genus)

  return(num_animals)
}

# Call function
numberAnimalsOfGenus <- calculate_numberAnimalsGenus()

# Calculate percentage of specific animal
percentage_of_animal <- round((numberAnimalsOfGenus / num_all_animals) * 100, 2)

# Safe data in RDS-File
saveRDS(list(numberAllAninmals = num_all_animals, numberAnimalsGenus = numberAnimalsOfGenus, highestAnimalAge = max_age_value, percent = percentage_of_animal), file = "r/genus_specific.RDS")
