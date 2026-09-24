let num = document.getElementsByClassName("num")
let msg = document.getElementsByClassName("msg")
let haikei = document.getElementsByClassName("haikei")

let oto = []

let window1 = { sx:640, sy:480 }
let timerno 
let timerv = 30 
let canvas 
let fuchi = 20 
let maxcols = 7 

let timer = timerv 
let mode = 0 
let mouse 
let cols = 3 
let bombs = cols - 2
let boxs = cols * cols
let boxsize = (window1.sy - fuchi * 2) / cols
let map = [] 
let vmap = [] 
let flags = 0 
let gametimer = cols * 20 
let zlist = [] 
let znum = 0 

function init() {
    canvas = document.getElementById('canvas')
    ctx = canvas.getContext('2d')
    canvas.addEventListener('click', onclick_canvas, false)
    start()
}

function mousezahyo(canvas, event) {
    let rect = canvas.getBoundingClientRect()
    return { 
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

function drawbox(i, j, no = -2) {
    let x = boxsize * i + fuchi
    let y = boxsize * j + fuchi
    if (no === -2) {
        ctx.drawImage(box, x, y, boxsize, boxsize)
    } else if (no === -1) {
        ctx.drawImage(empty, x, y, boxsize, boxsize)
    } else if (no === 9) {
        ctx.drawImage(bomb, x, y, boxsize, boxsize)
    } else if (no === 8) {
        ctx.drawImage(flag, x, y, boxsize, boxsize)
    } else {
        ctx.drawImage(num[no], x, y, boxsize, boxsize)
    }
}

function drawbombs(mybombs) {
    ctx.font = '30pt Arial'
    ctx.fillStyle = 'white' 
    ctx.fillText(":" + mybombs, 545, 230)
}

function drawflags(myflags) {
    ctx.font = '30pt Arial' 
    ctx.fillStyle = 'white'
    ctx.fillText(":" + myflags, 545, 280)
}

function drawtimer(mytimer) {
    ctx.font = '36pt Arial'
    ctx.fillStyle = 'white'
    let inttimer = Math.ceil(mytimer)
    ctx.fillText(("000" + inttimer).slice(-3), 510, 400)
}


function setmap() {
    for (let i = 0; i < cols; i++) {
        map[i] = [];
        vmap[i] = [];
        for (let j = 0; j < cols; j++) {
            map[i][j] = -1
            vmap[i][j] = -2
        }
    }
}

function setbomb(mybombs) {
    for (let i = 0; i < mybombs; i++) {
        for (;;) {
            let x = Math.floor(Math.random() * cols)
            let y = Math.floor(Math.random() * cols)
            if (map[x][y] === -1) {
                map[x][y] = 9
                break
            }
        }
    }
}

function setbombs() {
    for (let i = 0; i < cols; i++) { 
        for (let j = 0; j < cols; j++) { 
            if (map[i][j] !== 9) {
                map[i][j] = getbnums(i, j)
            }
        }
    }
}

function getbnums(x, y) {
    let n = 0
    if (x > 0 && y > 0 && map[x - 1][y - 1] === 9) {
        n++;
    }
    if (y > 0 && map[x][y - 1] === 9) {
        n++; 
    }
    if (x < cols - 1 && y > 0 && map[x + 1][y - 1] === 9) {
        n++; 
    }
    if (x > 0 && map[x - 1][y] === 9) {
        n++; 
    }
    if (x < cols - 1 && map[x + 1][y] === 9) {
        n++; 
    }
    if (x > 0 && y < cols - 1 && map[x - 1][y + 1] === 9) {
        n++; 
    }
    if (y < cols - 1 && map[x][y + 1] === 9) {
        n++; 
    }
    if (x < cols - 1 && y < cols - 1 && map[x + 1][y + 1] === 9) {
        n++; 
    }
    return n;
}

function getmousemap(mymouse) {
    let xy = { x:0, y:0 }
    xy.x = Math.floor((mymouse.x - fuchi) / boxsize) 
    xy.y = Math.floor((mymouse.y - fuchi) / boxsize) 
    if (xy.x < cols && xy.y < cols) {
        return xy 
    } else {
        xy.x = -1 
        return xy
    }
}

function isflag(mymouse) {
    let x = (mymouse.x - fuchi) / boxsize 
    x = x - Math.floor(x) 
    let y = (mymouse.y - fuchi) / boxsize 
    y = y - Math.floor(y) 
    return  x > 0.75 && y < 0.25 
}

function isnext(mymouse) {
    return mymouse.x > 490 && mymouse.x < 610 && mymouse.y > 325 && mymouse.y < 385
}

function isagain(mymouse) {
    return mymouse.x > 490 && mymouse.x < 610 && mymouse.y > 385 && mymouse.y < 445
}

function autoopen(x, y) {
    if (x >= 0 && y >= 0 && x < cols && y < cols && vmap[x][y] === -2) {
        vmap[x][y] = map[x][y]
        boxs--
        if (map[x][y] === 0) {
            let myxy  = { x:0, y:0 }
            myxy.x = x
            myxy.y = y
            zlist[znum] = myxy 
            znum++
        }
    }
}

function taneakashi() {
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < cols; j++) {
            vmap[i][j] = map[i][j]
        }
    }
}
