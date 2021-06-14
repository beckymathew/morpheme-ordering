data = read.csv("collectCPMIs.py.tsv", sep="\t", header=F)
names(data) <- c("Language", "POS", "Affix", "Mean", "SD", "SE")

library(ggplot2)
library(tidyr)
library(dplyr)

data$Affix = factor(data$Affix, levels=c("Derivation", "Valence", "Voice", "TAM", "Agreement", "Number", "Case", "Possessor", "Possessed"))


plot = ggplot(data %>% filter(Affix != "NA", !is.na(Affix), POS == "Verbs"), aes(x=Affix, y=Mean, group=Language, color=Language)) + geom_point(size=2) + geom_line() + ylab("Conditional MI with Root") + theme_bw()
ggsave(plot, file="visualizeCPMI.R_verbs.pdf", width=4.8, height=3)

plot = ggplot(data %>% filter(Affix != "NA", !is.na(Affix), POS == "Nouns", Affix %in% c("Number", "Case")), aes(x=Affix, y=Mean, group=Language, color=Language)) + geom_point(size=2) + geom_line() + ylab("Conditional MI with Root") + theme_bw()
ggsave(plot, file="visualizeCPMI.R_nouns.pdf", width=3, height=3)




