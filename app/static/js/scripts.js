// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    // แสดงข้อความในคอนโซลเพื่อยืนยันว่าไฟล์ JavaScript ทำงาน
    console.log('JavaScript is running!');
    const abc=document.getElementsByClassName('abc');
    abc[0].innerHTML += '<p>12345667</p>';
    // ฟังก์ชันสำหรับการทักทายผู้ใช้เมื่อคลิกปุ่ม
    const greetButton = document.getElementById('greetButton');
    if (greetButton) {
        greetButton.addEventListener('click', function () {
            alert('let\'s go');
            window.location.href = 'https://youtu.be/A-9K9IpgTho?si=Lwg_SumcNt8LXHvy';
        });
    }
});
