async function getRecommendations(videoId) {
    try {
      const response = await fetch('http://127.0.0.1:8000/recommend/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ course_id: videoId }), // The key must match what the FastAPI backend expects
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      let recommendedCourses = [];
      const data = await response.json();
      for(let i=0;i<data.recommended_courses.length;i++){
        recommendedCourses.push(data.recommended_courses[i].videoId);
      console.log('Recommended Courses:', data.recommended_courses[i].videoId);
      }
    //   const recommendedCourses = data.recommended_courses;
      return recommendedCourses;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  }

async function fetching(){
    let new_courses=await getRecommendations('sM2C-SsREgM');
    console.log(new_courses);
}
// getRecommendations('sM2C-SsREgM');
fetching();