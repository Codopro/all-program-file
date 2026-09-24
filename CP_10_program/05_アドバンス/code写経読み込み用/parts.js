//画像のリスト
let base = document.getElementsByClassName("base")
let guides = document.getElementsByClassName("guides")
let chara = document.getElementsByClassName("chara")
let leader = document.getElementsByClassName("leader")
let subleader = document.getElementsByClassName("subleader")
let member = document.getElementsByClassName("member")
let hyouka = document.getElementsByClassName("hyouka")
let yakuwarib = document.getElementsByClassName("yakuwarib")
let uns = document.getElementsByClassName("uns")
let unnotuyosa = document.getElementsByClassName("unnotuyosa")

let oto = []

let window1 = { sx:630, sy:480 }
let timers
let timerv = 30
let canvas

let timer = timerv
let mode = 0
let moused
let powers = [6, 5, 4, 3, 5, 6, 4, 3]
let untuyosav = [0, 0, 1, 2, 0, 0, 1, 2]
let untuyosavr = [0, 0, 0, 0, 0, 0, 0, 0]
let selectnum = -1
let leadernum = -1
let subleadernum = -1
let membernum = -1
let ptakarabako = [0, 0, 0]
let unplus = [0, 0, 0]
let playerkei = 0;
let cleadernum = -1
let csubleadernum = -1
let cmembernum = -1
let ctakarabako = [0, 0, 0]
let compkei = 0
let slidecnt = 0
let yakuwaribai = [[4, 3, 2], [3, 4, 2], [2, 3, 4], [1, 1, 3]]
let seikaku = [0, 0, 0, 0, 0, 0, 0, 0]
let sukinac = [0, 0, 0, 0, 0, 0, 0, 0]
let sukinaleader = [-1, 6, 3, 7]
let sukinazouka  = [ 0, 2, 3, 4]
let subpowerplus = 0
let mempowerplus = 0
let takaracnt = 0
let hyoukanum = 0

function init() {
    canvas = document.getElementById('canvas')
    ctx = canvas.getContext('2d')
    canvas.addEventListener('click', onclick_canvas, false)
    start()
}

function haikei9() {
    for (let j = 0; j < 3; j++) {
        for (let i = 0; i < 3; i++) {
            ctx.drawImage(base[1], i * 210, j * 160)
        }
    }
}

function charapage() {
    for (let j = 0; j < 3; j++) {
        for (let i = 0; i < 3; i++) {
            if (i !== 1 || j !== 1) {
                if (moused.x >= i * 210 && moused.x <= i * 210 + 105 &&
                   moused.y >= j * 160 && moused.y <= j * 160 + 159) {
                    return charnum(i, j)
                }
            }
        }
    }
    return -1;
}

function kettei() {
    if (leadernum !== -1 ||  subleadernum !== -1 || membernum !== -1) {
        if (moused.x >= 210 && moused.x <= 420 &&
           moused.y >= 160 && moused.y <= 320) {
            return true
        }
    }
    return false
}

function leaderbutton() {
    for (let j = 0; j < 3; j++) {
        for (let i = 0; i < 3; i++) {
            if (i !== 1 || j !== 1) {
                let n = charnum(i, j)
                if (moused.x >= i * 210 + 120 && moused.x <= i * 210 + 190 &&
                   moused.y >= j * 160 + 94 && moused.y <= j * 160 + 115) {
                    if (n === subleadernum) {
                        subleadernum = -1
                    }
                    if (n === membernum) {
                        membernum = -1
                    }
                    leadernum = n
                    return
                }
            }
        }
    }
}

function subleaderbutton() {
    for (let j = 0; j < 3; j++) {
        for (let i = 0; i < 3; i++) {
            if (i !== 1 || j !== 1) {
                let n = charnum(i, j)
                if (moused.x >= i * 210 + 120 && moused.x <= i * 210 + 190 &&
                   moused.y >= j * 160 + 116 && moused.y <= j * 160 + 137) {
                    if (n === leadernum) {
                        leadernum = -1
                    }
                    if (n === membernum) {
                        membernum = -1
                    }
                    subleadernum = n
                    return
                }
            }
        }
    }
}

function memberbutton() {
    for (let j = 0; j < 3; j++) {
        for (let i = 0; i < 3; i++) {
            if (i !== 1 || j !== 1) {
                let n = charnum(i, j)
                if (moused.x >= i * 210 + 120 && moused.x <= i * 210 + 190 &&
                   moused.y >= j * 160 + 138 && moused.y <= j * 160 + 159) {
                    if (n === leadernum) {
                        leadernum = -1
                    }
                    if (n === subleadernum) {
                        subleadernum = -1
                    }
                    membernum = n
                    return
                }
            }
        }
    }
}

function mousezahyo(canvas, event) {
    let rect = canvas.getBoundingClientRect()
    return {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

function charnum(i, j) {
    let charamap = [0, 1, 2, 3, -1, 4, 5, 6, 7]
    return charamap[j * 3 + i]
}

function kekkahyouka() {
    if (playerkei >= compkei) {
        return 0
    } else if (playerkei > compkei * 0.80) {
        return 1
    } else if (playerkei > compkei * 0.70) {
        return 2
    } else if (playerkei > compkei * 0.50) {
        return 3
    } else {
        return 4
    }
}

function compkekka() {
    let pname = ["レッド", "パープル", "ブラウン", "ブルー", "オレンジ", "ホワイト", "グリーン", "ピンク"]
    if (moused.x >= 420 && moused.y >= 320) {
        alert("コンピュータの計算結果：\n"
        + "リーダー："     + pname[cleadernum]    + "(" + ctakarabako[0] + ")\n"
        + "サブリーダー：" + pname[csubleadernum] + "(" + ctakarabako[1] + ")\n"
        + "メンバー："     + pname[cmembernum]    + "(" + ctakarabako[2] + ")\n"
        + "宝箱の合計数：" + compkei + "\n"
        + "※うんの強さの乱数の分は加算していません")
    }
}

function drawleaderk() {
    if (leadernum !== -1) {
        ctx.drawImage(chara[leadernum], 0, 0)
        ctx.drawImage(leader[1], 120, 94)
        ctx.drawImage(subleader[0], 120, 116)
        ctx.drawImage(member[0], 120, 138)
        let p = powers[leadernum] + " x " + yakuwaribai[seikaku[leadernum]][0] + " + " + unplus[0] + " = " + ptakarabako[0]
        ctx.fillText(p, 120, 80)
    }
}

function drawsubleaderk() {
    if (subleadernum !== -1) {
        ctx.drawImage(chara[subleadernum], 0, 160)
        ctx.drawImage(leader[0], 120, 254)
        ctx.drawImage(subleader[1], 120, 276)
        ctx.drawImage(member[0], 120, 298)
        let p = "(" + powers[subleadernum] + " + " + subpowerplus + ")"
        p = p + " x " + yakuwaribai[seikaku[subleadernum]][1] + " + " + unplus[1] + " = " + ptakarabako[1]
        ctx.fillText(p, 120, 240)
    }
}

function drawmemberk() {
    if (membernum !== -1) {
        ctx.drawImage(chara[membernum], 0, 320)
        ctx.drawImage(leader[0], 120, 414)
        ctx.drawImage(subleader[0], 120, 436)
        ctx.drawImage(member[1], 120, 458)
        let p = "(" + powers[membernum] + " + " + mempowerplus + ")"
        p = p + " x " + yakuwaribai[seikaku[membernum]][2] + " + " + unplus[2] + " = " + ptakarabako[2]
        ctx.fillText(p, 120, 400)
    }
}

function leadertakarabako() {
    if (leadernum !== -1) {
        return powers[leadernum] * yakuwaribai[seikaku[leadernum]][0] + unplus[0]
    } else {
        return 0
    }
}

function subleadertakarabako() {
    if (subleadernum !== -1) {
        let wpower = powers[subleadernum]
        if (leadernum === sukinaleader[sukinac[subleadernum]]) {
            subpowerplus = sukinazouka[sukinac[subleadernum]]
            wpower +=  subpowerplus
        }
        return wpower * yakuwaribai[seikaku[subleadernum]][1] + unplus[1]
    } else {
        return 0
    }
}

function membertakarabako() {
    if (membernum !== -1) {
        let wpower = powers[membernum]
        if (leadernum === sukinaleader[sukinac[membernum]]) {
            mempowerplus = sukinazouka[sukinac[membernum]]
            wpower += mempowerplus
        }
        return wpower * yakuwaribai[seikaku[membernum]][2] + unplus[2]
    } else {
        return 0
    }
}

function comptakarabako() {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            for (let k = 0; k < 8; k++) {
                if (j !== i && k !== i && k !== j) {
                    let cleader = powers[i]
                    cleader *= yakuwaribai[seikaku[i]][0]
                    cleader += untuyosavr[i]
                    let csubleader = powers[j]
                    if (i === sukinaleader[sukinac[j]]) {
                        csubleader += sukinazouka[sukinac[j]];
                    }
                    csubleader *= yakuwaribai[seikaku[j]][1]
                    csubleader += untuyosavr[j]
                    let cmember = powers[k]
                    if (i === sukinaleader[sukinac[k]]) {
                        cmember += sukinazouka[sukinac[k]];
                    }
                    cmember *= yakuwaribai[seikaku[k]][2]
                    cmember += untuyosavr[k]
                    if (compkei < cleader + csubleader + cmember) {
                        cleadernum = i
                        csubleadernum = j
                        cmembernum = k
                        ctakarabako[0] = cleader
                        ctakarabako[1] = csubleader
                        ctakarabako[2] = cmember
                        compkei = cleader + csubleader + cmember
                    }
                }
            }
        }
    }
}

function drawplay(i, j) {
	let n = charnum(i, j)
    ctx.drawImage(chara[n], i * 210, j * 160)
	if (n === leadernum) {
	    ctx.drawImage(leader[1], i * 210 + 115, j * 160 + 94)
	} else {
	    ctx.drawImage(leader[0], i * 210 + 115, j * 160 + 94)
	}
	if (n === subleadernum) {
	    ctx.drawImage(subleader[1], i * 210 + 115, j * 160 + 115)
	} else {
	    ctx.drawImage(subleader[0], i * 210 + 115, j * 160 + 115)
	}
	if (n === membernum) {
	    ctx.drawImage(member[1], i * 210 + 115, j * 160 + 136)
	} else {
	    ctx.drawImage(member[0], i * 210 + 115, j * 160 + 136)
	}
    ctx.font = '13pt Arial'
    ctx.fillText(yakuwaribai[seikaku[n]][0], i * 210 + 187, j * 160 + 110)
    ctx.fillText(yakuwaribai[seikaku[n]][1], i * 210 + 187, j * 160 + 131)
    ctx.fillText(yakuwaribai[seikaku[n]][2], i * 210 + 187, j * 160 + 152)
    ctx.font = '30pt Arial'
    ctx.fillText(powers[n], i * 210 + 5, j * 160 + 35)
}

function kekkaguide() {
    ctx.drawImage(guides[4], 420, 0)
    ctx.drawImage(guides[5], 420, 320)
}

function drawplayun(i, j) {
    let n = charnum(i, j)
    ctx.drawImage(uns[untuyosav[n]], i * 210 + 120, j * 160 + 52)
}

function unplustakarabako() {
    for (let i = 0; i < 8; i++) {
        if (untuyosav[i] > 0) {
            untuyosavr[i] = untuyosav[i] * 5 + Math.floor(Math.random() * 3)
        }
    }
    unplus[0] = untuyosavr[leadernum]
    unplus[1] = untuyosavr[subleadernum]
    unplus[2] = untuyosavr[membernum]
}

function cunplustakarabako() {
    for (let i = 0; i < 8; i++) {
        untuyosavr[i] = untuyosav[i] * 5
    }
}

function drawkekka(n) {
    ctx.font = '46pt Arial'
    ctx.fillText(n, 525, 48)
    for (let i = 0; i < n; i++) {
        ctx.drawImage(takara, 420 + i % 10 * 20, 50 + Math.floor(i / 10) * 9)
    }
}
