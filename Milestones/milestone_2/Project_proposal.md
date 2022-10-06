
### *Motivation and Contributions/Originality:* 

In light of the current COVID-19 pandemic, our motivation is to understand the sentiment on education, vaccines and politics in different countries and how it changed during the last 12 months. In general, early detection of COVID-19 sentiment from collected tweets can help us understand and deal with the pandemic and its negative impacts better. Furthermore, it might help us reveal the attitudes towards the changes concerning education, vaccines and politics and how they range among various countries. Therefore, the result of the study might later be used either for a more extensive scope study that encompasses all the countries using Twitter or is used by the sociologists, statisticians, lawmakers and even social media platforms of Canada, the US, the UK, Australia, and New Zealand to address the problems connected with education, vaccines or politics since our study might enable us to reveal what moods/attitudes prevail in some country within a specific period. Additionally, our study will be centred around the latest tweets and represent the sentiment change on a three-point ordinal scale: POSITIVE, NEUTRAL, and NEGATIVE. Moreover, we will apply the result of the last years' deep learning innovations and use the latest state-of-the-art model, BERTweet, which we expect will enable us to ensure that our final result is credible and trustworthy.


### *Data:*

To build our corpus, we will use the Twitter API to collect tweets from various random Twitter users related to COVID-19 from the Twitter database by writing queries to search by topic. Considering project time limitations, we plan to collect tweets on such topics as vaccines and masks discussed in Canada, the UK, and, probably, the US from March 2021 to March 2022. After that, we will consider 12 months separately and analyze if there are changes in sentiments and how they change. Meanwhile, we will only focus on tweets in English, filtering out tweets in other languages. Once the data collection is complete, we plan to store them in multiple CSV files according to each topic. There would be four columns in each topic CSV file: Country_name, Time, Tweet_id, Tweet_content.

We have not started building the corpus yet due to the fact that we managed to secure Academic Research Access only a couple of days ago. With the elevated access we managed to built two small test sets(masks and vaccines, you can find them in milestone 2 folder - test_masks.tsv and test_vaccines.tsv). We performed a manual annotation on both of them, each file was annotated by two students and only the tweets with the annotation agreement are included in the final test files. Since we performed a small EDA on our training data(data_analysis.ipynb in milestone 2 folder), we also looked into how our test files look like, as it turned out our vaccines test file was extremely unbalanced towards neutral tweets(85%/10%/5% neu/neg/pos correspondingly) and our masks test set was really unbalanced towards negative tweets(approximately similar numbers), we manually added positive and negative tweets there as well to understand how good/bad our models are going to deal with them. Under no condition we are planning to do the same thing with our tweets corpus data.<br>
When it comes to the main corpus, one of our tasks was the next week is to work on the API queries and collect all the tweets which we are going to use in order to do our sentiment analysis. The number of tweets is going to defined by the availability of the data. When it comes to the queries, we will base them on the key words as well as on the tags, we will have to develop such queries that our data is devoid of ads, reposts, super short and meaningless tweets and gibberish. As an idea, it would be interested to focus our research on private tweets and discussions, rather than news or announcements.<br>
It is important to mention as well that we also gathered an [annotated training data](https://alt.qcri.org/semeval2017/task4/?id=download-the-full-training-data-for-semeval-2017-task-4) with positive/negative/neutral labels and our training set is comprised of around 15000 examples. Let us discuss the engineering side of things and what we did with the training set.


### *Engineering:*

As mentioned in milestone 1, our research and development is going to be centered around BERTweet model. However, since it does have some drawbacks, for example, it is not trained on emojies, we decided to address this problem and to train 3 separate models, namely, CNN(on SemeVal2017 corpus), BERTweet(on SemeVal2017 corpus) and BERTweet(on emoji corpus + fine-tuning on SemeVal2017 corpus).

<!-- #raw -->
Discussion:

1) CNN 
As suggested in plenty of 
s, CNN is one of the optimal options for sentiment analysis. Therefore, we tried to looked deeper into this model. Our baseline for vanilla CNN is 0.48 accuracy and 0.39 f-1 score. In order to improve the scores, we performed a random hyperparameter search, we were looking into the different kernel sizes, embedding dimension, dropout % and learning rate. On 30 iterations, which took us almost 14 hours, we managed to find the hyperparameters that enables us to boost the scores to 0.55 accuracy and 0.52 f-1, which was a promising result. On following the suggestion in the [article](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9336549), we also gave a try to:

BiLSTM                     (0.54 acc, 0.52 f-1)
CNN + BiLSTM               (0.51 acc, 0.51 f-1)

We also tried using pre-trained embeddings, glove.twitter.27B.200d, and got the following results:

CNN + BiLSTM               (0.56 acc, 0.55 f-1)
Deep CNN - 3 layers        (0.55 acc, 0.53 f-1)
Deep CNN - 5 layers        (0.56 acc, 0.53 f-1)

As follows from the result the model that yielded us the highest scores is CNN + BiLSTM, it is also the most tme consuing model in terms of the training. In order to see how performs on our task, we passed two separate test files(vaccines and masks test files) and got the fillowing results:

vaccines_test.tsv          0.68 acc, 0.70 f-1
masks_test.tsv             0.45 acc, 0.43 f-1

The reason why the results are so different from the validation set is most likely because the training data is very unbalanced and there are fewer negative examples there, while in our test set negative label is prevailing, so it looks like the model did not manage to catch all of them. For the next milestone, we will look more closely at out test examples and try to interpret the model in order to trace how it bahaves with our test tweets. Unfortunately, we did not manage to do it this week as the training and hyperparameter search took an immense amount of time.


2) BERTweet(on SemeVal2017 corpus)
- The pertained Betweet + untrained linear model is trained on Google Colab on GPU. The documentation of pertained Bertweet can be found [here](https://huggingface.co/docs/transformers/model_doc/bertweet). The code for data preparation and training process based off the [BERT tutorial](https://github.ubc.ca/mds-cl-2021-22/COLX_585_trends_students/blob/master/tutorials/BPE-BERT/bert_pytorch.ipynb). The code for training the Bertweet + linear layer model can be found [here](https://github.ubc.ca/maryisme/covid_sentiment/blob/jiajing/milestone_2/Bertweet.ipynb).
- With three epochs, the model's F1 scored 0.6516 on the development set.  

3) BERTweet(on emoji corpus + fine-tuning on SemeVal2017 corpus) will be trained the following week, the results will be reported.
<!-- #endraw -->

**Architecture**:  

We are planning to train three models and then put them all together in ensemble to let them vote and make the predictions on the tweets. This is going to be done by the end of the next week.


### *Previous Works:*

Sentiment analysis has been a central topic of dozens of projects and all of them approach the task from different angles. One of the extensive studies relevant to our project is [Sentiment Analysis In Tweets](https://arxiv.org/pdf/2105.14373.pdf). Published in 2021, it discusses state-of-the-art Transformer-based autoencoder models with regards to the sentiment classification of tweets and their fine-tuning. The project suggests that one of the most appropriate language models to be used in the sentiment classification of tweets is BERTweet. In particular, the authors highlight that the model achieved the best overall results when it is combined with LR and MLP classifiers. In comparison to the other state-of-the-art models, BERTweet appears to be as demanding in terms of the training data. The paper also discusses the fine-tuning of BERTweet which we are going to take advantage of later in our project. 

Another deep work which drew our attention is [Topic Detection And Sentiment Analysis In Twitter Content Related To
COVID-19 From Brazil And The USA](https://reader.elsevier.com/reader/sd/pii/S1568494620309959?token=C97EBF27675DB4CB18FC39AE89B9E0A5D092DE0B14E169DF42E2CAFD8313E6ABA42C2766DC26AFB9C64394F60E7E5906&originRegion=us-east-1&originCreation=20220403000432). Unlike our project the main goal if which is to reveal how the sentiment on various topics was changing over 12 months in 5 different countries, the authors look into how the sentiment was changing over an earlier period of time. They also appear to cover a much larger number of topics, like economic impacts, case reports/statistics, proliferation care, politics, entertainment, treatments, online events, charity, sports and anti-racism protests. Another peculiarity of the study is connected with the fact that it centers around only the USA and Brazil countries and encompasses two languages-English and Portugese. The result of the study unfolds what topics include mainly positive or negative tweets as well what was the trend for their change over the studied period of time. A very valuable part of the study is allocated to the sentiment analysis and topic modeling, which is going to give us some guidance in our own project.  

A good article is [Contextualized Embedding based Approaches for Social Media-specific Sentiment Analysis](https://ieeexplore.ieee.org/abstract/document/9680025), published in 2021. They used a BERTweet model capable of generating contextual word embeddings using a "multi-head self-attention" mechanism. Semantic-level features are then extracted from the learned contextual embeddings using convolutional neural networks or transformer encoders. Their experimental data have demonstrated that BERTweet models incorporating CNNs or Transformers improve performance compared to vanilla BERTweet models. Their research on the integration of BETwee and CNN or Transformer is of great reference value for us.

The model:

![Model](Pics/sakhr3-p8-sakhr-large.gif)    

4. [Classifying Tweet Sentiment Using the Hidden State and Attention Matrix of a Fine-tuned BERTweet Model](https://arxiv.org/abs/2109.14692). 
- In this paper, the author compared the performance of various embedding and classification model combinations on classifying sentiment of tweets. The pipeline of tackling the task in shown below.  ![General pipeline](Pics/pipeline.png?raw=true "General pipeline")
- The result shows that using a fine-tuned Bertweet model to produce tweet embeddings along with a Multi-layer Perceptron Classifier yeilds better result than other embedding+classification combinations. 
![Result](Pics/result.png?raw=true "Result table")
- The detailed of the best model structure they proposed is: 
	- a.  use Bertweet tokenizer to pre-process the tweets.
	- b. fine-tune the parameters of Bertweet model with sentiment specific data.
	- c. combine values from hidden states and attention to generate features.
	- d. use MLP and majority voting to classify. 


### *Evaluation:*

Since the nature of our project is connected with the text classification, namely, sentiment analysis, we are going to train our models and then evaluate them separately on the test sets using ``accuracy`` and ``macro F1`` score. Then we will build an ensamble and evaluate it the same way. Since our models predictions are not perfect and it is quite difficult to reach very high scores in terms of accuracy and f-1, what we are going to do is let our final model make the prediction, then we will consider the confidence and leave only those tweets in the labels of which our model is going to be quite certain about. This will enable us to get more accurate results.


### *Conclusion (optional):*

The purpose of this proposal is to outline the plan for the project and to define its scope. It discusses the steps we are going to undertake in order to answer the problem/question stated in the proposal.
