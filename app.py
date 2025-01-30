
from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import secrets
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

email = ""

# Download NLTK data if not already present
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
"""if not os.path.exists(nltk_data_path):
    nltk.download('punkt', download_dir=nltk_data_path)
    nltk.download('stopwords', download_dir=nltk_data_path)
    nltk.download('wordnet', download_dir=nltk_data_path)"""

# Initialize NLTK
nltk.data.path.append(nltk_data_path)

app = Flask(__name__)

# Load hotel data (replace this with your actual hotel data)
hotel = pd.read_csv('final_hotel_details.csv',encoding='latin1')

sender_email = 'hotelrecommendationsystem@gmail.com'  # Replace with your email address
sender_password = 'xxrg caiu idgo tmnq'  # Replace with your email password
smtp_server = 'smtp.gmail.com'
smtp_port = 587


@app.route('/send_email_for_login', methods=['POST'])
def send_email_for_login():
    # Create message
    data = request.json
    receiver_email = data.get('email')
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Hotel Recommendation'

    body = f'Hello,\n\nWelcome to Our Hotel Recommendation System!\n\nThank you for signing in to our Hotel Recommendation System! We are thrilled to have you on board.\n\nHave a Good Day'
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(f'Email notification sent to {receiver_email} successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')



@app.route('/send_email_verification_code', methods=['GET'])
def send_email_for_verfication():
    # Create message
    print("In send_email_for_verification")
    receiver_email = request.args.get('email')
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Hotel Recommendation'

    body = f'Hello,\n\nTo complete your registration, please use the following verification code:\n\nVerification Code: 748732\n\nIf you did not request this verification code, please ignore this email.\n\nBest Regards,\nHotel Recommendation System Team'
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(f'Email notification sent to {receiver_email} successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

def citybased(city):
    hotel['city']=hotel['city'].str.lower()
    citybase=hotel[hotel['city']==city.lower()]
    citybase=citybase.sort_values(by='starrating',ascending=False)
    citybase.drop_duplicates(subset='hotelcode',keep='first',inplace=True)
    if(citybase.empty==0):
        hname=citybase[['hotelname','starrating','address','roomamenities','ratedescription','url']]
        return hname.head()
    else:
        print('No Hotels Available')
def recommender(city,number,features,price):
    hotel['city']=hotel['city'].str.lower()
    hotel['description']=hotel['ratedescription'].str.lower()
    features=features.lower()
    features_tokens=word_tokenize(features)
    sw=stopwords.words('english')
    lemm=WordNetLemmatizer()
    f1_set={w for w in features_tokens if not w in sw}
    f_set=set()
    for se in f1_set:
        f_set.add(lemm.lemmatize(se))
    reqbased=hotel[hotel['city']==city.lower()]
    reqbased=reqbased[reqbased['guests_no']==number]
    reqbased=reqbased[reqbased['price']<=price].sort_values(by='starrating',ascending=False)
    reqbased=reqbased.set_index(np.arange(reqbased.shape[0]))
    cos=[]
    for i in range(reqbased.shape[0]):
        temp_tokens=word_tokenize(reqbased['description'][i])
        temp1_set={w for w in temp_tokens if not w in sw}
        temp_set=set()
        for se in temp_set:
            temp_set.add(lemm.lemmatize(se))
        rvector=temp_set.intersection(f_set)
        cos.append(len(rvector))
    reqbased['similarity']=cos
    reqbased=reqbased.sort_values(by='similarity',ascending=False)
    reqbased.drop_duplicates(subset='hotelcode',keep='first',inplace=True)
    return reqbased[['city','hotelname','roomtype','price','guests_no','starrating','address','description','similarity','url']].head(10)

def requirementbased(city,number,features):
    hotel['city']=hotel['city'].str.lower()
    hotel['roomamenities']=hotel['roomamenities'].str.lower()
    features=features.lower()
    features_tokens=word_tokenize(features)  
    sw = stopwords.words('english')
    lemm = WordNetLemmatizer()
    f1_set = {w for w in features_tokens if not w in sw}
    f_set=set()
    for se in f1_set:
        f_set.add(lemm.lemmatize(se))
    reqbased=hotel[hotel['city']==city.lower()]
    reqbased=reqbased[reqbased['guests_no']==number]
    reqbased=reqbased.set_index(np.arange(reqbased.shape[0]))
    l1 =[];l2 =[];cos=[];
    lemm = WordNetLemmatizer()

    for i in range(reqbased.shape[0]):
        temp_tokens=word_tokenize(reqbased['roomamenities'][i])
        temp1_set={w for w in temp_tokens if not w in sw}
        temp_set=set()
        for se in temp1_set:
            temp_set.add(lemm.lemmatize(se))
        rvector = temp_set.intersection(f_set)
        cos.append(len(rvector))

    temp_lemmatized = [lemm.lemmatize(se) for se in temp1_set]
    temp_text = ' '.join(temp_lemmatized)
    f_lemmatized = [lemm.lemmatize(se) for se in f_set]
    f_text = ' '.join(f_lemmatized)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([temp_text, f_text])
    cosine_sim = cosine_similarity(X[0], X[1])
    reqbased['similarity'] = cosine_sim[0][0]
    reqbased = reqbased.sort_values(by='similarity', ascending=False)

    reqbased.drop_duplicates(subset='hotelcode', keep='first', inplace=True)
    reqbased=reqbased.sort_values(by='similarity',ascending=False)
    reqbased.drop_duplicates(subset='hotelcode',keep='first',inplace=True)
    return reqbased[['city','hotelname','roomtype','guests_no','starrating','address','roomamenities','similarity','url']].head(10)

def recommende(city, number, features, price):
    hotel['city'] = hotel['city'].str.lower()
    hotel['description'] = hotel['ratedescription'].str.lower()
    features = features.lower()
    features_tokens = word_tokenize(features)
    sw = stopwords.words('english')
    lemm = WordNetLemmatizer()
    f1_set = {w for w in features_tokens if not w in sw}
    f_set = set()
    for se in f1_set:
        f_set.add(lemm.lemmatize(se))
    
    # Content-based filtering using TF-IDF and K-means clustering
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(hotel['description'])
    
    k = 10  # Number of clusters
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(tfidf_matrix)
    hotel['cluster'] = kmeans.labels_
    
    # Filter hotels based on city, number of guests, and price
    reqbased = hotel[(hotel['city'] == city.lower()) & 
                     (hotel['guests_no'] == number) & 
                     (hotel['price'] <= price)]
    
    # Get hotels from the same cluster as the user's preferences
    cluster_id = kmeans.predict(tfidf_vectorizer.transform([features]))[0]
    reqbased = reqbased[reqbased['cluster'] == cluster_id]
    
    # Sort based on star rating
    reqbased = reqbased.sort_values(by='starrating', ascending=False)
    reqbased = reqbased.set_index(np.arange(reqbased.shape[0]))
    
    # Calculate similarity based on keyword matching
    cos = []
    for i in range(reqbased.shape[0]):
        temp_tokens = word_tokenize(reqbased['description'][i])
        temp1_set = {w for w in temp_tokens if not w in sw}
        temp_set = set()
        for se in temp_set:
            temp_set.add(lemm.lemmatize(se))
        rvector = temp_set.intersection(f_set)
        cos.append(len(rvector))
    reqbased['similarity'] = cos
    
    # Sort based on similarity and other factors
    reqbased = reqbased.sort_values(by='similarity', ascending=False)
    reqbased.drop_duplicates(subset='hotelcode', keep='first', inplace=True)
    
    return reqbased[['city','hotelname', 'roomtype', 'price', 'guests_no', 'starrating', 'address', 'description', 'similarity', 'url']].head(10)

def generate_verification_code(length=6):
    alphabet = "0123456789"  # You can include more characters if needed
    verification_code = ''.join(secrets.choice(alphabet) for _ in range(length))
    return verification_code

    
@app.route('/')
def index():
    return render_template('sample.html')

@app.route('/logsign.html')
def login_signup():
    return render_template('logsign.html')

@app.route('/forgotpass.html')
def forgot_pass():
    return render_template('forgotpass.html')

@app.route('/verification.html')
def verification():
    return render_template('verification.html')

@app.route('/login', methods=['GET'])
def login_page():
    success = request.args.get('success', default=False, type=bool)
    if success:
        return render_template('login.html', success=True)
    else:
        return render_template('login.html')

@app.route('/input.html')
def input():
    return render_template('input.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        city = request.form['location']
        number = request.form['guest']
        price = request.form['Budget']
        features = request.form['amenities']

        if number == '' and price == '' and features == '':
            recommended_hotels = citybased(city)

        elif price == '':
            number = int(request.form['guest'])
            recommended_hotels = requirementbased(city,number,features)

        else:
            number = int(request.form['guest'])
            price = int(request.form['Budget'])
            recommended_hotels = recommender(city, number, features, price)

        if recommended_hotels.empty:
            return render_template('no_results.html')
        else:
            return render_template('recommendations.html', recommended_hotels=recommended_hotels)
    except Exception as e:
        print(e)
        return render_template('error.html', error_message=str(e))


if __name__ == '__main__':
    app.run(debug=True)
