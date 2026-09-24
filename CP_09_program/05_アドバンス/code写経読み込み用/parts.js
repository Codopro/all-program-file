let robot = document.getElementsByClassName("robot") ;

let window1 = { sx:640, sy:480 }
let timerno
let timerv = 30
let robots = { sx:60, sy:60, move:10 }
let inryokus = 1.02
let ugokihaba = 10
let menhaba = window1.sx / ugokihaba

let timer = timerv
let mode = 0
let counter = 0
let haikeikaisi = 0
let robotno = 1
let robotd = { x:40, y:210 }
let keyue = 0
let keyshita = 0
let score = 0
let oldtimer = timer
let itemscore = 0
let inryoku = inryokus
let robomapy1
let robomapy2
let robomapx1
let robomapx2

function init() {
    ctx = document.getElementById('canvas').getContext('2d')
    addEventListener('keydown', keyDown, true)
    addEventListener('keyup', keyUp, true)
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 16; j++) {
            maps[i * 16 + j] = new Array(12)
        }
    }
    start()
}

function itemxy() {
    robomapy1 = Math.floor(robotd.y / 40)
    robomapy2 = Math.floor((robotd.y + 60) / 40)
    robomapx1 = Math.floor(-haikeikaisi / 40)
    robomapx2 = Math.floor((-haikeikaisi + 70)/ 40)
}

function bonusscore(n) {
    for (let i = robomapx1; i <= robomapx2; i++) {
        for (let j = robomapy1; j <= robomapy2; j++) {
            if (maps[i][j] === 2) {
                maps[i][j] = 5
                score += n
            }
        }
    }
}

function speedupscore(n, m) {
    for (let i = robomapx1; i <= robomapx2; i++) {
        for (let j = robomapy1; j <= robomapy2; j++) {
            if (maps[i][j] === 3) {
                maps[i][j] = 6
                timer = Math.floor(timer * (1.0 - m / 100) + 0.5)
                itemscore += n
            }
        }
    }
}

function speeddownscore(n, m) {
    for (let i = robomapx1; i <= robomapx2; i++) {
        for (let j = robomapy1; j <= robomapy2; j++) {
            if (maps[i][j] === 4) {
                maps[i][j] = 6
                timer = Math.floor(timer * (1.0 + m / 100) - 0.5)
                itemscore += n
            }
        }
    }
}

function shogaicrash() {
    for (let i = robomapx1; i <= robomapx2; i++) {
        for (let j = robomapy1; j <= robomapy2; j++) {
            if (maps[i][j] === 1) {
                mode = 8
                return
            }
        }
    }
}

function drawbonus() {
    for (let i = 1 * 16; i < 8 * 16; i++) {
        if (haikeikaisi + i * 40 > -40 && haikeikaisi + i * 40 < window1.sx + 40) {
            for (let j = 0; j < 12; j++) {
                if (maps[i][j] === 2) {
                    ctx.drawImage(bonusitem, haikeikaisi + i * 40, j * 40)
                }
            }
        }
    }
}

function drawbonusget() {
    for (let i = 1 * 16; i < 8 * 16; i++) {
        if (haikeikaisi + i * 40 > -40 && haikeikaisi + i * 40 < window1.sx + 40) {
            for (let j = 0; j < 12; j++) {
                if (maps[i][j] === 5) {
                    ctx.drawImage(bonusget, haikeikaisi + i * 40, j * 40)
                }
            }
        }
    }
}

function drawspeedup() {
    for (let i = 1 * 16; i < 8 * 16; i++) {
        if (haikeikaisi + i * 40 > -40 && haikeikaisi + i * 40 < window1.sx + 40) {
            for (let j = 0; j < 12; j++) {
                if (maps[i][j] === 3) {
                    ctx.drawImage(speedup, haikeikaisi + i * 40, j * 40)
                }
            }
        }
    }
}

function drawspeeddown() {
    for (let i = 1 * 16; i < 8 * 16; i++) {
        if (haikeikaisi + i * 40 > -40 && haikeikaisi + i * 40 < window1.sx + 40) {
            for (let j = 0; j < 12; j++) {
                if (maps[i][j] === 4) {
                    ctx.drawImage(speeddown, haikeikaisi + i * 40, j * 40)
                }
            }
        }
    }
}

function drawspeedupget() {
    for (let i = 1 * 16; i < 8 * 16; i++) {
        if (haikeikaisi + i * 40 > -40 && haikeikaisi + i * 40 < window1.sx + 40) {
            for (let j = 0; j < 12; j++) {
                if (maps[i][j] === 6) {
                    ctx.drawImage(itemget, haikeikaisi + i * 40, j * 40)
                }
            }
        }
    }
}

function drawshogai() {
    for (let i = 1 * 16; i < 8 * 16; i++) {
        if (haikeikaisi + i * 40 > -40 && haikeikaisi + i * 40 < window1.sx + 40) {
            for (let j = 0; j < 12; j++) {
                if (maps[i][j] === 1) {
                    ctx.drawImage(hazard, haikeikaisi + i * 40, j * 40)
                }
            }
        }
    }
}
