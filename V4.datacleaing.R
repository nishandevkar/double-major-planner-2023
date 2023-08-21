library(readxl)
library(dplyr)
library(tidyr)
library(openxlsx)
# read path
excel_file_path <- "Sequence export (3).xlsx"

# find the Degree 
second_row <- read_excel(excel_file_path, range = "A2:A2", col_names = FALSE)
second_row_content <- as.character(second_row$...1)

# take the degree code
course <- gsub(".*in (MJD-[^ ]+).*", "\\1", second_row_content)

# read file except first 2 rows
data <- read_excel(excel_file_path, skip = 2)

# To that degree,  to see what is required 
is_core <- grepl("as core", data$Curriculum, ignore.case = TRUE)
data$Is_Core <- is_core

# split "Availabilities" 
data_split <- data %>%
  separate(Availabilities, into = paste0("Avail_", 1:7), sep = ";", fill = "right") %>%
  mutate_at(vars(starts_with("Avail_")), ~ trimws(.))


data_with_availabilities <- data_split %>%
  mutate_at(vars(starts_with("Avail_")), list(
    Semester_Year = ~ ifelse(. == "", "", gsub(".*Semester (\\d) (\\d{4}).*", "\\1 Semester \\2", .)),
    Location = ~ ifelse(. == "", "", ifelse(grepl("Crawley", .), "Crawley", "Albany")),
    Teaching_Mode = ~ ifelse(. == "", "", ifelse(grepl("Online", .), "Online", "Face to face"))
  ))

#  Prerequisites、Corequisites and Incompatibilities
data_with_availabilities$Has_Prerequisites <- !grepl("^Nil\\.", data$Prerequisites)
data_with_availabilities$Has_Corequisites <- !grepl("^Nil\\.", data$Corequisites)
data_with_availabilities$Has_Incompatibilities <- !grepl("^Nil\\.", data$Incompatibilities)

#  Level 
data_with_availabilities <- data_with_availabilities %>%
  mutate(
    Level = substr(Code, 5, 5)  
  )

wb <- createWorkbook()


addWorksheet(wb, "data_with_availabilities")


writeData(wb, "data_with_availabilities", data_with_availabilities)


saveWorkbook(wb, "sample3.xlsx")

cat("Finished processing and wrote data to output_data.xlsx\n")

