document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('track-select').addEventListener('change', function() {
        const selectedImage = this.value;
        const imageElement = document.getElementById('driver-image');
        const baseUrl = imageElement.getAttribute('data-base-url');

        if (selectedImage) {
            imageElement.src =  baseUrl + selectedImage + '.png';
            imageElement.style.display = 'block';
            imageElement.style.width = '300px';
            imageElement.style.height = 'auto';
        } else {
            imageElement.style.display = 'none';
        }
    });
})

function qualiExpandList() {
    var scrollBox = document.getElementById("quali-scroll-box");
    var expandButton = document.getElementById("quali-expand-button");
    var otherBox = document.getElementById("race-scroll-box");
    
    if (scrollBox.style.height === "300px" || scrollBox.style.height === "") {
        scrollBox.style.height = "auto";
        scrollBox.style.margin = "0px 0px 0px 0px";
        expandButton.textContent = "-";
        otherBox.style.display = "none";
    } else {
        scrollBox.style.height = "300px";
        scrollBox.style.margin = "7% 0px 0px 0px";
        expandButton.textContent = "+";
        otherBox.style.display = "block";
    }
}

function resultExpandList() {
    var scrollBox = document.getElementById("race-scroll-box");
    var expandButton = document.getElementById("race-expand-button");
    var otherBox = document.getElementById("quali-scroll-box");

    console.log("Other box display:", otherBox.style.display);
    
    if (scrollBox.style.height === "300px" || scrollBox.style.height === "") {
        scrollBox.style.height = "auto";
        scrollBox.style.margin = "0px 0px 0px 0px";;
        expandButton.textContent = "-";
        otherBox.style.display = "none";
    } else {
        scrollBox.style.height = "300px";
        scrollBox.style.margin = "7% 0px 0px 0px";
        expandButton.textContent = "+";
        otherBox.style.display = "block";
    }
}