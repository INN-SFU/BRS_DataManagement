#### LOAD LIBRARIES ####
# changes working directory to folder with script
setwd(dirname(rstudioapi::getSourceEditorContext()$path))

library(tidyverse)

# read all lines from participant's raw MST text file 
# CHANGE THE NAME OF THE TEXT FILE PER PARTICIPANT
raw_lines <- read_lines("data/MST_data/sub-BRS0008_mst.txt")

#### EXTRACTING RELEVANT TESTING INFORMATION ####
test_info_data <- tibble(raw = raw_lines) %>%
  mutate(line_number = row_number()) %>%
  filter(line_number %in% c(2, 5, 8)) %>%
  pivot_wider(names_from = line_number, values_from = raw, names_prefix = "line_") %>%
  mutate(date = format(parse_date_time(line_2, orders = "a b d H:M:S Y"), "%m/%d/%y"),
         set = str_extract(line_5, "(?<=Set: Set )\\S+"),
         duration = as.numeric(str_extract(line_8, "(?<=Dur: )\\d+\\.?\\d*")),
         ISI = as.numeric(str_extract(line_8, "(?<=ISI:)\\d+\\.?\\d*"))) %>%
  select(date, set, duration, ISI)

# locate the start lines of the data for study phase & test phase
# since all text files are in the same format, study_start should always be line 142; test_start should always be line 411
study_start <- which(str_detect(raw_lines, "Study phase started at:")) + 2  # +2 to skip header
test_start <- which(str_detect(raw_lines, "Test phase started at:")) + 2

# find the column headers of the data for study phase & test phase
study_header <- raw_lines[study_start - 1]
test_header <- raw_lines[test_start - 1]

test_end <- length(raw_lines)

study_data <- raw_lines[study_start:(test_start - 142)]  # -142 txt file lines to stop before "Test phase started at:"

test_data <- raw_lines[test_start:(test_start + 191)] # +191 txt file lines to stop at the end of last trial of Test phase

# after running, ensure there are 128 observations in df_study_data
df_studyPhase <- read_table(paste(c(study_header, study_data), collapse = "\n"))

# after running, ensure there are 192 observations in df_testPhase
df_testPhase <- read_table(paste(c(test_header, test_data), collapse = "\n"))

# study phase is only for incidental encoding
# assigning phase = 1, condition = S (study), 0 to  "lure bins" because do not exist, 0 to "accuracy" column because no accuracy here
df_studyPhase_clean <- df_studyPhase %>%
  mutate(Phase = 1,
         Cond = "S",
         LBin = 0,
         Acc = 0) %>%
  select(Phase, Trial, Img, Resp, RT, Cond, LBin, Acc)

# assigning phase = 2, no changes to any of the test phase data 
df_testPhase_clean <- df_testPhase %>%
  mutate(Phase = 2) %>%
  select(Phase, Trial, Img, Resp, RT, Cond, LBin, Acc)

# combine both study phase & test phase datasets
df_mst_combined <- bind_rows(df_studyPhase_clean, df_testPhase_clean)

# renaming columns and recoding variables
df_mst_combined <- df_mst_combined %>%
  rename(phase = Phase,
         trial = Trial,
         image = Img,
         response = Resp,
         reaction_time = RT,
         condition = Cond,
         lure_bin = LBin,
         accuracy = Acc) %>%
  mutate(condition = recode(condition,
                       "S" = "study",
                       "F" = "foil",
                       "L" = "lure",
                       "T" = "target"))

# recode the "response" variable for the TEST PHASE
# leave the study phase as numbers because responses do not matter for that phase
# in test phase: response of 0 = no response; 1 = old; 2 = similar; 3 = new
# leave responses of 0 as 0, will be excluded from analysis because no answer
df_mst_combined <- df_mst_combined %>%
  mutate(response = case_when(phase == 2 & response == 1 ~ "old",
                              phase == 2 & response == 2 ~ "similar",
                              phase == 2 & response == 3 ~ "new",
                              TRUE ~ as.character(response)))

# IMPORTANT: setting subID column according to the BRS participant ID in the text file 
df_mst_combined <- df_mst_combined[, c("subID", setdiff(names(df_mst_combined), "subID"))]

# combine the test_info_data file & the df_mst_combined
# CHECKS: Set should be 1, duration should be 2.5, ISI should be 0.5
df_mst_combined <- df_mst_combined %>%
  mutate(date = test_data$date,
         set = test_data$set,
         duration = test_data$duration,
         ISI = test_data$ISI) %>%
  select(subID, date, set, duration, ISI, everything()) 

# write csv file - one file per participant
# final csv should have 320 observations and 8 columns/variables
# naming convention returns back to the BRS convention when csv is saved
write_csv(df_mst_combined, "sub-BRS0008_mst.csv")
