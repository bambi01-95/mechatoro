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



let frame1_dir = "/video_feed"
let frame2_dir = "/video_feed_back"

// send keyboard input
let count = 0;
const countUp = () => {
    if(connected == true){
        sendCmnd(w+a+d+"," +s+ "," + i + "," + j);
    }
}
setInterval(countUp, 1000); // 1000 = 1 sec -> 30

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

    if(keys.w == true){
        w = "1";

    }
    if(keys.a == true){
        a = "1";
    }
    if(keys.s == true){
        s = "1";
        let stock = frame1_dir;
        let stockk = frame2_dir;
        frame1_dir = stockk;
        frame2_dir = stock;
        document.getElementById("frame1").src = frame1_dir;
    }
    if(keys.d == true){
        d = "1";
    }

    if(keys.i == true){
        i = "1";
    }
    if(keys.j == true){
        j = "1";
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
    if(keys.w == false){
        w = "0";
    }
    if(keys.a == false){
        a = "0";
    }
    if(keys.s == false){
        s = "0";
    }
    if(keys.d == false){
        d = "0";
    }
    if(keys.i == false){
        i = "0";
    }
    if(keys.j == false){
        j = "0";
    }
    document.getElementById('output').innerHTML = a + s + d + w + i + j;
    return false; 
}