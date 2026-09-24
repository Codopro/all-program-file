let wall = document.getElementsByClassName("wall")
let ball = document.getElementsByClassName("ball")

let oto = []

let window1 = { sx:640, sy:480 }
let timerno
let timerv = 20
let canvas
let cols = 14
let lines = 14
let walls = { x:24, y:24 }
let walltops = { x:152, y:24 }
let padxys = { x:272, y:432 }
let pads = { x:96, y:24 }
let padspeed = 15
let balls = { x:24, y:24 }
let ballxys = { x:padxys.x + 36, y:padxys.y }
let ballspeed = 3
let ballvs = 1
let restballs = 2

let timer = timerv
let mode = 0
let walltop =  { x:walltops.x, y:walltops.y }
let stageno = 0
let lapno = 0
let padxy = { x:padxys.x, y:padxys.y }
let ballxy = { x:ballxys.x, y:ballxys.y }
let ballv = ballvs
let restball = restballs
let animecnt = -1
let wmove = 0.2
let ballwall = {i:-1, j:-1}

function init() {
    canvas = document.getElementById('canvas')
    ctx = canvas.getContext('2d')
    addEventListener('keydown', keyDown, true)
    addEventListener('keyup', keyUp, true)
    start()
}

function drawstart() {
    ctx.font = '18pt Arial'
    ctx.fillStyle = 'Blue'
    ctx.fillText("Hit ENTER to start", 224, 432)
}

function drawwall() {
    let himedraw = 0
    for (let j = 0; j < lines; j++) {
        for (let i = 0; i < cols; i++) {
            if (nmap[i][j] === 9) {
                if (himedraw === 0) {
                    ctx.drawImage(himemini, walltop.x + i * walls.x, walltop.y + walls.y * j)
                    himedraw = 1
                }
            } else if (nmap[i][j] !== -1) {
                ctx.drawImage(wall[nmap[i][j]], walltop.x + i * walls.x, walltop.y + walls.y * j)
            }
        }
    }
}

function edgecheck(v, xy) {
    if (v === 0) {
        if (xy.y < 1) {
            return 3
        } else if (xy.x < 1) {
            return 1
        }
    } else if (v === 1) {
        if (xy.y < 1) {
            return 2
        } else if (xy.x > window1.sx - balls.x) {
            return 0
        }
    } else if (v === 2) {
        if (xy.x > window1.sx - balls.x) {
            return 3
        }
    } else {
        if (xy.x < 1) {
            return 2
        }
    }
    return v
}

function padcheck(v, bxy, pxy) {
    if (v === 2 &&
        bxy.y + balls.y > pxy.y && bxy.y + balls.y < pxy.y + pads.y &&
        bxy.x + balls.x >= pxy.x && bxy.x <= pxy.x + pads.x + balls.x / 4) {
        return 1
    } else
    if (v === 3 &&
        bxy.y + balls.y > pxy.y && bxy.y + balls.y < pxy.y + pads.y &&
        bxy.x >= pxy.x - balls.x / 4 && bxy.x <= pxy.x + pads.x) {
        return 0
    } else {
        return v
    }
}

function drawrestball(restball) {
    for (let i = 0; i < restball; i++) {
        ctx.drawImage(ball[1], 610 - 24 * i, 10)
    }
}

function ballback() {
    padxy.x = padxys.x
    padxy.y = padxys.y
    ballxys = { x:padxys.x + 36, y:padxys.y }
    ballxy = { x:ballxys.x, y:ballxys.y }
    ballv = ballvs
    walltop.x = walltops.x
}

function drawnext() {
    ctx.font = '18pt Arial'
    ctx.fillStyle = 'Blue'
    ctx.fillText("Hit ENTER to next", 224, 432)
}

function wallcheck(xy) {
    ballwall = getwall(xy)
    if (ballwall.i === -1) {
        return -1
    } else if (nmap[ballwall.i][ballwall.j] === 9) {
        return 9
    } else if (nmap[ballwall.i][ballwall.j] === 2) {
        nmap[ballwall.i][ballwall.j] = 1
    } else if (nmap[ballwall.i][ballwall.j] === 0 || nmap[ballwall.i][ballwall.j] === 1) {
        nmap[ballwall.i][ballwall.j] = -1
    } else if (nmap[ballwall.i][ballwall.j] === 3) {
        if (restball < 5) {
            restball = restball + 1
        }
        nmap[ballwall.i][ballwall.j] = -1
    }
    return 0
}

function wallbound(v, xy) {
    let ballwallxy = getwallxy(ballwall.i, ballwall.j)
    if (v === 0) {
        if (Math.abs((ballwallxy.x + walls.x) - xy.x) > Math.abs((ballwallxy.y + walls.y) - xy.y)) {
            return 3
        } else  {
            return 1
        }
    } else if (v === 1) {
        if (Math.abs(ballwallxy.x - (xy.x + balls.x)) > Math.abs((ballwallxy.y + walls.y) - xy.y)) {
            return 2
        } else  {
            return 0
        }
    } else if (v === 2) {
        if (Math.abs(ballwallxy.x - (xy.x + balls.x)) > Math.abs(ballwallxy.y - (xy.y + balls.y))) {
            return 1
        } else  {
            return 3
        }
    } else {
        if (Math.abs((ballwallxy.x + walls.x) - xy.x) > Math.abs(ballwallxy.y - (xy.y + balls.y))) {
            return 0
        } else  {
            return 2
        }
    }
}

function getwall(xy) {
    let wij = {i:-1, j:-1}
    wij.i = Math.floor((xy.x + balls.x / 2 - walltop.x) / walls.x)
    wij.j = Math.floor((xy.y + balls.y / 2 - walltop.y) / walls.y)
    if (wij.i >= 0 && wij.i < cols && wij.j >= 0 && wij.j < lines && nmap[wij.i][wij.j] !== -1) {
        return wij
    } else {
        wij.i = -1
        return wij
    }
}

function getwallxy(i, j) {
    let wxy = {x:0, y:0}
    wxy.x = walltop.x + walls.x * i
    wxy.y = walltop.y + walls.y * j
    return wxy
}

function drawnextstage() {
    ctx.font = '18pt Arial'
    ctx.fillStyle = 'Blue'
    ctx.fillText("Hit ENTER to next stage", 188, 432)
}

function setmap(sno) {
    for (let j = 0; j < lines; j++) {
        for (let i = 0; i < cols; i++) {
            nmap[i][j] = wmap[sno][i][j]
        }
    }
}

function drawstageno() {
    ctx.font = '18pt Arial'
    ctx.fillStyle = 'White'
    ctx.fillText("Stage : " + (lapno + 1) + "-" + (stageno + 1), 6, 26)
}

