name <- 'pvalues_RvsN.csv'

data <- read.csv(name)

L = data$proteins
q_values_ttest <- p.adjust(data$p_values_ttest, method = "BH")
#q_values_utest <- p.adjust(data$p_values_utest, method = "BH")
q_values_welch <- p.adjust(data$p_values_welch, method = "BH")

data2 <- cbind(L, q_values_ttest, q_values_welch)

csv_name <- paste0("q_", name)
write.csv(data2, csv_name)
#write.csv(q_values_utest, 'q_utest.csv')
#write.csv(q_values_welch, 'q_welch_control_sbma.csv')
