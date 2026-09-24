let window1 = { sx:640, sy:480 }

let score = 0
let playerx
let playery
let tamax
let tamay
let tekimx
let tekilast

function init() {
    playerx  = player.x
    playery  = player.y
    tamax = 0
    tamay = playery - tama.sy
    tekimx = teki.mx
    tekilast = -1
    ctx = document.getElementById('canvas').getContext('2d')
    addEventListener('keydown', keyDown, true)
    addEventListener('keyup', keyUp, true)
    start()
}

function start() {
    Timer = setInterval(mainloop, timer)
}

function ccheck(xa, ya, wa, ha, xb, yb, wb, hb) {
    xa = xa + Math.floor(wa / 2)
    ya = ya + Math.floor(ha / 2)
    let r1 = (wa < ha) ? Math.floor(wa / 2) : Math.floor(ha / 2)
    xb = xb + Math.floor(wb / 2)
    yb = yb + Math.floor(hb / 2)
    let r2 = (wb < hb) ? Math.floor(wb / 2) : Math.floor(hb / 2)
    if ((xa - xb) * (xa - xb) + (ya - yb) * (ya - yb) < (r1 + r2) * (r1 + r2)) {
        return true
    } else {
        return false
    }
}

function tekijunbi() {
    for (let i = 0; i < 32; i++) {
        let wx = Math.floor(i % 8) * 60 + Math.floor(i % 8 / 4) * 40  + teki.x
        let wy = Math.floor(i / 8) * 60 + teki.y
        tekia[i] = { x:wx, y:wy, f:1 }
    }
    tekinum = 32
}

function hit() {
    for (let i = 0; i < 32; i++) {
        if (tekia[i].f === 1) {
            if (ccheck(tamax, tamay, tama.sx, tama.sy, tekia[i].x, tekia[i].y, teki.sx, teki.sy)) {
                tekia[i].f = 0
                tekinum--
                score += 10
                return 0
            }
        }
    }
    return 1
}

function tamaidou() {
    if (tamay >= tama.sy) {
        tamay -= tama.mx
    }
    if (tamay <= tama.sy) {
        return 0
    } else {
        return 1
    }
}

function tamauchi() {
    tamax = playerx + 10
    tamay = playery - tama.sy
}

function hidariidou() {
    if (playerx >= player.mx) {
        playerx -= player.mx
    }
}

function migiidou() {
    if (playerx < window1.sx - player.sx) {
        playerx += player.mx
    }
}

function tekiidou() {
    let tekilimitl = window1.sx
    let tekilimitr = 0
    let tekimy = 0
    for (let i = 0; i < 32; i++) {
        if (tekia[i].f === 1) {
            if (tekimx > 0 && tekia[i].x > tekilimitr) {
                tekilimitr = tekia[i].x
            } else if (tekimx < 0 && tekia[i].x < tekilimitl) {
                tekilimitl = tekia[i].x
            }
        }
    }
    if (tekimx > 0 && tekilimitr >= window1.sx - teki.sx || tekimx < 0 && tekilimitl <= 0) {
        tekimx = -tekimx
        tekimy = teki.my
    }
    for (let i = 0; i < 32; i++) {
        if (tekia[i].f === 1) {
            if (tekimy === 0) {
                tekia[i].x += tekimx
            } else {
                tekia[i].y += tekimy
            }
            tekilast = i
        }
    }
}

function shinryaku() {
    if (tekia[tekilast].y + teki.sy > playery + teki.my) {
        return 1
    } else {
        return 0
    }
}
