# Install Hmisc only if it is not already installed
if (!requireNamespace("Hmisc", quietly = TRUE)) {
  install.packages("Hmisc")
}

library(Hmisc)


# Read the input CSV file
# The first column is assumed to contain sample identifiers
data <- read.csv(
  "Book13.csv",
  header = TRUE,
  check.names = FALSE,
  na.strings = c("", "NA")
)


# Exclude the first column and retain variables for correlation analysis
analysis_data <- data[, -1, drop = FALSE]


# Convert all variables to numeric format
analysis_data[] <- lapply(
  analysis_data,
  function(x) suppressWarnings(as.numeric(as.character(x)))
)


# Remove columns containing only missing values
analysis_data <- analysis_data[
  vapply(analysis_data, function(x) any(!is.na(x)), logical(1))
]


# Confirm that sufficient data are available for correlation analysis
if (ncol(analysis_data) < 2) {
  stop("At least two numeric variables are required.")
}

if (nrow(analysis_data) < 5) {
  stop("At least five observations are required for Hmisc::rcorr().")
}


# Convert the data frame to a numeric matrix
data_matrix <- as.matrix(analysis_data)


# Calculate Pearson correlation coefficients and corresponding P values
# Missing values are handled using pairwise complete observations
correlation <- rcorr(
  data_matrix,
  type = "pearson"
)


# Display the correlation coefficient matrix
print(correlation$r)


# Display the P-value matrix
print(correlation$P)


# Display the number of observations used for each correlation
print(correlation$n)


# Export the results as CSV files
write.csv(
  correlation$r,
  "correlation_coefficients.csv",
  row.names = TRUE
)

write.csv(
  correlation$P,
  "p_values.csv",
  row.names = TRUE
)

write.csv(
  correlation$n,
  "number_of_observations.csv",
  row.names = TRUE
)
