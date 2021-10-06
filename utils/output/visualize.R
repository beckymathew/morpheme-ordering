library(ggplot2)
library(tidyr)
library(dplyr)

data = read.csv("accuracies.tsv", sep="\t")
names(data) <- c("POS", "Language", "Type", "Accuracy", "Accuracy_Full", "Accuracy_Full_Types")

optimized = data %>% filter(Type=="Optimized") %>% group_by(Language, POS) %>% summarise(AccuracyOpt=mean(Accuracy))

quantiles = merge(data %>% filter(Type != "Optimized"), optimized, by=c("Language", "POS")) %>% group_by(Type, Language, POS) %>% summarise(Quantile = mean(Accuracy<=AccuracyOpt), Lower=binom.test(sum(Accuracy<=AccuracyOpt), NROW(Accuracy))$conf.int[[1]], Upper=binom.test(sum(Accuracy<=AccuracyOpt), NROW(Accuracy))$conf.int[[2]], PValue=binom.test(sum(Accuracy<=AccuracyOpt), NROW(Accuracy), alternative="greater")$p.val, AccuracyOpt=mean(AccuracyOpt))
#quantiles = quantiles %>% mutate(star = ifelse(PValue > 0.05, "", ifelse(PValue > 0.01, "*", ifelse(PValue > 0.001, "**", "***"))))
quantiles = quantiles %>% mutate(star = ifelse(PValue > 0.05, "", "*"))


means = data %>% group_by(Type, POS, Language) %>% filter(Type != "Optimized") %>% summarise(Accuracy=mean(Accuracy))

plot = ggplot(data  %>% filter(POS == "Nouns", Type != "Optimized"), aes(x=Type, y=Accuracy, color=Type, fill=Type)) + geom_violin(width=0.5) #+ geom_text(data=quantiles %>% filter(POS == "Nouns"), aes(y=AccuracyOpt-0.1, label=paste("", star)), size=5, color="black")
plot = plot + geom_segment(data=means %>% filter(POS == "Nouns", Type == "Random"), aes(x=0.5, xend=1.5, y=Accuracy, yend=Accuracy), size=1)
plot = plot + geom_segment(data=means %>% filter(POS == "Nouns", Type == "Universals"), aes(x=1.5, xend=2.5, y=Accuracy, yend=Accuracy), size=1)
plot = plot + geom_segment(data = data %>% filter(POS == "Nouns", Type == "Optimized") %>% group_by(Type, Language) %>% summarise(Accuracy=mean(Accuracy)), aes(x=c(0.5), xend=c(2.5), y=Accuracy, yend=Accuracy), size=1) 
plot = plot + geom_label(data = quantiles %>% filter(POS == "Nouns"), aes(x=Type, y=0.1, label=round(Quantile,2), fill=NULL, color=NULL))
plot = plot + facet_wrap(~Language) + theme_bw() + xlab("")
ggsave("accuracies_nouns.pdf", height=3, width=6)


#
#plot = ggplot(data  %>% filter(POS == "Verbs", Type != "Optimized"), aes(x=Type, y=Accuracy, color=Type, fill=Type)) + geom_violin(width=0.5)
##geom_text(data=quantiles %>% filter(POS == "Verbs"), aes(y=AccuracyOpt-0.1, label=paste("", star)), size=5, color="black")
#plot = plot + geom_segment(data=means %>% filter(POS == "Verbs", Type == "Random"), aes(x=0.5, xend=1.5, y=Accuracy, yend=Accuracy), size=1)
#plot = plot + geom_segment(data=means %>% filter(POS == "Verbs", Type == "Universals"), aes(x=1.5, xend=2.5, y=Accuracy, yend=Accuracy), size=1)
#plot = plot  + geom_segment(data = data %>% filter(POS == "Verbs", Type == "Optimized") %>% group_by(Type, Language) %>% summarise(Accuracy=mean(Accuracy)), aes(x=c(0.5), xend=c(2.5), y=Accuracy, yend=Accuracy), size=1)
#plot = plot  + facet_wrap(~Language) + theme_bw() + xlab("")
#ggsave("accuracies_verbs.pdf", height=6, width=6)
#




plot = ggplot(data  %>% filter(POS == "Verbs", Type != "Optimized"), aes(x=Type, y=Accuracy, color=Type, fill=Type)) + geom_violin(width=0.5)
#geom_text(data=quantiles %>% filter(POS == "Verbs"), aes(y=AccuracyOpt-0.1, label=paste("", star)), size=5, color="black")
plot = plot + geom_segment(data=means %>% filter(POS == "Verbs", Type == "Random"), aes(x=0.5, xend=1.5, y=Accuracy, yend=Accuracy), size=1)
plot = plot + geom_segment(data=means %>% filter(POS == "Verbs", Type == "Universals"), aes(x=1.5, xend=2.5, y=Accuracy, yend=Accuracy), size=1)
plot = plot  + geom_segment(data = data %>% filter(POS == "Verbs", Type == "Optimized") %>% group_by(Type, Language) %>% summarise(Accuracy=mean(Accuracy)), aes(x=c(0.5), xend=c(2.5), y=Accuracy, yend=Accuracy), size=1)
plot = plot + geom_label(data = quantiles %>% filter(POS == "Verbs"), aes(x=Type, y=0.1, label=round(Quantile,2), fill=NULL, color=NULL))
plot = plot  + facet_wrap(~Language) + theme_bw() + xlab("")
ggsave("accuracies_verbs.pdf", height=6, width=6)


