setwd('~/Documents/Projects/mattermark-bubble/')
library(ggplot2)
library(scales)

data = read.csv("mattermark_clean.csv", header = TRUE)
data['Date'] = lapply(data['Date'], function (x) 
  as.Date(strptime(gsub("(\\d{1,})[A-Za-z]+", "\\1", x), format="%A %B %d %Y")))
data[2:ncol(data)][is.na(data[2:ncol(data)])] <- 0

all = subset(data, as.Date(Date) >= '2014-01-01' & as.Date(Date) <= '2015-08-25')
sub = subset(data, as.Date(Date) >= '2014-01-01' & as.Date(Date) <= '2015-04-15')

ggplot(all, aes(Date)) + ylim(0,3) +
  theme(legend.title=element_blank()) +
  geom_point(aes(y = bubble, colour = "Bubble")) +
  geom_smooth(aes(y = bubble, colour = "Trend"), method='loess', se = FALSE) + 
  geom_vline(xintercept=as.numeric(as.Date('2015-04-15')), linetype=3) +
  scale_x_date(breaks = date_breaks("3 months"), labels = date_format("%b %Y")) + xlab("") + ylab("Frequency") + ggtitle("Appearance of the word 'Bubble' in the Mattermark Daily")

ggplot(sub, aes(Date)) + ylim(0,3) +
  theme(legend.title=element_blank()) +
  geom_point(aes(y = bubble, colour = "Bubble")) +
  geom_smooth(aes(y = bubble, colour = "Trend"), method='loess', se = FALSE) + 
  scale_x_date(breaks = date_breaks("3 months"), labels = date_format("%b %Y")) + xlab("") + ylab("Frequency") + ggtitle("Appearance of the word 'Bubble' in the Mattermark Daily")