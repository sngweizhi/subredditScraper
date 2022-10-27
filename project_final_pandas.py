# Nick Sng
# COMP112-03
# Python Project - Subreddit wordcloud generator

##libraries
import pandas as pd
import matplotlib.pyplot as plt
import os
import praw
import sys
from wordcloud import WordCloud
import numpy as np
from PIL import Image


##Functions

def split_words(text):
    '''
    sig: list[str] -> list[str]
    splits a list of sentences into a list of words
    '''
    new_list = []
    for s in text:
        new_list.extend(s.split())
    return new_list

def only_alpha(wordlist):
    '''
    sig: list[str] -> list[str]
    removes punctuations and numbers from strings
    '''
    acc = ''
    acc2 = []
    for w in wordlist:
        for c in w:
            if c.isalpha() or c.isdigit() == True:
                acc += c.upper()
        if acc != '':
            acc2.append(acc)
        acc = ''
    new_wordlist = acc2
    return new_wordlist

def remove_stopwords(wordlist):
    '''
    sig: list[str] -> list[str]
    removes common words from list of words
    '''
    stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
    stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
    stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
    stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
    stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
    stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
    stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
    stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
    stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
    stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
    stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
    stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
    stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
    stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
    stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
    stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
    stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
    stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
    stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
    stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
    stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
    stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
    stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
    stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
    stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
    stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
    stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
    stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
    stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
    stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
    stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
    stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
    stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
    stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
    stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
    stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
    stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
    stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
    stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
    stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
    stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
    stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
    stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
    stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
    stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
    stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
    stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
    stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
    stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
    stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
    stopwords += ['yours', 'yourself', 'yourselves']
    new_wordlist = [w for w in wordlist if w.lower() not in stopwords and len(w)>1]
    return new_wordlist

def word_frequency_dict(text):
    '''
    sig: list[str] -> dict{str:int}
    counts frequency of words and stores values in a dictionary
    '''
    dictionary = {}
    for w in text:
        if w not in dictionary:
            dictionary[w]=1
        else:
            dictionary[w]+=1
    return dictionary

def dict_sort(dictionary):
    '''
    sig: dict{str:int} -> list[tuple(str, int)]
    sorts the words in descending frequency
    '''
    dict_sort = [(dictionary[key],key) for key in dictionary]
    dict_sort.sort()
    dict_sort.reverse()
    new_dict = [(x[1],x[0]) for x in dict_sort] 
    return new_dict

def word_process_panda(text): #word processing for pandas method
    text = text.split()
    text = only_alpha(text)
    text = remove_stopwords(text)
    return text

def word_processing(text):
    '''
    sig: list[str] -> list[tuple(str, int)]
    combines word processing functions
    '''
    text = split_words(text)
    text = only_alpha(text)
    text = remove_stopwords(text)
    text = word_frequency_dict(text)
    text = dict_sort(text)
    return text

def get_sub():
    '''
    sig: None -> str
    returns user input for subreddit name
    '''
    subreddit = input("Input a name of a subreddit. \n")
    return subreddit
    
def get_time():
    '''
    sig: None -> str
    returns user input for timeline to scrape
    '''
    timeline_dict={'a':'all','d':'day','h':'hour','m':'month','w':'week','y':'year'}
            
    time = input("Input a timeline for scraping top 1000 posts: 'a' = all, 'd' = day, 'h'= hour, 'm' = month, 'w' = week, 'y' = year")
    
    while True:
        if time in timeline_dict:
            timeline = timeline_dict[time.lower()]
            break
        else:
            print("Invalid timeline. Please try again.")
    return timeline

def get_reddit(sub, time):
    '''
    sig: str, str -> df
    scrapes subreddit and stores data in a pandas dataframe
    '''
    posts = []
    subreddit = reddit.subreddit(sub)
    for post in subreddit.top(time_filter=time, limit=1000):
        posts.append([post.title, post.subreddit, post.created, post.num_comments, post.score])
    posts = pd.DataFrame(posts,columns=['title', 'subreddit','created','comments','upvotes'])
    posts['created'] = pd.to_datetime(posts['created'],unit='s') #change unix time to normal date time
    posts['processed_title']=posts['title'].apply(word_process_panda)
    posts = posts.explode("processed_title").reset_index().drop("index",1)
    return posts

def to_csv(data, name):
    '''
    sig: df -> None
    saves dataframe as csv in current working directory
    '''
    while os.path.isfile(name+'.csv'): #if file name already exists
        file_exist = input("A file with same name already exists. Input 'o' to overwrite. Input 'r' to rename\n")
        if file_exist.lower() == 'o':
            break
        elif file_exist.lower() == 'r':
            name = input("Rename the file\n")
        else:
            print("Invalid input.")
                    
    data.to_csv ('{}.csv'.format(name), header=True)
    print("\n{}.csv has been created and saved at {}".format(name, os.path.abspath(name+'.csv')))

def search_dir():
    '''
    sig: None -> None
    searches current working directory for CSV files
    '''
    file_names = []
    dir_content = os.listdir()
    print("Available datasets:\n")
    for file in dir_content:
        if os.path.isfile(file) and ".csv" in file:
            file_names.append(file)
    if len(file_names) > 0:
        for filename in file_names:
            print(filename)
    else:
        print('No CSV file available in current directory. Please change directory.')
        
def change_dir():
    '''
    sig: None -> None
    changes current working directory
    '''
    try:
        changecwd = input('Input path to change current working directory to. \n')
        os.chdir(changecwd)
    except FileNotFoundError:
        print('Sorry, that is an invalid path. Please try again.\n')

def plot_cloud(wordcloud):
    '''
    sig: wordcloud -> None
    plots the wordcloud
    '''
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud) 
    plt.axis("off")
    plt.show()
    return

#reddit authentication
reddit = praw.Reddit(client_id='NRkaMpo0QN6JfA', client_secret='c_rVdXZIs0pQQfSii3lUHia0IzgORw', user_agent='word cloud generator v1.0 by /u/seerealentrepreneur')

## 1. PRAW Scraping of subreddit


while True:

    landingpage = '''\n
-------------------------------------------------------------
*****Welcome to the Subreddit Wordcloud Generator V1.0*****
*------------------Developed by Nick Sng------------------*

Type the following commands:

    's' - to scrape a new subreddit

    'w' - to generate a wordcloud from an existing dataset

    'e' - to exit the program

-------------------------------------------------------------\n'''
    
    user_action = input(landingpage)


    if user_action.lower() == 's':
        sub = get_sub()    
        time = get_time()

        try:
            
            dataset = get_reddit(sub, time)
            
            print(dataset)

            to_csv(dataset, sub)
            
        except ValueError:
            print('Invalid input.')
        except:
            print('Invalid Subreddit.')

    elif user_action.lower() == 'w':


## 2. Word processing

        while True:
            searchpage = '''
***Search for a dataset to use for wordcloud generation***

Current Working Directory: {}

Input 's' to search current directory | 'c' to change directory |'d' - to continue to selection of dataset.\n'''.format(os.getcwd())

            wd = input(searchpage)
            if wd.lower() == 's':
                
                search_dir()
            
            elif wd.lower() == 'c':
                
                change_dir()
              
            elif wd.lower() == 'd':
                break
            else:
                print('Invalid command.')
            
        #read csv file
        while True:
            dataset = input("Input name of dataset to use for the word cloud. \n")
            try:
                df = pd.read_csv(dataset+".csv", index_col=0)
                break
            except:
                print("Invalid dataset. Please try again.")
    

        #word frequency histogram
        
        print("There are {} posts in this dataset.".format(len(df.title)))

        text_string = df['processed_title'].tolist()

        text_string = split_words(text_string)
        
        text_frequency = word_frequency_dict(text_string)

        text_frequency = dict_sort(text_frequency)

        df2 = pd.DataFrame(text_frequency, columns=["Word","Frequency"])

        words_cloud = df2
        words_cloud.index = words_cloud.index+1 #set index to start from 1
        number_words_show = 10 

        print("Table of word frequencies:\n"+"----------------------------\n", words_cloud.iloc[:number_words_show],"\n.\n.\n.\n"+"----------------------------\n")
        print("Total number of unique words in dataset:", len(words_cloud),"\n")

# 3. Word cloud generation

        while True:
            wordcloud_main = input("*****Word Cloud Generator*****\nInput 's' to show more words in the frequency table. \
Input 'r' to remove specific words. Input 'l' to limit the number of words. Input 'wc' to generate word cloud. \
Input 'g' to plot a bar graph. Input 'e' to exit to main page.\n")

            if wordcloud_main.lower() in "slr":
            
                if wordcloud_main.lower() == "s":
                    number_words_show = int(input("Input number of words to show:\n")) 
                    
                elif wordcloud_main.lower() == "l":
                    number_words_cloud = int(input("Input max number of words for word cloud:\n"))
                    words_cloud = words_cloud.iloc[:number_words_cloud]

                elif wordcloud_main.lower() == 'r':
                    word_remove_list = []
                    while True:
                        word_remove = str(input("Input words to remove. Input 'r' to remove all words in list. Input 'e' to cancel.\n"))
                        if word_remove == 'r':
                            break
                        elif word_remove =='e':
                            print('Operation cancelled.')
                            word_remove_list = []
                            break
                        elif word_remove.upper() not in words_cloud['Word'].values:
                            print("Invalid word. Please try again.")
                            continue
                        elif word_remove.upper() in word_remove_list:
                            print("Word already exists.")
                            continue
                        word_remove_list.append(word_remove.upper())
                        print('Words to remove:',word_remove_list)
                    wordindex = words_cloud[words_cloud["Word"].isin(word_remove_list)].index
                    words_cloud = words_cloud.drop(wordindex)
                    words_cloud = words_cloud.reset_index(drop=True)
                    words_cloud.index = words_cloud.index+1
         
                print("Table of word frequencies:\n"+"----------------------------\n", words_cloud.iloc[:number_words_show],"\n.\n.\n.\n"+"----------------------------\n")
                print("Total number of unique words in dataset:", len(words_cloud),"\n")

            elif wordcloud_main.lower() == 'g':
                words_plot = words_cloud[:20].sort_values(by='Frequency')
                words_plot.plot.barh(x='Word',y='Frequency', title='Frequency of Top 20 words')
                plt.show()
                
            elif wordcloud_main.lower() == 'wc':
                
                while True:
                    select_mask = input("Would you like to use a mask? Y/N\n")
                    if select_mask.lower() == 'y':
                        file_names = []
                        dir_content = os.listdir()
                        print("Available masks:\n")
                        for file in dir_content:
                            if os.path.isfile(file) and ".png" in file:
                                file_names.append(file)
                        if len(file_names) > 0:
                            for filename in file_names:
                                print(filename)
                        
                            while True:
                                mask_name = input("Input name of mask you would like to use. Input 'e' to cancel\n")
                                if mask_name.lower() == 'e':
                                    break
                                try:
                                    mask = np.array(Image.open(mask_name+".png"))
                                    break
                                except:
                                    print("Invalid input. Please try again.")
                            break
                        else:
                            print('No PNG masks are available in the current directory. Place a suitable PNG file in the directory and try again.')
                    if select_mask.lower()=='n':
                        mask_name = 'default'
                        mask = None
                        break

                while True:
                    background_dict = {'w':'white','b':'black','s':'salmon','c':'coral','r':'tomato'}
                    background_color_select = input("Select a background color for the word cloud. 'w' = white, 'b' = black, 's' = salmon, 'c' = coral, 'r' = red\n")
                    if background_color_select in background_dict:
                        background_color = background_dict[background_color_select]
                        break
                    else:
                        print("Invalid input. Please try again.")
                        
                while True:
                    colormap_dict = {'p':'pastel1','r':'rainbow','a':'autumn','sp':'spring','w':'winter','su':'summer'}
                    colormap_select = input("Select a colormap for the words. 'p' = pastel, 'r' = rainbow, 'a' = autumn, 'sp' = spring, 'w' = winter, 'su' = summer\n") 
                    if colormap_select in colormap_dict:
                        colormap = colormap_dict[colormap_select]
                        break
                    else:
                        print("Invalid input. Please try again.")
            
                print("Generating wordcloud of {} dataset with {} mask, {} background and {} colormap...".format(dataset,mask_name,background_color,colormap))
                
                
                cloud_text = words_cloud.set_index("Word").to_dict()
                
                wordcloud = WordCloud(width = 3000, height = 1500, random_state=1, \
                      background_color=background_color, colormap='Pastel1', \
                      collocations=False, mask = mask, include_numbers=True).generate_from_frequencies(cloud_text['Frequency'])
                
                plot_cloud(wordcloud)
                
                while True:
                    save_cloud = input('Would you like to save the wordcloud as a JPG file? Y/N\n')
                    if save_cloud.lower() == 'y':
                        cloud_name = dataset+'.jpg'
                        wordcloud.to_file(cloud_name)
                        print(cloud_name,'has been saved at',os.path.abspath(cloud_name),"\n")
                        break
                    elif save_cloud.lower() == 'n':
                        break
                    else:
                        print("Invalid input. Please try again.")
                
            elif wordcloud_main.lower() == "e":
                break
            
            else:
                print("Invalid input. Please try again.")
                
    elif user_action.lower() == "e":
        print("Thank you for using Subreddit Wordcloud Generator V1.0!")
        sys.exit()
    
    else:
        print('Invalid input. Please try again.')
        







