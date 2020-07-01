This program usedb pandas to read csv file, matplotlib to draw graphs, and math to do the calculation.

Before run the program, you need to modify the filepath of csv file at line 14.In my code, I used the relative path. 

During the running, you will be ask to input A or B or C or D to choose run basetest or experiment1  or experiment2 or experiment3.

Due to the experiment4, in my understanding,  remove the top 5% 10% 15% 20% 25% most frequent words are words' frequency sorted descending order

and remove percentage word. Program will take a bit of time when generate second graph because of the massive data.(About 20s)

 if it is still not work you can contact marvelrex0725@gmail.com :) 

For each one, I output the model, vocabulary, and results.

In the code, I created lots of datastructure to store and I add comments to each one. To be convient, I summarized all important data structure here.

trainingset: All data that between 2018-01-01(included) to 2019-01-01(excluded)

testingset: Store all data after 2019-01-01(included)

Story: Store all data which post type is story

Ask: Store all data which post type is ask_hn

Show: Store all data which post type is show_hn

Poll: Store all data which post type is poll

vocabularys: A 2-d list that include each title and each title include all words.

wordcount: Dict record all word and its frequency.

wordcountsorted: List that record all word and frequency in descending order.

dicttrain: record single word and its type as key and frequency as value  {(word,typle) : frequency}

storyfre: The word is story and its frequency

askfre: The word is ask_hn and its frequency

showfre: The word is show_hn and its frequency

pollfre: The word is poll and its frequency

vocset: record all words distinct

dictprob: Record the probabilty for a single word with different post type {word:(P(word|story),P(ask_hn|story),P(show_hn|story),P(poll|story))}

