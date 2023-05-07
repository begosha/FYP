document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('take-picture-btn');
    const captureForm = document.getElementById('capture-form');
    const fileInput = document.querySelector('input[type="file"]');

    // Request permission to access the user's media devices
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            // Set the video source to the user's webcam stream
            video.srcObject = stream;
            video.play();
        })
        .catch(error => {
            console.error('Error accessing user media devices:', error);
        });

    // Add an event listener to the "Capture" button
    captureButton.addEventListener('click', event => {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Create a canvas element to draw the captured image onto
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert the canvas image to a Blob
        canvas.toBlob(blob => {
            // Get the current date and time
            const currentDate = new Date();
            const offset = 6 * 60; // GMT+6 in minutes
            const localDate = new Date(currentDate.getTime() + offset * 60 * 1000);
            const timestamp = localDate.toISOString().slice(0, 19).replace(/:/g, '').replace(/-/g, '').replace('T', '_');
            // Create a File object from the captured Blob with the timestamp-based name
            const imageFile = new File([blob], `captured_image_${timestamp}.jpg`, {type: "image/jpeg"});

            // Assign the File object to the input file field
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(imageFile);
            fileInput.files = dataTransfer.files;

            // Submit the form
            captureForm.submit();
        }, 'image/jpeg', 0.9);
    });
});
