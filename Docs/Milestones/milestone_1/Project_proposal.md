<!-- #region -->


## Project proposal



### *Introduction:* 

The COVID-19 pandemic has had an indelible impact on many people, bringing negative emotions such as severe panic, anxiety, etc. As one of the most important microblogging social media globally, Twitter provides the best platform for millions of users to express their feelings and emotions. In our engineering project, we are going to use COVID-19 data collected from Twitter to analyze how sentiment on several topics, namely vaccines, education, and politics, was changing over the last 12 months(March 2021 - March 2022) across various English-speaking countries(Canada, the US, the UK, Australia, and New Zealand). We are planning to collect a certain number of tweets (presumably 10K) for each topic for each month and for each country and on classifying the sentiment of each tweet analyze if and how the sentiment was changing. The sentiment analysis of the tweets is going to take place on a five-point ordinal scale for the sentiment of each tweet: Strongly Positive, Weakly Positive, Neutral, Weakly Negative, and Strongly Negative. The scale is referenced in the article SemEval-2017 Task 4: Sentiment Analysis in Twitter.  

### *Motivation and Contributions/Originality:*

In light of the current COVID-19 pandemic, our motivation is to understand the sentiment on education, vaccines and politics in different countries and how it was changing during the last 12 months. In general, early detection of COVID-19 sentiment from collected tweets can help us understand and deal with the pandemic and its negative impacts better. It might help us reveal the attitudes towards the changes concerning education, vaccines and politics and how they ranged among various countries. Therefore, the result of the study might later be used either for a larger scope study that encompasses all the countries using twitter, or be used by the sociologists, statisticians, lawmakers and even social media platforms of Canada, the US, the UK, Australia, and New Zealand to address the problems connected with education, vaccines or politics, since our study might enable us to reveal what moods/attitudes prevail in some country within a specific period of time. Unlike similar projects that consider mainly POS, NEG and NEU sentiments, our study is going to be centered around the latest tweets and represent the sentiment change on a five-point ordinal scale. Moreover, we are going to apply the result of the last years deep learning innovations and use the latest state-of-the-art model, BERTweet, which we expect will enable us to ensure that our final result are credible and trustworthy.


### *Data:*

To build our corpus, we will use the Twitter API to collect tweets from various random Twitter users related to COVID-19 from the Twitter database by writing queries to search by topic. Considering project time limitations, we plan to collect 10,000 tweets on vaccines, education and politics in Canada, the US, the UK, Australia, and New Zealand from March 2021 to March 2022. After that, we will consider 12 months separately and analyze if there are changes in sentiments and how they change. Meanwhile, we will only focus on tweets in English, filtering out tweets in other languages. Once the data collection is complete, we plan to store them in multiple CSV files according to each topic. There would be four columns in each topic CSV file: Country_name, Time, Tweet_id, Tweet_content. However, we may change the data size based on our project needs.


### *Engineering:*

In our study, we are going to rely mainly on Google Colab for the training and classification part of our project, however, our corpus collection is going to be done with the help of our personal computers. 
When it comes to the deep learning methods, we decided to focus on the recent years developments, mainly, text classification with BERT. On studying the available types of pre-trained transformers available, we decided to stop on BERTweet, which is a pre-trained language model for English Tweets. Another factor that made this model quite favourable for our sentiment classification is the fact that it allows to take advantage of various types of pre-trained data, namely, 23M COVID-19 English Tweets - which suits our task perfectly. 
Architecture:
BERTweet's architecture is similar to BERTbase and is trained with a masked language modeling objective. BERTweet is trained using the RoBERTa pre-training procedure. (Ref.:https://aclanthology.org/2020.emnlp-demos.2.pdf)
The existing codebase we are going to base our training on is represented here:
https://huggingface.co/docs/transformers/model_doc/bertweet#bertweet
https://github.com/VinAIResearch/BERTweet


### *Previous Works (minimal):*

Sentiment analysis has been a central topic of dozens of projects and all of them approach the task from different angles. One of the extensive studies relevant to our project is Sentiment Analysis In Tweets(https://arxiv.org/pdf/2105.14373.pdf). Published in 2021, it discusses state-of-the-art Transformer-based autoencoder models with regards to the sentiment classification of tweets and their fine-tuning. The project suggests that one of the most appropriate language models to be used in the sentiment classification of tweets is BERTweet. In particular, the authors highlight that the model achieved the best overall results when it is combined with LR and MLP classifiers. In comparison to the other state-of-the-art models, BERTweet appears to be as demanding in terms of the training data. The paper also discusses the fine-tuning of BERTweet which we are going to take advantage of later in our project. 
<br>
Another deep work which drew our attention is Topic Detection And Sentiment Analysis In Twitter Content Related To
COVID-19 From Brazil And The USA(https://reader.elsevier.com/reader/sd/pii/S1568494620309959?token=C97EBF27675DB4CB18FC39AE89B9E0A5D092DE0B14E169DF42E2CAFD8313E6ABA42C2766DC26AFB9C64394F60E7E5906&originRegion=us-east-1&originCreation=20220403000432). Unlike our project the main goal if which is to reveal how the sentiment on various topics was changing over 12 months in 5 different countries, the authors look into how the sentiment was changing over an earlier period of time. They also appear to cover a much larger number of topics, like economic impacts, case reports/statistics, proliferation care, politics, entertainment, treatments, online events, charity, sports and anti-racism protests. Another peculiarity of the study is connected with the fact that it centers around only the USA and Brazil countries and encompasses two languages-English and Portugese. The result of the study unfolds what topics include mainly positive or negative tweets as well what was the trend for their change over the studied period of time. A very valuable part of the study is allocated to the sentiment analysis and topic modeling, which is going to give us some guidance in our own project.  



### *Evaluation:*

Since the nature of our project is connected with the text classification, namely, sentiment analysis, we are going to train our model and then evaluate it on the test set using ``accuracy`` and ``macro F1`` score.


### *Conclusion (optional):*

The purpose of this proposal is to outline the plan for the project and to define its scope. It discusses the steps we are going to undertake in order to answer the problem/question stated in the proposal.

<!-- #endregion -->

```python

```
