let tekitamax
let tekitamay
let shogaia = []

function tekitamaido() {
    if (tekitamay <= window1.sy) {
        tekitamay += tekitama.my
    }
    if (tekitamay >= window1.sy) {
        return 0
    }
    return 1
}

function tekikogeki() {
    let d = window1.sx * window1.sx + window1.sy * window1.sy
    let ni = 32;
    for (let i = 0; i < 32; i++) {
        if (tekia[i].f === 1) {
            let di = (tekia[i].x - playerx) * (tekia[i].x - playerx) + (tekia[i].y - playery) * (tekia[i].y - playery)
            if (di < d) {
                d = di
                ni = i
            }
        }
    }
    tekitamax = tekia[ni].x + teki.sx / 2
    tekitamay = tekia[ni].y + teki.sy
}

function tekitamaplayerhit() {
    if (ccheck(tekitamax, tekitamay, tekitama.sx, tekitama.sy, playerx, playery, player.sx, player.sy)) {
        mode = 9
        return 0
    } else {
        return 1
    }

}

function tekitamatamahit() {
    if (ccheck(tekitamax, tekitamay, tekitama.sx, tekitama.sy, tamax, tamay, tama.sx, tama.sy)) {
        score += 100
        return 0
    } else {
        return 1
    }

}

function shogaijunbi() {
    for (let i = 0; i < 24; i++) {
        let wx = (i % 12) * 20 + shogai.x + Math.floor((i % 12 / 3)) * 100
        let wy = (i < 12 ? 0 : 1) * 20 + shogai.y
        shogaia[i] = { x:wx, y:wy, f:1 }
    }
}

function tekitamashogaihit() {
    for (let i = 0; i < 24; i++) {
        if (shogaia[i].f === 1) {
               if (ccheck(tekitamax, tekitamay, tekitama.sx, tekitama.sy, shogaia[i].x, shogaia[i].y, shogai.sx, shogai.sy)) {
                   shogaia[i].f = 0
                   return 0
               }
        }
    }
    return 1
}

function tamashogaihit() {
    for (let i = 0; i < 24; i++) {
        if (shogaia[i].f === 1) {
            if (ccheck(tamax, tamay, tama.sx, tama.sy, shogaia[i].x, shogaia[i].y, shogai.sx, shogai.sy)) {
                shogaia[i].f = 0
                return 0
            }
        }
    }
    return 1
}

function tekishogaihit() {
    for (let i = 0; i < 32; i++) {
        if (tekia[i].f === 1) {
            for (let j = 0; j < 24; j++) {
                if (shogaia[j].f === 1) {
                    if (ccheck(tekia[i].x, tekia[i].y, teki.sx, teki.sy, shogaia[j].x, shogaia[j].y, shogai.sx, shogai.sy)) {
                        shogaia[j].f = 0
                    }
                }
            }
        }
    }
}

