# An R script to load data from XLS file and convert it into valid CSV data.
library(readxl)


# Loading data
print("Please, remember to cook first the excel by removing some unwanted rows")
#
parsed_cpheur17_MODIFIED <- read_excel("C:/Users/elekt/OneDrive/Escritorio/parsed_cpheur17_MODIFIED.xls")
#Save csv in disk
write.csv(parsed_cpheur17_MODIFIED, file="electricity_price_2017.csv", row.names = FALSE)
