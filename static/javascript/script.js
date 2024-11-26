const musicContainer = document.getElementsByClassName("playList")[0];
const audioTag = document.getElementsByClassName("play")[0];
const playingTimeTag = document.getElementById("playingTime");
const currentProgressTag = document.getElementById("currentProgress");
const playButtonTag = document.querySelector(".playButton");
const pauseButtonTag = document.querySelector(".pauseButton");
const previousButtonTag = document.querySelector(".previousButton");
const nextButtonTag = document.querySelector(".nextButton");
const trackImageTag = document.getElementById("trackImages");
const repeatButtonTag = document.getElementById("repeatButton");
const shuffleButtonTag = document.querySelector(".fa-shuffle");

let tracks = [];
let currentPlayingIndex = 0;
let isPlaying = false;
let isShuffle = false;
let repeatMode = 'no-repeat'; // Default repeat mode is "no-repeat"

// Fetch Tracks Dynamically
document.querySelectorAll(".trackItem").forEach((trackElement, index) => {
    const trackID = trackElement.getAttribute("data-track-id");
    const image = trackElement.getAttribute("data-image");
    const title = trackElement.textContent.trim();
    tracks.push({ trackID, title, image });

    trackElement.addEventListener("click", () => {
        currentPlayingIndex = index;
        playTrack(trackID);
    });
});

const playTrack = (trackID) => {
    audioTag.src = `/static/${trackID}`; // Adjust path for Flask
    audioTag.play();
    isPlaying = true;
    updatePlayAndPauseButton();
    updateTrackImage(trackID);
};

// Event Listeners for Play, Pause, Next, Previous
playButtonTag.addEventListener("click", () => {
    if (audioTag.src === "") {
        playTrack(tracks[currentPlayingIndex].trackID);
    } else {
        audioTag.play();
        isPlaying = true;
        updatePlayAndPauseButton();
    }
});

pauseButtonTag.addEventListener("click", () => {
    audioTag.pause();
    isPlaying = false;
    updatePlayAndPauseButton();
});

nextButtonTag.addEventListener("click", () => {
    if (currentPlayingIndex < tracks.length - 1) {
        currentPlayingIndex++;
        playTrack(tracks[currentPlayingIndex].trackID);
    } else if (repeatMode === 'repeat-all') {
        currentPlayingIndex = 0;
        playTrack(tracks[currentPlayingIndex].trackID);
    }
});

previousButtonTag.addEventListener("click", () => {
    if (currentPlayingIndex > 0) {
        currentPlayingIndex--;
        playTrack(tracks[currentPlayingIndex].trackID);
    } else if (repeatMode === 'repeat-all') {
        currentPlayingIndex = tracks.length - 1;
        playTrack(tracks[currentPlayingIndex].trackID);
    }
});

// Update Track Image
const updateTrackImage = (trackID) => {
    const track = tracks.find(track => track.trackID === trackID);
    trackImageTag.src = `/static/${track.image}`;
};

// Update Play/Pause Buttons
const updatePlayAndPauseButton = () => {
    if (isPlaying) {
        playButtonTag.style.display = "none";
        pauseButtonTag.style.display = "inline";
    } else {
        playButtonTag.style.display = "inline";
        pauseButtonTag.style.display = "none";
    }
};

// Update Progress Bar and Playing Time
audioTag.addEventListener("timeupdate", () => {
    const currentTime = Math.floor(audioTag.currentTime);
    const duration = Math.floor(audioTag.duration);
    const currentTimeText = formatTime(currentTime);
    const durationText = formatTime(duration);

    playingTimeTag.textContent = `${currentTimeText} / ${durationText}`;
    currentProgressTag.style.width = `${(500 / duration) * currentTime}px`;
});

const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes.toString().padStart(2, "0")}:${remainingSeconds.toString().padStart(2, "0")}`;
};

// Handle Repeat Button
repeatButtonTag.addEventListener("click", () => {
    if (repeatMode === 'no-repeat') {
        repeatMode = 'repeat-one'; // Repeat the current track
        repeatButtonTag.querySelector('.One').style.display = 'inline'; // Show repeat one icon
    } else if (repeatMode === 'repeat-one') {
        repeatMode = 'repeat-all'; // Repeat the whole playlist
        repeatButtonTag.querySelector('.One').style.display = 'none'; // Hide repeat one icon
    } else {
        repeatMode = 'no-repeat'; // No repeat
        repeatButtonTag.querySelector('.One').style.display = 'none'; // Hide repeat one icon
    }
    console.log(`Repeat mode: ${repeatMode}`);
});

// Handle Shuffle Button
shuffleButtonTag.addEventListener("click", () => {
    isShuffle = !isShuffle;
    if (isShuffle) {
        shuffleButtonTag.style.color = "green"; // Highlight shuffle button
    } else {
        shuffleButtonTag.style.color = "black"; // Reset color
    }
});

// Audio End Event - Handle Repeat or Shuffle Logic
audioTag.addEventListener("ended", () => {
    if (repeatMode === 'repeat-one') {
        playTrack(tracks[currentPlayingIndex].trackID); // Repeat current track
    } else if (repeatMode === 'repeat-all') {
        currentPlayingIndex = (currentPlayingIndex + 1) % tracks.length; // Loop through the playlist
        playTrack(tracks[currentPlayingIndex].trackID);
    } else if (isShuffle) {
        currentPlayingIndex = Math.floor(Math.random() * tracks.length); // Play random track
        playTrack(tracks[currentPlayingIndex].trackID);
    }
});
