from newspaper import Article
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

#download the punkt package
nltk.download('punkt', quiet = True)

#get the article
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus = article.text

#print the article's test
# print(corpus)
# print('\n')

#tokenisation
text = corpus
sentence_list = nltk.sent_tokenize(text)

# print(sentence_list)

# a function to return a random greeting respone to a user's greeting
def greeting_response(text):
  text = text.lower()

  #bots greeting
  bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'hola']
  #user's greeting
  user_greetings = ['hi', 'hello', 'hey', 'hola', 'greetings', 'wassup']

  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)

# sorts the indices according to the descending order (bubble sort)
def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        #swap
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp
  return list_index

#create the bot's response
def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  # usr input appended at the last
  bot_response = ''
  cm = CountVectorizer().fit_transform(sentence_list)   # converts the sentence_list into a matrix of frequency of words per document
  similarity_scores = cosine_similarity(cm[-1], cm)   # creates a similarity_scores list containing the similarity of the user_input and the whole siilarity_score matrix with each other
  similarity_scores_list = similarity_scores.flatten()    # converts the 2D matrix into 1D
  index = index_sort(similarity_scores_list)    # sorts the indices according to the value present int the similarity_scores_list
  index = index[1:]   # the first value is neglected as it is the cosine_similarity of the usr_input with itself and has the highest value, otherwise the bot will reply whatever the us typos
  response_flag = 0

  j = 0   # flag used to give only the first 2 matching sentences
  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0.0: # similarity scores should be > 0.0 as cos value = 0.0 indicates 180 deg
      bot_response = bot_response+' '+sentence_list[index[i]]
      response_flag = 1
      j += 1
    if j > 2:
      break
  if response_flag == 0:
    bot_response = bot_response+' '+'I apologise, I dont understand'

  sentence_list.remove(user_input)
  return bot_response

#start the chat
print('Doc Bot: Hi! I am Doctor Bot or Doc Bot for short, I will answer your queries about Chronic Kidney Disease. If you want to exit, type bye')

exit_list = ['exit', 'see you later', 'bye', 'quit', 'break']

while(True):
  user_input = input("Your response : ")
  if user_input.lower() in exit_list:
    print('Doc Bot: Chat with you later! Bye.')
    break
  else:
    if greeting_response(user_input) != None:
      print('Doc Bot: '+greeting_response(user_input))
    else:
      print('Doc Bot: '+bot_response(user_input))