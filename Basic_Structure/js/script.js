
document.querySelectorAll('.custom-capsule').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.custom-capsule').forEach(innerBtn => {
            innerBtn.classList.remove('active');
        });
        btn.classList.add('active');
    });
});
