library(readxl)
library(dplyr)
library(tidyr)
library(openxlsx)
library(stringr)


excel_file_path <- "Sequence export (5).xlsx"


second_row <- read_excel(excel_file_path, range = "A2:A2", col_names = FALSE)
second_row_content <- as.character(second_row$...1)


course <- gsub(".*in (MJD-[^ ]+).*", "\\1", second_row_content)


data <- read_excel(excel_file_path, skip = 2)


is_core <- grepl("as core", data$Curriculum, ignore.case = TRUE)
data$Is_Core <- is_core


data_split <- data %>%
  separate(Availabilities, into = paste0("Avail_", 1:7), sep = ";", fill = "right") %>%
  mutate_at(vars(starts_with("Avail_")), ~ trimws(.))

data_with_availabilities <- data_split %>%
  mutate_at(vars(starts_with("Avail_")), list(
    Semester_Year = ~ ifelse(. == "", "", gsub(".*Semester (\\d) (\\d{4}).*", "\\1 Semester \\2", .)),
    Location = ~ ifelse(. == "", "", ifelse(grepl("Crawley", .), "Crawley", "Albany")),
    Teaching_Mode = ~ ifelse(. == "", "", ifelse(grepl("Online", .), "Online", "Face to face"))
  ))


data_with_availabilities$Has_Prerequisites <- !grepl("^Nil\\.", data$Prerequisites)
data_with_availabilities$Has_Corequisites <- !grepl("^Nil\\.", data$Corequisites)
data_with_availabilities$Has_Incompatibilities <- !grepl("^Nil\\.", data$Incompatibilities)


data_with_availabilities <- data_with_availabilities %>%
  mutate(
    Level = substr(Code, 5, 5)  
  )



extract_courses <- function(prereq_str) {
  if (grepl("[A-Z]{4}\\d{4}", prereq_str)) {
    # Extract patterns within parentheses and standalone course codes
    patterns <- c(str_extract_all(prereq_str, "\\(.*?\\)")[[1]], str_extract_all(prereq_str, "(?<![A-Za-z])[A-Z]{4}\\d{4}(?![A-Za-z])")[[1]])
    course_patterns <- lapply(patterns, function(pattern) {
      courses <- str_extract_all(pattern, "[A-Z]{4}\\d{4}")[[1]]
      courses_str <- paste(courses, collapse = " or ")
      return(courses_str)
    })
    
    return(paste(course_patterns, collapse = " and "))
  } else {
    return(NA)
  }
}



extract_specials <- function(prereq_str) {

  course_pattern_matches <- str_extract_all(prereq_str, "[A-Z]{4}\\d{4} [^();,]+")[[1]]
  

  for (course_pattern in course_pattern_matches) {
    prereq_str <- str_remove_all(prereq_str, course_pattern)
  }
  

  specials_patterns <- c(
    "\\bequivalent\\b",
    "for pre-\\d{4} courses: .*?\\bunits\\b",
    "for pre-\\d{4} courses: .*?\\bequivalent\\b"
  )
  
  specials <- unlist(lapply(specials_patterns, function(pattern) str_extract(prereq_str, pattern)))
  
  # Filter out NA values and return result
  specials <- specials[!is.na(specials)]
  
  if(length(specials) > 0) {
    return(paste(unique(specials), collapse = " or "))
  } else {
    return(NA)
  }
}

data_with_availabilities <- data_with_availabilities %>%
  mutate(
    Corequisite_Codes = str_extract_all(Corequisites, "[A-Z]{4}\\d{4}") %>% 
      sapply(function(x) paste(x, collapse = ", ")),
    Incompatibility_Codes = str_extract_all(Incompatibilities, "[A-Z]{4}\\d{4}") %>%
      sapply(function(x) paste(x, collapse = ", "))
  )




data_with_availabilities <- data_with_availabilities %>%
  rowwise() %>%
  mutate(
    course_prerequisite = extract_courses(coalesce(Prerequisites, "")),
    special_prerequisite = extract_specials(coalesce(Prerequisites, ""))
  ) %>%
  ungroup()



data_with_grouping <- data_with_availabilities %>%
  mutate(
    grouping = case_when(
      !Is_Core & Level == "1" ~ "electiveLV1",
      !Is_Core & Level == "2" ~ "electiveLV2",
      !Is_Core & Level == "3" ~ "electiveLV3",
      Is_Core & Level == "1" ~ "coreLV1",
      Is_Core & Level == "2" ~ "coreLV2",
      Is_Core & Level == "3" ~ "coreLV3",
      TRUE ~ NA_character_  # default case to handle unexpected scenarios
    )
  )





wb <- createWorkbook()
addWorksheet(wb, "data_with_grouping")
writeData(wb, "data_with_grouping", data_with_grouping)

saveWorkbook(wb, "newsample5.xlsx")





