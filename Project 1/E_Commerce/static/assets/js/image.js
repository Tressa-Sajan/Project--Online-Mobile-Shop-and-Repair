document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const fileInput = document.getElementById('fileInput');
    const saveBtn = document.getElementById('saveBtn');

    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function () {
            const img = new Image();
            img.onload = function () {
                // Dimensions of the mobile cover template (iPhone 14 Pro Max)
                const coverWidth = 77.6; // in mm
                const coverHeight = 160.7; // in mm

                // Calculate scaling factor to fit the image onto the cover
                const scaleFactor = Math.min(coverWidth / img.width, coverHeight / img.height);

                // Calculate dimensions of the scaled image
                const scaledWidth = img.width * scaleFactor;
                const scaledHeight = img.height * scaleFactor;

                // Calculate position to center the image on the cover
                const offsetX = (coverWidth - scaledWidth) / 2;
                const offsetY = (coverHeight - scaledHeight) / 2;

                // Clear canvas
                context.clearRect(0, 0, canvas.width, canvas.height);

                // Draw the cover template
                context.fillStyle = '#FFFFFF'; // Set background color
                context.fillRect(0, 0, coverWidth, coverHeight);

                // Draw the uploaded image on the cover
                context.drawImage(img, offsetX, offsetY, scaledWidth, scaledHeight);
            };
            img.src = reader.result;
        };

        reader.readAsDataURL(file);
    });

    saveBtn.addEventListener('click', function () {
        // Convert canvas to image data URL
        const imageData = canvas.toDataURL('image/png');
        
        // Create a temporary anchor element to download the image
        const downloadLink = document.createElement('a');
        downloadLink.href = imageData;
        downloadLink.download = 'mobile_cover_design.png';
        
        // Trigger a click event to download the image
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        
        // Alert the user
        alert('Design saved successfully!');
    });
});
