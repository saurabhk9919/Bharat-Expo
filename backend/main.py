# # Import necessary libraries
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Initialize FastAPI app
# app = FastAPI()

# # Load course data (Assume we have a CSV file with 'title', 'description', 'url')
# data = pd.read_csv('youtube_api.csv')  # Update the filename as needed

# # Preprocess data
# data['description'] = data['description'].fillna('').str.lower()

# # TF-IDF Vectorization
# vectorizer = TfidfVectorizer(stop_words='english')
# tfidf_matrix = vectorizer.fit_transform(data['description'])

# # Compute Cosine Similarity Matrix
# cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# # Pydantic model for input validation
# class RecommendationRequest(BaseModel):
#     course_id: int

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Course Recommendation API!"}

# @app.post("/recommend")
# def recommend_courses(request: RecommendationRequest):
#     course_id = request.course_id
    
#     # Validate the course ID
#     if course_id < 0 or course_id >= len(data):
#         raise HTTPException(status_code=404, detail="Course not found")
    
#     # Get similarity scores for the input course
#     similarity_scores = list(enumerate(cosine_sim_matrix[course_id]))
#     # Sort courses based on similarity scores
#     sorted_courses = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
#     # Get top 5 recommendations (excluding itself)
#     top_recommendations = sorted_courses[1:6]
#     recommendations = [
#         {
#             "title": data['title'].iloc[i[0]],
#             "url": data['url'].iloc[i[0]],
#             "similarity_score": i[1]
#         } for i in top_recommendations
#     ]
    
#     return {"recommendations": recommendations}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load your dataset (make sure to specify the correct path)
df = pd.read_csv('youtube_api.csv')  # Assuming columns like 'course_id', 'name', 'description', 'video_id'

# Build the TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'])

# FastAPI setup
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Allow requests from your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Request model
class CourseIDRequest(BaseModel):
    course_id: str

@app.post("/recommend/")
async def recommend_courses_by_id(request: CourseIDRequest):
    # Get the course_id from the request
    input_course_id = request.course_id
    
    # Check if the course ID exists
    if input_course_id not in df['videoId'].values:
        raise HTTPException(status_code=404, detail="Course ID not found")

    # Get the index of the input course
    input_index = df.index[df['videoId'] == input_course_id].tolist()[0]

    # Compute cosine similarity scores
    cosine_similarities = linear_kernel(tfidf_matrix[input_index], tfidf_matrix).flatten()

    # Get top recommended courses (excluding the input course itself)
    similar_indices = cosine_similarities.argsort()[-6:-1][::-1]
    recommended_courses = df.iloc[similar_indices][['title', 'videoId','channelTitle']]

    # Convert recommended courses to a list of dictionaries for the response
    response = recommended_courses.to_dict(orient='records')
    
    return {"recommended_courses": response}
