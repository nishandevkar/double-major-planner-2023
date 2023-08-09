library(readxl)
library(stringr)
library(dplyr)


excel_file_path <- "Sequence export (1).xlsx"
data <- read_excel(excel_file_path, skip = 2)  

extract_semesters <- function(availabilities) {
  semesters <- str_extract_all(availabilities, "Semester \\d \\d{4}")
  return(semesters)
}

data <- data %>%
  rowwise() %>%
  mutate(Semesters = extract_semesters(Availabilities)) %>%
  ungroup()


data$Semester_1 <- sapply(data$Semesters, function(semesters) any(grepl("Semester 1", semesters)))
data$Semester_2 <- sapply(data$Semesters, function(semesters) any(grepl("Semester 2", semesters)))

is_major <- function(curriculum) {
  grepl("as core \\[Active\\]", curriculum, ignore.case = TRUE)
}


data <- data %>%
  rowwise() %>%
  mutate(Is_Major = is_major(Curriculum)) %>%
  ungroup()


data$Has_Prerequisites <- !grepl("^Nil\\.", data$Prerequisites)

data$Has_Corequisites <- !grepl("^Nil\\.", data$Corequisites)

data$Has_Incompatibilities <- !grepl("^Nil\\.", data$Incompatibilities)


print(data)
