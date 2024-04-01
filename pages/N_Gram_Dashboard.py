import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import streamlit as st

def load_data_n_gram():
    penguin_file = st.file_uploader("Select Your Local n-gram CSV file")
    if penguin_file is None:
        st.stop()
    # Create a new column 'Name_Count' to store the counts
    n_gram_df = pd.read_csv(penguin_file)
    # col_names = senti_df.columns.tolist()
    # senti_df[col_names[0]] = senti_df[col_names[0]].map(lambda x: x[:3].strip().replace(".","") if x[0].isdigit() else x)
    # print(senti_df[col_names[0]])
    return n_gram_df

loaded_df = load_data_n_gram()

# Function to generate bigrams for a document
def get_bigrams(sentences):
  bigrams = []
  for sentence in sentences:
    for i in range(len(sentence) - 1):
      bigram = (sentence[i], sentence[i+1])  # Create bigram tuple
      bigrams.append(bigram)
  return Counter(bigrams)

def replace_bigrams_in_sentences(sentences, bigram_counts, threshold=1):
  """
  Replaces bigrams in sentences with concatenated string based on frequency.

  Args:
      sentences: List of lists, where each inner list is a tokenized sentence.
      bigram_counts: Counter object containing bigram frequencies.
      threshold: Minimum frequency for considering a bigram frequent (default=1).

  Returns:
      A new list of lists with bigrams replaced in each sentence.
  """
  updated_sentences = []
  for sentence in sentences:
    updated_sentence = []
    flag = False
    skip = 0
    for i in range(len(sentence)-1):
        if skip>0 and skip == i:
            continue
        bigram = (sentence[i], sentence[i+1])
        if bigram in bigram_counts and bigram_counts[bigram] > threshold:
            # Replace bigram with concatenated form
            concatenated_bigram = "_".join(bigram)
            updated_sentence.append(concatenated_bigram)
            if i == len(sentence)-1:
                flag = True
            skip = i+1
        else:
            # Keep individual words for infrequent bigrams
            updated_sentence.append(sentence[i])  # Add both words separately
    # Add the last word (no bigram check needed)
    if flag == False:
        updated_sentence.append(sentence[-1])
    updated_sentences.append(updated_sentence)
  return updated_sentences

def bigram_2_word_cloud(df,question):
    df_C_F = df.loc[:,question].dropna().apply(eval).tolist()
    bigram_counts = get_bigrams(df_C_F)
    # Replace bigrams with threshold of 1 (appearing more than once)
    threshold = 2
    updated_df_C_F = replace_bigrams_in_sentences(df_C_F, bigram_counts, threshold)
    # Join sentences with "." separator
    joined_string_sentences = [" ".join(sentence) for sentence in updated_df_C_F]
    # Combine all strings into a single string
    all_text = " ".join(joined_string_sentences)
    wordcloud = WordCloud(width = 500, height = 500,
                background_color ='white',
                min_font_size = 5).generate(all_text)
    return wordcloud

options = st.multiselect(
    'Which question you want to analyze',
    loaded_df.columns.tolist())
# print(len(options)==0)
maping_dict = {}

if len(options)==0:
    st.stop()
else:
    for i,opt in enumerate(options):
        maping_dict["Word_Cloud_{}".format(i)] = opt
    st.write(maping_dict)
    for tab,Q in zip(st.tabs(maping_dict.keys()),maping_dict.values()):
        with tab:
            # print(Q)
            word_cloud = bigram_2_word_cloud(loaded_df,Q)
            try:
                # plot the WordCloud image                       
                plt.figure(figsize = (5, 5), facecolor = None)
                plt.imshow(word_cloud)
                plt.axis("off")
                plt.tight_layout(pad = 0)
                st.pyplot(plt)
            except:
                st.rerun()
# plt_word_cloud = bigram_2_word_cloud(loaded_df,loaded_df.columns[0])
# st.pyplot(plt_word_cloud)