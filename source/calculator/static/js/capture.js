 document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('take-picture-btn');
    const photo = document.getElementById('captured-image');

    function setupCamera() {
      navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(stream => {
          video.srcObject = stream;
          video.play();
        })
        .catch(err => {
          console.error("An error occurred: " + err);
        });
    }

    function takePhoto() {
      const context = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imageData = canvas.toDataURL('image/png');
      photo.setAttribute('src', imageData);
    }
    // captureButton.addEventListener('click', takePhoto);
    setupCamera();
  });
