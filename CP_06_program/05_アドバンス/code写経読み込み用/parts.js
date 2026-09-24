let haikei = document.getElementsByClassName("haikei")
let box = document.getElementsByClassName("box")
let msg = document.getElementsByClassName("msg")

let oto = []

let window1 = { sx:640, sy:480 }
let timerno
let timerv = 30
let canvas
let sspeed = 2
let boxs = { x:64, y:64 }
let drones = { x:128, y:128 }
let dronei = { x:window1.sx / 2, y:window1.sy - drones.y / 2 }
let dronespeed = [15, 5]
let targetnum = 20
let targets = { x:90, y:90 }
let targeti = { x:116 + targets.x / 2, y:-targets.y / 2 }
let targetti = 480
let targettm = 2
let boxnum = 40
let dropy = 17
let dronenums = 3
let maxx = Math.floor((targets.x + boxs.x * 0.4) / 2)
let maxy = Math.floor((targets.y + boxs.y * 0.4) / 2)

let ctx
let timer = timerv
let mode = 0
let haikeiy = 0
let dronexy = { x:dronei.x, y:dronei.y }
let dronemode = 0
let onbox = 0
let target = []
let targett = targetti
let targetnext = targett
let boxlist = []
let score = 0
let hiscore = [0, 0, 0]
let dronenum = dronenums
let kaze = 0
let sakurax = 0

function init() {
    canvas = document.getElementById('canvas')
    ctx = canvas.getContext('2d')
    addEventListener('keydown', keyDown, true)
    addEventListener('keyup', keyUp, true)
    for (let i = 0; i < targetnum; i++) {
        target[i] = { e:0, x:targeti.x, y:targeti.y, on:0 }
    }
    for (let i = 0; i < boxnum; i++) {
        boxlist[i] =  { e:0, n:0, x:dronexy.x, y:dronexy.y + boxs.y / 2, s:1, p:0 }
    }
    start()
}

function haikeirenketsu(y) {
    if (y < window1.sy) {
        return y + sspeed
    } else {
        return 0
    }
}

function movedrone(key, xx, yy) {
    let xy = { x:xx, y:yy }
    if (key === 37 && xy.x >= drones.x) {
        xy.x = xy.x - dronespeed[dronemode]
    }
    if (key === 38 && xy.y >= drones.y / 2) {
        xy.y = xy.y - dronespeed[dronemode]
    }
    if (key === 39 && xy.x < window1.sx - drones.x) {
        xy.x = xy.x + dronespeed[dronemode]
    }
    if (key === 40 && xy.y < window1.sy - drones.y / 2) {
        xy.y = xy.y + dronespeed[dronemode]
    }
    return xy
}

function targetmove(i) {
    if (target[i].y < window1.sy + targets.y) {
        target[i].y = target[i].y + sspeed
    } else {
        target[i].e = 0
    }
}

function nexttarget() {
    targetnext = targetnext - targettm
    if (targetnext <= 0) {
        for (let i = 0; i < targetnum; i++) {
            if (target[i].e === 0) {
                target[i].e = 1
                target[i].x = Math.floor(((Math.random() * (window1.sx - targeti.x * 2)) + targeti.x) / 5) * 5
                target[i].y = -targets.y / 2
                target[i].on = 0
                break
            }
        }
        targetnext = targett
    }
}

function targetspeedup() {
    if (haikeiy === 0 && targett > targetti / 3) {
        return targett - targettm * 10
    } else {
        return targett
    }
}

function drawbox(n, x, y, m=1) {
    let sx = Math.floor(boxs.x * m)
    let sy = Math.floor(boxs.y * m)
    ctx.drawImage(box[n], x - sx / 2, y - sy / 2, sx, sy)
}

function drawdrone(x, y) {
    ctx.drawImage(drone, x - drones.x / 2, y - drones.y / 2)
}

function drawtarget(n) {
    ctx.drawImage(target0, target[n].x - targets.x / 2, target[n].y - targets.y / 2)
}

function getnextbox() {
    let flag = false
    for (let i = 0; i < boxnum; i++) {
        if (boxlist[i].e === 0) {
            onbox = i
            boxlist[i].e = 6
            flag = true
            return 6
        }
    }
    return mode
}

function movedropedbox(i) {
    if (boxlist[i].e >= 2 && boxlist[i].e <= 5) {
        boxlist[i].y = boxlist[i].y + sspeed
    }
}

function boxdroping(i) {
    if (boxlist[i].e >= 2 && boxlist[i].e <= 4) {
        boxlist[i].e = boxlist[i].e + 1
    }
}

function removebox(i) {
    if (boxlist[i].y > window1.sy + boxs.y && boxlist[i].e <= 5) {
        boxlist[i].e = 0
    }
}

function dropnextbox() {
    boxlist[onbox].e = boxlist[onbox].e + 1
    if (boxlist[onbox].e >= 20) {
        dronemode = 1
        boxlist[onbox].e = 1
        return 5
    } else {
        return 6
    }
}

function drawscore(myscore) {
    ctx.font = '24pt Arial'
    ctx.fillStyle = 'black'
    ctx.fillText(("000000" + myscore).slice(-6), 530, 32)
}

function getpoint(mybox, mytarget) {
    let x = Math.abs(boxlist[mybox].x - target[mytarget].x)
    let y = Math.abs(boxlist[mybox].y - target[mytarget].y)
    if (x < maxx && y < maxy) {
        return 50 - Math.floor((x + y) * 50 / (maxx + maxy))
    } else {
        return 0
    }
}

function drawpoint(mybox) {
    ctx.font = '24pt Arial'
    ctx.fillStyle = 'white'
    ctx.fillText(("00" + boxlist[mybox].p).slice(-2), boxlist[mybox].x - 16, boxlist[mybox].y - 16)
}

function drawgameover() {
    ctx.font = '80pt Arial'
    ctx.fillStyle = 'Black'
    ctx.fillText('Game Over', 40, 258)
    ctx.fillStyle = 'Orange'
    ctx.fillText('Game Over', 42, 260)
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

function drawhiscore() {
    ctx.font = '24pt Arial'
    ctx.fillStyle = 'Black'
    ctx.fillText("HI-SCORE", 174, 302)
    ctx.fillStyle = 'Orange'
    ctx.fillText("HI-SCORE", 176, 304)
    for (let i = 0; i < 3; i++) {
        ctx.fillStyle = 'Black'
        ctx.fillText((i + 1) + ": " + ("000000" + hiscore[i]).slice(-6), 342, 302 + 34 * i)
        ctx.fillStyle = 'Orange' //文字をオレンジ色に
        ctx.fillText((i + 1) + ": " + ("000000" + hiscore[i]).slice(-6), 344, 304 + 34 * i)
    }
}

function drawdronenum(num) {
    for (let i = 0; i < num - 1; i++) {
        ctx.drawImage(drone, 5 + i * 24, 5, 22, 22)
    }
}
