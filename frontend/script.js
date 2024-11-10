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
