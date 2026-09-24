let ufox
let ufoy

function ufoido() {
    if (ufox + ufo.sx <= window1.sx) {
        ufox += ufo.mx
    }
    if (ufox + ufo.sx >= window1.sx) {
    	ufow = ufo.wait
        return 0
    }
    return 1
}

function ufojunbi() {
    ufox = ufo.x
    ufoy = ufo.y
}

function ufohit() {
    if (ccheck(ufox, ufoy, ufo.sx, ufo.sy, tamax, tamay, tama.sx, tama.sy)) {
        score += 200
    	ufow = ufo.wait
        return 0
    } else {
    	return 1
    }
}

function ufohit2() {
    if (ccheck(ufox, ufoy, ufo.sx, ufo.sy, tamax, tamay, tama.sx, tama.sy)) {
        score += 200
    	ufobw = ufob.wait
        return 2
    } else {
    	return 1
    }
}

