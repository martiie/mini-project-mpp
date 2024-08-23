// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    // แสดงข้อความในคอนโซลเพื่อยืนยันว่าไฟล์ JavaScript ทำงาน
    console.log('JavaScript is running!');
    const abc=document.getElementsByClassName('abc');
    abc[0].innerHTML += '<p>let\' fucking go</p>';
    // ฟังก์ชันสำหรับการทักทายผู้ใช้เมื่อคลิกปุ่ม
    const greetButton = document.getElementById('greetButton');
    if (greetButton) {
        greetButton.addEventListener('click', function () {
            alert('let\'s go');
            window.location.href = 'https://youtu.be/vOreqez4v9Y?si=cUVz-q4TX-GXKDbw';
        });
    }
    if (showButton) {
        showButton.addEventListener('click', function () {
            window.location.href = '/show';
        });
    }
});
