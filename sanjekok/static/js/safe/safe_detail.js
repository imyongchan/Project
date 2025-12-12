function openModal(imgUrl) {
    const modal = document.getElementById("imgModal");
    const modalImg = document.getElementById("modalImg");

    modal.style.display = "block";
    modalImg.src = imgUrl;
}

function closeModal() {
    document.getElementById("imgModal").style.display = "none";
}
