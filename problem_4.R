# Problem 4

numbers <- c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90, 100, 1000)
words <- c("", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "onethousand")
words.len <- nchar(words)
number.to.word <- data.frame(words, words.len, row.names=numbers)


GetVal <- function(n) {
  return(number.to.word[as.character(n), "words.len"])
}


ProcessTens <- function(n) {
  units <- n %% 10
  return(GetVal(n - units)  + GetVal(units))
}


ProcessHundreds <- function(n) {
  hundreds <- n %/% 100
  remainder <- n %% 100
  return(GetVal(hundreds) + GetVal(100) + ProcessNumber(remainder))
}


ProcessNumber <- function(n){
  val <- GetVal(n)
  if (!is.na(val)) {
    if (n == 100) {
      return(GetVal(1) + GetVal(100))
    }
    return(val)
  }
  
  if (n < 100) {
    return(ProcessTens(n))
  }
  
  if (n < 1000) {
    return(ProcessHundreds(n))
  }
}


CountLettersRange <- function(from.val=1, to.val=1000) {
  # Count the number of letters needed for writing all numbers in range {from_val,...,to_val} as words.
  # Conditions:   
  # - do not count spaces or hyphens.
  # - do not use "and" when writing out numbers.
  # - from_val and to_val have to be integers in range {1,...,1000} (inclusive)
  # 
  # Args:
  #   from.val: The lower limit of the range - minimum 1 (default).
  #   to.val: The upper limit of the range (inclusive) - maximum 1000 (default).
  #   
  # Returns:
  #   The number of letters needed for writing all numbers in range {from_val,...,to_val} as words.
  letters.sum <- 0
  for (n in from.val:to.val) {
    letters.sum <- letters.sum + ProcessNumber(n)
  }
  return(letters.sum)
}


# Examples:

# execution time measure - begin
ptm <- proc.time()

CountLettersRange(1, 5)
CountLettersRange(342, 342)
CountLettersRange(115, 115)
CountLettersRange(10, 100)
CountLettersRange(1, 1000)
CountLettersRange(1)
CountLettersRange()

# execution time measure - end
proc.time() - ptm

