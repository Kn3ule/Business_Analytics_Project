library(RPostgres)

# Establish a connection using RPostgres
con <- dbConnect(
  RPostgres::Postgres(),
  dbname = "Business_Analytics_Project",
  user = "postgres",
  password = "",
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

#max_age_value <- max(filter_genus$estimated_age)

tryCatch({
  max_age_value <- max(filter_genus$estimated_age)
},error = function(e) {
  # Hier können Sie den Fehler behandeln oder eine Meldung ausgeben
  cat("No data to calculate maxAge", conditionMessage(e), "\n")
})

calculate_numberAnimalsGenus <- function() {
  # Count rows in filter_genus
  num_animals <- nrow(filter_genus)

  # Return value rows
  return(num_animals)
}
numberAnimalsOfGenus <- calculate_numberAnimalsGenus()

percentage_of_animal <- round((numberAnimalsOfGenus / num_all_animals) * 100, 2)

saveRDS(list(numberAllAninmals = num_all_animals, numberAnimalsGenus = numberAnimalsOfGenus, highestAnimalAge = max_age_value, percent = percentage_of_animal), file = "genus_specific.RDS")