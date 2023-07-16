// https://1-notes.com/javascript-addeventlistener-key-ivent/
document.addEventListener('keypress', keypress_ivent);
document.addEventListener('keyup',    keyup_ivent);


// for mult input
let keys = {
    a:false,
    s:false,
    d:false,
    w:false,
  
    f:false,
    r:false,
    i:false,
    j:false,
};
let spd = "0"

// for moving direction
let w = "0";
let a = "0";
let d = "0";
let s = "0";
// for moving direction's mode
let mode = "0";
// for arm
let f = "0";
let r = "0";
let i = "0";
let j = "0";

// send keyboard input
let count = 0;
const countUp = () => {
    if(connected == true){
        //        wad       s      speed      mode      fr        ij
        sendCmnd(w+a+d+"," +s+ ","+ spd+"," + mode+"," +f+r +"," +i+j);
        if(mode=="1"){
            mode = "0"
        }
    }
}
setInterval(countUp, 500); // 1000 = 1 sec -> 30

function keypress_ivent(e) {
    // 同時入力が可能にするため
    switch(e.key){
        // for moving direction
        case 'a':keys.a = true;break;
        case 's':keys.s = true;break;
        case 'd':keys.d = true;break;
        case 'w':keys.w = true;break;
        // for arm
        case 'f':keys.f = true;break;
        case 'r':keys.r = true;break;
        case 'i':keys.i = true;break;
        case 'j':keys.j = true;break;
        // for spd
        case '0':spd="0";break;
        case '1':spd="1";break;
        case '2':spd="2";break;
        case '3':spd="3";break;
        case '4':spd="4";break;
        case '5':spd="5";break;
        case '6':spd="6";break;
        case '7':spd="7";break;
        case '8':spd="8";break;
        case '9':spd="9";break;
    }
    if(keys.w == true){w = "1";}
    if(keys.a == true){a = "1";}
    if(keys.s == true){s = "1";}
    if(keys.d == true){d = "1";}
    if(keys.f == true){f = "1";}
    if(keys.r == true){r = "1";}
    if(keys.i == true){i = "1";}
    if(keys.j == true){j = "1";}
    document.getElementById('output').innerHTML = a + s + d + w + i + j + mode ;
    return false; 
}

function keyup_ivent(e) {
    // 同時入力に必要
    switch(e.key){
        case 'a':keys.a = false;break;
        case 's':keys.s = false;break;
        case 'd':keys.d = false;break;
        case 'w':keys.w = false;break;

        case 'f':keys.f = false;break;
        case 'r':keys.r = false;break;
        case 'i':keys.i = false;break;
        case 'j':keys.j = false;break;

        case 'm':mode = "1";break;
    }
    if(keys.w == false){w = "0";}
    if(keys.a == false){a = "0";}
    if(keys.s == false){s = "0";}
    if(keys.d == false){d = "0";}
    if(keys.f == false){f = "0";}
    if(keys.r == false){r = "0";}
    if(keys.i == false){i = "0";}
    if(keys.j == false){j = "0";}
    document.getElementById('output').innerHTML = a + s + d + w + i + j;
    return false; 
}