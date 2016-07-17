# Problem 1.

FillNa <- function(x, value) {
  # Replaces all missing values (NA) in the input vector x with the given value.
  #
  # Args:
  #   x: A vector that may contain missing values.
  #   value: The value by which all NA in the input vector should be replaced.
  #
  # Returns:
  #   The input vector with all NA replaced by the given value.
  x[is.na(x)] <- value
  return(x)
}


RelaceMissingMean <- function(x) {
  # Replaces all missing values (NA) of a vector with the mean of that vector.
  #
  # Args:
  #   x: A numeric vector that may contain missing values (NA).
  #
  # Returns:
  #   The input vector with all NA replaced by the mean of that vector.
  value <- mean(x, na.rm=TRUE)
  return(FillNa(x, value))
}


# Problem 2.

RelaceMissingVal <- function(x, fun) {
  # Replaces all missing values (NA) in the input vector x with the value
  # computed by fun.
  #
  # Args:
  #   x: A vector that may contain missing values.
  #   fun: A function that takes a vector and a boolean value (na.rm)
  #         and returns a value that should be used to replace all NA in the vector.
  #
  # Returns:
  #   The input vector with all NA replaced by the value computed by fun.
  value <- fun(x, na.rm = TRUE)
  return(FillNa(x, value))
}


ComputeMode <- function(x, na.rm = FALSE) {
  # Computes the modal value of the input vector x.
  #
  # Args:
  #   x: A vector that may contain missing values.
  #   na.rm: A logical value indicating whether NA values should be stripped
  #            before the computation proceeds.
  #
  # Returns:
  #   The modal value of the input vector.
  if (na.rm == TRUE) {
    x <- na.omit(x)
  }
  ux <- unique(x)
  return(ux[which.max(tabulate(match(x, ux)))])
}


ReplaceMissing <- function(x) {
  # Replace all missing values of a given vector with:
  # - the mean of the values in that vector - in case of numeric vectors,
  # - the modal value (if one exists) - otherwise.
  # 
  # Args:
  #   x: A vector that may contain missing values.
  # 
  # Returns:
  # 	The input vector with missing values replaced by the mean (in case of numeric vector)
  # 	or the modal value - if one exists - (otherwise) of that vector
  if (mode(x) == "numeric") {
    fun <- mean
  }
  else {
    fun <- ComputeMode
  }
  return(RelaceMissingVal(x, fun))
}

# Examples:
ReplaceMissing(c(NA))
ReplaceMissing(c(NA, NA))
ReplaceMissing(c(1, 2, 3))
ReplaceMissing(c(NA, -2, 3, 0))
ReplaceMissing(c(NA, -2, 3, NA))
ReplaceMissing(c(NA, NA, NA, NA, 1))
ReplaceMissing(c(NA, "a", "a", "b", NA))
ReplaceMissing(c(NA, "a", NA, NA, NA))



# Problem 3.

# read in the data sample
sample.data <- read.csv("sample.csv", stringsAsFactors=FALSE)

# impute the mean (for numeric variables) or mode (for character strings) where there are missing values
sample.data <- data.frame(sample.data[c("caseid",  "disposition",	"regstate")],
                          lapply(sample.data[c("pid7", "ideo5", "birthyr", "gender", "race", "educ")],
                                 ReplaceMissing))

# take integral part of the year
sample.data$birthyr <- floor(sample.data$birthyr)

# chceck that there are no missing values in the data frame
any(is.na(sample.data))

head(sample.data)
