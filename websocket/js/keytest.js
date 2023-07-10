// https://1-notes.com/javascript-addeventlistener-key-ivent/
document.addEventListener('keypress', keypress_ivent);
document.addEventListener('keyup', keyup_ivent);

let keys = {
    a:false,
    s:false,
    d:false,
    w:false,

    j:false,
    i:false
};

let a = "";
let s = "";
let d = "";
let w = "";
let count = 0;
let frame1_dir = "./img/home.png"
let frame2_dir = "./img/tata_app_logo.png"
// send keyboard input
const countUp = () => {
    if(connected == true){
        sendCmnd(a + s + d + w);
    }
}
setInterval(countUp, 1000); // 1000 = 1 sec

function keypress_ivent(e) {
    // 同時入力が可能にするため
    switch(e.key){
        case 'a':keys.a = true;break;
        case 's':keys.s = true;break;
        case 'd':keys.d = true;break;
        case 'w':keys.w = true;break;
        case 'i':keys.i = true;break;
        case 'j':keys.j = true;break;
    }

    if(keys.a == true){
        a = "a";
    }
    if(keys.s == true){
        s = "s";
        let stock = frame1_dir;
        frame1_dir = frame2_dir;
        frame2_dir = stock;
        document.getElementById("frame1").src = frame1_dir;
        document.getElementById("frame2").src = frame2_dir;
    }
    if(keys.d == true){
        d = "d";
    }
    if(keys.w == true){
        w = "w";
    }
    if(keys.i == true){
        i = "i";
    }
    if(keys.j == true){
        j = "j";
    }
    document.getElementById('output').innerHTML = a + s + d + w + i + j;
    return false; 
}

function keyup_ivent(e) {
    // 同時入力に必要
    switch(e.key){
        case 'a':keys.a = false;break;
        case 's':keys.s = false;break;
        case 'd':keys.d = false;break;
        case 'w':keys.w = false;break;
        case 'i':keys.i = false;break;
        case 'j':keys.j = false;break;
    }

    if(keys.a == false){
        a = "";
    }
    if(keys.s == false){
        s = "";
    }
    if(keys.d == false){
        d = "";
    }
    if(keys.w == false){
        w = "";
    }
    if(keys.i == false){
        i = "";
    }
    if(keys.j == false){
        j = "";
    }
    document.getElementById('output').innerHTML = a + s + d + w + i + j;
    return false; 
}