// remote.js

class ValUpDown {
    constructor(name, code, val, step, min, max) {
        this.name = name;
        this.code = code;
        this.val = val;
        this.step = step;
        this.min = min;
        this.max = max;
    }
    
    valUp() {
        if (this.val + this.step <= this.max) {
            this.val += this.step;
        }
        document.getElementById(this.name).value = this.val;
        sendCmnd(this.code + "," +  this.val.toString())
    }

    valDown() {
        if (this.val - this.step >= this.min) {
            this.val -= this.step;
        }
        document.getElementById(this.name).value = this.val;
        sendCmnd(this.code + "," + this.val.toString())
    }
}

function valueUp(no) {
    values[no].valUp()
}

function valueDown(no) {
    values[no].valDown()
}


function unitChange(){    // unit change
    var unit;
    for (var i = 0; i < document.formName0.choice.length; i++) {
        if(document.formName0.choice[i].checked) {
            unit = parseInt(document.formName0.choice[i].value);
            break;
        }
        unit = parseInt(document.formName0.choice[i].value);
    }
    sendCmnd("U, " + unit.toString())
    console.log("Unit=", unit);
}

function keyBd(keyNo) {
    sendCmnd("K, " + keyNo)
    console.log("key=", keyNo);
}

var values = []
values.push(new ValUpDown('spd', 'SPD', 0, 1, -10, 10))
values.push(new ValUpDown('acc', 'ACC', 0, 1, -10, 10))