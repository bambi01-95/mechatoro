// webSocket.js
var connection;
var connected = false;// in keystest.js

let myElement = document.getElementById("myElementId");

if (myElement) {
  myElement.innerHTML = "Some content";
}

// document.getElementById("Status").innerHTML = "not connected";

function wsOpen() {
    host = document.getElementById("Host").value;
    port = document.getElementById("Port").value;
    connection = new WebSocket('ws://' + host + ':' + port);
    
    //接続成功
    connection.onopen = function(event) {
        connected = true;
        document.getElementById("Status").innerHTML = "connected";
    };

    //接続時エラー発生
    connection.onerror = function(error) {
        document.getElementById("Status").innerHTML = "connected error";
        connected = false;
    };

    //メッセージ受信 change
    connection.onmessage = function(event) {
        let datas =  event.data.split(',',3);
        document.getElementById("settingSpd").innerHTML = datas[0];
        document.getElementById("cSpd").innerHTML = datas[1];
        document.getElementById("mode").innerHTML = datas[2]
    };
    
    //切断
    connection.onclose = function() {
        document.getElementById("Status").innerHTML = "not connected";
        connected = false;
    };
}

//メッセージ送信
function sendMsg(){
    connection.send(document.getElementById("SndMsg").value);
}

//切断
function wsClose(){
    connection.close();
     document.getElementById("Status").value = "切断";
}

//コマンド送信
function sendCmnd(cmnd) {
    document.getElementById("SndMsg").value = cmnd;
    connection.send(cmnd);
}