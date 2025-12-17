### script for combining and cleaning nsf and nih grant data

#packages and libraries
install.packages("readr")
install.packages("data.table")

library(readr)
library(data.table)

###make awards dataset
##bring in data
nsf_all <- fread('../input/grants_igert_nrt.csv')

###make papers dataset
##bring in sciscinet csvs- download from https://doi.org/10.6084/m9.figshare.c.6076908.v1
ssn_nsf_meta <- fread('../input/SciSciNet_NSF_Metadata.tsv')

#df of all papers
ssn_papers <- fread('SciSciNet/SciSciNet_Papers.tsv')

#extract matching nsf papers
ssn_nsf <- fread('SciSciNet/SciSciNet_Link_NSF.tsv')

#match nsf award number field format
nsf_all$NSF_Award_Number<- paste0('NSF-',nsf_all$AwardNumber)

nsf_and_ssn <- merge(ssn_nsf, nsf_all, by="NSF_Award_Number")
nsf_and_ssn <- merge(nsf_and_ssn, ssn_papers, by="PaperID")

##save csv of papers with metadata
write.csv(nsf_and_ssn, file="../output/grant_papers.csv")