let candyb = document.getElementsByClassName("candyb")
let candy = document.getElementsByClassName("candy")

let oto = [] 

let window1 = { sx:640, sy:480 }
let timerno
let timerv = 30
let canvas
let catxys = { x:320, y:240 }
let cats = { x:64, y:64 }
let stars = { x:64, y:64 }
let ropefrom = { x:320, y:400 }
let ropelen = 10
let netss = { x:202, y:63 }
let netcounts = 20
let candys = { x:32, y:32 }
let candyspeed = 3
let candyspeeds = [3, 4, 5, 5]
let point = [10, 20, 30, 40]

let timer = timerv
let mode = 0
let mouse
let catxy = { x:catxys.x - (cats.x / 2) , y:catxys.y - (cats.y / 2) }
let stardist = -1
let starxy = { x:0, y:0 }
let ropestep = 0
let ropev = { x:0, y:0 }
let ropecount = 0
let ropeto = { x:0, y:0 }
let inaction = 0
let netxy = { x:0, y:0 }
let nets = { x:0, y:0 }
let netcount = 0
let canxy = { x:-1, y:0 }
let candyget = 0
let score = 0
let cantype = 0
let hiscore = [0, 0, 0]
let catnum = 2
let precantype = 0

function init() {
    canvas = document.getElementById('canvas')
    ctx = canvas.getContext('2d')
    canvas.addEventListener('click', onclick_canvas, false)
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

function drawcatcher(x, y) {
    ctx.drawImage(catcher, x - cats.x / 2, y - cats.y / 2)
}

function getstardist(x, y) {
    if (Math.abs(ropefrom.x - x) > Math.abs(ropefrom.y - y)) {
        return Math.abs(ropefrom.x - x)
    } else {
        return Math.abs(ropefrom.y - y)
    }
}

function getropelen(step) {
    let r = { x:0, y:0 }
    r.x = Math.floor((starxy.x - ropefrom.x) / step)
    r.y = Math.floor((starxy.y - ropefrom.y) / step)
    return r
}

function getropeto(count) {
    let r = { x:0, y:0 }
    r.x = ropefrom.x + ropev.x * count
    r.y = ropefrom.y + ropev.y * count
    return r
}

function drawstar(x, y) {
    ctx.drawImage(star, x - stars.x / 2, y - stars.y / 2)
}

function drawrope(x, y) {
    ctx.lineWidth = "5"
    ctx.strokeStyle = "yellow"
    ctx.beginPath()
    ctx.moveTo(ropefrom.x, ropefrom.y)
    ctx.lineTo(x, y)
    ctx.stroke()
}

function drawnet(x, y, c) {
    nets.x = netss.x * c / netcounts
    nets.y = netss.y * c / netcounts
    ctx.drawImage(net, x - nets.x / 2, y - nets.y / 2, nets.x, nets.y)
}

function setcandy() {
    let x = 320
    do {
        x = Math.floor(Math.random() * (window1.sx - candys.x)) + candys.x / 2
    } while (x >= 288 && x <= 354)
    return x
}

function drawcandy(x, y, n = 0) {
    ctx.drawImage(candy[n], x - candys.x / 2, y - candys.y / 2)
}

function netcandycheck() {
    if (candyget === 0) {
        if (starxy.x - nets.x / 2 < canxy.x && starxy.x + nets.x / 2 > canxy.x
         && starxy.y - nets.y / 2 < canxy.y && starxy.y + nets.y / 2 > canxy.y) {
            canxy.x = -1
            canxy.y = 0
            precantype = cantype
            return 1
        }
        return 0
    }
    return 1
}

function drawgameover() {
    ctx.font = '80pt Arial'
    ctx.fillStyle = 'Red'
    ctx.fillText('Game Over', 42, 260)
}

function drawscore(myscore) {
    ctx.font = '24pt Arial'
    ctx.fillStyle = 'white'
    ctx.fillText("SCORE:" + ("00000" + myscore).slice(-5), 10, 40)
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
        if (hiscore[0] === myscore) {
            return 1
        }
    }
    return 0
}

function drawhiscore(n) {
    ctx.fillText(n + ": " + ("00000" + hiscore[n - 1]).slice(-5), 344, 270 + 34 * n)
}

function drawplayagain() {
    ctx.font = '20pt Arial'
    ctx.fillStyle = 'Red'
    ctx.fillText('Click to', 200, 457)
    ctx.fillText('Play Again', 358, 457)
}

function drawcatnum(num) {
    for (let i = 0; i < num; i++) {
        ctx.drawImage(catcher, 610 - 24 * i, 10, 24, 24)
    }
}
