library(readxl)
library(stringr)
library(dplyr)

merged_data <- data.frame()

for (i in 1:10) {
  excel_file_path <- paste0("Sequence export (", i, ").xlsx")
  cat("Processing file:", excel_file_path, "\n")
  data <- read_excel(excel_file_path, skip = 2)

extract_courses <- function(curriculum) {
  courses <- gsub("\\[.*?\\]", "", curriculum)  
  courses <- gsub("^\\s+|\\s+$", "", courses)  
  courses <- unlist(strsplit(courses, "; "))  
  return(courses)
}

data <- data %>%
  rowwise() %>%
  mutate(Courses = list(extract_courses(Curriculum))) %>%
  ungroup()

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


extract_mode_and_address <- function(availabilities) {
  modes <- str_extract_all(availabilities, "\\([a-zA-Z- ]+\\)")
  return(data.frame(Mode = unlist(modes)))
}


data <- data %>%
  rowwise() %>%
  mutate(ModeAndAddress = list(extract_mode_and_address(Availabilities))) %>%
  ungroup()

data <- data %>%
  rowwise() %>%
  mutate(
    Mode = ifelse(length(ModeAndAddress$Mode) == 0, "Unknown",
                  paste(data.table::transpose(ModeAndAddress)[[1]], collapse = "; "))
  ) %>%
  ungroup() %>%
  select(-ModeAndAddress)

data <- data %>%
  mutate(
    FaceToFace = ifelse(str_detect(Mode, "Face to face"), "Face to face", ""),
    Online = ifelse(str_detect(Mode, "Online"), "Online", ""),
    Mode = ifelse(FaceToFace != "" | Online != "", Mode, "Unknown")
  ) %>%
  select(-FaceToFace, -Online)

data <- data %>%
  rowwise() %>%
  mutate(
    Semester_Mode = str_extract_all(Availabilities, "Semester \\d \\d{4}") %>%
      lapply(function(x) paste(x, Mode, sep = " - "))
  ) %>%
  ungroup() %>%
  select(-Mode)



merged_data <- rbind(merged_data, data)
cat("Finished processing file:", excel_file_path, "\n\n")
}


