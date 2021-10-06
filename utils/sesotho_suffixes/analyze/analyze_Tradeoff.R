library(tidyr)
library(dplyr)
library(ggplot2)


RED = "#F8766D"
GREEN = "#7CAE00"
BLUE = "#00BFC4"
PURPLE = "#C77CFF"
SCALE = c( GREEN, RED, BLUE, PURPLE)
######################################

byWords_real = read.csv("../estimates_byWord/forWords_Hungarian_RandomOrder_Coarse_FineSurprisal_ForSlot.py_Sesotho_Acqdiv_REAL", sep="\t") %>% mutate(Ordering = "Real")
byWords_reverse = read.csv("../estimates_byWord/forWords_Hungarian_RandomOrder_Coarse_FineSurprisal_ForSlot.py_Sesotho_Acqdiv_REVERSE", sep="\t") %>% mutate(Ordering = "Reverse")

byWords = rbind(byWords_real, byWords_reverse)

plot = ggplot(byWords, aes(x=Distance, y=Surprisal, color=Ordering, group=Ordering)) + geom_line() + facet_wrap(~Slot)


MIs = c()
for(i in (1:nrow(byWords))) {
  ordering = byWords$Ordering[[i]]
  distance  = byWords$Distance[[i]]
  slot = byWords$Slot[[i]]
  if(distance == 0) {
    MIs = c(MIs, NA)
  } else {
    surprisalHere = min((byWords %>% filter(Slot==slot, Distance<=distance, Ordering==ordering))$Surprisal)
    surprisalPrevious = min((byWords %>% filter(Slot==slot, Distance<distance, Ordering==ordering))$Surprisal)
    MIs = c(MIs, surprisalPrevious-surprisalHere)
  }
}
byWords$MI = MIs

plot = ggplot(byWords %>% filter(Slot %in% c("Derivation", "Valence", "Voice", "Tense/Aspect", "Mood", "Relative")), aes(x=Distance, y=MI, color=Ordering, group=Ordering)) + geom_line() + facet_wrap(~Slot) + theme_classic() + ylab("Conditional Mutual Information")
ggsave(plot, file="miBySlot_Real-Reverse.pdf", height=3, width=5)

slotCounts = read.csv("slotCounts.tsv", sep="\t") %>% filter(Slot %in% c("Derivation", "Valence", "Voice", "Tense/Aspect", "Mood", "Relative", "EOS", "ROOT"))
slotCounts$Count = slotCounts$Count / sum(slotCounts$Count)
byWords = merge(byWords, slotCounts, by=c("Slot"))

overallMI = byWords %>% group_by(Distance, Ordering) %>% summarise(MI = sum(MI*Count, na.rm=TRUE), Surprisal=sum(Surprisal*Count, na.rm=TRUE))

plot = ggplot(overallMI %>% filter(Distance>0), aes(x=Distance, y=MI, color=Ordering, group=Ordering)) + geom_line() + theme_classic() + ylab("Conditional Mutual Information")
ggsave(plot, file="miAvg_Real-Reverse.pdf", height=3, width=4)

#
#Memory = c()
#Surprisal = c()
#for(i in (1:nrow(overallMI))) {
#  ordering = overallMI$Ordering[[i]]
#  distance  = overallMI$Distance[[i]]
#    relevantMIs = (overallMI %>% filter(Distance<=distance, Ordering==ordering))
#    surprisal = min(relevantMIs$Surprisal, na.rm=TRUE)
#    memory = sum(relevantMIs$MI * relevantMIs$Distance, na.rm=TRUE)
#    Memory = c(Memory, memory)
#    Surprisal = c(Surprisal, surprisal)
#}
#overallMI$Memory = Memory
#overallMI$Surprisal = Surprisal
#
#minimum = as.data.frame(overallMI %>% group_by(Ordering) %>% summarise(Surprisal=min(Surprisal, na.rm=TRUE)) %>% mutate(Memory = 7, Distance=10, MI=0) %>% group_by())
#overallMI = rbind(as.data.frame(overallMI), minimum)
#
#plot = ggplot(overallMI, aes(x=Memory, y=Surprisal, color=Ordering, group=Ordering)) + geom_line() + theme_bw() + ylab("Surprisal") + xlab("Memory")
#ggsave(plot, file="tradeoff_Real-Reverse.pdf", height=3, width=4)
#
#



# Slot counts are obtained from forWords_Hungarian_RandomOrder_Coarse_FineSurprisal_CountSlot.py

data = read.csv("results.tsv", sep="\t")
#data = data %>% filter(Script == "forWords_Finnish_RandomOrder_Coarse_FineSurprisal.py")


data$Type = ifelse(data$Model %in% c("REAL", "RANDOM", "REVERSE"), as.character(data$Model), "Optimized")
data$Type = ifelse(data$Type %in% c("REAL"), "Real", as.character(data$Type))
data$Type = ifelse(data$Type %in% c("RANDOM"), "Random", as.character(data$Type))
data$Type = ifelse(data$Type %in% c("REVERSE"), "Reverse", as.character(data$Type))
data$Type = ifelse(data$Model %in% c("UNIV"), "Universals", as.character(data$Type))

data_ = data %>% filter(Type %in% c("Real", "Random", "Optimized", "Reverse", "Universals"))

#randomAUCs = data %>% filter(Type == "Random")
#meanAUCs = data %>% filter(Type == "Real") %>% group_by(Type) %>% summarise(AUC = mean(AUC)) %>% mutate(Quantile = round(mean(AUC < randomAUCs$AUC), 2), ConfIntLower = round((binom.test(sum(AUC<randomAUCs$AUC), nrow(randomAUCs))$conf.int[[1]]),2), ConfIntUpper = round((binom.test(sum(AUC<randomAUCs$AUC), nrow(randomAUCs))$conf.int[[2]]),2))

#barWidth = (max(data$AUC) - min(data$AUC))/30

#plot = ggplot(data_ %>% group_by(Distance, Type) %>% summarise(MI=mean(MI)), aes(x=Distance, y=MI, color=Type, group=Type)) + geom_line()

data__ = data_ %>% group_by(Script, Type, Run, Model, UnigramCE) %>% summarise(Surprisal=min(Surprisal)) %>% mutate(Memory=10, MI=0, Distance=20)

data_ = rbind(as.data.frame(data_), as.data.frame(data__))

plot = ggplot(data_ %>% filter(Type %in% c("Real", "Reverse")) %>% group_by(Memory, Type) %>% summarise(Surprisal=mean(Surprisal)), aes(x=Memory, y=Surprisal, color=Type, group=Type)) + geom_line()
plot = plot + theme_classic()
#plot = plot + theme(text=element_text(size=30))
plot = plot  + theme (legend.position = "none")
ggsave(plot, file="tradeoff_Real-Reverse.pdf", height=3, width=4)



