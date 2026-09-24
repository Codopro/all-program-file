let hammer = document.getElementsByClassName("hammer")

let itachix  = [169, 282, 392, 129, 269, 406,  82, 256, 428]
let itachiy  = [106, 106, 106, 138, 138, 138, 205, 205, 205]
let itachisx = [ 75,  75,  75, 101, 101, 101, 125, 125, 125]
let itachisy = [ 83,  83,  83, 109, 109, 109, 139, 139, 139]

let oto = []

let window1 = { sx:640, sy:480 } 
let timerno 
let timerv = 30 
let canvas 
let hammax = 393 
let hammin = 166 
let itachiwaiti = 50 
let itachicounti = 75 
let gametimeri = 100

let timer = timerv 
let mode = 0 
let mouse 
let score = 0 
let hiscore = [0, 0, 0] 
let hammers = 0 
let hamsize = 0 
let hammerx = 0 
let hammery = 0 
let itachis = [0, 0, 0, 0, 0, 0, 0, 0, 0] 
let itachiwait = 20 
let itachicount = 0 
let itachino = -1 
let gametimer = gametimeri 
let bonustime = gametimeri / 2 
let sanren = 0 

function init() {
    canvas = document.getElementById('canvas') 
    ctx = canvas.getContext('2d') 
    canvas.addEventListener('click', onclick_canvas, false) 
    canvas.addEventListener('mousedown', ondown_canvas, false) 
    canvas.addEventListener('mouseup', onup_canvas, false) 
    canvas.addEventListener('mousemove', onmove_canvas, false) 
    start() 
}

function mousezahyo(canvas, event) {
    let rect = canvas.getBoundingClientRect() 
    return { 
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

function onstart(mousex, mousey) {
    if (mousex > 240 && mousey > 390 && mousex < 396 && mousey < 437) {
        hamsize = hammax 
        hammerx = mousex - hamsize / 2 
        hammery = mousey - hamsize / 2 
        return true
    } else {
        return false
    }
}

function onrestart(mousex, mousey) {
    if (mousex > 450 && mousey > 390 && mousex < 606 && mousey < 437) {
        hamsize = hammax 
        hammerx = mousex - hamsize / 2 
        hammery = mousey - hamsize / 2 
        return true
    } else {
        return false
    }
}

function hammersize(mousey) {
    let hamhiritsu = mousey / (window1.sy * 2 / 3) 
    let size = Math.floor(hammax * hamhiritsu) 
    if (size > hammax) { 
        size = hammax
    } else if (size < hammin) {
        size = hammin
    }
    return size
}

function getitachino() {
    return Math.floor(Math.random() * 9) 
}

function getitachiwait() {
    return Math.floor(itachiwaiti * (Math.random() + 0.5)) 
}

function hammeritachi(no) {
    let hamhitx0 = hammerx + hamsize * 0.05 
    let hamhity0 = hammery + hamsize * 0.65 
    let hamhitx1 = hammerx + hamsize * 0.30
    let hamhity1 = hammery + hamsize * 0.75 
    let itachixm = itachix[no] + itachisx[no] / 2 
    let itachiym = itachiy[no] 
    return hamhitx0 < itachixm && hamhitx1 > itachixm && hamhity0 < itachiym && hamhity1 > itachiym 
}

function sounditachi(no) {
    if (oto.length > 0) { 
        oto[no].currentTime = 0 
        oto[no].play() 
    }
}

function drawitachi(no) {
    ctx.drawImage(itachi, itachix[no], itachiy[no], itachisx[no], itachisy[no]) 
}

function drawitachig(no) {
    ctx.drawImage(itachig, itachix[no], itachiy[no], itachisx[no], itachisy[no]) 
}

function drawatari(no) {
    ctx.drawImage(atari, itachix[no], itachiy[no], itachisx[no], itachisx[no]) 
}

function drawtimer(mytimer) {
    ctx.font = '36pt Arial' 
       ctx.fillStyle = 'white' 
    let inttimer = Math.ceil(mytimer)
    ctx.fillText("TIME:" + ("000" + inttimer).slice(-3), 168, 65) 
}

function hiscoreupdate(myscore) {
    if (hiscore[2] < myscore) { 
        hiscore[2] = myscore 
        for (let i = 2; i > 0; i--) { 
            if (hiscore[i - 1] < hiscore[i]) { 
                let temp = hiscore[i - 1]
                hiscore[i - 1] = hiscore[i] 
                hiscore[i] = temp
            } else { 
                break 
            }
        }
    }
}

function drawhiscore(no) {
    ctx.fillText(no + ": " + ("0000" + hiscore[no - 1]).slice(-4), 198, 358 + 34 * no)
}

function getpoint(no, mymode = 5) {
    if (no <= 2) { 
        return 3 * (mymode - 4) 
    } else if (no <= 5) { 
        return 2 * (mymode - 4) 
    } else { 
        return 1 * (mymode - 4) 
    }
}
