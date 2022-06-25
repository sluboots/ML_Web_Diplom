import pickle
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from math import sqrt
import numpy as np
from sklearn.decomposition import TruncatedSVD


def get_class(text):
    LabeledSentence1 = gensim.models.doc2vec.TaggedDocument
    all_content_train = []
    j=0
    for em in df_train['all_texts'].values:
        all_content_train.append(LabeledSentence1(em,[j]))
        j+=1
    print('Number of texts processed: ', j)
    j+=1
    all_content_train.append(LabeledSentence1(text,[j]))
    d2v_model_train = Doc2Vec(all_content_train, vector_size = 100, window = 10, min_count = 500, workers=7, dm = 1,alpha=0.025, min_alpha=0.001)
    load_model_svc = pickle.load(open('model_main_svc.pkl', 'rb'))
    print(len(d2v_model_train.dv.vectors))
    vector = d2v_model_train.infer_vector(text, alpha=0.025, min_alpha=0.01, epochs=5)
    classif = load_model_svc.predict(d2v_model_train.dv.vectors.astype('double'))
    return vector, classif

def get_cluster_and_text_coor(text_vector, text_class):
    name_model = 'model_main_' + str(text_class) + '.pkl'
    name_model_pca = 'model_pca_' + str(text_class) + '.pkl'
    loaded_model_pca = pickle.load(open(name_model_pca,'rb'))
    loaded_model = pickle.load(open(name_model, 'rb'))
    result_clustering = loaded_model.predict([text_vector.astype('double')])
    result_pca = loaded_model_pca.transform([text_vector])
    return result_clustering, result_pca


def lemm_text(text):
    import unicodedata
    from string import punctuation
    russian_stopwords = stopwords.words("russian")
    rdy_tmp = []
    tmp_str = str()
    tmp = []
    doc = nlp(text)
    for token in doc:
        tmp.append(token.lemma_)
    tmp_str = ' '.join(tmp)
    tmp_str = unicodedata.normalize("NFKD", tmp_str)
    tmp_str = tmp_str.replace('   ', ' ')
    rdy_tmp.append(tmp_str)
    return rdy_tmp


def get_link_true(classif, cluster, pca_coor):
    from math import sqrt
    name_df = 'C:\\Users\\slubo\\Desktop\\Diplom_CSV\\df_' + str(classif[0]) + '.csv'
    name_model = 'model_main_' + str(classif[0]) + '.pkl'
    name_model_pca = 'model_pca_' + str(classif[0]) + '.pkl'
    name_model_doc2vec = 'doc2vec_' + str(classif[0]) + '.model'

    id_arr = []
    df = pd.read_csv(name_df)
    loaded_model_pca = pickle.load(open(name_model_pca, 'rb'))
    loaded_model = pickle.load(open(name_model, 'rb'))
    loaded_model_doc2vec = Doc2Vec.load(name_model_doc2vec)

    datapoint = loaded_model_pca.transform(loaded_model_doc2vec.dv.vectors.astype('double'))
    result_vector_arr = []
    for i in range(len(loaded_model.labels_)):
        if cluster == loaded_model.labels_[i]:
            id_arr.append(i)
    for i in range(datapoint[loaded_model.labels_ == cluster].shape[0]):
        result_vector_arr.append(
            (sqrt(np.sum((pca_coor[0] - datapoint[loaded_model.labels_ == cluster][i]) ** 2)), id_arr[i]))
    result_vector_arr.sort()
    link_id = []
    for i in range(5):
        link_id.append(result_vector_arr[i][1])
    links = df.iloc[link_id]['vacancy_url']
    link_array = []
    for link in links:
        link_array.append(link)
    return link_array


def get_cluster(text):
    with open("C:\\Users\\slubo\\PycharmProjects\\Diplom_Work\\Site\\static\\ML_Model\\kmean.pkl", 'rb') as file:
        kmean_model = pickle.load(file)
    mystem = Mystem()
    russian_stopwords = stopwords.words("russian")
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]
    new_text = " ".join(tokens)
    df = pd.read_csv('C:\\Users\\slubo\\Desktop\\ML_diplom1.csv')
    df = df.drop('Unnamed: 0', axis=1)
    count_vect = CountVectorizer()
    len(df['completed_text'])
    df['completed_text'] += new_text
    len(df['completed_text'])
    bow = count_vect.fit_transform(df['completed_text'].values)
    #bow = count_vect.transform([new_text])
    bow.todense()
    result = kmean_model.fit_predict(bow)
    return result[-1]


def get_cluster1(text):
    df = pd.read_csv('C:\\Users\\slubo\\Desktop\\ML_diplom1.csv')
    with open("C:\\Users\\slubo\\PycharmProjects\\Diplom_Work\\Site\\static\\ML_Model\\model_kmean.pkl", 'rb') as file:
        kmean_cluster = pickle.load(file)
    mystem = Mystem()
    russian_stopwords = stopwords.words("russian")
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]
    new_text = " ".join(tokens)
    df = df.append({'completed_text': new_text}, ignore_index = True)
    count_vect = CountVectorizer()
    bow = count_vect.fit_transform(df['completed_text'].values)
    svd = TruncatedSVD(n_components=5, random_state = 0)
    X_2d = svd.fit_transform(bow.todense())
    result = kmean_cluster.predict(X_2d)
    return X_2d, result[-1], result


def get_link(text_number, cluster, labels):
    print(text_number[-1])
    print(len(labels))
    df = pd.read_csv('C:\\Users\\slubo\\Desktop\\ML_diplom1.csv')
    df_link = pd.read_csv('C:\\Users\\slubo\\Desktop\\vacancy1.csv')
    df['vacancy_url'] = df_link['vacancy_url']
    with open("C:\\Users\\slubo\\PycharmProjects\\Diplom_Work\\Site\\static\\ML_Model\\model_kmean.pkl", 'rb') as file:
        kmeans_cluster = pickle.load(file)
    id_cluster= []
    tmp = []
    array_length = []
    for i in range(len(labels)):
        if labels[i] == cluster:
            id_cluster.append(i)
    result_vector_array = []
    tmp_array = []
    for i in range(text_number[labels == cluster].shape[0]-1):
        for j in range(5):
            tmp_array.append(text_number[-1][j] - text_number[labels == cluster][i][j])
        result_vector_array.append((tmp_array, id_cluster[i]))
        tmp_array = []
    for i in range(len(result_vector_array)):
        for j in range(len(result_vector_array[i][0])):
            tmp.append(result_vector_array[i][0][j]**2)
        new_tmp = np.array(tmp)
        array_length.append((sqrt((np.sum(tmp))), id_cluster[i]))
        tmp = []
        new_tmp = []
    array_length.sort()
    link_id = []
    for i in range(5):
        link_id.append(array_length[i][1])
    links = df.iloc[link_id]['vacancy_url']
    link_array = []
    for link in links:
        link_array.append(link)
        print(link)
    return link_array

