
function playSuggestedVideo(videoSrc, title, description) {
    const videoPlayer = document.getElementById('main-video');
    const videoTitle = document.getElementById('video-title');
    const videoDescription = document.getElementById('video-description');

    // Update the video source, title, and description
    videoPlayer.src = videoSrc;
    videoTitle.textContent = title;
    videoDescription.textContent = description;

    // Play the new video
    videoPlayer.play();
}

// Voice recognition for the microphone button
if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    // Get the search input and mic button elements
    const searchInput = document.getElementById("search");
    const micButton = document.getElementById("micBtn");

    micButton.addEventListener("click", () => {
        recognition.start();
    });

    recognition.onresult = (event) => {
        // Get the transcript of what was said and fill the search input
        const transcript = event.results[0][0].transcript;
        searchInput.value = transcript;
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
    };
} else {
    alert("Your browser does not support speech recognition.");
}
