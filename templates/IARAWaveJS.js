const wavyContainers = document.getElementsByClassName("wavyContainer")
const titleWave1 = document.getElementById('wave1')
const titleWave2 = document.getElementById('wave2')

const width = document.documentElement.clientWidth

const height = .04 * width

for (var wavyContainer of wavyContainers) {
    wavyContainer.style.marginTop = -height

    wcCSS = window.getComputedStyle(wavyContainer, null)
    let currentPadding = wcCSS.getPropertyValue("padding-top")
    wavyContainer.style.paddingTop = parseFloat(currentPadding) + height/2 + 'px'
}


const T = 7 * 60 //seconds * frame rate = period in frames
const freqAng = 2 * Math.PI / T
const delay = .5 * 1/freqAng

const A = .9 // % of height/2
const dx = 1

let xs = []
for (var x = 0; x <= 100; x+=dx) {xs.push(x)}

let xsTitle = []
for (var x = 0; x <= width; x+=10) {xsTitle.push(x)}

function envelope (x, width) {
    return Math.exp((-4 * (x/width - 1) ** 2))
}

function waveForm (x, t, width, height, wlen) {
    return height/2 * (1 + A * envelope(x, width) *
     Math.sin(x * 2 * Math.PI / wlen - freqAng * t))
}

function zip (Xs, t, width, height, wlen) {
    ys = xs.map((x) => (waveForm(x, t, width, height, wlen)))
    return Xs.map((x, i) => (`${x}%  ${ys[i]}px`))
}


var xsRev = [...xs]
xsRev.reverse()
let xy = []

let t = 0

function animateWave() {

    //Animate title waves

    xy = xsTitle.map(x => x+','+waveForm(x, t, width/2, 60, width/2)).join(' ')
    titleWave1.setAttribute('points', xy)


    xy = xsTitle.map(x => x+','+waveForm(x, t + delay, width/2, 60, width/2)).join(' ')
    titleWave2.setAttribute('points', xy)


    //Animate containers' wavy borders

    for (var i = 0; i < wavyContainers.length; i++) {

  if (i%2) {
      let xy = zip(xsRev, -t, 100, .04*width, 50).join(',')
      wavyContainers[i].style.clipPath = `polygon(100% 100%, ${xy}, 0 100%)`
  }

  else {
      let xy = zip(xs, t, 100, .04*width, 50).join(',')
      wavyContainers[i].style.clipPath = `polygon(0 100%, ${xy}, 100% 100%)`
  }
    }

    t = (t+1) % T
    requestAnimationFrame(animateWave)
}

animateWave()