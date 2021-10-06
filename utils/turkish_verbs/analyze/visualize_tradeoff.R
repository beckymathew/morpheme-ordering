library(tidyr)
library(dplyr)
library(ggplot2)


RED = "#F8766D"
GREEN = "#7CAE00"
BLUE = "#00BFC4"
PURPLE = "#C77CFF"
SCALE = c( GREEN, RED, BLUE, PURPLE)
######################################


data = read.csv("results.tsv", sep="\t")
#data = data %>% filter(Script == "forWords_Finnish_RandomOrder_Coarse_FineSurprisal.py")


data$Type = ifelse(data$Model %in% c("REAL", "RANDOM", "REVERSE"), as.character(data$Model), "Optimized")
data$Type = ifelse(data$Type %in% c("REAL"), "Real", as.character(data$Type))
data$Type = ifelse(data$Type %in% c("RANDOM"), "Random", as.character(data$Type))
data$Type = ifelse(data$Type %in% c("REVERSE"), "Reverse", as.character(data$Type))
data$Type = ifelse(data$Model %in% c("UNIV"), "Universals", as.character(data$Type))

data_ = data %>% filter(Type %in% c("Real", "Random", "Optimized", "Reverse", "Universals"))

randomAUCs = data %>% filter(Type == "Random")
meanAUCs = data %>% filter(Type == "Real") %>% group_by(Type) %>% summarise(AUC = mean(AUC)) %>% mutate(Quantile = round(mean(AUC < randomAUCs$AUC), 2), ConfIntLower = round((binom.test(sum(AUC<randomAUCs$AUC), nrow(randomAUCs))$conf.int[[1]]),2), ConfIntUpper = round((binom.test(sum(AUC<randomAUCs$AUC), nrow(randomAUCs))$conf.int[[2]]),2))

barWidth = (max(data$AUC) - min(data$AUC))/30

plot = ggplot(data_ %>% group_by(Distance, Type) %>% summarise(Surprisal = mean(Surprisal)), aes(x=Distance, y=Surprisal, color=Type, group=Type))
plot = plot + geom_line()



plot = ggplot(data_ %>% group_by(Memory, Type) %>% summarise(Surprisal = mean(Surprisal)), aes(x=Memory, y=Surprisal, color=Type, group=Type))
plot = plot + geom_line()
plot = plot + theme_classic()
plot = plot + xlab("Area under Curve") + ylab("Density")
plot = plot + theme(text=element_text(size=30))
plot = plot + geom_density(data= data_%>%filter(Type %in% c("Universals", "Random")), aes(y=..scaled..), size=2) 
plot = plot + geom_bar(data = data_ %>% filter(!(Type %in% c("Universals", "Random"))) %>% group_by(Type) %>% summarise(AUC=mean(AUC)) %>% mutate(y=1),  aes(y=y, group=Type, fill=Type), width=barWidth, stat="identity", position = position_dodge()) # + scale_colour_manual(values=SCALE) + scale_fill_manual(values=SCALE)
plot = plot + geom_label(data=meanAUCs, aes(x=AUC, y=1, label=paste(Quantile, " [", ConfIntLower, ", ", ConfIntUpper, "]"), group=Type), color="black", fill="white") + theme (legend.position = "none")
ggsave(plot, file=paste("tradeoff.pdf", sep=""), height=4, width=8)



