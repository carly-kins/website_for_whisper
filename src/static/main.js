document.addEventListener("DOMContentLoaded", () => {

    const recorder = document.getElementById("recorder");
    const player = document.getElementById("player");

    recorder.addEventListener("change", function (e) {
        const file = e.target.files[0];
        const url = URL.createObjectURL(file);
        player.src = url;
        });  
    });
