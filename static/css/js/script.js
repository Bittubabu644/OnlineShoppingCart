document.addEventListener("DOMContentLoaded", function () {

    const flashMessage = document.querySelector(".flash-message");

    if (flashMessage) {

        setTimeout(function () {

            flashMessage.style.opacity = "0";

            setTimeout(function () {
                flashMessage.remove();
            }, 500);

        }, 2500);
    }

});