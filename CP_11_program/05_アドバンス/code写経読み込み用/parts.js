let enemy = document.getElementsByClassName("enemy")
let goal = document.getElementsByClassName("goal")
let message = document.getElementsByClassName("message")

let oto = []

let window1 = { sx:640, sy:480 }
let timerno
let timerv = 30
let canvas

let timer = timerv
let mode = 0
let mouse
let player = { x:1, y:9 }
let playeri = { x:1, y:9 }
let playerp = { x:1, y:9 }
let goalmode = 0
let score = 0
let teki = { x:9, y:1 }
let tekii = { x:9, y:1 }
let tekimuki = 0
let warpmode = 0
let hidariwarp = { x:1, y:1 }
let migiwarp = { x:9, y:1 }
let fruit = { x:5, y:1 }
let fruitari = 1
let warpcount = -99
let warpstart = 47
let hiscore = [0, 0, 0]

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

function fillblack(x1, y1, x2, y2) {
    ctx.fillStyle = 'black'
    ctx.fillRect(x1, y1, x2, y2)
}

function haikeiwall() {
    for (let j = 0; j < 11; j++) {
        for (let i = 0; i < 14; i++) {
            ctx.drawImage(wall, i * 48 - 24, j * 48 - 24)
        }
    }
    ctx.drawImage(minititle, 478, 24)
}

function drawmessage(n) {
    ctx.drawImage(message[n], 478, 128)
}

function allclear() {
    for (let i = 0; i < 11; i++) {
        for (let j = 0; j < 11; j++) {
            if (map1[j][i] === 0) {
                return 0
            }
        }
    }
    return 1
}

function onplayer() {
    return mouse.x >= player.x * 48 - 24 && mouse.x <= player.x * 48 + 24 && mouse.y >= player.y * 48 - 24 && mouse.y <= player.y * 48 + 24
}

function tuukashori(a, b) {
    if (map1[player.y][player.x] === 0) {
        map1[player.y][player.x] = 1
        score = score + a
    } else if (map1[player.y][player.x] === 1 && (playerp.x !== player.x || playerp.y !== player.y) ) {
        if (score >= b) {
            score = score - 10
        } else {
            score = 0
        }
    }
}

function fillblue48(i, j) {
    ctx.fillStyle = 'Blue'
    ctx.fillRect(i * 48 - 24, j * 48 - 24, 48, 48)
}

function drawscore(n) {
    ctx.drawImage(scoreboard, 478, 225)
    ctx.fillStyle = 'White'
    ctx.font = '26pt Arial'
    ctx.fillText(("000000" + n).slice(-6), 490, 295)
}

function drawcenter(s, x, f) {
    ctx.fillStyle = 'White'
    ctx.font = f + 'pt Arial'
    ctx.fillText(s, x, 276)
}

function onhidariwarp() {
    return mouse.x >= hidariwarp.x * 48 - 24 && mouse.x <= hidariwarp.x * 48 + 24 && mouse.y >= hidariwarp.y * 48 - 24 && mouse.y <= hidariwarp.y * 48 + 24
}

function onmigiwarp() {
    return mouse.x >= migiwarp.x * 48 - 24 && mouse.x <= migiwarp.x * 48 + 24 && mouse.y >= migiwarp.y * 48 - 24 && mouse.y <= migiwarp.y * 48 + 24
}

function hiscoreupdate() {
    if (hiscore[2] < score) {
        hiscore[2] = score
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

function hcenter() {
    return player.x === Math.floor(player.x)
}

function vcenter() {
    return player.y === Math.floor(player.y)
}

function hantei() {
    return Math.abs(player.y - teki.y) < 1 && Math.abs(player.x - teki.x) < 1
}

function playerdousa() {
    if (hcenter()) {
        let pmy = mouse.y - player.y * 48
        if (pmy > 24 && map1[Math.floor(player.y) + 1][Math.floor(player.x)] < 8) {
            player.y += 0.5
        } else if (pmy < -24 && map1[Math.ceil(player.y) - 1][Math.ceil(player.x)] < 8) {
            player.y -= 0.5
        }
    }
    if (vcenter()) {
        let pmx = mouse.x - player.x * 48
        if (pmx > 24 && map1[Math.floor(player.y)][Math.floor(player.x) + 1] < 8) {
            player.x += 0.5
        } else if (pmx < -24 && map1[Math.ceil(player.y)][Math.ceil(player.x) - 1] < 8) {
            player.x -= 0.5
        }
    }
}

function tekidousa(n) {
    if (Math.floor(Math.random() * 100) < n) {
        if (teki.x === Math.floor(teki.x)) {
            let pmy = player.y - teki.y
            if (pmy > 0 && map1[Math.floor(teki.y) + 1][Math.floor(teki.x)] < 8) {
                teki.y += 0.5
            } else if (pmy < 0 && map1[Math.ceil(teki.y) - 1][Math.ceil(teki.x)] < 8) {
                teki.y -= 0.5
            }
        }
        if (teki.y === Math.floor(teki.y)) {
            let pmx = player.x - teki.x
            if (pmx > 0 && map1[Math.floor(teki.y)][Math.floor(teki.x) + 1] < 8) {
                teki.x += 0.5
                tekimuki = 1
            } else if (pmx < 0 && map1[Math.ceil(teki.y)][Math.ceil(teki.x) - 1] < 8) {
                teki.x -= 0.5
                tekimuki = 0
            }
        }
    }
}

function retry() {
    if(confirm("やりなおしますか？")) {
        for (let j = 0; j < 11; j++) {
            for (let i = 0; i < 11; i++) {
                map1[j][i] = map0[j][i]
            }
        }
        player.x = playeri.x
        player.y = playeri.y
        playerp.x = playeri.x
        playerp.y = playeri.y
        goalmode = 0
        score = 0
        teki.x = tekii.x
        teki.y = tekii.y
        fruitari = 1
        mode = 4
    }
}
