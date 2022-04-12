from wordcloud import WordCloud

def word_cloud(docs, exclusion=[], background="white"):
    # Join the different processed titles together.
    wc_docs = ' '.join([str(doc) for doc in docs])
    wc_docs = wc_docs.replace('tidak','')
    if exclusion:
        for i in exclusion:
            wc_docs = wc_docs.replace(i,'')
    # Create a WordCloud object
    wordcloud = WordCloud(background_color=background, max_words=220, width=700, height=350, contour_width=2, colormap='Set2', contour_color='steelblue', collocations=False)
    wordcloud.generate(wc_docs)
    # Visualize the word cloud
    return wordcloud.to_image()