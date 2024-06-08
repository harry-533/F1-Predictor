document.addEventListener("DOMContentLoaded", function() {
    var driverId = document.getElementById("driver-info").getAttribute("data-driver-id");
    var carbonElement = document.querySelectorAll(".carbon");
    var gradientElement = document.querySelectorAll(".gradient")
    var gradientElement2 = document.querySelectorAll(".gradient-2")
    var submitColor = document.querySelectorAll(".submit-color")
    const imageElement = document.getElementById('carbon');
    const baseUrl = imageElement.getAttribute('data-base-url');

    // Write conditions to change the background based on driverId
    if (driverId === 'norris' || driverId === 'piastri') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #ff6f00, #ff8f00, #ffa726, #ff8f00, #ff6f00)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #ff6f00, #ff8f00, #ffa726, #ff8f00, #ff6f00) 30";
            gradientElement.style.backgroundColor = "#1c0c00";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #ff6f00, #ff8f00, #ffa726, #ff8f00, #ff6f00)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#1c0c00";
            submitColor.style.borderColor = "#ff6f00";
        });
    } else if (driverId === 'max_verstappen' || driverId === 'perez') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #002245, #003366, #004080, #003366, #002245)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #002245, #003366, #004080, #003366, #002245) 30";
            gradientElement.style.backgroundColor = "#000d1a";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #002245, #003366, #004080, #003366, #002245)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#000d1a";
            submitColor.style.borderColor = "#002245";
        });
    } else if (driverId === 'leclerc' || driverId === 'sainz') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #ff0000, #cc0000, #990000, #cc0000, #ff0000)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #ff0000, #cc0000, #990000, #cc0000, #ff0000) 30";
            gradientElement.style.backgroundColor = "#160000";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #ff0000, #cc0000, #990000, #cc0000, #ff0000)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#160000";
            submitColor.style.borderColor = "#ff0000";
        });
    } else if (driverId === 'hamilton' || driverId === 'russell') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #01DFC0, #01DFA0, #01DF80, #01DFA0, #01DFC0)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #01DFC0, #01DFA0, #01DF80, #01DFA0, #01DFC0) 30";
            gradientElement.style.backgroundColor = "#001a17";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #01DFC0, #01DFA0, #01DF80, #01DFA0, #01DFC0)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#001a17";
            submitColor.style.borderColor = "#01DFC0";
        });
    } else if (driverId === 'alonso' || driverId === 'stroll') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #204f43, #358d76, #4fc59e, #358d76, #204f43)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #204f43, #358d76, #4fc59e, #358d76, #204f43) 30";
            gradientElement.style.backgroundColor = "#001a00";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #204f43, #358d76, #4fc59e, #358d76, #204f43)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#001a00";
            submitColor.style.borderColor = "#204f43";
        });
    } else if (driverId === 'tsunoda' || driverId === 'ricciardo') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #06396c, #27408B, #7AA8E6, #27408B, #06396c)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #06396c, #27408B, #7AA8E6, #27408B, #06396c) 30";
            gradientElement.style.backgroundColor = "#000d1a";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #06396c, #27408B, #7AA8E6, #27408B, #06396c)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#000d1a";
            submitColor.style.borderColor = "#06396c";
        });
    } else if (driverId === 'hulkenberg' || driverId === 'kevin_magnussen') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #f0f0f0, #e0e0e0, #d0d0d0, #e0e0e0, #f0f0f0)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #f0f0f0, #e0e0e0, #d0d0d0, #e0e0e0, #f0f0f0) 30";
            gradientElement.style.backgroundColor = "#1d1d1d";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #f0f0f0, #e0e0e0, #d0d0d0, #e0e0e0, #f0f0f0)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#1d1d1d";
            submitColor.style.borderColor = "#f0f0f0";
        });
    } else if (driverId === 'albon' || driverId === 'sargeant') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #3399ff, #4da6ff, #66b3ff, #4da6ff, #3399ff)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #3399ff, #4da6ff, #66b3ff, #4da6ff, #3399ff) 30";
            gradientElement.style.backgroundColor = "#001020";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #3399ff, #4da6ff, #66b3ff, #4da6ff, #3399ff)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#001020";
            submitColor.style.borderColor = "#3399ff";
        });
    } else if (driverId === 'ocon' || driverId === 'gasly') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #de86ad, #e7a6bd, #f0c6cd, #e7a6bd, #de86ad)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #de86ad, #e7a6bd, #f0c6cd, #e7a6bd, #de86ad) 30";
            gradientElement.style.backgroundColor = "#1d001c";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #de86ad, #e7a6bd, #f0c6cd, #e7a6bd, #de86ad)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#1d001c";
            submitColor.style.borderColor = "#de86ad";
        });
    } else if (driverId === 'bottas' || driverId === 'zhou') {
        carbonElement.forEach(carbonElement => {
            carbonElement.style.backgroundImage = `url(${baseUrl}/carbon.jpg), linear-gradient(144deg, #00FF00, #00FF33, #00FF66, #00FF33, #00FF00)`;
        });
        gradientElement.forEach(gradientElement => {
            gradientElement.style.borderImage = "linear-gradient(144deg, #00FF00, #00FF33, #00FF66, #00FF33, #00FF00) 30";
            gradientElement.style.backgroundColor = "#001900";
        });
        gradientElement2.forEach(gradientElement => {
            gradientElement.style.backgroundImage = "linear-gradient(black, black), linear-gradient(144deg, #00FF00, #00FF33, #00FF66, #00FF33, #00FF00)";
        });
        submitColor.forEach(submitColor => {
            submitColor.style.backgroundColor = "#001900";
            submitColor.style.borderColor = "#00FF00";
        });
    } 
});