document.addEventListener('DOMContentLoaded', function() {
    const raceButton = document.querySelector('.chose-race')
    const driverButton = document.querySelector('.chose-driver')
    driverButton.classList.add('clicked')

    raceButton.addEventListener('click', function() {
        document.querySelector('.driver').style.display = 'none';
        document.querySelector('.race').style.display = 'block';
        raceButton.classList.add('clicked');
        driverButton.classList.remove('clicked');

    })

    driverButton.addEventListener('click', function() {
        document.querySelector('.driver').style.display = 'block';
        document.querySelector('.race').style.display = 'none';
        driverButton.classList.add('clicked');
        raceButton.classList.remove('clicked');
    })

    document.getElementById('track-select').addEventListener('change', function() {
        const selectedImage = this.value;
        const imageElement = document.getElementById('driver-image');
        const baseUrl = imageElement.getAttribute('data-base-url');

        if (selectedImage) {
            imageElement.src =  baseUrl + selectedImage + '.png';
            imageElement.style.display = 'block';
            imageElement.style.width = '180px';
            imageElement.style.height = 'auto';
        } else {
            imageElement.style.display = 'none';
        }
    });
})